#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script principal para executar o scraper da SSP-SP
"""

import sys
import os
import argparse

# Adicionar o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.scraper import SSPDataScraper
from config.settings import settings
from utils.logger import setup_logger

def main():
    """Função principal"""
    # Configurar logger
    logger = setup_logger("scraper_main")
    
    parser = argparse.ArgumentParser(description='Scraper de Dados SSP-SP')
    parser.add_argument('--ano', type=int, help='Ano desejado (ex: 2024)')
    args = parser.parse_args()
    
    print("=== Scraper de Dados SSP-SP ===")
    print("Este script irá baixar dados criminais e filtrar por São José dos Campos")
    print("Usando Pydoll para automação de browser")
    print()
    
    ano = args.ano
    if ano:
        print(f"Buscando dados do ano: {ano}")
    else:
        # Perguntar o ano (opcional)
        ano_input = input("Digite o ano desejado (ou pressione Enter para usar o mais recente): ").strip()
        if ano_input:
            try:
                ano = int(ano_input)
                print(f"Buscando dados do ano: {ano}")
            except ValueError:
                print("Ano inválido. Usando o ano mais recente disponível.")
                ano = None
        else:
            print("Usando o ano mais recente disponível.")
            ano = None
    print()
    print("Iniciando o scraping com Pydoll...")
    print("Isso pode demorar alguns minutos...")
    print()
    try:
        # Criar e executar o scraper
        scraper = SSPDataScraper(target_year=ano)
        success = scraper.run()
        print()
        if success:
            print("=== Scraping Concluído com Sucesso! ===")
        else:
            print("=== Scraping Concluído com Problemas ===")
        print(f"Arquivos JSON foram salvos na pasta '{settings.OUTPUT_DIR}/'")
        print(f"Arquivos originais foram salvos na pasta '{settings.DOWNLOADS_DIR}/'")
        print(f"Logs detalhados estão em '{settings.LOG_FILE}'")
        print()
        print("💡 Próximos passos:")
        print("   python scripts/geo_search.py")
        print("   python scripts/geo_analyzer_cli.py")
    except KeyboardInterrupt:
        print("\nScraping interrompido pelo usuário.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Erro durante o scraping: {e}")
        print(f"\nErro durante o scraping: {e}")
        print(f"Verifique o arquivo de log '{settings.LOG_FILE}' para mais detalhes.")
        sys.exit(1)

if __name__ == "__main__":
    main() 