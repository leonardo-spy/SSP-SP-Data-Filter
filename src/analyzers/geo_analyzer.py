#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analisador Geográfico para Dados da SSP-SP
Analisa arquivos JSON de saída e busca por localização
"""

import os
import json
import logging
from datetime import datetime
from typing import List, Dict, Tuple, Optional
try:
    from ..config.settings import settings
    from ..utils.logger import setup_logger
    from ..utils.geo_utils import GeoUtils
    from ..utils.file_utils import FileUtils
except ImportError:
    # Fallback para quando executado da raiz
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
    from config.settings import settings
    from utils.logger import setup_logger
    from utils.geo_utils import GeoUtils
    from utils.file_utils import FileUtils

class GeoAnalyzer:
    def __init__(self, output_dir: Optional[str] = None):
        """
        Inicializa o analisador geográfico
        
        Args:
            output_dir (str, optional): Diretório com os arquivos JSON de saída
        """
        self.output_dir = output_dir or settings.OUTPUT_DIR
        self.geo_utils = GeoUtils()
        self.file_utils = FileUtils()
        self.logger = setup_logger("geo_analyzer")
        
        # Verificar se o diretório existe
        if not os.path.exists(self.output_dir):
            raise FileNotFoundError(f"Diretório {self.output_dir} não encontrado")
    
    def load_all_json_files(self) -> List[Dict]:
        """
        Carrega todos os arquivos JSON do diretório de saída
        
        Returns:
            List[Dict]: Lista com todos os dados carregados
        """
        return self.file_utils.load_all_json_files(self.output_dir)
    
    def search_by_street(self, street_name: str) -> Optional[Tuple[float, float]]:
        """
        Busca coordenadas por nome da rua nos dados
        
        Args:
            street_name (str): Nome da rua para buscar
            
        Returns:
            Optional[Tuple[float, float]]: (latitude, longitude) ou None se não encontrado
        """
        all_data = self.load_all_json_files()
        return self.geo_utils.search_by_street(street_name, all_data)
    
    def find_records_in_radius(self, center_lat: float, center_lon: float, 
                              radius_km: float = 5.0) -> List[Dict]:
        """
        Encontra registros dentro de um raio específico
        
        Args:
            center_lat (float): Latitude do centro
            center_lon (float): Longitude do centro
            radius_km (float): Raio em quilômetros
            
        Returns:
            List[Dict]: Lista de registros com distância calculada
        """
        all_data = self.load_all_json_files()
        return self.geo_utils.find_records_in_radius(center_lat, center_lon, radius_km, all_data)
    
    def search_and_analyze(self, query: str, radius_km: float = 5.0) -> List[Dict]:
        """
        Busca e analisa registros por query (rua ou coordenadas)
        
        Args:
            query (str): Query de busca (nome da rua ou coordenadas)
            radius_km (float): Raio de busca em quilômetros
            
        Returns:
            List[Dict]: Lista de registros encontrados
        """
        try:
            # Verificar se é formato de coordenadas
            if self.geo_utils.is_coordinate_format(query):
                lat, lon = self.geo_utils.parse_coordinates(query)
                self.logger.info(f"Buscando por coordenadas: {lat}, {lon}")
                return self.find_records_in_radius(lat, lon, radius_km)
            
            # Buscar por rua
            else:
                self.logger.info(f"Buscando por rua: {query}")
                coords = self.search_by_street(query)
                
                if coords:
                    lat, lon = coords
                    return self.find_records_in_radius(lat, lon, radius_km)
                else:
                    self.logger.warning(f"Rua '{query}' não encontrada")
                    return []
                    
        except Exception as e:
            self.logger.error(f"Erro na busca: {e}")
            return []
    
    def print_results(self, records: List[Dict], query: str, radius_km: float):
        """
        Imprime resultados da busca de forma organizada
        
        Args:
            records (List[Dict]): Registros encontrados
            query (str): Query de busca
            radius_km (float): Raio de busca
        """
        if not records:
            print(f"\n❌ Nenhum registro encontrado para '{query}' em raio de {radius_km}km")
            return
        
        print(f"\n✅ Encontrados {len(records)} registros para '{query}' em raio de {radius_km}km")
        print("=" * 80)
        
        # Agrupar por categoria
        categorias = {}
        for record in records:
            cat = record['categoria']
            if cat not in categorias:
                categorias[cat] = []
            categorias[cat].append(record)
        
        # Mostrar estatísticas gerais
        total_dist = sum(r['distancia_km'] for r in records)
        media_dist = total_dist / len(records)
        min_dist = records[0]['distancia_km']
        max_dist = records[-1]['distancia_km']
        
        print(f"\n📊 Estatísticas Gerais:")
        print(f"   📏 Distância média: {media_dist:.2f}km")
        print(f"   📏 Distância mínima: {min_dist}km")
        print(f"   📏 Distância máxima: {max_dist}km")
        print(f"   📋 Categorias encontradas: {len(categorias)}")
        
        # Mostrar por categoria
        for categoria, cat_records in categorias.items():
            print(f"\n📋 Categoria: {categoria}")
            print(f"   Registros: {len(cat_records)}")
            print("-" * 80)
            
            for i, record in enumerate(cat_records[:10], 1):  # Mostrar apenas os 10 primeiros
                print(f"{i:2d}. 📍 Distância: {record['distancia_km']}km")
                print(f"    🌍 Coordenadas: {record['latitude']}, {record['longitude']}")
                
                # Mostrar TODOS os campos relevantes dos dados originais
                dados = record['dados_originais']
                
                # Campos prioritários (sempre mostrar se existirem)
                priority_fields = settings.PRIORITY_FIELDS
                shown_fields = set()
                
                for field in priority_fields:
                    if field in dados and dados[field] and str(dados[field]).strip():
                        print(f"    📝 {field.title()}: {dados[field]}")
                        shown_fields.add(field)
                
                # Mostrar outros campos relevantes que não foram mostrados
                other_relevant_fields = settings.SECONDARY_FIELDS
                
                for field in other_relevant_fields:
                    if (field in dados and dados[field] and 
                        str(dados[field]).strip() and field not in shown_fields):
                        print(f"    📋 {field.title()}: {dados[field]}")
                        shown_fields.add(field)
                
                # Mostrar campos adicionais que não estão nas listas
                for field, value in dados.items():
                    if (field not in shown_fields and 
                        field not in ['id', 'index', 'row'] and
                        value and str(value).strip() and
                        len(str(value)) < 100):  # Evitar campos muito longos
                        print(f"    📄 {field.title()}: {value}")
                
                print()
            
            if len(cat_records) > 10:
                print(f"    ... e mais {len(cat_records) - 10} registros")
        
        # Mostrar estatísticas por categoria
        print(f"\n📈 Estatísticas por Categoria:")
        for cat, cat_records in categorias.items():
            cat_distances = [r['distancia_km'] for r in cat_records]
            cat_media = sum(cat_distances) / len(cat_distances)
            print(f"   📋 {cat}: {len(cat_records)} registros (média: {cat_media:.2f}km)")
        
        # Mostrar tipos de ocorrência se disponíveis
        tipos = {}
        for record in records:
            dados = record['dados_originais']
            if 'tipo' in dados and dados['tipo']:
                tipo = str(dados['tipo']).strip()
                if tipo not in tipos:
                    tipos[tipo] = 0
                tipos[tipo] += 1
        
        if tipos:
            print(f"\n🚨 Tipos de Ocorrência:")
            for tipo, count in sorted(tipos.items(), key=lambda x: x[1], reverse=True):
                print(f"   - {tipo}: {count}")
    
    def export_detailed_results(self, records: List[Dict], query: str, radius_km: float, 
                               output_file: Optional[str] = None) -> Optional[str]:
        """
        Exporta resultados detalhados para arquivo JSON
        
        Args:
            records (List[Dict]): Registros encontrados
            query (str): Query de busca
            radius_km (float): Raio de busca
            output_file (str, optional): Nome do arquivo de saída
        
        Returns:
            Optional[str]: Caminho do arquivo salvo ou None se erro
        """
        return self.file_utils.save_detailed_results(records, query, radius_km, output_file)

def main():
    """Função principal para teste"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Analisador Geográfico SSP-SP')
    parser.add_argument('query', help='Rua ou coordenadas (formato: "lat,lon")')
    parser.add_argument('--raio', type=float, default=5.0, help='Raio em km (padrão: 5)')
    parser.add_argument('--output-dir', default='output', help='Diretório com arquivos JSON')
    parser.add_argument('--export', action='store_true', help='Exportar resultados detalhados para JSON')
    parser.add_argument('--output-file', help='Nome do arquivo de saída para exportação')
    
    args = parser.parse_args()
    
    try:
        # Criar analisador
        analyzer = GeoAnalyzer(args.output_dir)
        
        # Realizar busca
        records = analyzer.search_and_analyze(args.query, args.raio)
        
        # Imprimir resultados
        analyzer.print_results(records, args.query, args.raio)
        
        # Exportar se solicitado
        if args.export:
            output_file = analyzer.export_detailed_results(
                records, args.query, args.raio, args.output_file
            )
            if output_file:
                print(f"\n💾 Resultados exportados para: {output_file}")
            else:
                print("\n❌ Erro ao exportar resultados")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 