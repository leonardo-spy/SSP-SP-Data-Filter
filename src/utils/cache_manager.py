#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerenciador de Cache - Controla arquivos processados e configurações
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Set
try:
    from ..config.settings import settings
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
    from config.settings import settings

class CacheManager:
    """Gerencia cache de arquivos processados e configurações"""
    
    def __init__(self):
        """Inicializa o gerenciador de cache"""
        self.cache_file = settings.CACHE_FILE
        self.cache_data = self._load_cache()
        self.logger = logging.getLogger(__name__)
    
    def _load_cache(self) -> Dict:
        """Carrega dados do cache"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logging.warning(f"Erro ao carregar cache: {e}")
        
        return {
            "processed_files": {},
            "processed_cities": {},
            "available_years": set(),
            "last_update": datetime.now().isoformat(),
            "version": "1.0"
        }
    
    def _save_cache(self):
        """Salva dados do cache"""
        try:
            # Converter sets para listas para serialização JSON
            cache_to_save = self.cache_data.copy()
            if "available_years" in cache_to_save and isinstance(cache_to_save["available_years"], set):
                cache_to_save["available_years"] = list(cache_to_save["available_years"])
            
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_to_save, f, indent=2, ensure_ascii=False)
            
            self.logger.debug(f"Cache salvo em: {self.cache_file}")
        except Exception as e:
            self.logger.error(f"Erro ao salvar cache: {e}")
    
    def is_file_processed(self, category: str, year: int) -> bool:
        """Verifica se um arquivo já foi processado"""
        key = f"{category}_{year}"
        return key in self.cache_data.get("processed_files", {})
    
    def mark_file_processed(self, category: str, year: int, file_info: Dict):
        """Marca um arquivo como processado"""
        key = f"{category}_{year}"
        self.cache_data.setdefault("processed_files", {})[key] = {
            "category": category,
            "year": year,
            "processed_at": datetime.now().isoformat(),
            "file_info": file_info
        }
        self._save_cache()
    
    def is_city_processed(self, category: str, year: int, city: str) -> bool:
        """Verifica se uma cidade já foi processada para uma categoria/ano"""
        key = f"{category}_{year}_{city}"
        return key in self.cache_data.get("processed_cities", {})
    
    def mark_city_processed(self, category: str, year: int, city: str, file_info: Dict):
        """Marca uma cidade como processada"""
        key = f"{category}_{year}_{city}"
        self.cache_data.setdefault("processed_cities", {})[key] = {
            "category": category,
            "year": year,
            "city": city,
            "processed_at": datetime.now().isoformat(),
            "file_info": file_info
        }
        self._save_cache()
    
    def add_available_year(self, year: int):
        """Adiciona um ano à lista de anos disponíveis"""
        # Garantir que available_years seja sempre um set
        if "available_years" not in self.cache_data:
            self.cache_data["available_years"] = set()
        elif isinstance(self.cache_data["available_years"], list):
            self.cache_data["available_years"] = set(self.cache_data["available_years"])
        
        self.cache_data["available_years"].add(year)
        self._save_cache()
    
    def get_available_years(self) -> Set[int]:
        """Retorna anos disponíveis"""
        years = self.cache_data.get("available_years", set())
        if isinstance(years, list):
            return set(years)
        return years
    
    def validate_year(self, year: int) -> bool:
        """Valida se o ano é permitido (não futuro)"""
        current_year = datetime.now().year
        if year > current_year:
            self.logger.warning(f"Ano {year} é futuro. Ano atual: {current_year}")
            return False
        return True
    
    def get_processed_files(self) -> Dict:
        """Retorna todos os arquivos processados"""
        return self.cache_data.get("processed_files", {})
    
    def get_processed_cities(self) -> Dict:
        """Retorna todas as cidades processadas"""
        return self.cache_data.get("processed_cities", {})
    
    def clear_cache(self):
        """Limpa todo o cache"""
        self.cache_data = {
            "processed_files": {},
            "processed_cities": {},
            "available_years": set(),
            "last_update": datetime.now().isoformat(),
            "version": "1.0"
        }
        self._save_cache()
        self.logger.info("Cache limpo")
    
    def get_cache_info(self) -> Dict:
        """Retorna informações sobre o cache"""
        return {
            "total_processed_files": len(self.cache_data.get("processed_files", {})),
            "total_processed_cities": len(self.cache_data.get("processed_cities", {})),
            "available_years": list(self.get_available_years()),
            "last_update": self.cache_data.get("last_update"),
            "cache_file": self.cache_file
        } 