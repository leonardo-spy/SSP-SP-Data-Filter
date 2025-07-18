#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para scraping com cidade específica
Uso: python scripts/scraper_cidade.py "Nome da Cidade"
"""

import sys
import os
import argparse

# Adicionar o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description='Scraper SSP-SP com cidade específica')
    parser.add_argument('cidade', help='Nome da cidade para filtrar')
    parser.add_argument('--ano', type=int, help='Ano específico (opcional)')
    
    args = parser.parse_args()
    
    print(f"=== Scraper SSP-SP para {args.cidade} ===")
    print(f"Cidade: {args.cidade}")
    print(f"Ano: {args.ano or 'Mais recente'}")
    print()
    
    try:
        # Importar módulos dinamicamente
        from core.scraper import SSPDataScraper
        from config.settings import settings
        
        # Configurar cidade
        settings.DEFAULT_CITY = args.cidade
        
        # Criar e executar o scraper
        scraper = SSPDataScraper(target_year=args.ano)
        success = scraper.run()
        
        print()
        if success:
            print("=== Scraping Concluído com Sucesso! ===")
        else:
            print("=== Scraping Concluído com Problemas ===")
            
        print(f"Arquivos JSON foram salvos na pasta '{settings.OUTPUT_DIR}/'")
        print(f"Filtrados por: {args.cidade}")
        
    except KeyboardInterrupt:
        print("\nScraping interrompido pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\nErro durante o scraping: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 