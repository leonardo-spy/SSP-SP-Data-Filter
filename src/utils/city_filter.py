#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filtro de Cidade - Utilitário para busca flexível por cidade
"""

import re
import unicodedata
import logging
from typing import List, Dict, Any
try:
    from ..config.settings import settings
except ImportError:
    # Fallback para quando executado da raiz
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
    from config.settings import settings

class CityFilter:
    """Classe para filtro flexível de cidades"""
    
    def __init__(self):
        """Inicializa o filtro de cidade"""
        self.similarity_threshold = settings.CITY_SIMILARITY_THRESHOLD
        self.min_significant_words_ratio = settings.MIN_SIGNIFICANT_WORDS_RATIO
        self.min_significant_words_count = settings.MIN_SIGNIFICANT_WORDS_COUNT
    
    def normalize_city_name(self, city_name: str) -> str:
        """
        Normaliza o nome da cidade para busca flexível
        
        Args:
            city_name (str): Nome da cidade
            
        Returns:
            str: Nome normalizado
        """
        # Converter para minúsculas
        normalized = city_name.lower()
        
        # Remover acentos
        normalized = unicodedata.normalize('NFD', normalized)
        normalized = ''.join(c for c in normalized if not unicodedata.combining(c))
        
        # Remover pontuação e espaços extras
        normalized = re.sub(r'[^\w\s]', '', normalized)
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        
        return normalized
    
    def city_matches(self, cell_value: str, normalized_city: str) -> bool:
        """
        Verifica se o valor da célula corresponde à cidade normalizada usando algoritmo genérico
        
        Args:
            cell_value (str): Valor da célula
            normalized_city (str): Nome da cidade normalizado
            
        Returns:
            bool: True se corresponder
        """
        try:
            # Normalizar o valor da célula
            cell_normalized = self.normalize_city_name(str(cell_value))
            
            # Verificar correspondência exata
            if cell_normalized == normalized_city:
                return True
            
            # Verificar se contém a cidade (para casos como "S.JOSE DOS CAMPOS")
            if normalized_city in cell_normalized:
                return True
            
            # Verificar correspondência por palavras-chave
            city_words = normalized_city.split()
            cell_words = cell_normalized.split()
            
            if len(city_words) >= 2:
                # Algoritmo de correspondência por palavras principais
                matches = 0
                significant_matches = 0
                
                for city_word in city_words:
                    if len(city_word) > 2:  # Ignorar palavras muito curtas
                        # Verificar se a palavra está em qualquer lugar do texto da célula
                        if city_word in cell_normalized:
                            matches += 1
                            # Verificar se é uma palavra significativa (não apenas "dos", "de", etc.)
                            if city_word not in ['dos', 'das', 'do', 'da', 'de']:
                                significant_matches += 1
                
                # Critérios de correspondência:
                # 1. Pelo menos 2 palavras principais correspondem
                # 2. Ou pelo menos 60% das palavras significativas correspondem
                # 3. Ou pelo menos 3 palavras totais correspondem (para cidades longas)
                
                total_significant_words = len([w for w in city_words if w not in ['dos', 'das', 'do', 'da', 'de'] and len(w) > 2])
                
                if (significant_matches >= self.min_significant_words_count or 
                    (total_significant_words > 0 and significant_matches / total_significant_words >= self.min_significant_words_ratio) or
                    matches >= 3):
                    return True
            
            # Algoritmo de correspondência por similaridade de strings
            if self.string_similarity(cell_normalized, normalized_city) >= self.similarity_threshold:
                return True
            
            # Verificar abreviações genéricas
            if self.check_generic_abbreviations(cell_normalized, normalized_city):
                return True
            
            return False
            
        except Exception as e:
            logging.debug(f"Erro ao verificar correspondência: {e}")
            return False
    
    def string_similarity(self, str1: str, str2: str) -> float:
        """
        Calcula a similaridade entre duas strings usando algoritmo baseado em conjuntos
        
        Args:
            str1 (str): Primeira string
            str2 (str): Segunda string
            
        Returns:
            float: Similaridade entre 0 e 1
        """
        try:
            # Converter para conjuntos de caracteres e calcular similaridade
            set1 = set(str1)
            set2 = set(str2)
            
            if not set1 and not set2:
                return 1.0
            
            intersection = set1.intersection(set2)
            union = set1.union(set2)
            
            return len(intersection) / len(union) if union else 0.0
            
        except Exception:
            return 0.0
    
    def check_generic_abbreviations(self, cell_normalized: str, normalized_city: str) -> bool:
        """
        Verifica abreviações genéricas que podem ser aplicadas a qualquer cidade
        
        Args:
            cell_normalized (str): Valor da célula normalizado
            normalized_city (str): Nome da cidade normalizado
            
        Returns:
            bool: True se encontrar abreviação válida
        """
        try:
            city_words = normalized_city.split()
            
            # Verificar se é uma abreviação por iniciais
            if len(city_words) >= 2:
                # Gerar possíveis abreviações por iniciais
                initials = ''.join(word[0] for word in city_words if len(word) > 0)
                if len(initials) >= 2 and initials in cell_normalized:
                    return True
                
                # Verificar abreviação por primeira letra + resto da primeira palavra
                if len(city_words[0]) > 1:
                    first_word_abbr = city_words[0][0] + '.' + city_words[0][1:]
                    if first_word_abbr in cell_normalized:
                        return True
                
                # Verificar padrões comuns de abreviação
                patterns = [
                    f"{city_words[0][0]} {city_words[1]}",  # S PAULO
                    f"{city_words[0][0]}.{city_words[1]}",  # S.PAULO
                    f"{city_words[0][0]}{city_words[1]}",   # SPAULO
                ]
                
                for pattern in patterns:
                    if pattern in cell_normalized:
                        return True
            
            return False
            
        except Exception as e:
            logging.debug(f"Erro ao verificar abreviações: {e}")
            return False
    
    def find_city_columns(self, df_columns: List[str]) -> List[str]:
        """
        Encontra colunas que podem conter informações de cidade
        
        Args:
            df_columns (List[str]): Lista de colunas do DataFrame
            
        Returns:
            List[str]: Lista de colunas de cidade encontradas
        """
        city_columns = []
        for col in df_columns:
            col_lower = str(col).lower()
            if any(keyword in col_lower for keyword in ['cidade', 'municipio', 'local', 'city', 'município']):
                city_columns.append(col)
        
        return city_columns
    
    def filter_dataframe_by_city(self, df, city_name: str = "São José dos Campos") -> Any:
        """
        Filtra o DataFrame pela cidade especificada com busca flexível
        
        Args:
            df: DataFrame com os dados
            city_name (str): Nome da cidade para filtrar
            
        Returns:
            DataFrame: DataFrame filtrado
        """
        try:
            # Procurar por colunas que possam conter o nome da cidade
            city_columns = self.find_city_columns(df.columns)
            
            if not city_columns:
                logging.warning("Nenhuma coluna de cidade encontrada. Retornando dados completos.")
                return df
            
            # Normalizar o nome da cidade para busca
            normalized_city = self.normalize_city_name(city_name)
            logging.info(f"Buscando por cidade: '{city_name}' (normalizado: '{normalized_city}')")
            
            # Tentar filtrar por cada coluna de cidade
            filtered_df = None
            for col in city_columns:
                try:
                    # Converter para string e normalizar
                    df[col] = df[col].astype(str).str.strip()
                    
                    # Aplicar filtro flexível
                    temp_filtered = df[df[col].apply(lambda x: self.city_matches(x, normalized_city))]
                    
                    if not temp_filtered.empty:
                        filtered_df = temp_filtered
                        logging.info(f"Dados filtrados pela coluna: {col}")
                        logging.info(f"Encontrados {len(filtered_df)} registros para '{city_name}'")
                        break
                        
                except Exception as e:
                    logging.warning(f"Erro ao filtrar pela coluna {col}: {e}")
                    continue
            
            if filtered_df is None or filtered_df.empty:
                logging.warning(f"Nenhum dado encontrado para {city_name}. Retornando dados completos.")
                return df
            
            return filtered_df
            
        except Exception as e:
            logging.error(f"Erro ao filtrar por cidade: {e}")
            return df 