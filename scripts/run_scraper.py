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
    parser.add_argument('--cidade', type=str, help='Cidade específica para filtrar (ex: "São José dos Campos")')
    parser.add_argument('--forcar-reprocessamento', action='store_true', help='Forçar reprocessamento mesmo se já existir cache')
    parser.add_argument('--limpar-cache', action='store_true', help='Limpar cache antes de executar')
    parser.add_argument('--mostrar-cache', action='store_true', help='Mostrar informações do cache')
    
    args = parser.parse_args()
    
    print("=== Scraper de Dados SSP-SP ===")
    print("Este script irá baixar dados criminais e filtrar por cidade")
    print("Usando Pydoll para automação de browser")
    print()
    
    # Configurar ano
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
    
    # Configurar cidade
    cidade = args.cidade
    if cidade:
        print(f"Filtrando dados para cidade: {cidade}")
    else:
        cidade_input = input("Digite a cidade para filtrar (ou pressione Enter para processar todas): ").strip()
        if cidade_input:
            cidade = cidade_input
            print(f"Filtrando dados para cidade: {cidade}")
        else:
            print("Processando dados de todas as cidades.")
            cidade = None
    
    print()
    print("Iniciando o scraping com Pydoll...")
    print("Isso pode demorar alguns minutos...")
    print()
    
    try:
        # Importar cache manager para operações de cache
        from utils.cache_manager import CacheManager
        cache_manager = CacheManager()
        
        # Mostrar cache se solicitado
        if args.mostrar_cache:
            cache_info = cache_manager.get_cache_info()
            print("=== Informações do Cache ===")
            print(f"Arquivos processados: {cache_info['total_processed_files']}")
            print(f"Cidades processadas: {cache_info['total_processed_cities']}")
            print(f"Anos disponíveis: {cache_info['available_years']}")
            print(f"Última atualização: {cache_info['last_update']}")
            print()
            return 0
        
        # Limpar cache se solicitado
        if args.limpar_cache:
            response = input("Tem certeza que deseja limpar o cache? (s/N): ").strip().lower()
            if response in ['s', 'sim', 'y', 'yes']:
                cache_manager.clear_cache()
                print("Cache limpo!")
                return 0
            else:
                print("Operação cancelada.")
                return 0
        
        # Configurar reprocessamento forçado
        if args.forcar_reprocessamento:
            settings.FORCE_REPROCESS = True
            print("⚠️  Modo de reprocessamento forçado ativado")
        
        # Criar e executar o scraper
        scraper = SSPDataScraper(target_year=ano, target_city=cidade)
        success = scraper.run()
        
        print()
        if success:
            print("=== Scraping Concluído com Sucesso! ===")
        else:
            print("=== Scraping Concluído com Problemas ===")
        
        print(f"Arquivos JSON foram salvos na pasta '{settings.OUTPUT_DIR}/'")
        if cidade:
            print(f"Arquivos filtrados por cidade foram salvos em '{settings.OUTPUT_DIR}/cities/'")
        print(f"Arquivos originais foram salvos na pasta '{settings.DOWNLOADS_DIR}/'")
        print(f"Cache salvo em '{settings.CACHE_FILE}'")
        print(f"Logs detalhados estão em '{settings.LOG_FILE}'")
        print()
        print("💡 Próximos passos:")
        print("   python scripts/geo_search.py")
        print("   python scripts/geo_analyzer_cli.py")
        print("   python scripts/run_scraper.py --mostrar-cache")
        
    except KeyboardInterrupt:
        print("\nScraping interrompido pelo usuário.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Erro durante o scraping: {e}")
        print(f"\nErro durante o scraping: {e}")
        print(f"Verifique o arquivo de log '{settings.LOG_FILE}' para mais detalhes.")
        sys.exit(1)

if __name__ == "__main__":
    exit(main()) 