#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Interativo para Análise Geográfica dos Dados SSP-SP
"""

import sys
import os

# Adicionar o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from analyzers.geo_analyzer import GeoAnalyzer
from config.settings import settings
from utils.logger import setup_logger

def main():
    """Função principal interativa"""
    # Configurar logger
    logger = setup_logger("geo_search")
    
    print("🔍 Analisador Geográfico SSP-SP")
    print("=" * 50)
    print("Este script analisa os dados JSON de saída e busca por localização")
    print()
    
    # Verificar se existe o diretório output
    if not os.path.exists(settings.OUTPUT_DIR):
        print(f"❌ Diretório '{settings.OUTPUT_DIR}' não encontrado!")
        print("Execute primeiro o scraper para gerar os arquivos JSON:")
        print("python scripts/run_scraper.py")
        return 1
    
    try:
        # Criar analisador
        analyzer = GeoAnalyzer(settings.OUTPUT_DIR)
        print("✅ Analisador inicializado com sucesso")
        print()
        
        while True:
            print("\nEscolha uma opção:")
            print("1. Buscar por rua")
            print("2. Buscar por coordenadas")
            print("3. Exportar resultados detalhados")
            print("4. Sair")
            
            choice = input("\nDigite sua escolha (1-4): ").strip()
            
            if choice == "1":
                # Buscar por rua
                street = input("Digite o nome da rua: ").strip()
                if not street:
                    print("❌ Nome da rua não pode estar vazio")
                    continue
                
                radius = input(f"Digite o raio em km (padrão: {settings.DEFAULT_RADIUS_KM}): ").strip()
                try:
                    radius_km = float(radius) if radius else settings.DEFAULT_RADIUS_KM
                except ValueError:
                    print(f"❌ Raio inválido, usando {settings.DEFAULT_RADIUS_KM}km")
                    radius_km = settings.DEFAULT_RADIUS_KM
                
                print(f"\n🔍 Buscando por rua: {street}")
                print(f"📏 Raio: {radius_km}km")
                print("⏳ Processando...")
                
                records = analyzer.search_and_analyze(street, radius_km)
                analyzer.print_results(records, street, radius_km)
                
            elif choice == "2":
                # Buscar por coordenadas
                print("\nFormato: latitude,longitude")
                print("Exemplo: -23.5505,-46.6333 (São Paulo)")
                coords = input("Digite as coordenadas: ").strip()
                
                if not coords:
                    print("❌ Coordenadas não podem estar vazias")
                    continue
                
                if not analyzer.is_coordinate_format(coords):
                    print("❌ Formato de coordenadas inválido")
                    print("Use o formato: latitude,longitude")
                    continue
                
                radius = input(f"Digite o raio em km (padrão: {settings.DEFAULT_RADIUS_KM}): ").strip()
                try:
                    radius_km = float(radius) if radius else settings.DEFAULT_RADIUS_KM
                except ValueError:
                    print(f"❌ Raio inválido, usando {settings.DEFAULT_RADIUS_KM}km")
                    radius_km = settings.DEFAULT_RADIUS_KM
                
                print(f"\n🔍 Buscando por coordenadas: {coords}")
                print(f"📏 Raio: {radius_km}km")
                print("⏳ Processando...")
                
                records = analyzer.search_and_analyze(coords, radius_km)
                analyzer.print_results(records, coords, radius_km)
                
            elif choice == "3":
                # Exportar resultados detalhados
                print("\n💾 Exportar Resultados Detalhados")
                print("=" * 40)
                
                # Perguntar sobre a busca
                export_query = input("Digite a busca (rua ou coordenadas): ").strip()
                if not export_query:
                    print("❌ Busca não pode estar vazia")
                    continue
                
                export_radius = input(f"Digite o raio em km (padrão: {settings.DEFAULT_RADIUS_KM}): ").strip()
                try:
                    export_radius_km = float(export_radius) if export_radius else settings.DEFAULT_RADIUS_KM
                except ValueError:
                    print(f"❌ Raio inválido, usando {settings.DEFAULT_RADIUS_KM}km")
                    export_radius_km = settings.DEFAULT_RADIUS_KM
                
                output_filename = input("Nome do arquivo de saída (opcional): ").strip()
                if not output_filename:
                    output_filename = None
                
                print(f"\n🔍 Buscando e exportando: {export_query}")
                print(f"📏 Raio: {export_radius_km}km")
                print("⏳ Processando...")
                
                # Realizar busca
                export_records = analyzer.search_and_analyze(export_query, export_radius_km)
                
                if export_records:
                    # Exportar resultados
                    output_file = analyzer.export_detailed_results(
                        export_records, export_query, export_radius_km, output_filename
                    )
                    
                    if output_file:
                        print(f"✅ Exportação concluída!")
                        print(f"📁 Arquivo: {output_file}")
                        print(f"📊 Registros exportados: {len(export_records)}")
                        
                        # Mostrar estatísticas rápidas
                        categories = {}
                        for record in export_records:
                            cat = record['categoria']
                            if cat not in categories:
                                categories[cat] = 0
                            categories[cat] += 1
                        
                        print(f"\n📋 Resumo por categoria:")
                        for cat, count in categories.items():
                            print(f"   - {cat}: {count} registros")
                    else:
                        print("❌ Erro ao exportar resultados")
                else:
                    print("❌ Nenhum registro encontrado para exportar")
                
            elif choice == "4":
                print("\n👋 Saindo...")
                break
                
            else:
                print("❌ Opção inválida. Digite 1, 2, 3 ou 4.")
            
            # Perguntar se quer continuar
            if choice in ["1", "2", "3"]:
                continue_search = input("\nDeseja fazer outra busca? (s/n): ").strip().lower()
                if continue_search not in ['s', 'sim', 'y', 'yes']:
                    print("\n👋 Saindo...")
                    break
    
    except KeyboardInterrupt:
        print("\n\n👋 Interrompido pelo usuário")
        return 0
    except Exception as e:
        logger.error(f"Erro no geo_search: {e}")
        print(f"\n❌ Erro: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 