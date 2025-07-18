"""
Configurações centralizadas do sistema SSP-SP Data Filter
"""

import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime

@dataclass
class Settings:
    """Configurações do sistema"""
    
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
    
    # Campos de coordenadas suportados
    LATITUDE_FIELDS: List[str] = field(default_factory=lambda: [
        'latitude', 'lat', 'coordenada_lat', 'coord_lat', 'LATITUDE'
    ])
    LONGITUDE_FIELDS: List[str] = field(default_factory=lambda: [
        'longitude', 'lon', 'lng', 'coordenada_lon', 'coord_lon', 'LONGITUDE'
    ])
    
    # Campos de endereço suportados
    ADDRESS_FIELDS: List[str] = field(default_factory=lambda: ['endereco', 'logradouro', 'rua', 'address', 'local'])
    
    # Campos prioritários para exibição
    PRIORITY_FIELDS: List[str] = field(default_factory=lambda: ['tipo', 'endereco', 'logradouro', 'rua', 'local', 'descricao', 'data'])
    
    # Campos secundários para exibição
    SECONDARY_FIELDS: List[str] = field(default_factory=lambda: [
        'bairro', 'cep', 'numero', 'complemento', 'referencia',
        'periodo', 'hora', 'dia_semana', 'mes', 'ano',
        'vitima', 'suspeito', 'arma', 'veiculo', 'objeto',
        'valor', 'quantidade', 'unidade', 'observacao', 'observações'
    ])
    
    DEBUG: bool = field(default_factory=lambda: (
        os.getenv('SSP_DEBUG', '0').lower() in ['1', 'true', 'yes']
    ))
    
    def __post_init__(self):
        """Cria diretórios necessários após inicialização"""
        os.makedirs(self.DOWNLOADS_DIR, exist_ok=True)
        os.makedirs(self.OUTPUT_DIR, exist_ok=True)
    
    @classmethod
    def from_env(cls) -> 'Settings':
        """Cria configurações a partir de variáveis de ambiente"""
        target_year = os.getenv('SSP_TARGET_YEAR')
        parsed_target_year = None
        if target_year and target_year.strip():
            try:
                parsed_target_year = int(target_year)
            except ValueError:
                parsed_target_year = None
        # Novo: headless
        pydoll_headless_env = os.getenv('PYDOLL_HEADLESS', '1').lower() in ['1', 'true', 'yes']
        return cls(
            DEFAULT_TARGET_YEAR=parsed_target_year,
            DEFAULT_CITY=os.getenv('SSP_DEFAULT_CITY', cls.DEFAULT_CITY),
            REQUEST_TIMEOUT=int(os.getenv('SSP_REQUEST_TIMEOUT', cls.REQUEST_TIMEOUT)),
            CONCURRENT_REQUESTS=int(os.getenv('SSP_CONCURRENT_REQUESTS', cls.CONCURRENT_REQUESTS)),
            DEFAULT_RADIUS_KM=float(os.getenv('SSP_DEFAULT_RADIUS_KM', cls.DEFAULT_RADIUS_KM)),
            PYDOLL_HEADLESS=pydoll_headless_env
        )

# Instância global das configurações
settings = Settings.from_env() 