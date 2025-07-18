#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scraper Principal da SSP-SP - Versão Síncrona com Pydoll
Acessa o site da SSP-SP e baixa dados criminais com filtro por cidade
"""

import pandas as pd
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
import numpy as np
import datetime as dt
try:
    from ..config.settings import settings
    from ..utils.logger import setup_logger
    from ..utils.city_filter import CityFilter
    from ..utils.file_utils import FileUtils
    from ..models.data_models import ScrapingResult
    from ..utils.ssp_browser_scraper import SSPBrowserScraper
    from ..utils.cache_manager import CacheManager
except ImportError:
    # Fallback para quando executado da raiz
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
    from config.settings import settings
    from utils.logger import setup_logger
    from utils.city_filter import CityFilter
    from utils.file_utils import FileUtils
    from models.data_models import ScrapingResult
    from utils.ssp_browser_scraper import SSPBrowserScraper
    from utils.cache_manager import CacheManager

def to_serializable(val):
    if pd.isna(val):
        return None
    if isinstance(val, (pd.Timestamp, dt.datetime, dt.date)):
        return val.isoformat()
    if isinstance(val, dt.time):
        return val.isoformat()
    if isinstance(val, (np.integer, int)):
        return int(val)
    if isinstance(val, (np.floating, float)):
        return float(val)
    return str(val) if not isinstance(val, (str, bool, dict, list, type(None))) else val

class SSPDataScraper:
    """Scraper síncrono para dados da SSP-SP usando Pydoll"""
    
    def __init__(self, target_year: Optional[int] = None, target_city: Optional[str] = None):
        """
        Inicializa o scraper
        
        Args:
            target_year (int, optional): Ano específico para buscar. Se None, usa o mais recente.
            target_city (str, optional): Cidade específica para filtrar. Se None, processa todas.
        """
        self.target_year = target_year or settings.DEFAULT_TARGET_YEAR
        self.target_city = target_city or settings.DEFAULT_CITY
        self.consultas_url = settings.CONSULTAS_URL
        self.categories = settings.CATEGORIES
        self.city_filter = CityFilter()
        self.file_utils = FileUtils()
        self.cache_manager = CacheManager()
        self.logger = setup_logger("ssp_scraper")
        self.browser_scraper = SSPBrowserScraper(self.consultas_url)
        self.category_links = None
    
    def validate_target_year(self) -> bool:
        """Valida se o ano alvo é permitido"""
        if self.target_year and not self.cache_manager.validate_year(self.target_year):
            self.logger.error(f"Ano {self.target_year} não é permitido (futuro)")
            return False
        return True
    
    def get_available_years(self) -> List[int]:
        """
        Obtém os anos disponíveis a partir dos links reais
        """
        if self.category_links is None:
            self.category_links = self.browser_scraper.get_links()
        anos = set()
        for cat in self.category_links.values():
            anos.update(cat.keys())
        return sorted(anos, reverse=True)

    def find_download_links(self, category_key: str) -> Dict[int, str]:
        """
        Encontra links de download reais para uma categoria
        """
        if self.category_links is None:
            self.category_links = self.browser_scraper.get_links()
        return self.category_links.get(category_key, {})
    
    def download_file(self, url: str, filename: str) -> bool:
        """
        Baixa um arquivo usando o browser scraper
        
        Args:
            url (str): URL do arquivo
            filename (str): Nome do arquivo local
            
        Returns:
            bool: True se baixou com sucesso
        """
        try:
            return self.browser_scraper.download_file(url, filename)
        except Exception as e:
            self.logger.error(f"Erro ao baixar {url}: {e}")
            return False
    
    def process_excel_file_complete(self, file_path: str, category_name: str, year: int) -> ScrapingResult:
        """
        Processa um arquivo Excel completo (sem filtro de cidade)
        
        Args:
            file_path (str): Caminho do arquivo Excel
            category_name (str): Nome da categoria
            year (int): Ano dos dados
            
        Returns:
            ScrapingResult: Resultado do processamento
        """
        try:
            # Ler arquivo Excel
            df = pd.read_excel(file_path)
            total_registros = len(df)
            
            self.logger.info(f"Processando {file_path}: {total_registros} registros")
            
            # Converter todos os tipos para tipos Python nativos
            df = df.map(to_serializable)

            # Converter para lista de dicionários
            dados = df.to_dict('records')
            
            # Criar resultado
            result = ScrapingResult(
                categoria=category_name,
                arquivo_original=os.path.basename(file_path),
                total_registros=total_registros,
                registros_filtrados=total_registros,  # Todos os registros
                cidade_filtro="TODAS",  # Indica que não foi filtrado por cidade
                data_processamento=datetime.now(),
                dados=dados
            )
            
            self.logger.info(f"Processados {total_registros} registros completos para {category_name}")
            return result
            
        except Exception as e:
            self.logger.error(f"Erro ao processar {file_path}: {e}")
            return ScrapingResult(
                categoria=category_name,
                arquivo_original=os.path.basename(file_path),
                total_registros=0,
                registros_filtrados=0,
                cidade_filtro="TODAS",
                data_processamento=datetime.now(),
                dados=[],
                sucesso=False,
                erro=str(e)
            )
    
    def process_city_filter(self, category: str, year: int, city: str) -> Optional[ScrapingResult]:
        """
        Processa filtro por cidade usando dados já baixados
        
        Args:
            category (str): Categoria dos dados
            year (int): Ano dos dados
            city (str): Cidade para filtrar
            
        Returns:
            Optional[ScrapingResult]: Resultado filtrado ou None se erro
        """
        try:
            # Verificar se já foi processado
            if self.cache_manager.is_city_processed(category, year, city):
                self.logger.info(f"Dados para {city} já processados (categoria: {category}, ano: {year})")
                return None
            
            # Carregar dados completos
            data = self.file_utils.load_category_year_data(category, year)
            if not data:
                self.logger.error(f"Dados completos não encontrados para {category}_{year}")
                return None
            
            # Converter para DataFrame para filtrar
            df = pd.DataFrame(data['dados'])
            total_registros = len(df)
            
            # Filtrar por cidade
            filtered_df = self.city_filter.filter_dataframe_by_city(df, city)
            registros_filtrados = len(filtered_df)
            
            # Converter tipos
            filtered_df = filtered_df.map(to_serializable)
            dados_filtrados = filtered_df.to_dict('records')
            
            # Criar resultado
            result = ScrapingResult(
                categoria=data['categoria'],
                arquivo_original=data['arquivo_original'],
                total_registros=total_registros,
                registros_filtrados=registros_filtrados,
                cidade_filtro=city,
                data_processamento=datetime.now(),
                dados=dados_filtrados
            )
            
            self.logger.info(f"Filtrados {registros_filtrados} registros para {city}")
            return result
            
        except Exception as e:
            self.logger.error(f"Erro ao filtrar por cidade {city}: {e}")
            return None
    
    def scrape_category(self, category_key: str, category_name: str) -> bool:
        """
        Faz scraping de uma categoria específica (arquivo completo)
        
        Args:
            category_key (str): Chave da categoria
            category_name (str): Nome da categoria
            
        Returns:
            bool: True se processou com sucesso
        """
        try:
            self.logger.info(f"Processando categoria: {category_name}")
            
            # Encontrar links de download reais
            download_links = self.find_download_links(category_key)
            
            if not download_links:
                self.logger.warning(f"Nenhum link encontrado para {category_name} - Categoria não disponível no momento")
                return True  # Retorna True para não contar como falha
            
            # Selecionar o ano mais próximo
            anos_disponiveis = sorted(download_links.keys(), reverse=True)
            ano_alvo = self.target_year
            
            if not ano_alvo or ano_alvo not in anos_disponiveis:
                # Pega o mais recente se não houver o ano exato
                ano_alvo = anos_disponiveis[0]
                self.logger.info(f"Ano {self.target_year} não encontrado, usando {ano_alvo}")
            
            # Validar ano
            if not self.cache_manager.validate_year(ano_alvo):
                self.logger.error(f"Ano {ano_alvo} não é permitido")
                return False
            
            # Verificar se já foi processado
            if self.cache_manager.is_file_processed(category_key, ano_alvo) and not settings.FORCE_REPROCESS:
                self.logger.info(f"Arquivo {category_key}_{ano_alvo} já processado. Pulando...")
                return True
            
            url = download_links[ano_alvo]
            filename = f"{category_key}_{ano_alvo}.xlsx"
            
            if self.download_file(url, filename):
                file_path = os.path.join(settings.DOWNLOADS_DIR, filename)
                if os.path.exists(file_path):
                    result = self.process_excel_file_complete(file_path, category_name, ano_alvo)
                    
                    # Salvar dados completos
                    if self.file_utils.save_category_year_data(result.to_dict(), category_key, ano_alvo):
                        # Marcar como processado no cache
                        self.cache_manager.mark_file_processed(category_key, ano_alvo, {
                            "filename": filename,
                            "total_registros": result.total_registros,
                            "cidade_filtro": result.cidade_filtro
                        })
                        
                        # Adicionar ano aos disponíveis
                        self.cache_manager.add_available_year(ano_alvo)
                        
                        self.logger.info(f"Categoria {category_name} processada com sucesso")
                        return True
                    else:
                        self.logger.error(f"Erro ao salvar dados de {category_name}")
                        return False
                else:
                    self.logger.error(f"Arquivo não encontrado: {file_path}")
                    return False
            else:
                self.logger.error(f"Falha ao baixar arquivo para {category_name}")
                return False
                
        except Exception as e:
            self.logger.error(f"Erro ao processar categoria {category_name}: {e}")
            return False
    
    def process_city_data(self, category: str, year: int, city: str) -> bool:
        """
        Processa dados filtrados por cidade
        
        Args:
            category (str): Categoria dos dados
            year (int): Ano dos dados
            city (str): Cidade para filtrar
            
        Returns:
            bool: True se processou com sucesso
        """
        try:
            result = self.process_city_filter(category, year, city)
            if result:
                # Salvar dados filtrados por cidade
                if self.file_utils.save_city_filtered_data(result.to_dict(), category, year, city):
                    # Marcar como processado no cache
                    self.cache_manager.mark_city_processed(category, year, city, {
                        "registros_filtrados": result.registros_filtrados,
                        "total_registros": result.total_registros
                    })
                    self.logger.info(f"Dados de {city} processados com sucesso")
                    return True
                else:
                    self.logger.error(f"Erro ao salvar dados de {city}")
                    return False
            else:
                self.logger.info(f"Dados de {city} já processados ou não encontrados")
                return True
                
        except Exception as e:
            self.logger.error(f"Erro ao processar dados de {city}: {e}")
            return False
    
    def run(self):
        """
        Executa o scraping completo
        """
        self.logger.info("Iniciando scraping da SSP-SP")
        self.logger.info(f"Ano alvo: {self.target_year or 'Mais recente'}")
        self.logger.info(f"Cidade alvo: {self.target_city or 'Todas'}")
        
        # Validar ano alvo
        if not self.validate_target_year():
            return False
        
        # Criar diretórios necessários
        self.file_utils.ensure_directory_exists(settings.DOWNLOADS_DIR)
        self.file_utils.ensure_directory_exists(settings.OUTPUT_DIR)
        
        # Buscar links reais antes de iniciar
        self.logger.info("Buscando links de download...")
        self.category_links = self.browser_scraper.get_links()
        
        # Ajustar ano alvo se necessário
        if not self.target_year:
            anos = set()
            for cat in self.category_links.values():
                anos.update(cat.keys())
            if anos:
                self.target_year = max(anos)
                self.logger.info(f"Usando ano mais recente: {self.target_year}")
        
        # Processar cada categoria
        success_count = 0
        total_count = len(self.categories)
        
        for category_key, category_name in self.categories.items():
            self.logger.info(f"[LOOP] Iniciando processamento da categoria: {category_key} - {category_name}")
            try:
                if self.scrape_category(category_key, category_name):
                    success_count += 1
                    self.logger.info(f"✅ {category_name} - Sucesso")
                else:
                    self.logger.error(f"❌ {category_name} - Falha")
            except Exception as e:
                self.logger.error(f"❌ {category_name} - Erro: {e}")
            self.logger.info(f"[LOOP] Fim do processamento da categoria: {category_key} - {category_name}")
        
        # Processar cidade específica se solicitado
        if self.target_city and self.target_city != "Todas":
            self.logger.info(f"Processando dados filtrados para cidade: {self.target_city}")
            # Garantir que temos um ano válido
            target_year = self.target_year
            if not target_year:
                self.logger.error("Ano alvo não definido para processar cidade")
                return success_count > 0
                
            for category_key, category_name in self.categories.items():
                if self.process_city_data(category_key, target_year, self.target_city):
                    self.logger.info(f"✅ {category_name} - {self.target_city} processado")
                else:
                    self.logger.error(f"❌ {category_name} - {self.target_city} falhou")
        
        # Resumo dos resultados
        self.logger.info(f"Scraping concluído: {success_count}/{total_count} categorias processadas com sucesso")
        if success_count == 0:
            self.logger.error("Nenhuma categoria foi processada com sucesso")
        else:
            self.logger.info("Scraping concluído com sucesso!")
        
        # Mostrar informações do cache
        cache_info = self.cache_manager.get_cache_info()
        self.logger.info(f"Cache: {cache_info['total_processed_files']} arquivos, {cache_info['total_processed_cities']} cidades")
        
        return success_count > 0 