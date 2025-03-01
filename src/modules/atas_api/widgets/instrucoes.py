from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from paths import ICONS_DIR 

class InstructionWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        # Configura o layout principal do widget
        layout = QVBoxLayout(self)

        # Título
        title_label = QLabel("Instruções para Gerar Atas (API)", self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 30px; font-weight: bold;")
        layout.addWidget(title_label)

        # Descrição principal
        description_label = QLabel(
            "Siga as etapas abaixo para realizar a geração das atas:",
            self
        )
        
        layout.addSpacing(35)
        
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description_label.setWordWrap(True)
        description_label.setStyleSheet("font-size: 20px; color: #555")
        layout.addWidget(description_label)
        
        layout.addSpacing(35)
        
        # Orientações simplificadas
        steps = [
            "1. Importe os dados do Termo de Referência para preencher as colunas 'catalogo', 'descricao' e 'descricao_detalhada'.",
            "2. Use a API do PNCP para gerar atas com base no número sequencial da contratação.",
            "3. Obtenha o nível de credenciamento 1 do SICAF para incluir os dados das empresas na ata.",
            "4. Utilize o botão 'Gerar Ata' para criar as atas automaticamente com base nos dados carregados.",
        ]

        for step in steps:
            step_label = QLabel(step, self)
            step_label.setWordWrap(True)
            step_label.setFont(QFont('Arial', 12))
            layout.addWidget(step_label)
            layout.addSpacing(5)
            
        layout.addStretch()
