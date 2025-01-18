from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from paths import *
from modules.config.config_widget import linha_divisoria_sem_spacer_layout
import sqlite3
from pathlib import Path
import pandas as pd
import os
import json

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

    
class AgentesResponsaveisWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.database_path = CONTROLE_DADOS
        print(f"Database Path: {self.database_path}")

        self.database_manager = DatabaseManager(self.database_path)
        self.setWindowTitle("Alterar Agentes Responsáveis")
        self.setFixedSize(1100, 600)
        self.layout = QVBoxLayout(self)

        header_widget = self.update_title_label_config()
        self.layout.addWidget(header_widget)
        self.initialize_ui()

    def update_title_label_config(self):
        html_text = "Alterar Agentes Responsáveis<br>"
        if not hasattr(self, 'titleLabel'):
            self.titleLabel = QLabel()
            self.titleLabel.setTextFormat(Qt.TextFormat.RichText)
            self.titleLabel.setStyleSheet("font-size: 30px; font-weight: bold;")

        self.titleLabel.setText(html_text)

        if not hasattr(self, 'header_layout'):
            self.header_layout = QHBoxLayout()
            self.header_layout.addWidget(self.titleLabel)
            self.header_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

            header_widget = QWidget()
            header_widget.setLayout(self.header_layout)
            header_widget.setFixedHeight(100)
            self.header_widget_config = header_widget

        return self.header_widget_config

    def initialize_ui(self):
        self.table_view = QTableView()
        self.table_view.setFont(QFont('Arial', 12))
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        self.carregarAgentesResponsaveis()
        self.layout.addWidget(self.table_view)

        add_button = QPushButton("Adicionar")
        add_button.clicked.connect(self.adicionarAgente)
        gerar_Tabela_button = QPushButton("Gerar Tabela")
        gerar_Tabela_button.clicked.connect(self.gerarTabela)
        importar_tabela_button = QPushButton("Importar Tabela")
        importar_tabela_button.clicked.connect(self.importarTabela)
        save_button = QPushButton("Salvar")
        save_button.clicked.connect(self.save_and_emit)
        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.cancel_action)  # Altere aqui

        button_layout = QHBoxLayout()
        button_layout.addWidget(add_button)
        button_layout.addWidget(gerar_Tabela_button)
        button_layout.addWidget(importar_tabela_button)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        self.layout.addLayout(button_layout)
        self.table_view.installEventFilter(self)

    def cancel_action(self):
        """Ação executada ao clicar em Cancelar."""
        # Opcionalmente, limpe a interface ou emita um sinal para o widget pai
        self.clear_content()
        QMessageBox.information(self, "Informação", "Ação cancelada.")


    def carregarAgentesResponsaveis(self):
        try:
            print("Carregando agentes responsáveis do banco de dados...")
            query = "SELECT nome, posto, funcao FROM controle_agentes_responsaveis"
            agentes_responsaveis = self.database_manager.execute_query(query)
            
            if agentes_responsaveis:
                agentes_responsaveis = [list(row) for row in agentes_responsaveis]  # Converte tuplas em listas
                self.table_model = AgentesResponsaveisTableModel(agentes_responsaveis, self.database_manager)
                self.table_view.setModel(self.table_model)
                self.table_view.setItemDelegateForColumn(1, ComboBoxDelegate([
                    "Capitão de Mar e Guerra (IM)", "Capitão de Fragata (IM)", "Capitão de Corveta (IM)", 
                    "Capitão-Tenente (IM)", "Primeiro-Tenente (IM)", "Primeiro-Tenente (Rm2-T)", 
                    "Segundo-Tenente (IM)", "Segundo-Tenente (Rm2-T)"
                ], self.table_view))
                self.table_view.setItemDelegateForColumn(2, ComboBoxDelegate([
                    "Ordenador de Despesa", "Ordenador de Despesa Substituto", "Agente Fiscal", 
                    "Agente Fiscal Substituto", "Gerente de Crédito", "Operador de Dispensa Eletrônica",
                    "Responsável pela Demanda", "Encarregado da Divisão de x"
                ], self.table_view))
                self.table_view.setColumnWidth(0, 400)
                self.table_view.setColumnWidth(1, 300)
                self.table_view.setColumnWidth(2, 300)
            else:
                QMessageBox.information(self, "Informação", "Nenhum agente responsável encontrado.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

    def adicionarAgente(self):
        self.table_model.addRow()

    def excluirAgente(self):
        selected_indexes = self.table_view.selectionModel().selectedRows()
        if selected_indexes:
            for index in sorted(selected_indexes, reverse=True):
                self.table_model.removeRow(index.row())
        else:
            QMessageBox.information(self, "Informação", "Nenhuma linha selecionada.")

    def gerarTabela(self):
        try:
            # Conectar ao banco de dados
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT nome, posto, funcao FROM controle_agentes_responsaveis")
                data = cursor.fetchall()
            
            # Converter os dados para um DataFrame do pandas
            df = pd.DataFrame(data, columns=["Nome", "Posto", "Função"])
            
            # Definir o caminho para salvar a planilha Excel
            excel_path = Path("controle_agentes_responsaveis.xlsx")
            
            # Salvar o DataFrame como um arquivo Excel usando pandas
            df.to_excel(excel_path, index=False)
            
            # Ajustar o tamanho das colunas usando openpyxl
            from openpyxl import load_workbook
            wb = load_workbook(excel_path)
            ws = wb.active

            # Ajustar o tamanho das colunas
            column_widths = {"A": 45, "B": 30, "C": 35}
            for col, width in column_widths.items():
                ws.column_dimensions[col].width = width

            # Salvar as alterações no arquivo Excel
            wb.save(excel_path)
            
            # Abrir o arquivo Excel criado
            os.startfile(excel_path)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao gerar a tabela: {e}")

    def importarTabela(self):
        try:
            # Abrir o diálogo para selecionar o arquivo Excel
            file_dialog = QFileDialog()
            file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
            file_dialog.setNameFilter("Arquivos Excel (*.xlsx)")
            if file_dialog.exec():
                file_path = file_dialog.selectedFiles()[0]

                # Ler o arquivo Excel usando pandas
                df = pd.read_excel(file_path)

                # Verificar se as colunas necessárias estão presentes
                required_columns = ["Nome", "Posto", "Função"]
                if not all(column in df.columns for column in required_columns):
                    raise Exception("O arquivo Excel deve conter as colunas: Nome, Posto, Função")

                # Conectar ao banco de dados
                with sqlite3.connect(self.database_path) as conn:
                    cursor = conn.cursor()
                    
                    # Deletar os valores existentes
                    cursor.execute("DELETE FROM controle_agentes_responsaveis")
                    
                    # Inserir os novos valores
                    for _, row in df.iterrows():
                        cursor.execute("INSERT INTO controle_agentes_responsaveis (nome, posto, funcao) VALUES (?, ?, ?)",
                                    (row["Nome"], row["Posto"], row["Função"]))
                    
                    conn.commit()

                # Recarregar a tabela na interface
                self.carregarAgentesResponsaveis()
                QMessageBox.information(self, "Sucesso", "Tabela importada com sucesso!")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao importar a tabela: {e}")
            
    def save_and_emit(self):
        self.accept()
        self.config_updated.emit()

    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Delete:
            self.excluirAgente()
        return super().eventFilter(source, event)

def create_button(text, icon, callback, tooltip_text, parent, icon_size=QSize(30, 30)):
    btn = QPushButton(text, parent)
    if icon:
        btn.setIcon(QIcon(icon))
        btn.setIconSize(icon_size)
    if callback:
        btn.clicked.connect(callback)
    if tooltip_text:
        btn.setToolTip(tooltip_text)

    return btn

class ComboBoxDelegate(QStyledItemDelegate):
    def __init__(self, options, parent=None):
        super().__init__(parent)
        self.options = options

    def createEditor(self, parent, option, index):
        combo_box = QComboBox(parent)
        combo_box.setEditable(True)
        combo_box.addItems(self.options)
        combo_box.setFont(QFont('Arial', 12))
        
        # Definir um QListView para o QComboBox para controlar o estilo dos itens da lista
        list_view = QListView()
        list_view.setFont(QFont('Arial', 12))
        combo_box.setView(list_view)

        # Definir a fonte do line_edit diretamente
        line_edit = combo_box.lineEdit()
        line_edit.setFont(QFont('Arial', 12))

        return combo_box

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.ItemDataRole.EditRole)
        if value:
            editor.setCurrentText(value)  # Chame setCurrentText no QComboBox

    def setModelData(self, editor, model, index):
        value = editor.currentText()  # Obtenha o texto atual do QComboBox
        model.setData(index, value, Qt.ItemDataRole.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
        
class AgentesResponsaveisTableModel(QAbstractTableModel):
    def __init__(self, data, database_path):
        super().__init__()
        self._data = data
        self._headers = ["Nome", "Posto", "Função"]
        self.database_path = database_path

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._headers)

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            return self._data[index.row()][index.column()]

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._headers[section]
            if orientation == Qt.Orientation.Vertical:
                return section + 1

    def setData(self, index, value, role):
        if role == Qt.ItemDataRole.EditRole:
            self._data[index.row()][index.column()] = value
            self.updateDatabase(index.row(), index.column(), value)
            self.dataChanged.emit(index, index, (Qt.ItemDataRole.EditRole,))
            return True
        return False

    def flags(self, index):
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable

    def updateDatabase(self, row, column, value):
        try:
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.cursor()
                headers = ['nome', 'posto', 'funcao']
                query = f"UPDATE controle_agentes_responsaveis SET {headers[column]} = ? WHERE rowid = ?"
                cursor.execute(query, (value, row + 1))  # rowid é 1-indexado
                conn.commit()
        except Exception as e:
            QMessageBox.critical(None, "Erro", f"Erro ao atualizar o banco de dados: {e}")

    def addRow(self):
        self.beginInsertRows(QModelIndex(), self.rowCount(None), self.rowCount(None))
        self._data.append(["", "", ""])  # Adiciona uma linha vazia
        self.endInsertRows()

        try:
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO controle_agentes_responsaveis (nome, posto, funcao) VALUES (?, ?, ?)", ("", "", ""))
                conn.commit()
        except Exception as e:
            QMessageBox.critical(None, "Erro", f"Erro ao adicionar ao banco de dados: {e}")

    def removeRow(self, row, parent=QModelIndex()):
        self.beginRemoveRows(QModelIndex(), row, row)
        self._data.pop(row)
        self.endRemoveRows()

        try:
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM controle_agentes_responsaveis WHERE rowid = ?", (row + 1,))
                conn.commit()
        except Exception as e:
            QMessageBox.critical(None, "Erro", f"Erro ao remover do banco de dados: {e}")
class EditPredefinicoesDialog(QDialog):
    def __init__(self, categoria, config_data, parent=None):
        super().__init__(parent)
        self.categoria = categoria
        self.config_data = config_data
        self.setWindowTitle(f"Editar {categoria.capitalize()}")

        layout = QVBoxLayout(self)
        self.list_widget = QListWidget()
        self.list_widget.addItems(config_data[categoria])
        layout.addWidget(self.list_widget)

        if categoria == "ordenador_despesas":
            # Campo Nome (com caixa alta)
            self.nome_input = QLineEdit()
            self.nome_input.setPlaceholderText("Nome")
            self.nome_input.textChanged.connect(self.forcar_caixa_alta)
            layout.addWidget(self.nome_input)
            
            # Campo Posto (QComboBox com opções predefinidas e entrada personalizada)
            self.posto_input = QComboBox()
            self.posto_input.setEditable(True)  # Permite entrada personalizada
            self.posto_input.addItems([
                "Capitão de Mar e Guerra (IM)",
                "Capitão de Fragata (IM)",
                "Capitão de Corveta (IM)"
            ])
            self.posto_input.setPlaceholderText("Selecione ou digite o posto")
            layout.addWidget(self.posto_input)
            
            # Checkboxes para tipo de ordenador com exclusividade
            self.checkbox_ordenador = QCheckBox("Ordenador de Despesa")
            self.checkbox_substituto = QCheckBox("Ordenador de Despesa Substituto")
            layout.addWidget(self.checkbox_ordenador)
            layout.addWidget(self.checkbox_substituto)

            # Conectar os checkboxes para que apenas um seja selecionado de cada vez
            self.checkbox_ordenador.stateChanged.connect(self.desmarcar_substituto)
            self.checkbox_substituto.stateChanged.connect(self.desmarcar_ordenador)

            # Conectar o clique no item da lista ao preenchimento dos campos
            self.list_widget.itemClicked.connect(self.preencher_campos)

        else:
            # Campo de entrada genérico para outras categorias
            self.input_edit = QLineEdit()
            layout.addWidget(self.input_edit)

        # Botões para adicionar e remover itens
        add_btn = QPushButton("Adicionar")
        add_btn.clicked.connect(self.adicionar_item)
        layout.addWidget(add_btn)

        remove_btn = QPushButton("Remover")
        remove_btn.clicked.connect(self.remover_item)
        layout.addWidget(remove_btn)

        save_btn = QPushButton("Salvar")
        save_btn.clicked.connect(self.salvar_e_fechar)
        layout.addWidget(save_btn)

    def forcar_caixa_alta(self):
        """Garante que o nome seja sempre em caixa alta."""
        self.nome_input.setText(self.nome_input.text().upper())

    def desmarcar_substituto(self):
        """Desmarca 'Ordenador de Despesa Substituto' se 'Ordenador de Despesa' for selecionado."""
        if self.checkbox_ordenador.isChecked():
            self.checkbox_substituto.setChecked(False)

    def desmarcar_ordenador(self):
        """Desmarca 'Ordenador de Despesa' se 'Ordenador de Despesa Substituto' for selecionado."""
        if self.checkbox_substituto.isChecked():
            self.checkbox_ordenador.setChecked(False)

    def preencher_campos(self, item):
        """Preenche os campos editáveis com os valores do item selecionado."""
        # Extrair nome, posto e tipo de ordenador do item selecionado
        partes = item.text().split("\n")
        
        if len(partes) >= 2:
            nome = partes[0].strip()
            posto = partes[1].strip()
            tipo_ordenador = partes[2].strip() if len(partes) > 2 else ""

            # Preenche os campos com os valores extraídos
            self.nome_input.setText(nome)
            self.posto_input.setCurrentText(posto)

            # Seleciona o checkbox apropriado
            if tipo_ordenador == "Ordenador de Despesa":
                self.checkbox_ordenador.setChecked(True)
            elif tipo_ordenador == "Ordenador de Despesa Substituto":
                self.checkbox_substituto.setChecked(True)

    def adicionar_item(self):
        # Lógica para 'ordenador_despesas' com campos de nome e posto
        if self.categoria == "ordenador_despesas":
            nome = self.nome_input.text()
            posto = self.posto_input.currentText()
            if self.checkbox_ordenador.isChecked():
                tipo_ordenador = "Ordenador de Despesa"
            elif self.checkbox_substituto.isChecked():
                tipo_ordenador = "Ordenador de Despesa Substituto"
            else:
                QMessageBox.warning(self, "Aviso", "Selecione o tipo de ordenador.")
                return

            # Formatar o texto final para o combobox
            item_text = f"{nome} \n {posto} \n {tipo_ordenador}"
            self.list_widget.addItem(item_text)

            # Limpar campos após adicionar
            self.nome_input.clear()
            self.posto_input.setCurrentIndex(-1)  # Desmarca a seleção
            self.checkbox_ordenador.setChecked(False)
            self.checkbox_substituto.setChecked(False)

        else:
            # Adicionar item para categorias normais
            item_text = self.input_edit.text()
            self.list_widget.addItem(item_text)
            self.input_edit.clear()

    def remover_item(self):
        selected_item = self.list_widget.currentItem()
        if selected_item:
            self.list_widget.takeItem(self.list_widget.row(selected_item))

    def salvar_e_fechar(self):
        # Salvar todos os itens na configuração JSON
        items = [self.list_widget.item(i).text() for i in range(self.list_widget.count())]
        self.config_data[self.categoria] = items
        self.accept()
