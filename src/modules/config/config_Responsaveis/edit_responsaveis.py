from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from paths.base_paths import *
from modules.config.config_widget import linha_divisoria_sem_spacer_layout
from .edit_agentes_responsaveis import EditPredefinicoesDialog

def show_agentes_responsaveis_widget(content_layout, icons, parent):
    """Exibe o widget para Alteração dos Agentes Responsáveis."""
    # Limpa o layout de conteúdo
    while content_layout.count():
        item = content_layout.takeAt(0)
        widget = item.widget()
        if widget:
            widget.deleteLater()
        elif item.layout():
            clear_layout(item.layout)

    def clear_layout(layout):
        """Recursivamente limpa um layout."""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            elif item.layout():
                clear_layout(item.layout)

    # Widget principal para o conteúdo
    main_widget = QWidget()
    layout = QVBoxLayout(main_widget)

    # Título
    title = QLabel("Alteração dos Agentes Responsáveis")
    title.setStyleSheet("font-size: 20px; font-weight: bold; color: #4E648B")
    layout.addWidget(title)

    # Carregar dados do arquivo JSON
    try:
        with open(AGENTES_RESPONSAVEIS_FILE, 'r', encoding='utf-8') as file:
            config_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        config_data = {}

    # Lista de agentes
    agentes = [
        "Ordenador de Despesa",
        "Agente Fiscal",
        "Gerente de Crédito",
        "Responsável pela Demanda",
        "Operador da Contratação",
        "Pregoeiro",
    ]

    # Criando botões para cada agente
    for agente in agentes:
        categoria = agente.lower().replace(" ", "_")
        item_layout = QVBoxLayout()

        linha_divisoria = linha_divisoria_sem_spacer_layout()
        item_layout.addWidget(linha_divisoria)

        # Exibir valores existentes no JSON acima do botão
        if categoria in config_data:
            for item in config_data[categoria]:
                item_label = QLabel(
                    f"{item['Nome']} - {item['Posto']} - {item['Abreviacao']} - {item['Funcao']}"
                )
                item_label.setStyleSheet("font-size: 14px; color: #E3E3E3;")
                item_layout.addWidget(item_label)

        # Layout horizontal para o botão com espaçadores laterais
        button_layout = QHBoxLayout()
        button_layout.addStretch()  # Espaçador à esquerda

        # Botão com texto do agente
        button = QPushButton(agente)
        button.setIcon(icons.get("edit"))  # Ajuste para o ícone correto
        button.setStyleSheet("font-size: 14px; padding: 5px;")
        button.clicked.connect(partial(edit_agent, parent, agente))  # Passa o nome do agente para a função
        button_layout.addWidget(button)

        button_layout.addStretch()  # Espaçador à direita
        item_layout.addLayout(button_layout)

        layout.addLayout(item_layout)

    # Adiciona espaçador para empurrar o conteúdo para o topo
    layout.addStretch()

    # Configura o widget no layout principal
    content_layout.addWidget(main_widget)


def edit_agent(parent, agente):
    """Função chamada ao clicar em 'Editar'."""
    categoria = agente.lower().replace(" ", "_")  # Transformar em formato adequado para JSON
    try:
        # Carregar os dados do JSON
        if not Path(AGENTES_RESPONSAVEIS_FILE).exists():
            with open(AGENTES_RESPONSAVEIS_FILE, 'w', encoding='utf-8') as file:
                json.dump({}, file, ensure_ascii=False, indent=4)

        with open(AGENTES_RESPONSAVEIS_FILE, 'r', encoding='utf-8') as file:
            config_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        config_data = {}

    # Garantir que a categoria exista no dicionário
    if categoria not in config_data:
        config_data[categoria] = []

    # Abrir o diálogo de edição
    dialog = EditPredefinicoesDialog(categoria, config_data, parent)
    if dialog.exec():
        # Salvar alterações no JSON
        with open(AGENTES_RESPONSAVEIS_FILE, 'w', encoding='utf-8') as file:
            json.dump(config_data, file, ensure_ascii=False, indent=4)

        # Atualizar o widget após salvar as alterações
        show_agentes_responsaveis_widget(parent.content_layout, parent.icons, parent)
