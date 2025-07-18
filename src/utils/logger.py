"""
Sistema de logging centralizado para o SSP-SP Data Filter
"""

import logging
import os
from datetime import datetime
from typing import Optional
try:
    from ..config.settings import settings
except ImportError:
    # Fallback para quando executado da raiz
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
    from config.settings import settings

def setup_logger(
    name: str = "ssp_scraper",
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    console_output: bool = True
) -> logging.Logger:
    """
    Configura um logger personalizado
    
    Args:
        name: Nome do logger
        level: Nível de logging
        log_file: Arquivo de log (opcional)
        console_output: Se deve mostrar no console
        
    Returns:
        Logger configurado
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Evitar duplicação de handlers
    if logger.handlers:
        return logger
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para console
    if console_output:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # Handler para arquivo
    if log_file:
        # Usar arquivo padrão se não especificado
        if log_file is True:
            log_file = settings.LOG_FILE
        
        # Criar diretório se não existir
        log_dir = os.path.dirname(log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def get_logger(name: str = "ssp_scraper") -> logging.Logger:
    """
    Obtém um logger já configurado
    
    Args:
        name: Nome do logger
        
    Returns:
        Logger configurado
    """
    return logging.getLogger(name)

# Logger padrão do sistema
default_logger = setup_logger("ssp_scraper", log_file=settings.LOG_FILE) 