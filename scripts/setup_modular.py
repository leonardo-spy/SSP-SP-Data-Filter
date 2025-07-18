#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de setup do SSP-SP Data Filter
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command: str, description: str) -> bool:
    """Executa um comando e mostra o progresso"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Concluído")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Erro:")
        print(f"   {e.stderr}")
        return False

def check_python_version() -> bool:
    """Verifica se a versão do Python é compatível"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7 ou superior é necessário para suporte a async/await")
        print(f"   Versão atual: {version.major}.{version.minor}.{version.micro}")
        return False
    else:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True

def create_directories() -> bool:
    """Cria diretórios necessários"""
    print("📁 Criando estrutura de diretórios...")
    
    directories = [
        "downloads",
        "output", 
        "logs",
        "docs",
        "examples"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"   ✅ {directory}/")
    
    return True

def install_dependencies() -> bool:
    """Instala as dependências do projeto"""
    print("\n📦 Instalando dependências...")
    
    # Atualizar pip
    if not run_command("python -m pip install --upgrade pip", "Atualizando pip"):
        return False
    
    # Instalar dependências
    if not run_command("pip install -r requirements.txt", "Instalando dependências do requirements.txt"):
        return False
    
    return True

def test_imports() -> bool:
    """Testa se os módulos podem ser importados"""
    print("\n🧪 Testando imports dos módulos...")
    
    try:
        # Testar se os arquivos principais existem
        core_files = [
            "src/core/scraper.py",
            "src/analyzers/geo_analyzer.py",
            "src/config/settings.py",
            "src/utils/logger.py",
            "src/models/data_models.py"
        ]
        
        for file_path in core_files:
            if os.path.exists(file_path):
                print(f"   ✅ {file_path}")
            else:
                print(f"   ❌ {file_path} - Arquivo não encontrado")
                return False
        
        # Testar se os arquivos podem ser executados
        test_script = '''
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

success = True

try:
    from config.settings import settings
    print("   ✅ config.settings - OK")
except Exception as e:
    print(f"   ❌ config.settings - Erro: {e}")
    success = False

try:
    from utils.logger import setup_logger
    print("   ✅ utils.logger - OK")
except Exception as e:
    print(f"   ❌ utils.logger - Erro: {e}")
    success = False

try:
    from models.data_models import ScrapingResult, GeoRecord
    print("   ✅ models.data_models - OK")
except Exception as e:
    print(f"   ❌ models.data_models - Erro: {e}")
    success = False

if success:
    print("   ✅ Todos os imports funcionando")
else:
    print("   ❌ Alguns imports falharam")
    sys.exit(1)
'''
        
        # Executar teste de imports
        result = subprocess.run([sys.executable, '-c', test_script], 
                              capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            print(result.stdout.strip())
            return True
        else:
            print(result.stderr.strip())
            return False
        
    except Exception as e:
        print(f"   ❌ Erro nos testes: {e}")
        return False

def create_example_scripts() -> bool:
    """Cria scripts de exemplo"""
    print("\n📝 Criando scripts de exemplo...")
    
    examples_dir = Path("examples")
    examples_dir.mkdir(exist_ok=True)
    
    # Exemplo básico de uso
    basic_example = '''#!/usr/bin/env python3
"""
    Exemplo básico de uso do SSP-SP Data Filter
"""

import asyncio
import sys
import os

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.scraper import SSPDataScraper
from analyzers.geo_analyzer import GeoAnalyzer
from config.settings import settings

async def main():
    """Exemplo básico de scraping e análise"""
    print("🚀 Exemplo básico de uso")
    print("=" * 40)
    
    # 1. Executar scraping
    print("1. Executando scraping...")
    scraper = SSPDataScraper(target_year=2024)
    await scraper.run()
    
    # 2. Análise geográfica
    print("\\n2. Análise geográfica...")
    analyzer = GeoAnalyzer(settings.OUTPUT_DIR)
    records = analyzer.search_and_analyze("São José", 3.0)
    
    if records:
        print(f"✅ Encontrados {len(records)} registros")
        analyzer.print_results(records, "São José", 3.0)
    else:
        print("❌ Nenhum registro encontrado")

if __name__ == "__main__":
    asyncio.run(main())
'''
    
    with open(examples_dir / "exemplo_basico.py", "w", encoding="utf-8") as f:
        f.write(basic_example)
    
    print("   ✅ examples/exemplo_basico.py")
    
    # Exemplo de configuração
    config_example = '''#!/usr/bin/env python3
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
    
    print("\\n📋 Categorias disponíveis:")
    for key, value in settings.CATEGORIES.items():
        print(f"   - {key}: {value}")

if __name__ == "__main__":
    main()
'''
    
    with open(examples_dir / "exemplo_config.py", "w", encoding="utf-8") as f:
        f.write(config_example)
    
    print("   ✅ examples/exemplo_config.py")
    
    return True

def main():
    """Função principal do setup"""
    print("🚀 Setup do SSP-SP Data Filter")
    print("=" * 60)
    
    # Verificar versão do Python
    if not check_python_version():
        sys.exit(1)
    
    # Criar diretórios
    if not create_directories():
        print("\n❌ Falha na criação de diretórios")
        sys.exit(1)
    
    # Instalar dependências
    if not install_dependencies():
        print("\n❌ Falha na instalação das dependências")
        print("Tente executar manualmente:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    
    # Testar imports
    if not test_imports():
        print("\n❌ Falha nos testes de import")
        print("Verifique se todos os arquivos estão no lugar correto")
        sys.exit(1)
    
    # Criar exemplos
    if not create_example_scripts():
        print("\n❌ Falha na criação de exemplos")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("🎉 Setup concluído com sucesso!")
    print("\n📁 Estrutura criada:")
    print("   src/           - Código fonte modular")
    print("   scripts/       - Scripts executáveis")
    print("   tests/         - Testes organizados")
    print("   docs/          - Documentação")
    print("   examples/      - Exemplos de uso")
    print("   downloads/     - Arquivos baixados")
    print("   output/        - Arquivos processados")
    
    print("\n🚀 Para começar:")
    print("   python scripts/run_scraper.py")
    print("   python scripts/geo_search.py")
    print("   python examples/exemplo_basico.py")
    
    print("\n📚 Documentação:")
    print("   README.md         - Documentação completa")

if __name__ == "__main__":
    main() 