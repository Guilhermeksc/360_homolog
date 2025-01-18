from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt

class IndicadoresView(QWidget):
    def __init__(self, db_manager, data_atas_path, data_atas_api_path, parent=None):
        super().__init__(parent)

        self.db_manager = db_manager
        self.data_atas_path = data_atas_path
        self.data_atas_api_path = data_atas_api_path

        self.setup_ui()

    def setup_ui(self):
        """Configura a interface da view."""
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(15)

        # Rótulo de instrução
        self.label = QLabel("Selecione o banco de dados e a tabela para visualizar indicadores:", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.label)

        # Combobox para selecionar o banco de dados
        self.db_selector = QComboBox(self)
        self.db_selector.addItem("Controle Atas", self.data_atas_path)
        self.db_selector.addItem("Controle Atas API", self.data_atas_api_path)
        self.layout.addWidget(self.db_selector)

        # Botão para carregar tabelas
        self.load_button = QPushButton("Carregar Tabelas", self)
        self.load_button.clicked.connect(self.load_tables)
        self.layout.addWidget(self.load_button)

        # Tabela para exibir os dados
        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(3)  # Exemplo: 3 colunas para teste
        self.table_widget.setHorizontalHeaderLabels(["Coluna 1", "Coluna 2", "Coluna 3"])
        self.layout.addWidget(self.table_widget)

    def load_tables(self):
        # Obtém o caminho do banco selecionado
        selected_db_path = self.db_selector.currentData()

        # Busca tabelas que começam com "result" no banco selecionado
        tables = self.db_manager.get_tables_with_keyword('result', selected_db_path)
        if not tables:
            QMessageBox.warning(self, "Aviso", "Não há tabelas disponíveis que comecem com 'result'.")
            return

        # Apresenta um diálogo para o usuário selecionar a tabela
        table_name, ok = QInputDialog.getItem(
            self,
            "Selecionar Tabela",
            "Selecione uma tabela:",
            tables,
            0,
            False
        )
        if not ok or not table_name:
            return

        # Carrega os dados da tabela selecionada
        dataframe = self.db_manager.load_table_to_dataframe(table_name, selected_db_path)
        if dataframe is None or dataframe.empty:
            QMessageBox.warning(self, "Aviso", "Falha ao carregar a tabela selecionada.")
            return

        # Atualiza a exibição da tabela com os dados carregados
        self.update_table(dataframe)

    def update_table(self, dataframe):
        """Atualiza a exibição da tabela com os dados do DataFrame."""
        self.table_widget.setRowCount(len(dataframe))
        self.table_widget.setColumnCount(len(dataframe.columns))
        self.table_widget.setHorizontalHeaderLabels(dataframe.columns)

        for row_idx, row in dataframe.iterrows():
            for col_idx, value in enumerate(row):
                self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))