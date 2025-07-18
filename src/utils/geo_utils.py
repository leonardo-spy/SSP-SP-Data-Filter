#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilitários Geográficos - Funções para cálculos e manipulação de coordenadas
"""

import math
import logging
from typing import Tuple, Optional, List, Dict
try:
    from ..config.settings import settings
except ImportError:
    # Fallback para quando executado da raiz
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
    from config.settings import settings

class GeoUtils:
    """Classe com utilitários para cálculos geográficos"""
    
    def __init__(self):
        """Inicializa os utilitários geográficos"""
        self.earth_radius = settings.EARTH_RADIUS_KM
        self.latitude_fields = settings.LATITUDE_FIELDS
        self.longitude_fields = settings.LONGITUDE_FIELDS
        self.address_fields = settings.ADDRESS_FIELDS
    
    def extract_coordinates(self, record: Dict) -> Tuple[Optional[float], Optional[float]]:
        """
        Extrai coordenadas de um registro
        
        Args:
            record (Dict): Registro de dados
            
        Returns:
            Tuple[Optional[float], Optional[float]]: (latitude, longitude)
        """
        try:
            lat = None
            lon = None
            
            # Buscar latitude
            for field in self.latitude_fields:
                if field in record:
                    try:
                        lat = float(record[field])
                        break
                    except (ValueError, TypeError):
                        continue
            
            # Buscar longitude
            for field in self.longitude_fields:
                if field in record:
                    try:
                        lon = float(record[field])
                        break
                    except (ValueError, TypeError):
                        continue
            
            return lat, lon
            
        except Exception as e:
            logging.debug(f"Erro ao extrair coordenadas: {e}")
            return None, None
    
    def calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calcula a distância entre dois pontos usando a fórmula de Haversine
        
        Args:
            lat1 (float): Latitude do primeiro ponto
            lon1 (float): Longitude do primeiro ponto
            lat2 (float): Latitude do segundo ponto
            lon2 (float): Longitude do segundo ponto
            
        Returns:
            float: Distância em quilômetros
        """
        try:
            # Converter para radianos
            lat1_rad = math.radians(lat1)
            lon1_rad = math.radians(lon1)
            lat2_rad = math.radians(lat2)
            lon2_rad = math.radians(lon2)
            
            # Diferenças
            dlat = lat2_rad - lat1_rad
            dlon = lon2_rad - lon1_rad
            
            # Fórmula de Haversine
            a = (math.sin(dlat/2) ** 2 + 
                 math.cos(lat1_rad) * math.cos(lat2_rad) * 
                 math.sin(dlon/2) ** 2)
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            
            distance = self.earth_radius * c
            return round(distance, 2)
            
        except Exception as e:
            logging.error(f"Erro ao calcular distância: {e}")
            return float('inf')
    
    def is_coordinate_format(self, query: str) -> bool:
        """
        Verifica se a query está no formato de coordenadas
        
        Args:
            query (str): String para verificar
            
        Returns:
            bool: True se for formato de coordenadas
        """
        try:
            # Remover espaços
            query = query.strip()
            
            # Verificar se contém vírgula
            if ',' not in query:
                return False
            
            # Dividir por vírgula
            parts = query.split(',')
            if len(parts) != 2:
                return False
            
            # Tentar converter para float
            lat = float(parts[0].strip())
            lon = float(parts[1].strip())
            
            # Verificar limites geográficos
            if not (-90 <= lat <= 90):
                return False
            if not (-180 <= lon <= 180):
                return False
            
            return True
            
        except (ValueError, TypeError):
            return False
    
    def parse_coordinates(self, coord_string: str) -> Tuple[float, float]:
        """
        Converte string de coordenadas para tupla de floats
        
        Args:
            coord_string (str): String no formato "lat,lon"
            
        Returns:
            Tuple[float, float]: (latitude, longitude)
        """
        try:
            # Remover espaços e dividir
            parts = coord_string.strip().split(',')
            lat = float(parts[0].strip())
            lon = float(parts[1].strip())
            
            return lat, lon
            
        except (ValueError, IndexError) as e:
            raise ValueError(f"Formato de coordenadas inválido: {coord_string}") from e
    
    def search_by_street(self, street_name: str, all_data: List[Dict]) -> Optional[Tuple[float, float]]:
        """
        Busca coordenadas por nome da rua nos dados
        
        Args:
            street_name (str): Nome da rua para buscar
            all_data (List[Dict]): Lista com todos os dados carregados
            
        Returns:
            Optional[Tuple[float, float]]: (latitude, longitude) ou None se não encontrado
        """
        try:
            for data in all_data:
                for record in data.get('dados', []):
                    # Procurar por campos que possam conter endereço
                    for field in self.address_fields:
                        if field in record:
                            address_value = str(record[field]).lower()
                            if street_name.lower() in address_value:
                                # Tentar extrair coordenadas
                                lat, lon = self.extract_coordinates(record)
                                if lat and lon:
                                    logging.info(f"Rua '{street_name}' encontrada: {lat}, {lon}")
                                    return (lat, lon)
            
            logging.warning(f"Rua '{street_name}' não encontrada nos dados")
            return None
            
        except Exception as e:
            logging.error(f"Erro ao buscar rua: {e}")
            return None
    
    def find_records_in_radius(self, center_lat: float, center_lon: float, 
                              radius_km: float, all_data: List[Dict]) -> List[Dict]:
        """
        Encontra registros dentro de um raio específico
        
        Args:
            center_lat (float): Latitude do centro
            center_lon (float): Longitude do centro
            radius_km (float): Raio em quilômetros
            all_data (List[Dict]): Lista com todos os dados carregados
            
        Returns:
            List[Dict]: Lista de registros com distância calculada
        """
        try:
            records_in_radius = []
            
            for data in all_data:
                categoria = data.get('categoria', 'Desconhecida')
                
                for record in data.get('dados', []):
                    lat, lon = self.extract_coordinates(record)
                    
                    if lat and lon:
                        distance = self.calculate_distance(center_lat, center_lon, lat, lon)
                        
                        if distance <= radius_km:
                            record_with_distance = {
                                'categoria': categoria,
                                'latitude': lat,
                                'longitude': lon,
                                'distancia_km': distance,
                                'dados_originais': record
                            }
                            records_in_radius.append(record_with_distance)
            
            # Ordenar por distância (mais próximo primeiro)
            records_in_radius.sort(key=lambda x: x['distancia_km'])
            
            return records_in_radius
            
        except Exception as e:
            logging.error(f"Erro ao buscar registros em raio: {e}")
            return []
    
    def validate_coordinates(self, lat: float, lon: float) -> bool:
        """
        Valida se as coordenadas estão dentro dos limites geográficos
        
        Args:
            lat (float): Latitude
            lon (float): Longitude
            
        Returns:
            bool: True se as coordenadas são válidas
        """
        return -90 <= lat <= 90 and -180 <= lon <= 180
    
    def format_distance(self, distance_km: float) -> str:
        """
        Formata a distância para exibição
        
        Args:
            distance_km (float): Distância em quilômetros
            
        Returns:
            str: Distância formatada
        """
        if distance_km < 1:
            return f"{distance_km * 1000:.0f}m"
        else:
            return f"{distance_km:.2f}km" 