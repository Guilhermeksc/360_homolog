# paths/base_paths.py

import sys
from pathlib import Path

if getattr(sys, 'frozen', False):  # Executável compilado
    BASE_DIR = Path(sys._MEIPASS) / "src"  # Diretório temporário + 'src'
else:  # Ambiente de desenvolvimento
    BASE_DIR = Path(__file__).resolve().parent.parent
    
CONFIG_FILE = BASE_DIR / "config.json"    
DATABASE_DIR = BASE_DIR / "database"    
MODULES_DIR = BASE_DIR / "modules"

JSON_DIR = DATABASE_DIR / "json"
SQL_DIR = DATABASE_DIR / "sql"
CONTROLE_DADOS = SQL_DIR / "controle_dados.db"

# Assets
ASSETS_DIR = BASE_DIR / "assets"
TEMPLATE_DIR = ASSETS_DIR / "templates"
STYLE_PATH = ASSETS_DIR / "style.css" 
ICONS_DIR = ASSETS_DIR / "icons"


