"""
SSP-SP Data Filter - Sistema de Análise de Dados Criminais
Versão: 2.0.0
Autor: Leonardo
"""

__version__ = "2.0.0"
__author__ = "Leonardo"
__description__ = "Sistema completo para scraping e análise geográfica de dados criminais da SSP-SP"

# Imports principais para facilitar o uso
from .core.scraper import SSPDataScraper
from .analyzers.geo_analyzer import GeoAnalyzer

__all__ = [
    'SSPDataScraper',
    'GeoAnalyzer',
] 