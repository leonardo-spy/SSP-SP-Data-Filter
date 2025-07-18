#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilitários de Arquivo - Funções para manipulação de arquivos JSON e Excel
"""

import os
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
try:
    from ..config.settings import settings
except ImportError:
    # Fallback para quando executado da raiz
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
    from config.settings import settings

class FileUtils:
    """Classe com utilitários para manipulação de arquivos"""
    
    def __init__(self):
        """Inicializa os utilitários de arquivo"""
        self.downloads_dir = settings.DOWNLOADS_DIR
        self.output_dir = settings.OUTPUT_DIR
    
    def load_all_json_files(self, output_dir: Optional[str] = None) -> List[Dict]:
        """
        Carrega todos os arquivos JSON do diretório de saída
        
        Args:
            output_dir (str, optional): Diretório com os arquivos JSON. 
                                      Se None, usa o diretório padrão.
        
        Returns:
            List[Dict]: Lista com todos os dados carregados
        """
        if output_dir is None:
            output_dir = self.output_dir
            
        all_data = []
        
        try:
            if not os.path.exists(output_dir):
                logging.error(f"Diretório {output_dir} não encontrado")
                return []
            
            for filename in os.listdir(output_dir):
                if filename.endswith('.json'):
                    file_path = os.path.join(output_dir, filename)
                    
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        all_data.append(data)
                        
                    logging.info(f"Arquivo carregado: {filename}")
            
            logging.info(f"Total de arquivos carregados: {len(all_data)}")
            return all_data
            
        except Exception as e:
            logging.error(f"Erro ao carregar arquivos JSON: {e}")
            return []
    
    def save_json(self, data: Dict[str, Any], filename: str, output_dir: Optional[str] = None) -> bool:
        """
        Salva dados em arquivo JSON
        
        Args:
            data (Dict[str, Any]): Dados para salvar
            filename (str): Nome do arquivo
            output_dir (str, optional): Diretório de saída. Se None, usa o padrão.
        
        Returns:
            bool: True se salvou com sucesso
        """
        if output_dir is None:
            output_dir = self.output_dir
            
        try:
            # Criar diretório se não existir
            os.makedirs(output_dir, exist_ok=True)
            
            file_path = os.path.join(output_dir, filename)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logging.info(f"Arquivo salvo: {file_path}")
            return True
            
        except Exception as e:
            logging.error(f"Erro ao salvar arquivo JSON: {e}")
            return False
    
    def save_category_year_data(self, data: Dict[str, Any], category: str, year: int) -> bool:
        """
        Salva dados de uma categoria/ano (arquivo principal sem filtro de cidade)
        
        Args:
            data (Dict[str, Any]): Dados para salvar
            category (str): Categoria dos dados
            year (int): Ano dos dados
        
        Returns:
            bool: True se salvou com sucesso
        """
        filename = f"{category}_{year}.json"
        return self.save_json(data, filename)
    
    def save_city_filtered_data(self, data: Dict[str, Any], category: str, year: int, city: str) -> bool:
        """
        Salva dados filtrados por cidade
        
        Args:
            data (Dict[str, Any]): Dados filtrados para salvar
            category (str): Categoria dos dados
            year (int): Ano dos dados
            city (str): Cidade filtrada
        
        Returns:
            bool: True se salvou com sucesso
        """
        # Criar subdiretório para dados filtrados por cidade
        city_dir = os.path.join(self.output_dir, "cities")
        os.makedirs(city_dir, exist_ok=True)
        
        # Nome do arquivo: categoria_ano_cidade.json
        city_clean = city.replace(" ", "_").replace(".", "").replace(",", "")
        filename = f"{category}_{year}_{city_clean}.json"
        
        return self.save_json(data, filename, city_dir)
    
    def load_category_year_data(self, category: str, year: int) -> Optional[Dict]:
        """
        Carrega dados de uma categoria/ano
        
        Args:
            category (str): Categoria dos dados
            year (int): Ano dos dados
        
        Returns:
            Optional[Dict]: Dados carregados ou None se não encontrado
        """
        filename = f"{category}_{year}.json"
        file_path = os.path.join(self.output_dir, filename)
        
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logging.error(f"Erro ao carregar {file_path}: {e}")
        
        return None
    
    def load_city_filtered_data(self, category: str, year: int, city: str) -> Optional[Dict]:
        """
        Carrega dados filtrados por cidade
        
        Args:
            category (str): Categoria dos dados
            year (int): Ano dos dados
            city (str): Cidade filtrada
        
        Returns:
            Optional[Dict]: Dados carregados ou None se não encontrado
        """
        city_dir = os.path.join(self.output_dir, "cities")
        city_clean = city.replace(" ", "_").replace(".", "").replace(",", "")
        filename = f"{category}_{year}_{city_clean}.json"
        file_path = os.path.join(city_dir, filename)
        
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logging.error(f"Erro ao carregar {file_path}: {e}")
        
        return None
    
    def save_detailed_results(self, records: List[Dict], query: str, radius_km: float, 
                            output_file: Optional[str] = None) -> Optional[str]:
        """
        Salva resultados detalhados de análise geográfica
        
        Args:
            records (List[Dict]): Registros encontrados
            query (str): Query de busca
            radius_km (float): Raio de busca
            output_file (str, optional): Nome do arquivo de saída
        
        Returns:
            Optional[str]: Caminho do arquivo salvo ou None se erro
        """
        try:
            if not records:
                logging.warning("Nenhum registro para salvar")
                return None
            
            # Gerar nome do arquivo se não fornecido
            if output_file is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                query_clean = query.replace(',', '_').replace(' ', '_')
                output_file = f"analise_detalhada_{query_clean}_{radius_km}km_{timestamp}.json"
            
            # Preparar dados para exportação
            export_data = {
                "metadata": {
                    "query": query,
                    "raio_km": radius_km,
                    "total_registros": len(records),
                    "data_analise": datetime.now().isoformat(),
                    "versao": "1.0"
                },
                "estatisticas": self._calculate_statistics(records),
                "registros": records
            }
            
            # Salvar arquivo
            if self.save_json(export_data, output_file):
                return os.path.join(self.output_dir, output_file)
            else:
                return None
                
        except Exception as e:
            logging.error(f"Erro ao salvar resultados detalhados: {e}")
            return None
    
    def _calculate_statistics(self, records: List[Dict]) -> Dict[str, Any]:
        """
        Calcula estatísticas dos registros
        
        Args:
            records (List[Dict]): Lista de registros
        
        Returns:
            Dict[str, Any]: Estatísticas calculadas
        """
        try:
            if not records:
                return {}
            
            # Estatísticas de distância
            distances = [r['distancia_km'] for r in records]
            distancia_media = sum(distances) / len(distances)
            distancia_minima = min(distances)
            distancia_maxima = max(distances)
            
            # Estatísticas por categoria
            categorias = {}
            for record in records:
                cat = record['categoria']
                if cat not in categorias:
                    categorias[cat] = 0
                categorias[cat] += 1
            
            # Estatísticas por tipo de ocorrência
            tipos_ocorrencia = {}
            for record in records:
                dados = record['dados_originais']
                if 'tipo' in dados and dados['tipo']:
                    tipo = str(dados['tipo']).strip()
                    if tipo not in tipos_ocorrencia:
                        tipos_ocorrencia[tipo] = 0
                    tipos_ocorrencia[tipo] += 1
            
            return {
                "distancia_media": round(distancia_media, 2),
                "distancia_minima": distancia_minima,
                "distancia_maxima": distancia_maxima,
                "categorias": categorias,
                "tipos_ocorrencia": tipos_ocorrencia,
                "total_categorias": len(categorias),
                "total_tipos": len(tipos_ocorrencia)
            }
            
        except Exception as e:
            logging.error(f"Erro ao calcular estatísticas: {e}")
            return {}
    
    def ensure_directory_exists(self, directory: str) -> bool:
        """
        Garante que o diretório existe, criando se necessário
        
        Args:
            directory (str): Caminho do diretório
        
        Returns:
            bool: True se o diretório existe ou foi criado
        """
        try:
            os.makedirs(directory, exist_ok=True)
            return True
        except Exception as e:
            logging.error(f"Erro ao criar diretório {directory}: {e}")
            return False
    
    def get_file_info(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        Obtém informações sobre um arquivo
        
        Args:
            file_path (str): Caminho do arquivo
        
        Returns:
            Optional[Dict[str, Any]]: Informações do arquivo ou None se erro
        """
        try:
            if not os.path.exists(file_path):
                return None
            
            stat = os.stat(file_path)
            
            return {
                "nome": os.path.basename(file_path),
                "caminho": file_path,
                "tamanho_bytes": stat.st_size,
                "tamanho_mb": round(stat.st_size / (1024 * 1024), 2),
                "data_criacao": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "data_modificacao": datetime.fromtimestamp(stat.st_mtime).isoformat()
            }
            
        except Exception as e:
            logging.error(f"Erro ao obter informações do arquivo {file_path}: {e}")
            return None
    
    def list_json_files(self, directory: Optional[str] = None) -> List[str]:
        """
        Lista todos os arquivos JSON em um diretório
        
        Args:
            directory (str, optional): Diretório para listar. Se None, usa o padrão.
        
        Returns:
            List[str]: Lista de nomes de arquivos JSON
        """
        if directory is None:
            directory = self.output_dir
            
        try:
            if not os.path.exists(directory):
                return []
            
            json_files = []
            for filename in os.listdir(directory):
                if filename.endswith('.json'):
                    json_files.append(filename)
            
            return sorted(json_files)
            
        except Exception as e:
            logging.error(f"Erro ao listar arquivos JSON em {directory}: {e}")
            return [] 