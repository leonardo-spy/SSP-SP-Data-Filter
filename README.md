# SSP-SP Data Filter - Sistema Modular com Cache Inteligente

Sistema completo para scraping e análise geográfica de dados criminais da SSP-SP, com arquitetura modular, cache inteligente e processamento otimizado.

---

## 🆕 **Novidades da Versão 2.0**

### **🎯 Sistema de Cache Inteligente**
- **📁 Cache automático:** Rastreia arquivos e cidades já processados
- **⚡ Reprocessamento inteligente:** Evita trabalho desnecessário
- **📊 Controle de anos:** Bloqueia anos futuros automaticamente
- **💾 Persistência:** Cache salvo em `cache_config.json`

### **🔄 Novo Fluxo de Download**
- **📥 Download completo:** Baixa arquivos Excel sem filtro de cidade
- **🏙️ Filtro sob demanda:** Processa cidades apenas quando necessário
- **📂 Estrutura organizada:** Arquivos separados por ano/categoria/cidade
- **🎯 Eficiência máxima:** Otimiza uso de recursos e tempo

### **📊 Estrutura de Arquivos Melhorada**
```
output/
├── dados_criminais_2023.json          # Dados completos por ano/categoria
├── celulares_subtraidos_2023.json     # Dados completos
├── veiculos_subtraidos_2023.json      # Dados completos
├── objetos_subtraidos_2023.json       # Dados completos
├── dados_produtividade_2025.json      # Dados completos
└── cities/                            # Dados filtrados por cidade
    ├── dados_criminais_2023_São_José_dos_Campos.json
    ├── celulares_subtraidos_2023_Campinas.json
    └── veiculos_subtraidos_2023_São_Paulo.json
```

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
│   │   └── scraper.py           # Scraper principal com cache
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
│   │   ├── cache_manager.py     # Gerenciador de cache
│   │   └── ssp_browser_scraper.py # Scraper com Pydoll
│   └── __init__.py              # Módulo principal
├── scripts/                      # Scripts executáveis
│   ├── run_scraper.py           # Script principal com cache
│   ├── geo_search.py            # Interface de busca geográfica
│   ├── geo_analyzer_cli.py      # Análise geográfica CLI
│   ├── test_new_system.py       # Teste do sistema de cache
│   └── setup_modular.py         # Script de setup
├── tests/                        # Testes
│   ├── unit/                    # Testes unitários
│   └── integration/             # Testes de integração
├── docs/                         # Documentação
├── examples/                     # Exemplos de uso
├── downloads/                    # Arquivos Excel baixados
├── output/                       # Arquivos JSON processados
│   └── cities/                  # Dados filtrados por cidade
├── cache_config.json            # Cache de processamento
├── requirements.txt              # Dependências
└── README.md                     # Documentação principal
```

## 🚀 Vantagens da Nova Arquitetura

### **1. Sistema de Cache Inteligente**
- **💾 Cache persistente:** Evita reprocessamento desnecessário
- **📊 Rastreamento completo:** Arquivos, cidades e anos processados
- **⚡ Performance otimizada:** Processamento apenas do necessário
- **🔄 Controle granular:** Força reprocessamento quando necessário

### **2. Fluxo de Download Otimizado**
- **📥 Download completo:** Baixa todos os dados sem filtro inicial
- **🏙️ Filtro sob demanda:** Processa cidades apenas quando solicitado
- **📂 Estrutura organizada:** Separação clara de dados por categoria/ano/cidade
- **🎯 Eficiência máxima:** Minimiza downloads e processamento

### **3. Modularidade Avançada**
- **Separação de responsabilidades**: Cada módulo tem uma função específica
- **Reutilização de código**: Utilitários compartilhados entre módulos
- **Manutenibilidade**: Fácil de modificar e estender
- **Cache inteligente**: Sistema de cache integrado

### **4. Scraping com Pydoll**
- **Automação de browser**: Usa Pydoll para renderizar páginas JavaScript
- **Extração confiável**: Acessa links dinâmicos carregados via JavaScript
- **Fluxo síncrono**: Processamento sequencial e previsível
- **Fallback robusto**: Usa requests como backup para downloads
- **Sem dependências externas**: Não precisa de Chrome/WebDriver

### **5. Configuração Centralizada**
- **Arquivo de configurações**: Todas as configurações em um local
- **Variáveis de ambiente**: Suporte a configuração via env vars
- **Flexibilidade**: Fácil de personalizar sem modificar código

### **6. Modelos Estruturados**
- **Dataclasses**: Modelos de dados tipados e organizados
- **Validação**: Estruturas de dados consistentes
- **Documentação**: Modelos auto-documentados

### **7. Sistema de Logging**
- **Logging centralizado**: Sistema unificado de logs
- **Múltiplos handlers**: Console e arquivo
- **Configurável**: Níveis e formatos personalizáveis

### **8. Testes Organizados**
- **Testes unitários**: Testes isolados por funcionalidade
- **Testes de integração**: Testes de fluxo completo
- **Cobertura**: Melhor cobertura de código

## 🛠️ Instalação

### **1. Clone o repositório**
```bash
git clone https://github.com/leonardo-spy/SSP-SP-Data-Filter.git
cd SSP-SP-Data-Filter
```

### **2. Crie um ambiente virtual (recomendado)**
```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

### **3. Instale as dependências**
```bash
pip install -r requirements.txt
```

> **Nota:** O Pydoll será instalado via PyPI como `pydoll-python`.

### **4. Configure variáveis de ambiente (opcional)**
```bash
export SSP_TARGET_YEAR=2024
export SSP_DEFAULT_CITY="São José dos Campos"
export SSP_REQUEST_TIMEOUT=30
export SSP_DEFAULT_RADIUS_KM=5.0
export SSP_CACHE_ENABLED=true
export PYDOLL_HEADLESS=1
```

### **5. Teste a instalação**
```bash
# Testar o sistema de cache
python scripts/test_new_system.py

# Verificar se tudo está funcionando
python scripts/run_scraper.py --mostrar-cache
```

## 🎯 Como Usar

### **1. Executar o Scraper com Cache Inteligente**
```bash
# Script principal (baixa dados completos)
python scripts/run_scraper.py

# Scraper com ano e cidade específicos
python scripts/run_scraper.py --ano 2023 --cidade "São José dos Campos"

# Forçar reprocessamento (ignora cache)
python scripts/run_scraper.py --forcar-reprocessamento

# Mostrar informações do cache
python scripts/run_scraper.py --mostrar-cache

# Limpar cache
python scripts/run_scraper.py --limpar-cache

# Ou usando o módulo diretamente
python -c "
import sys
sys.path.append('src')
from core.scraper import SSPDataScraper

scraper = SSPDataScraper(target_year=2023, target_city='São José dos Campos')
success = scraper.run()
print(f'Scraping {'sucesso' if success else 'falha'}')
"
```

### **2. Análise Geográfica (Busca em Todos os Anos)**
```bash
# Interface interativa
python scripts/geo_search.py

# Linha de comando
python scripts/geo_analyzer_cli.py "Rua das Flores" --raio 3 --export
python scripts/geo_analyzer_cli.py "-23.5481315,-46.6375532" --raio 5 --export --output-file minha_analise.json

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

### **3. Gerenciamento de Cache**
```bash
# Verificar status do cache
python scripts/run_scraper.py --mostrar-cache

# Limpar cache (com confirmação)
python scripts/run_scraper.py --limpar-cache

# Testar sistema de cache
python scripts/test_new_system.py

# Forçar reprocessamento de arquivos específicos
python scripts/run_scraper.py --ano 2023 --forcar-reprocessamento
```

### **4. Scripts de Linha de Comando**

O sistema inclui scripts para uso direto via linha de comando:

```bash
# Scraper principal com cache
python scripts/run_scraper.py

# Scraper com parâmetros específicos
python scripts/run_scraper.py --ano 2023 --cidade "Campinas"

# Análise geográfica por rua
python scripts/geo_analyzer_cli.py "Rua das Flores" --raio 3 --export

# Análise geográfica por coordenadas
python scripts/geo_analyzer_cli.py --raio 5 --export --output-file minha_analise.json -- "-23.5481315,-46.6375532"

# Gerenciamento de cache
python scripts/run_scraper.py --mostrar-cache
python scripts/run_scraper.py --limpar-cache
```

### **5. Usar como Módulo Python**
```python
import sys
sys.path.append('src')

from core.scraper import SSPDataScraper
from analyzers.geo_analyzer import GeoAnalyzer
from utils.cache_manager import CacheManager
from config.settings import settings
from models.data_models import ScrapingResult, GeoRecord

# Configurar logger
from utils.logger import setup_logger
logger = setup_logger("meu_script")

# Usar configurações
print(f"Cidade padrão: {settings.DEFAULT_CITY}")
print(f"Raio padrão: {settings.DEFAULT_RADIUS_KM}km")

# Gerenciar cache
cache_manager = CacheManager()
cache_info = cache_manager.get_cache_info()
print(f"Arquivos processados: {cache_info['total_processed_files']}")

# Executar scraping com cache
scraper = SSPDataScraper(target_year=2023, target_city='São José dos Campos')
success = scraper.run()

# Análise geográfica (busca em todos os anos disponíveis)
analyzer = GeoAnalyzer('output')
records = analyzer.search_and_analyze('-23.5481315,-46.6375532', 5.0)
analyzer.print_results(records, '-23.5481315,-46.6375532', 5.0)
```

### **6. Exemplos de Uso Prático**

#### **Download Completo de Dados**
```bash
# Baixar todos os dados disponíveis (sem filtro de cidade)
python scripts/run_scraper.py

# Baixar dados de um ano específico
python scripts/run_scraper.py --ano 2023
```

#### **Processamento de Cidade Específica**
```bash
# Processar dados para uma cidade específica
python scripts/run_scraper.py --ano 2023 --cidade "São José dos Campos"

# O sistema irá:
# 1. Verificar se os dados completos já foram baixados
# 2. Baixar se necessário
# 3. Filtrar por cidade e salvar em output/cities/
```

#### **Análise Geográfica Completa**
```bash
# Buscar por coordenadas (procura em todos os anos disponíveis)
python scripts/geo_analyzer_cli.py --raio 5 --export --output-file centro_sp.json -- "-23.5481315,-46.6375532"

# Buscar por rua
python scripts/geo_analyzer_cli.py "Rua das Flores" --raio 3 --export
```

#### **Gerenciamento de Cache**
```bash
# Verificar o que já foi processado
python scripts/run_scraper.py --mostrar-cache

# Limpar cache se necessário
python scripts/run_scraper.py --limpar-cache

# Forçar reprocessamento
python scripts/run_scraper.py --forcar-reprocessamento
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
    CONCURRENT_REQUESTS: int = 5
    
    # Configurações de arquivos
    DOWNLOADS_DIR: str = "downloads"
    OUTPUT_DIR: str = "output"
    LOG_FILE: str = "ssp_scraper.log"
    CACHE_FILE: str = "cache_config.json"
    
    # Configurações de cache e controle de anos
    MAX_YEAR: int = field(default_factory=lambda: datetime.now().year)
    CACHE_ENABLED: bool = True
    FORCE_REPROCESS: bool = False
    
    # Configurações de análise geográfica
    DEFAULT_RADIUS_KM: float = 5.0
    EARTH_RADIUS_KM: float = 6371.0
    
    # Configuração do modo headless do Pydoll
    PYDOLL_HEADLESS: bool = field(default_factory=lambda: (
        os.getenv('PYDOLL_HEADLESS', '1').lower() in ['1', 'true', 'yes']
    ))
    
    # Categorias de dados
    CATEGORIES: Dict[str, str] = field(default_factory=lambda: {
        "dados_criminais": "Dados Criminais",
        "dados_produtividade": "Dados de Produtividade", 
        "morte_intervencao": "Morte Decorrente de Intervenção Policial",
        "celulares_subtraidos": "Celulares subtraídos",
        "veiculos_subtraidos": "Veículos subtraídos",
        "objetos_subtraidos": "Objetos subtraídos"
    })
    
    # Configurações de busca por cidade
    CITY_SIMILARITY_THRESHOLD: float = 0.7
    MIN_SIGNIFICANT_WORDS_RATIO: float = 0.6
    MIN_SIGNIFICANT_WORDS_COUNT: int = 2
    
    # Campos de coordenadas suportados (incluindo maiúsculas)
    LATITUDE_FIELDS: List[str] = field(default_factory=lambda: [
        'latitude', 'lat', 'coordenada_lat', 'coord_lat', 'LATITUDE'
    ])
    LONGITUDE_FIELDS: List[str] = field(default_factory=lambda: [
        'longitude', 'lon', 'lng', 'coordenada_lon', 'coord_lon', 'LONGITUDE'
    ])
    
    # Campos de endereço suportados
    ADDRESS_FIELDS: List[str] = field(default_factory=lambda: [
        'endereco', 'logradouro', 'rua', 'address', 'local'
    ])
    
    # Campos prioritários para exibição
    PRIORITY_FIELDS: List[str] = field(default_factory=lambda: [
        'tipo', 'endereco', 'logradouro', 'rua', 'local', 'descricao', 'data'
    ])
    
    # Campos secundários para exibição
    SECONDARY_FIELDS: List[str] = field(default_factory=lambda: [
        'bairro', 'cep', 'numero', 'complemento', 'referencia',
        'periodo', 'hora', 'dia_semana', 'mes', 'ano',
        'vitima', 'suspeito', 'arma', 'veiculo', 'objeto',
        'valor', 'quantidade', 'unidade', 'observacao', 'observações'
    ])
```

### **Variáveis de Ambiente**

```bash
# Configurações de scraping
SSP_TARGET_YEAR=2024
SSP_DEFAULT_CITY="São José dos Campos"
SSP_REQUEST_TIMEOUT=30

# Configurações de análise
SSP_DEFAULT_RADIUS_KM=5.0

# Configurações de cache
SSP_CACHE_ENABLED=true
SSP_FORCE_REPROCESS=false

# Configurações do Pydoll
PYDOLL_HEADLESS=1
```

### **Arquivo de Cache (`cache_config.json`)**

O sistema mantém um arquivo de cache que rastreia:

```json
{
  "processed_files": {
    "dados_criminais_2023": {
      "category": "dados_criminais",
      "year": 2023,
      "processed_at": "2025-07-20T21:14:17.896794",
      "file_info": {
        "filename": "dados_criminais_2023.xlsx",
        "total_registros": 14839,
        "cidade_filtro": "TODAS"
      }
    }
  },
  "processed_cities": {
    "dados_criminais_2023_São José dos Campos": {
      "category": "dados_criminais",
      "year": 2023,
      "city": "São José dos Campos",
      "processed_at": "2025-07-20T21:14:17.898410",
      "file_info": {
        "registros_filtrados": 100,
        "total_registros": 14839
      }
    }
  },
  "available_years": [2023, 2025],
  "last_update": "2025-07-20T21:14:17.896466",
  "version": "1.0"
}
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
        address_fields = ['endereco', 'logradouro', 'rua', 'local']
        for field in address_fields:
            if field in self.dados_originais:
                value = self.dados_originais[field]
                if value and str(value).strip():
                    return str(value).strip()
        return None
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

## 🔧 Troubleshooting e FAQ

### **Problemas Comuns**

#### **1. Cache não está funcionando**
```bash
# Verificar status do cache
python scripts/run_scraper.py --mostrar-cache

# Limpar cache se necessário
python scripts/run_scraper.py --limpar-cache

# Forçar reprocessamento
python scripts/run_scraper.py --forcar-reprocessamento
```

#### **2. Análise geográfica não encontra dados**
- **Verificar se os arquivos JSON existem:**
  ```bash
  ls -la output/*.json
  ```
- **Verificar se as coordenadas estão nos dados:**
  ```bash
  python -c "import json; data=json.load(open('output/dados_produtividade_2025.json')); print('Primeiras coordenadas:', [(r.get('LATITUDE'), r.get('LONGITUDE')) for r in data['dados'][:3] if r.get('LATITUDE')])"
  ```

#### **3. Erro de importação de módulos**
```bash
# Verificar se está no ambiente virtual
source .venv/bin/activate

# Verificar se as dependências estão instaladas
pip list | grep pydoll
```

#### **4. Pydoll não consegue baixar Chromium**
```bash
# Instalar dependências do sistema (Linux)
sudo apt-get update
sudo apt-get install -y chromium-browser libnss3 libatk-bridge2.0-0 libgtk-3-0 libxss1 libasound2 libgbm1 libxshmfence1 libxcomposite1 libxrandr2 libxdamage1 libxfixes3 libxext6 libx11-xcb1 libx11-6 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxi6 libxtst6 libxrandr2 libxss1 libxkbcommon0 libatspi2.0-0
```

### **FAQ**

#### **Q: Por que o sistema baixa dados completos em vez de filtrar por cidade?**
**A:** O novo fluxo otimiza a eficiência:
- Baixa dados completos uma vez
- Filtra por cidade sob demanda
- Evita reprocessamento desnecessário
- Permite análise geográfica em todos os dados

#### **Q: Como o cache funciona?**
**A:** O sistema mantém um arquivo `cache_config.json` que rastreia:
- Arquivos já processados (por categoria/ano)
- Cidades já filtradas (por categoria/ano/cidade)
- Anos disponíveis
- Metadados de processamento

#### **Q: Posso forçar o reprocessamento?**
**A:** Sim, use a flag `--forcar-reprocessamento`:
```bash
python scripts/run_scraper.py --forcar-reprocessamento
```

#### **Q: A análise geográfica busca em todos os anos?**
**A:** Sim! O sistema carrega todos os arquivos JSON disponíveis e busca em todos os anos automaticamente.

#### **Q: Como limpar o cache?**
**A:** Use o comando:
```bash
python scripts/run_scraper.py --limpar-cache
```

#### **Q: O sistema bloqueia anos futuros?**
**A:** Sim, automaticamente. O sistema não permite processar anos maiores que o ano atual.

### **Logs e Debugging**

#### **Verificar logs**
```bash
# Ver logs em tempo real
tail -f ssp_scraper.log

# Ver últimos 50 linhas
tail -50 ssp_scraper.log
```

#### **Modo debug**
```bash
# Ativar modo debug
export SSP_DEBUG=1
python scripts/run_scraper.py
```

#### **Testar componentes individuais**
```bash
# Testar sistema de cache
python scripts/test_new_system.py

# Testar análise geográfica
python scripts/geo_analyzer_cli.py --raio 1 -- "-23.5481315,-46.6375532"
```

## 📈 Performance e Otimizações

### **Cache Inteligente**
- **Evita reprocessamento:** Arquivos já processados são pulados
- **Filtro sob demanda:** Cidades processadas apenas quando necessário
- **Controle granular:** Força reprocessamento quando necessário

### **Estrutura de Arquivos Otimizada**
- **Dados completos:** Um arquivo por categoria/ano
- **Dados filtrados:** Subdiretório `cities/` para dados por cidade
- **Organização clara:** Fácil de navegar e gerenciar

### **Análise Geográfica Eficiente**
- **Busca em todos os anos:** Carrega todos os dados disponíveis
- **Campos de coordenadas flexíveis:** Suporta maiúsculas e minúsculas
- **Cálculo de distância otimizado:** Algoritmo eficiente de distância

## 🤝 Contribuindo

### **Como Contribuir**
1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

### **Padrões de Código**
- Use type hints em todas as funções
- Documente funções e classes
- Mantenha testes atualizados
- Siga o padrão de nomenclatura do projeto

### **Testes**
```bash
# Executar todos os testes
python -m pytest tests/

# Executar com cobertura
python -m pytest --cov=src tests/

# Executar testes específicos
python -m pytest tests/unit/test_cache_manager.py
```

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- **SSP-SP** pela disponibilização dos dados
- **Pydoll** pela automação de browser
- **Comunidade Python** pelas bibliotecas utilizadas

---

**Desenvolvido com ❤️ para análise de dados de segurança pública** 