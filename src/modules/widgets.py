# modules/widgets.py

# Utilidades
from modules.utils.icon_loader import load_icons

# Importações de views
# from modules.pca.pca import PCAWidget
from modules.inicio.view import InicioWidget
# from modules.pncp.pncp import PNCPWidget
# from modules.planejamento_novo.antigo_planejamento_button import PlanejamentoWidget

from modules.atas.view import GerarAtasView
# from modules.atas.classe_atas import AtasWidget
from modules.atas.model import GerarAtasModel
# from modules.pca.models import PCAModel  # Exemplo para PCA
# from modules.atas.models import AtasModel  # Exemplo para Atas

from modules.atas.controller import GerarAtasController

__all__ = [
    # Views
    # "PCAWidget",
    "InicioWidget",
    # "PNCPWidget",
    # "LicitacaoWidget",
    # "DispensaEletronicaWidget",
    # "DashboardWidget",
    "GerarAtasView",
    # "AtasWidget",
    # "ContratosView",
    
    # Models
    # "DispensaEletronicaModel",
    # "LicitacaoModel",
    "GerarAtasModel",
    # "ContratosModel",
    # "PCAModel",
    # "AtasModel",

    # Controllers
    # "DispensaEletronicaController",
    # "LicitacaoController",
    "GerarAtasController",
    # "ContratosController",

    # Utils
    "load_icons"
]