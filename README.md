# SSP-SP Data Filter - Sistema Modular

Sistema completo para scraping e análise geográfica de dados criminais da SSP-SP, com arquitetura modular e profissional.

---

## ⚠️ Requisitos do Navegador (Chromium)

O Pydoll depende de um navegador Chromium para funcionar. Por padrão, o Pydoll baixa e gerencia o Chromium automaticamente na primeira execução. **Em alguns ambientes Linux, pode ser necessário instalar dependências do sistema**:

```bash
sudo apt-get update
sudo apt-get install -y chromium-browser libnss3 libatk-bridge2.0-0 libgtk-3-0 libxss1 libasound2 libgbm1 libxshmfence1 libxcomposite1 libxrandr2 libxdamage1 libxfixes3 libxext6 libx11-xcb1 libx11-6 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxi6 libxtst6 libxrandr2 libxss1 libxkbcommon0 libatspi2.0-0
```

Se o Pydoll não conseguir baixar ou rodar o Chromium automaticamente, instale manualmente ou garanta que as dependências acima estejam presentes.

---

## 🖥️ Modo Headless (sem interface gráfica)

Por padrão, o scraper roda o navegador Chromium em modo **headless** (sem interface gráfica), tornando o scraping mais rápido e compatível com servidores e ambientes sem X11.

- O modo headless pode ser configurado de três formas (ordem de prioridade):
  1. **Parâmetro ao instanciar o scraper:**
     ```python
     from utils.ssp_browser_scraper import SSPBrowserScraper
     scraper = SSPBrowserScraper(headless=False)
     ```
  2. **Configuração centralizada em `src/config/settings.py`:**
     ```python
     # No settings.py
     PYDOLL_HEADLESS = True  # ou False
     ```
  3. **Variável de ambiente:**
     ```bash
     export PYDOLL_HEADLESS=0  # ou 1, true, false, yes, no
     ```

> **Nota:** Em servidores ou ambientes sem interface gráfica, mantenha o padrão headless=True.

---

## 🏗️ Arquitetura do Projeto

```
ssp-sp-data-filter/
├── src/                          # Código fonte principal
│   ├── core/                     # Funcionalidades principais
│   │   ├── __init__.py
│   │   └── scraper.py           # Scraper principal (Pydoll)
│   ├── analyzers/                # Analisadores de dados
│   │   ├── __init__.py
│   │   └── geo_analyzer.py      # Analisador geográfico
│   ├── config/                   # Configurações
│   │   ├── __init__.py
│   │   └── settings.py          # Configurações centralizadas
│   ├── models/                   # Modelos de dados
│   │   ├── __init__.py
│   │   └── data_models.py       # Modelos estruturados
│   ├── utils/                    # Utilitários
│   │   ├── __init__.py
│   │   ├── logger.py            # Sistema de logging
│   │   ├── city_filter.py       # Filtro de cidades
│   │   ├── geo_utils.py         # Utilitários geográficos
│   │   ├── file_utils.py        # Utilitários de arquivo
│   │   └── ssp_browser_scraper.py # Scraper com Pydoll
│   └── __init__.py              # Módulo principal
├── scripts/                      # Scripts executáveis
│   ├── run_scraper.py           # Script principal do scraper
│   ├── scraper_cidade.py        # Scraper com cidade específica
│   ├── geo_search.py            # Interface de busca geográfica
│   ├── geo_analyzer_cli.py      # Análise geográfica CLI
│   └── setup_modular.py         # Script de setup
├── tests/                        # Testes
│   ├── unit/                    # Testes unitários
│   └── integration/             # Testes de integração
├── docs/                         # Documentação
├── examples/                     # Exemplos de uso
├── downloads/                    # Arquivos baixados
├── output/                       # Arquivos JSON processados
├── requirements.txt              # Dependências
└── README.md                     # Documentação principal
```

## 🚀 Vantagens da Nova Arquitetura

### **1. Modularidade**
- **Separação de responsabilidades**: Cada módulo tem uma função específica
- **Reutilização de código**: Utilitários compartilhados entre módulos
- **Manutenibilidade**: Fácil de modificar e estender

### **2. Scraping com Pydoll**
- **Automação de browser**: Usa Pydoll para renderizar páginas JavaScript
- **Extração confiável**: Acessa links dinâmicos carregados via JavaScript
- **Fluxo síncrono**: Processamento sequencial e previsível
- **Fallback robusto**: Usa requests como backup para downloads
- **Sem dependências externas**: Não precisa de Chrome/WebDriver

### **3. Configuração Centralizada**
- **Arquivo de configurações**: Todas as configurações em um local
- **Variáveis de ambiente**: Suporte a configuração via env vars
- **Flexibilidade**: Fácil de personalizar sem modificar código

### **4. Modelos Estruturados**
- **Dataclasses**: Modelos de dados tipados e organizados
- **Validação**: Estruturas de dados consistentes
- **Documentação**: Modelos auto-documentados

### **5. Sistema de Logging**
- **Logging centralizado**: Sistema unificado de logs
- **Múltiplos handlers**: Console e arquivo
- **Configurável**: Níveis e formatos personalizáveis

### **6. Testes Organizados**
- **Testes unitários**: Testes isolados por funcionalidade
- **Testes de integração**: Testes de fluxo completo
- **Cobertura**: Melhor cobertura de código

## �� Instalação

### **1. Clone o repositório**
```bash
git clone https://github.com/leonardo-spy/SSP-SP-Data-Filter.git
cd data-filter-seguranca
```

### **2. Crie um ambiente virtual (recomendado)**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### **3. Instale as dependências**
```bash
pip install -r requirements.txt
pip install pydoll-python
```

> **Nota:** O Pydoll será instalado via PyPI como `pydoll-python`.

### **4. Configure variáveis de ambiente (opcional)**
```bash
export SSP_TARGET_YEAR=2024
export SSP_DEFAULT_CITY="São José dos Campos"
export SSP_REQUEST_TIMEOUT=30
export SSP_DEFAULT_RADIUS_KM=5.0
```

## 🎯 Como Usar

### **1. Executar o Scraper**
```bash
# Script principal
python scripts/run_scraper.py

# Scraper com cidade específica
python scripts/scraper_cidade.py "Campinas"
python scripts/scraper_cidade.py "Santos" --ano 2024

# Ou usando o módulo diretamente
python -c "
import sys
sys.path.append('src')
from core.scraper import SSPDataScraper

scraper = SSPDataScraper(target_year=2024)
success = scraper.run()
print(f'Scraping {'sucesso' if success else 'falha'}')
"
```

### **2. Análise Geográfica**
```bash
# Interface interativa
python scripts/geo_search.py

# Linha de comando
python scripts/geo_analyzer_cli.py "Rua das Flores" --raio 3 --export
python scripts/geo_analyzer_cli.py "-23.1891,-45.8841" --raio 5 --export --output-file minha_analise.json

# Como módulo Python
python -c "
import sys
sys.path.append('src')
from analyzers.geo_analyzer import GeoAnalyzer

analyzer = GeoAnalyzer('output')
records = analyzer.search_and_analyze('São José', 3.0)
analyzer.print_results(records, 'São José', 3.0)
"
```

### **3. Scripts de Linha de Comando**

O sistema inclui scripts para uso direto via linha de comando:

```bash
# Scraper principal
python scripts/run_scraper.py

# Scraper com cidade específica
python scripts/scraper_cidade.py "Campinas"

# Análise geográfica por rua
python scripts/geo_analyzer_cli.py "Rua das Flores" --raio 3 --export

# Análise geográfica por coordenadas
python scripts/geo_analyzer_cli.py "-23.1891,-45.8841" --raio 5 --export --output-file minha_analise.json
```

### **4. Usar como Módulo Python**
```python
import sys
sys.path.append('src')

from core.scraper import SSPDataScraper
from analyzers.geo_analyzer import GeoAnalyzer
from config.settings import settings
from models.data_models import ScrapingResult, GeoRecord

# Configurar logger
from utils.logger import setup_logger
logger = setup_logger("meu_script")

# Usar configurações
print(f"Cidade padrão: {settings.DEFAULT_CITY}")
print(f"Raio padrão: {settings.DEFAULT_RADIUS_KM}km")

# Executar scraping
scraper = SSPDataScraper(target_year=2024)
success = scraper.run()

# Análise geográfica
analyzer = GeoAnalyzer(settings.OUTPUT_DIR)
records = analyzer.search_and_analyze("-23.1891,-45.8841", 5.0)
```

## ⚙️ Configuração

### **Arquivo de Configurações (`src/config/settings.py`)**

```python
@dataclass
class Settings:
    # URLs e endpoints
    CONSULTAS_URL: str = "https://www.ssp.sp.gov.br/estatistica/consultas"
    
    # Configurações de scraping
    DEFAULT_TARGET_YEAR: Optional[int] = None
    DEFAULT_CITY: str = "São José dos Campos"
    REQUEST_TIMEOUT: int = 30
    MAX_RETRIES: int = 3
    
    # Configurações de arquivos
    DOWNLOADS_DIR: str = "downloads"
    OUTPUT_DIR: str = "output"
    LOG_FILE: str = "ssp_scraper.log"
    
    # Configurações de análise geográfica
    DEFAULT_RADIUS_KM: float = 5.0
    EARTH_RADIUS_KM: float = 6371.0
    
    # Categorias de dados
    CATEGORIES: Dict[str, str] = field(default_factory=lambda: {
        "dados_criminais": "Dados Criminais",
        "dados_produtividade": "Dados de Produtividade", 
        "morte_intervencao": "Morte Decorrente de Intervenção Policial",
        "celulares_subtraidos": "Celulares subtraídos",
        "veiculos_subtraidos": "Veículos subtraídos",
        "objetos_subtraidos": "Objetos subtraídos"
    })
```

### **Variáveis de Ambiente**

```bash
# Configurações de scraping
SSP_TARGET_YEAR=2024
SSP_DEFAULT_CITY="São José dos Campos"
SSP_REQUEST_TIMEOUT=30

# Configurações de análise
SSP_DEFAULT_RADIUS_KM=5.0
```

## 🧪 Testes

### **Executar Testes**
```bash
# Testes unitários
python -m pytest tests/unit/

# Testes de integração
python -m pytest tests/integration/

# Todos os testes
python -m pytest tests/
```

### **Cobertura de Código**
```bash
python -m pytest --cov=src tests/
```

## 📊 Modelos de Dados

### **ScrapingResult**
```python
@dataclass
class ScrapingResult:
    categoria: str
    arquivo_original: str
    total_registros: int
    registros_filtrados: int
    cidade_filtro: str
    data_processamento: datetime
    dados: List[Dict[str, Any]]
    sucesso: bool = True
    erro: Optional[str] = None
```

### **GeoRecord**
```python
@dataclass
class GeoRecord:
    categoria: str
    latitude: float
    longitude: float
    distancia_km: float
    dados_originais: Dict[str, Any]
    
    def get_address(self) -> Optional[str]:
        """Extrai endereço dos dados originais"""
    
    def get_type(self) -> Optional[str]:
        """Extrai tipo de ocorrência"""
```

### **AnalysisResult**
```python
@dataclass
class AnalysisResult:
    query: str
    raio_km: float
    total_registros: int
    registros: List[GeoRecord]
    estatisticas: CategoryStats
    data_analise: datetime
```

## 🔧 Desenvolvimento

### **Adicionar Nova Funcionalidade**

1. **Criar módulo** em `src/`
2. **Adicionar testes** em `tests/`
3. **Atualizar configurações** em `src/config/settings.py`
4. **Documentar** em `docs/`

### **Estrutura de um Novo Módulo**

```
src/novo_modulo/
├── __init__.py
├── main.py
├── utils.py
└── models.py
```

### **Padrões de Código**

- **Type hints**: Sempre usar type hints
- **Docstrings**: Documentar todas as funções
- **Logging**: Usar o sistema de logging centralizado
- **Configuração**: Usar as configurações centralizadas
- **Testes**: Escrever testes para novas funcionalidades

## 📈 Próximos Passos

### **Funcionalidades Planejadas**

1. **Interface Web**: Dashboard interativo
2. **API REST**: Endpoints para integração
3. **Visualização**: Mapas e gráficos
4. **Machine Learning**: Análise preditiva
5. **Cache**: Sistema de cache para performance
6. **Docker**: Containerização

### **Melhorias Técnicas**

1. **Database**: Persistência em banco de dados
2. **Queue**: Sistema de filas para processamento
3. **Monitoring**: Métricas e monitoramento
4. **CI/CD**: Pipeline de integração contínua
5. **Cache**: Sistema de cache para performance

## 🤝 Contribuição

1. **Fork** o repositório
2. **Crie** uma branch para sua feature
3. **Siga** os padrões de código
4. **Escreva** testes
5. **Documente** as mudanças
6. **Abra** um Pull Request

## 📄 Licença

Este projeto é para uso educacional e de pesquisa. Respeite os termos de uso do site da SSP-SP. 