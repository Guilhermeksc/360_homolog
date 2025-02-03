from modules.contratos.database_manager.db_manager import DatabaseManager
from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from functools import partial
import sqlite3  
import re

class ContratosModel(QObject):
    def __init__(self, database_path, parent=None):
        super().__init__(parent)
        self.database_manager = DatabaseManager(database_path)
        self.db = None  # Adiciona um atributo para o banco de dados
        self.model = None  # Atributo para o modelo SQL
        self.init_database()  # Inicializa a conexão e a estrutura do banco de dados

    def init_database(self):
        """Inicializa a conexão com o banco de dados e ajusta a estrutura da tabela."""
        if QSqlDatabase.contains("my_conn"):
            QSqlDatabase.removeDatabase("my_conn")
        self.db = QSqlDatabase.addDatabase('QSQLITE', "my_conn")
        self.db.setDatabaseName(str(self.database_manager.db_path))
        
        if not self.db.open():
            print("Não foi possível abrir a conexão com o banco de dados.")
        else:
            print("Conexão com o banco de dados aberta com sucesso.")
            self.adjust_table_structure()  # Ajusta a estrutura da tabela, se necessário

    def save_api_data(self, data_api):
        """Salva os dados da API no banco de dados com depuração aprimorada."""
        
        # Inspecionar `data_api`
        print("DEBUG: Conteúdo de `data_api`:", data_api)
        
        # Acessa `data_informacoes` e converte para dicionário, se for uma lista de tuplas
        data_informacoes = data_api['data_informacoes']
        if isinstance(data_informacoes, list):
            data_informacoes = dict(data_informacoes)

        numero_controle_pncp = data_informacoes.get('numeroControlePNCP')
        if not numero_controle_pncp:
            print("Erro: 'numeroControlePNCP' não encontrado.")
            return

        # Remover caracteres especiais do nome da tabela
        table_name = re.sub(r'[/-]', '_', numero_controle_pncp)
        print(f"DEBUG: Nome da tabela convertido: {table_name}")

        # SQL para criar a tabela com as colunas especificadas
        create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS '{table_name}' (
                numeroItem INTEGER PRIMARY KEY,
                descricao TEXT,
                materialOuServico TEXT,
                valorUnitarioEstimado REAL,
                valorTotal REAL,
                valorUnitarioHomologado REAL,
                valorTotalHomologado REAL,
                quantidadeHomologada REAL,
                unidadeMedida TEXT,
                situacaoCompraItemNome TEXT,
                dataAtualizacao TEXT,
                niFornecedor TEXT,
                nomeRazaoSocialFornecedor TEXT,
                situacaoCompraItemResultadoNome TEXT
            )
        """
        
        # Criação da tabela, se não existir
        with self.database_manager as conn:
            cursor = conn.cursor()
            cursor.execute(create_table_sql)
            conn.commit()
            print(f"Tabela '{table_name}' criada ou já existe.")

            # Inserir os dados de `resultados_completos` na tabela
            insert_sql = f"""
                INSERT OR REPLACE INTO '{table_name}' (
                    numeroItem,
                    descricao,
                    materialOuServico,
                    valorUnitarioEstimado,
                    valorTotal,
                    valorUnitarioHomologado,
                    valorTotalHomologado,
                    quantidadeHomologada,
                    unidadeMedida,
                    situacaoCompraItemNome,
                    dataAtualizacao,
                    niFornecedor,
                    nomeRazaoSocialFornecedor,
                    situacaoCompraItemResultadoNome
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            # Depuração para verificar o SQL de inserção e os valores
            print("DEBUG: SQL de inserção:", insert_sql)

            for resultado in data_api['resultados_completos']:
                # Preparando os valores para inserção
                valores = (
                    resultado.get("numeroItem"),
                    resultado.get("descricao"),
                    resultado.get("materialOuServico"),
                    resultado.get("valorUnitarioEstimado"),
                    resultado.get("valorTotal"),
                    resultado.get("valorUnitarioHomologado"),
                    resultado.get("valorTotalHomologado"),
                    resultado.get("quantidadeHomologada"),
                    resultado.get("unidadeMedida"),
                    resultado.get("situacaoCompraItemNome"),
                    resultado.get("dataAtualizacao"),
                    resultado.get("niFornecedor"),
                    resultado.get("nomeRazaoSocialFornecedor"),
                    resultado.get("situacaoCompraItemResultadoNome")
                )
                
                # Verificando o conteúdo dos valores antes de inserir
                print(f"DEBUG: Inserindo valores na tabela '{table_name}': {valores}")
                
                # Inserir os valores na tabela
                try:
                    cursor.execute(insert_sql, valores)
                except Exception as e:
                    print(f"Erro ao inserir dados na tabela '{table_name}': {e}")
            
            conn.commit()
        
        print(f"Dados inseridos com sucesso na tabela '{table_name}'.")

    def adjust_table_structure(self):
        """Verifica e cria a tabela 'controle_contratos' se não existir."""
        query = QSqlQuery(self.db)
        if not query.exec("SELECT name FROM sqlite_master WHERE type='table' AND name='controle_contratos'"):
            print("Erro ao verificar existência da tabela:", query.lastError().text())
        if not query.next():
            print("Tabela 'controle_contratos' não existe. Criando tabela...")
            self.create_table_if_not_exists()
        else:
            pass
            # print("Tabela 'controle_contratos' existe. Verificando estrutura da coluna...")

    def save_api_data_to_database(self, data_api):
        # Obtém o valor de 'numeroControlePNCP' para nome da tabela
        numero_controle_pncp = data_api['data_informacoes'].get('numeroControlePNCP')
        
        if not numero_controle_pncp:
            print("Erro: 'numeroControlePNCP' não encontrado nos dados da API.")
            return

        # Constrói a consulta de criação de tabela com o nome dinâmico
        create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS '{numero_controle_pncp}' (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                valorTotalEstimado REAL,
                valorTotalHomologado REAL,
                orcamentoSigilosoCodigo INTEGER,
                orcamentoSigilosoDescricao TEXT,
                numeroControlePNCP TEXT,
                linkSistemaOrigem TEXT,
                anoCompra INTEGER,
                sequencialCompra INTEGER,
                numeroCompra TEXT,
                processo TEXT
                -- Adicione outras colunas conforme necessário
            )
        """

        # Executa a criação da tabela
        with self.database_manager as conn:
            cursor = conn.cursor()
            cursor.execute(create_table_sql)
            
            # Insere os dados da API na tabela criada
            insert_sql = f"""
                INSERT INTO '{numero_controle_pncp}' (
                    valorTotalEstimado,
                    valorTotalHomologado,
                    orcamentoSigilosoCodigo,
                    orcamentoSigilosoDescricao,
                    numeroControlePNCP,
                    linkSistemaOrigem,
                    anoCompra,
                    sequencialCompra,
                    numeroCompra,
                    processo
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            # Extrai valores de 'data_informacoes' para inserir na tabela
            data_informacoes = data_api['data_informacoes']
            valores = (
                data_informacoes.get("valorTotalEstimado"),
                data_informacoes.get("valorTotalHomologado"),
                data_informacoes.get("orcamentoSigilosoCodigo"),
                data_informacoes.get("orcamentoSigilosoDescricao"),
                data_informacoes.get("numeroControlePNCP"),
                data_informacoes.get("linkSistemaOrigem"),
                data_informacoes.get("anoCompra"),
                data_informacoes.get("sequencialCompra"),
                data_informacoes.get("numeroCompra"),
                data_informacoes.get("processo")
            )
            
            cursor.execute(insert_sql, valores)
            conn.commit()
        
        print(f"Tabela '{numero_controle_pncp}' criada e dados inseridos com sucesso.")



    def create_table_if_not_exists(self):
        """Cria a tabela 'controle_contratos' com a estrutura definida, caso ainda não exista."""
        query = QSqlQuery(self.db)
        if not query.exec("""
            CREATE TABLE IF NOT EXISTS controle_contratos (
                status TEXT,
                dias TEXT,
                prorrogavel TEXT,
                custeio TEXT,
                numero TEXT,
                tipo TEXT,
                id_processo TEXT PRIMARY KEY,
                nome_fornecedor TEXT,
                objeto TEXT,
                valor_global TEXT,
                codigo TEXT,
                processo TEXT,
                cnpj_cpf_idgener TEXT,
                natureza_continuada TEXT,
                nome_resumido TEXT, 
                indicativo_om TEXT, 
                nome TEXT, 
                material_servico TEXT, 
                link_pncp TEXT,
                portaria TEXT, 
                gestor TEXT, 
                gestor_substituto TEXT, 
                fiscal TEXT, 
                fiscal_substituto TEXT, 
                fiscal_administrativo TEXT,
                vigencia_inicial TEXT,
                          vigencia_final TEXT, 
                          setor TEXT,
                comentarios TEXT, 
                          registro_status TEXT, 
                          termo_aditivo TEXT, 
                          atualizacao_comprasnet TEXT,
                instancia_governanca TEXT, 
                          comprasnet_contratos TEXT, 
                          licitacao_numero TEXT,
                data_assinatura TEXT, 
                          data_publicacao TEXT, 
                          categoria TEXT, 
                          subtipo TEXT,
                amparo_legal TEXT, 
                          modalidade TEXT, 
                          assinatura_contrato TEXT
                               
            )
        """):
            print("Falha ao criar a tabela 'controle_contratos':", query.lastError().text())
        else:
            print("Tabela 'controle_contratos' criada com sucesso.")

    def setup_model(self, table_name, editable=False):
        """Configura o modelo SQL para a tabela especificada."""
        # Passa o database_manager para o modelo personalizado
        self.model = CustomSqlTableModel(parent=self, db=self.db, database_manager=self.database_manager, non_editable_columns=[4, 8, 10, 13])
        self.model.setTable(table_name)
        
        if editable:
            self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
        
        self.model.select()
        return self.model

    def get_data(self, table_name):
        """Retorna todos os dados da tabela especificada."""
        return self.database_manager.fetch_all(f"SELECT * FROM {table_name}")
        
    def insert_or_update_data(self, data):
        print("Dados recebidos para salvar:", data)
        upsert_sql = '''
        INSERT INTO controle_contratos (
            status, dias, prorrogavel, custeio, numero, 
            tipo, id_processo, nome_fornecedor, objeto, valor_global, 
            codigo, processo, cnpj_cpf_idgener, natureza_continuada, nome_resumido, 
            indicativo_om, nome, material_servico, link_pncp, portaria, 
            gestor, gestor_substituto, fiscal, fiscal_substituto, fiscal_administrativo, 
            vigencia_inicial, vigencia_final, setor, comentarios, registro_status, termo_aditivo, 
            atualizacao_comprasnet, instancia_governanca, comprasnet_contratos, licitacao_numero, data_assinatura, 
            data_publicacao, categoria, subtipo, amparo_legal, modalidade, 
            assinatura_contrato
        ) VALUES (
            ?, ?, ?, ?, ?, 
            ?, ?, ?, ?, ?, 
            ?, ?, ?, ?, ?, 
            ?, ?, ?, ?, ?, 
            ?, ?, ?, ?, ?, 
            ?, ?, ?, ?, ?, 
            ?, ?, ?, ?, ?, 
            ?, ?, ?, ?, ?, 
            ?)
        ON CONFLICT(id_processo) DO UPDATE SET
                status=excluded.status,
                dias=excluded.dias,
                prorrogavel=excluded.prorrogavel,
                custeio=excluded.custeio,
                numero=excluded.numero,
                tipo=excluded.tipo,
                nome_fornecedor=excluded.nome_fornecedor,
                objeto=excluded.objeto,
                valor_global=excluded.valor_global,
                codigo=excluded.codigo,
                processo=excluded.processo,
                cnpj_cpf_idgener=excluded.cnpj_cpf_idgener,
                natureza_continuada=excluded.natureza_continuada,
                nome_resumido=excluded.nome_resumido,
                indicativo_om=excluded.indicativo_om,
                nome=excluded.nome,
                material_servico=excluded.material_servico,
                link_pncp=excluded.link_pncp,
                portaria=excluded.portaria,
                gestor=excluded.gestor,
                gestor_substituto=excluded.gestor_substituto,
                fiscal=excluded.fiscal,
                fiscal_substituto=excluded.fiscal_substituto,
                fiscal_administrativo=excluded.fiscal_administrativo,
                vigencia_inicial=excluded.vigencia_inicial,
                vigencia_final=excluded.vigencia_final,
                setor=excluded.setor,
                comentarios=excluded.comentarios,
                registro_status=excluded.registro_status,
                termo_aditivo=excluded.termo_aditivo,
                atualizacao_comprasnet=excluded.atualizacao_comprasnet,
                instancia_governanca=excluded.instancia_governanca,
                comprasnet_contratos=excluded.comprasnet_contratos,
                licitacao_numero=excluded.licitacao_numero,
                data_assinatura=excluded.data_assinatura,
                data_publicacao=excluded.data_publicacao,
                categoria=excluded.categoria,
                subtipo=excluded.subtipo,
                amparo_legal=excluded.amparo_legal,
                modalidade=excluded.modalidade,
                assinatura_contrato=excluded.assinatura_contrato
        '''

        # Verifica se 'situacao' está dentro dos valores válidos
        valid_situations = ["Planejamento", "Aprovado", "Sessão Pública", "Homologado", "Empenhado", "Concluído", "Arquivado"]
        data['situacao'] = data.get('situacao', 'Planejamento')
        if data['situacao'] not in valid_situations:
            data['situacao'] = 'Planejamento'

        # Executa a inserção ou atualização
        try:
            with self.database_manager as conn:
                cursor = conn.cursor()
                cursor.execute(upsert_sql, (
                    data.get('status'),
                    data.get('dias'),
                    data.get('prorrogavel'),
                    data.get('custeio'),
                    data.get('numero'),
                    data.get('tipo'),
                    data.get('id_processo'),
                    data.get('nome_fornecedor'),
                    data.get('objeto'),
                    data.get('valor_global'),
                    data.get('codigo'),
                    data.get('processo'),
                    data.get('cnpj_cpf_idgener'),
                    data.get('natureza_continuada'),
                    data.get('nome_resumido'),
                    data.get('indicativo_om'),
                    data.get('nome'),
                    data.get('material_servico'),
                    data.get('link_pncp'),
                    data.get('portaria'),
                    data.get('gestor'),
                    data.get('gestor_substituto'),
                    data.get('fiscal'),
                    data.get('fiscal_substituto'),
                    data.get('fiscal_administrativo'),
                    data.get('vigencia_inicial'),
                    data.get('vigencia_final'),
                    data.get('setor'),
                    data.get('comentarios'),
                    data.get('registro_status'),
                    data.get('termo_aditivo'),
                    data.get('atualizacao_comprasnet'),
                    data.get('instancia_governanca'),
                    data.get('comprasnet_contratos'),
                    data.get('licitacao_numero'),
                    data.get('data_assinatura'),
                    data.get('data_publicacao'),
                    data.get('categoria'),
                    data.get('subtipo'),
                    data.get('amparo_legal'),
                    data.get('modalidade'),
                    data.get('assinatura_contrato')
                    )) 
                conn.commit()

        except sqlite3.OperationalError as e:
            if "no such table" in str(e):
                QMessageBox.warning(None, "Erro", "A tabela 'controle_contratos' não existe. Por favor, crie a tabela primeiro.")
                return
            else:
                QMessageBox.warning(None, "Erro", f"Ocorreu um erro ao tentar salvar os dados: {str(e)}")

class CustomSqlTableModel(QSqlTableModel):
    def __init__(self, parent=None, db=None, database_manager=None, non_editable_columns=None):
        super().__init__(parent, db)
        self.database_manager = database_manager
        self.non_editable_columns = non_editable_columns if non_editable_columns is not None else []
        
        # Define os nomes das colunas
        self.column_names = [
            "status", "dias", "prorrogavel", "custeio", "numero", "tipo", "id_processo", "nome_fornecedor", "objeto",
            "valor_global", "codigo", "processo", "cnpj_cpf_idgener", "natureza_continuada", "nome_resumido", "indicativo_om",
            "nome", "material_servico", "link_pncp", "portaria", "gestor", "gestor_substituto", "fiscal", "fiscal_substituto",
            "fiscal_administrativo", "vigencia_inicial", "vigencia_final", "setor", "comentarios", "registro_status",
            "termo_aditivo", "atualizacao_comprasnet", "instancia_governanca", "comprasnet_contratos", "licitacao_numero",
            "data_assinatura", "data_publicacao", "categoria", "subtipo", "amparo_legal", "modalidade", "assinatura_contrato"       
        ]

    def flags(self, index):
        if index.column() in self.non_editable_columns:
            return super().flags(index) & ~Qt.ItemFlag.ItemIsEditable  # Remove a permissão de edição
        return super().flags(index)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        # Verifica se a coluna deve ser não editável e ajusta o retorno para DisplayRole
        if role == Qt.ItemDataRole.DisplayRole and index.column() in self.non_editable_columns:
            return super().data(index, role)

        return super().data(index, role)