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
try:
    from ..config.settings import settings
    from ..utils.logger import setup_logger
    from ..utils.city_filter import CityFilter
    from ..utils.file_utils import FileUtils
    from ..models.data_models import ScrapingResult
    from ..utils.ssp_browser_scraper import SSPBrowserScraper
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

class SSPDataScraper:
    """Scraper síncrono para dados da SSP-SP usando Pydoll"""
    
    def __init__(self, target_year: Optional[int] = None):
        """
        Inicializa o scraper
        
        Args:
            target_year (int, optional): Ano específico para buscar. Se None, usa o mais recente.
        """
        self.target_year = target_year or settings.DEFAULT_TARGET_YEAR
        self.consultas_url = settings.CONSULTAS_URL
        self.categories = settings.CATEGORIES
        self.city_filter = CityFilter()
        self.file_utils = FileUtils()
        self.logger = setup_logger("ssp_scraper")
        self.browser_scraper = SSPBrowserScraper(self.consultas_url)
        self.category_links = None
    
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
    
    def process_excel_file(self, file_path: str, category_name: str) -> ScrapingResult:
        """
        Processa um arquivo Excel e filtra por cidade
        
        Args:
            file_path (str): Caminho do arquivo Excel
            category_name (str): Nome da categoria
            
        Returns:
            ScrapingResult: Resultado do processamento
        """
        try:
            # Ler arquivo Excel
            df = pd.read_excel(file_path)
            total_registros = len(df)
            
            self.logger.info(f"Processando {file_path}: {total_registros} registros")
            
            # Filtrar por cidade
            filtered_df = self.city_filter.filter_dataframe_by_city(df, settings.DEFAULT_CITY)
            registros_filtrados = len(filtered_df)
            
            # Converter para lista de dicionários
            dados = filtered_df.to_dict('records')
            
            # Criar resultado
            result = ScrapingResult(
                categoria=category_name,
                arquivo_original=os.path.basename(file_path),
                total_registros=total_registros,
                registros_filtrados=registros_filtrados,
                cidade_filtro=settings.DEFAULT_CITY,
                data_processamento=datetime.now(),
                dados=dados
            )
            
            self.logger.info(f"Filtrados {registros_filtrados} registros para {settings.DEFAULT_CITY}")
            return result
            
        except Exception as e:
            self.logger.error(f"Erro ao processar {file_path}: {e}")
            return ScrapingResult(
                categoria=category_name,
                arquivo_original=os.path.basename(file_path),
                total_registros=0,
                registros_filtrados=0,
                cidade_filtro=settings.DEFAULT_CITY,
                data_processamento=datetime.now(),
                dados=[],
                sucesso=False,
                erro=str(e)
            )
    
    def scrape_category(self, category_key: str, category_name: str) -> bool:
        """
        Faz scraping de uma categoria específica
        
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
                self.logger.warning(f"Nenhum link encontrado para {category_name}")
                return False
            
            # Selecionar o ano mais próximo
            anos_disponiveis = sorted(download_links.keys(), reverse=True)
            ano_alvo = self.target_year
            
            if not ano_alvo or ano_alvo not in anos_disponiveis:
                # Pega o mais recente se não houver o ano exato
                ano_alvo = anos_disponiveis[0]
                self.logger.info(f"Ano {self.target_year} não encontrado, usando {ano_alvo}")
            
            url = download_links[ano_alvo]
            filename = f"{category_key}_{ano_alvo}.xlsx"
            
            if self.download_file(url, filename):
                file_path = os.path.join(settings.DOWNLOADS_DIR, filename)
                if os.path.exists(file_path):
                    result = self.process_excel_file(file_path, category_name)
                    # Salvar resultado em JSON
                    output_filename = f"{category_key}_{ano_alvo}.json"
                    self.file_utils.save_json(result.to_dict(), output_filename)
                    self.logger.info(f"Categoria {category_name} processada com sucesso")
                    return True
                else:
                    self.logger.error(f"Arquivo não encontrado: {file_path}")
                    return False
            else:
                self.logger.error(f"Falha ao baixar arquivo para {category_name}")
                return False
                
        except Exception as e:
            self.logger.error(f"Erro ao processar categoria {category_name}: {e}")
            return False
    
    def run(self):
        """
        Executa o scraping completo
        """
        self.logger.info("Iniciando scraping da SSP-SP")
        self.logger.info(f"Ano alvo: {self.target_year or 'Mais recente'}")
        self.logger.info(f"Cidade padrão: {settings.DEFAULT_CITY}")
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
        # Resumo dos resultados
        self.logger.info(f"Scraping concluído: {success_count}/{total_count} categorias processadas com sucesso")
        if success_count == 0:
            self.logger.error("Nenhuma categoria foi processada com sucesso")
        else:
            self.logger.info("Scraping concluído com sucesso!")
        return success_count > 0 