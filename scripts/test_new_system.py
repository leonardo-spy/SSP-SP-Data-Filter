#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para o novo sistema de cache e processamento de cidades
"""

import sys
import os

# Adicionar o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.cache_manager import CacheManager
from config.settings import settings

def test_cache_system():
    """Testa o sistema de cache"""
    print("=== Teste do Sistema de Cache ===")
    
    # Criar cache manager
    cache_manager = CacheManager()
    
    # Mostrar informações iniciais
    print("📊 Informações iniciais do cache:")
    cache_info = cache_manager.get_cache_info()
    for key, value in cache_info.items():
        print(f"   {key}: {value}")
    
    # Testar validação de anos
    print("\n🔍 Testando validação de anos:")
    test_years = [2020, 2023, 2025, 2030]
    for year in test_years:
        is_valid = cache_manager.validate_year(year)
        status = "✅ Válido" if is_valid else "❌ Inválido (futuro)"
        print(f"   Ano {year}: {status}")
    
    # Simular processamento de arquivos
    print("\n📁 Simulando processamento de arquivos:")
    test_files = [
        ("dados_criminais", 2023),
        ("celulares_subtraidos", 2023),
        ("veiculos_subtraidos", 2023)
    ]
    
    for category, year in test_files:
        if cache_manager.is_file_processed(category, year):
            print(f"   ✅ {category}_{year} já processado")
        else:
            print(f"   ⏳ {category}_{year} não processado")
            # Simular processamento
            cache_manager.mark_file_processed(category, year, {
                "filename": f"{category}_{year}.xlsx",
                "total_registros": 1000,
                "cidade_filtro": "TODAS"
            })
            cache_manager.add_available_year(year)
            print(f"   ✅ {category}_{year} marcado como processado")
    
    # Simular processamento de cidades
    print("\n🏙️ Simulando processamento de cidades:")
    test_cities = [
        ("dados_criminais", 2023, "São José dos Campos"),
        ("celulares_subtraidos", 2023, "Campinas"),
        ("veiculos_subtraidos", 2023, "São Paulo")
    ]
    
    for category, year, city in test_cities:
        if cache_manager.is_city_processed(category, year, city):
            print(f"   ✅ {category}_{year}_{city} já processado")
        else:
            print(f"   ⏳ {category}_{year}_{city} não processado")
            # Simular processamento
            cache_manager.mark_city_processed(category, year, city, {
                "registros_filtrados": 100,
                "total_registros": 1000
            })
            print(f"   ✅ {category}_{year}_{city} marcado como processado")
    
    # Mostrar informações finais
    print("\n📊 Informações finais do cache:")
    cache_info = cache_manager.get_cache_info()
    for key, value in cache_info.items():
        print(f"   {key}: {value}")
    
    print("\n✅ Teste do sistema de cache concluído!")

def test_file_utils():
    """Testa as novas funcionalidades do FileUtils"""
    print("\n=== Teste do FileUtils ===")
    
    from utils.file_utils import FileUtils
    
    file_utils = FileUtils()
    
    # Testar estrutura de diretórios
    print("📁 Testando estrutura de diretórios:")
    print(f"   Output dir: {file_utils.output_dir}")
    print(f"   Downloads dir: {file_utils.downloads_dir}")
    
    # Verificar se diretórios existem
    for dir_name, dir_path in [("Output", file_utils.output_dir), ("Downloads", file_utils.downloads_dir)]:
        if os.path.exists(dir_path):
            print(f"   ✅ {dir_name}: {dir_path}")
        else:
            print(f"   ❌ {dir_name}: {dir_path} (não existe)")
    
    print("\n✅ Teste do FileUtils concluído!")

def main():
    """Função principal"""
    print("🚀 Iniciando testes do novo sistema...")
    print()
    
    try:
        test_cache_system()
        test_file_utils()
        
        print("\n🎉 Todos os testes concluídos com sucesso!")
        print("\n💡 Para usar o novo sistema:")
        print("   python scripts/run_scraper.py --ano 2023 --cidade 'São José dos Campos'")
        print("   python scripts/run_scraper.py --mostrar-cache")
        print("   python scripts/run_scraper.py --limpar-cache")
        
    except Exception as e:
        print(f"\n❌ Erro durante os testes: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 