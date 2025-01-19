# paths/__init__.py

# Importando diretamente os objetos ou funções de cada módulo interno
from .base_path import BASE_DIR, CONFIG_FILE, DATABASE_DIR, MODULES_DIR, JSON_DIR, SQL_DIR, ASSETS_DIR, TEMPLATE_DIR, STYLE_PATH, ICONS_DIR
from .atas_path import CONTROLE_DADOS_ATA, TEMPLATE_PATH, DATA_ATAS_PATH
from .atas_api_path import CONFIG_API_FILE, DATA_ATAS_API_PATH
from .config_path import PRE_DEFINICOES_JSON, ORGANIZACOES_FILE, AGENTES_RESPONSAVEIS_FILE, PDF_DIR

# Definindo __all__ para controle explícito do que será exportado
__all__ = [
    # base_path
    "BASE_DIR", "CONFIG_FILE", "DATABASE_DIR", "MODULES_DIR", "JSON_DIR", "SQL_DIR", 
    "ASSETS_DIR", "TEMPLATE_DIR", "STYLE_PATH", "ICONS_DIR",
    
    # atas_path
    "CONTROLE_DADOS_ATA", "TEMPLATE_PATH", "DATA_ATAS_PATH",
    
    # atas_api_path
    "CONFIG_API_FILE", "DATA_ATAS_API_PATH",
    
    # config_path
    "PRE_DEFINICOES_JSON", "ORGANIZACOES_FILE", "AGENTES_RESPONSAVEIS_FILE", "PDF_DIR",
    ]
