# paths/__init__.py

# Importando diretamente os objetos ou funções de cada módulo interno
from .base_path import BASE_DIR, CONFIG_FILE, DATABASE_DIR, MODULES_DIR, JSON_DIR, SQL_DIR, ASSETS_DIR, TEMPLATE_DIR, STYLE_PATH, ICONS_DIR
from .atas_path import *  # Importe as funções e constantes definidas em atas_path.py
from .atas_api_path import *  # Importe as funções e constantes definidas em atas_api_path.py

# Definindo __all__ para controle explícito do que será exportado
__all__ = [
    # base_path
    "BASE_DIR", "CONFIG_FILE", "DATABASE_DIR", "MODULES_DIR", "JSON_DIR", "SQL_DIR", 
    "ASSETS_DIR", "TEMPLATE_DIR", "STYLE_PATH", "ICONS_DIR",
    
    # atas_path
    # Inclua os nomes específicos de funções/constantes de atas_path.py aqui,
    
    # atas_api_path
    # Inclua os nomes específicos de funções/constantes de atas_api_path.py aqui
]
