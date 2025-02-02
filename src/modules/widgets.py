# modules/widgets.py

# Utilidades
from modules.utils.icon_loader import load_icons

# Importações de views
# from modules.pca.pca import PCAWidget
from modules.inicio.view import InicioWidget
# from modules.pncp.pncp import PNCPWidget
# from modules.planejamento_novo.antigo_planejamento_button import PlanejamentoWidget

from modules.atas.view import GerarAtasView
from modules.atas.model import GerarAtasModel
from modules.atas.controller import GerarAtasController

from modules.atas_api.view import GerarAtasApiView
from modules.atas_api.model import GerarAtasApiModel
from modules.atas_api.controller import GerarAtasApiController

from modules.dispensa.view import DispensaEletronicaWidget
from modules.dispensa.model import DispensaEletronicaModel
from modules.dispensa.controller import DispensaEletronicaController

# from modules.atas.classe_atas import AtasWidget
# from modules.pca.models import PCAModel  # Exemplo para PCA
# from modules.atas.models import AtasModel  # Exemplo para Atas

from modules.indicadores.view import IndicadoresView
from modules.indicadores.database import DatabaseManager

__all__ = [
    # Views
    # "PCAWidget",
    "InicioWidget",
    # "PNCPWidget",
    # "LicitacaoWidget",
    # 
    # "DashboardWidget",

    "GerarAtasApiView",
    "GerarAtasApiModel",
    "GerarAtasApiController",
    "IndicadoresView",
    # "AtasWidget",
    # "ContratosView",
    
    "DispensaEletronicaController",
    "DispensaEletronicaWidget",
    "DispensaEletronicaModel",

    "GerarAtasView",
    "GerarAtasModel",
    "GerarAtasController",

    
    # "ContratosModel",
    # "PCAModel",
    # "AtasModel",

    # Controllers
    
    # "LicitacaoController",


    # "ContratosController",

    # Utils
    "load_icons",
    "DatabaseManager"
]