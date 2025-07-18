#!/usr/bin/env python3
"""
    Exemplo básico de uso do SSP-SP Data Filter
"""

import sys
import os

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.scraper import SSPDataScraper
from analyzers.geo_analyzer import GeoAnalyzer
from config.settings import settings

def main():
    """Exemplo básico de scraping e análise"""
    print("🚀 Exemplo básico de uso")
    print("=" * 40)
    
    # 1. Executar scraping
    print("1. Executando scraping...")
    scraper = SSPDataScraper(target_year=2024)
    success = scraper.run()
    
    if not success:
        print("❌ Erro no scraping")
        return
    
    # 2. Análise geográfica
    print("\n2. Análise geográfica...")
    analyzer = GeoAnalyzer(settings.OUTPUT_DIR)
    records = analyzer.search_and_analyze("São José", 3.0)
    
    if records:
        print(f"✅ Encontrados {len(records)} registros")
        analyzer.print_results(records, "São José", 3.0)
    else:
        print("❌ Nenhum registro encontrado")

if __name__ == "__main__":
    main()
