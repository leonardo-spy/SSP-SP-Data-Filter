#!/usr/bin/env python3
"""
Exemplo de configuração personalizada
"""

import sys
import os

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from config.settings import settings

def main():
    """Mostra como usar as configurações"""
    print("⚙️ Configurações do Sistema")
    print("=" * 30)
    
    print(f"Cidade padrão: {settings.DEFAULT_CITY}")
    print(f"Raio padrão: {settings.DEFAULT_RADIUS_KM}km")
    print(f"Timeout: {settings.REQUEST_TIMEOUT}s")
    print(f"Requisições concorrentes: {settings.CONCURRENT_REQUESTS}")
    
    print("\n📋 Categorias disponíveis:")
    for key, value in settings.CATEGORIES.items():
        print(f"   - {key}: {value}")

if __name__ == "__main__":
    main()
