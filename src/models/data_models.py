"""
Modelos de dados estruturados para o sistema SSP-SP Data Filter
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum

class CategoryType(Enum):
    """Tipos de categoria de dados"""
    DADOS_CRIMINAIS = "Dados Criminais"
    DADOS_PRODUTIVIDADE = "Dados de Produtividade"
    MORTE_INTERVENCAO = "Morte Decorrente de Intervenção Policial"
    CELULARES_SUBTRAIDOS = "Celulares subtraídos"
    VEICULOS_SUBTRAIDOS = "Veículos subtraídos"
    OBJETOS_SUBTRAIDOS = "Objetos subtraídos"

@dataclass
class ScrapingResult:
    """Resultado do scraping de uma categoria"""
    categoria: str
    arquivo_original: str
    total_registros: int
    registros_filtrados: int
    cidade_filtro: str
    data_processamento: datetime
    dados: List[Dict[str, Any]]
    sucesso: bool = True
    erro: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            "categoria": self.categoria,
            "arquivo_original": self.arquivo_original,
            "total_registros": self.total_registros,
            "registros_filtrados": self.registros_filtrados,
            "cidade_filtro": self.cidade_filtro,
            "data_processamento": self.data_processamento.isoformat(),
            "dados": self.dados,
            "sucesso": self.sucesso,
            "erro": self.erro
        }

@dataclass
class GeoRecord:
    """Registro com informações geográficas"""
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
    
    def get_type(self) -> Optional[str]:
        """Extrai tipo de ocorrência"""
        if 'tipo' in self.dados_originais:
            value = self.dados_originais['tipo']
            if value and str(value).strip():
                return str(value).strip()
        return None
    
    def get_date(self) -> Optional[str]:
        """Extrai data da ocorrência"""
        if 'data' in self.dados_originais:
            value = self.dados_originais['data']
            if value and str(value).strip():
                return str(value).strip()
        return None

@dataclass
class CategoryStats:
    """Estatísticas por categoria"""
    categoria: str
    total_registros: int
    distancia_media: float
    distancia_minima: float
    distancia_maxima: float
    tipos_ocorrencia: Dict[str, int] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            "categoria": self.categoria,
            "total_registros": self.total_registros,
            "distancia_media": self.distancia_media,
            "distancia_minima": self.distancia_minima,
            "distancia_maxima": self.distancia_maxima,
            "tipos_ocorrencia": self.tipos_ocorrencia
        }

@dataclass
class AnalysisResult:
    """Resultado de análise geográfica"""
    query: str
    raio_km: float
    total_registros: int
    registros: List[GeoRecord]
    estatisticas: CategoryStats
    data_analise: datetime = field(default_factory=datetime.now)
    
    def get_categories_summary(self) -> Dict[str, int]:
        """Resumo por categoria"""
        summary = {}
        for record in self.registros:
            cat = record.categoria
            summary[cat] = summary.get(cat, 0) + 1
        return summary
    
    def get_types_summary(self) -> Dict[str, int]:
        """Resumo por tipo de ocorrência"""
        summary = {}
        for record in self.registros:
            tipo = record.get_type()
            if tipo:
                summary[tipo] = summary.get(tipo, 0) + 1
        return summary
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            "query": self.query,
            "raio_km": self.raio_km,
            "total_registros": self.total_registros,
            "data_analise": self.data_analise.isoformat(),
            "registros": [
                {
                    "categoria": r.categoria,
                    "latitude": r.latitude,
                    "longitude": r.longitude,
                    "distancia_km": r.distancia_km,
                    "dados_originais": r.dados_originais
                }
                for r in self.registros
            ],
            "estatisticas": self.estatisticas.to_dict(),
            "resumo_categorias": self.get_categories_summary(),
            "resumo_tipos": self.get_types_summary()
        } 