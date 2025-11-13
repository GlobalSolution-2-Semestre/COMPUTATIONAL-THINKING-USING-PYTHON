"""
NOME: Guilherme Macedo Martins|RM: 562396|TURMA: 1TDSPF
NOME: Pedro Henrique Luiz Alves Duarte|RM: 563405|TURMA: 1TDSPF

"""

import oracledb  
import json      
from datetime import datetime  #

# --- CONFIGURAÇÃO DE CONEXÃO ORACLE ---
ORACLE_USER = "rm562396"
ORACLE_PASS = "230407"
ORACLE_DSN = "oracle.com.fiap:1521/orcl"  

print("""

███╗░░░███╗██╗███╗░░██╗██████╗░████████╗██████╗░░█████╗░░█████╗░██╗░░██╗
████╗░████║██║████╗░██║██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██║░██╔╝
██╔████╔██║██║██╔██╗██║██║░░██║░░░██║░░░██████╔╝███████║██║░░╚═╝█████═╝░
██║╚██╔╝██║██║██║╚████║██║░░██║░░░██║░░░██╔══██╗██╔══██║██║░░██╗██╔═██╗░
██║░╚═╝░██║██║██║░╚███║██████╔╝░░░██║░░░██║░░██║██║░░██║╚█████╔╝██║░╚██╗
╚═╝░░░░░╚═╝╚═╝╚═╝░░╚══╝╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝

 """)

# --- FUNÇÕES DE CONEXÃO COM O BANCO ---

def get_connection():
   
    try:
        conn = oracledb.connect(
            user=ORACLE_USER,
            password=ORACLE_PASS,
            dsn=ORACLE_DSN
        )
        return conn
    except oracledb.DatabaseError as e:
        print(f"Erro ao conectar ao Oracle Database: {e}")
        print("Verifique suas credenciais (usuário, senha, DSN) e se o banco está acessível.")
        return None
    except Exception as e:
        print(f"Erro inesperado na conexão: {e}")
        return None


# --- FUNÇÕES DE VALIDAÇÃO DE ENTRADA ---

def validar_int(prompt, min_val=None, max_val=None):
    """Valida a entrada de um número inteiro, opcionalmente dentro de um intervalo."""
    while True:
        try:
            # Tenta converter a entrada do usuário para inteiro
            valor_str = input(prompt)
            valor_int = int(valor_str)
            
            # Validações de intervalo (mínimo e máximo)
            if min_val is not None and valor_int < min_val:
                print(f"Valor inválido. O mínimo é {min_val}.")
            elif max_val is not None and valor_int > max_val:
                print(f"Valor inválido. O máximo é {max_val}.")
            else:
                # Se tudo estiver certo, retorna o valor
                return valor_int
        except ValueError:
            # Se a conversão para int() falhar, informa o usuário e o loop continua
            print("Entrada inválida. Por favor, digite um número inteiro.")

def validar_texto_nao_vazio(prompt):
    """Valida que a entrada de texto não está vazia."""
    while True:
        texto = input(prompt)
        # .strip() remove espaços em branco do início e fim
        if texto.strip():
            # Se a string (sem espaços) não estiver vazia, retorna
            return texto.strip()
        else:
            # Se a string estiver vazia, informa o usuário e o loop continua
            print("Este campo não pode ficar vazio. Por favor, digite um valor.")

def validar_opcao(prompt, opcoes_validas):
    # Converte a lista de opções válidas para minúsculas para comparação
    opcoes_lower = [str(opt).lower() for opt in opcoes_validas]
    while True:
        print(f"Opções válidas: {', '.join(opcoes_validas)}")
        # Obtém a entrada do usuário e a formata (minúscula, sem espaços)
        texto = input(prompt).strip().lower()
        
        # Verifica se a entrada formatada existe na lista de opções minúsculas
        if texto in opcoes_lower:
            # Retorna o valor com o case original (ex: 'Feliz' em vez de 'feliz')
            indice = opcoes_lower.index(texto)
            return opcoes_validas[indice]
        else:
            print("Opção inválida. Por favor, escolha uma das opções listadas.")



 # --- FUNÇÕES DE EXPORTAÇÃO JSON ---

def formatar_resultados_para_json(cursor, dados_brutos):
    """Converte resultados brutos do cursor em uma lista de dicionários."""
    # Obtém os nomes das colunas da consulta (ex: 'NOME', 'EMAIL')
    # cursor.description contém metadados das colunas
    colunas = [col[0].lower() for col in cursor.description]
    resultados = []
    
    # 2. Itera sobre cada linha de dados brutos (que são tuplas)
    for linha in dados_brutos:
        #  'zip' combina os nomes das colunas com os dados da linha
        #    dict() transforma essa combinação em um dicionário
        #    Ex: zip(['nome', 'email'], ('Ana', 'ana@email.com')) -> {'nome': 'Ana', 'email': 'ana@email.com'}
        resultados.append(dict(zip(colunas, linha)))
    return resultados

def exportar_para_json(dados, nome_arquivo):
    """Exporta uma lista de dicionários para um arquivo JSON."""
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False, default=str)
        print(f"\nSucesso! Dados exportados para '{nome_arquivo}'.")
    except IOError as e:
        print(f"Erro ao escrever o arquivo JSON: {e}")
    except Exception as e:
        print(f"Erro inesperado ao exportar JSON: {e}")

def prompt_exportar_json(cursor, dados_brutos, nome_base_arquivo):
    """Pergunta ao usuário se deseja exportar os resultados."""
    while True:
        escolha = input("\nDeseja exportar estes resultados para JSON? (s/n): ").strip().lower()
        if escolha == 's':
            # Formata os dados brutos (tuplas) para JSON (lista de dicts)
            dados_formatados = formatar_resultados_para_json(cursor, dados_brutos)
            # Cria um timestamp (data_hora) para garantir um nome de arquivo único
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"{nome_base_arquivo}_{timestamp}.json"
            # Chama a função de exportação
            exportar_para_json(dados_formatados, nome_arquivo)
            break
        elif escolha == 'n':
            break
        else:
            print("Opção inválida. Digite 's' ou 'n'.")



 # --- Função CRUD Colaborador  ---

def criar_colaborador(conn):
    print("\n---- Cadastrar Novo Colaborador ----")
    # Coleta e valida os dados de entrada
    nome = validar_texto_nao_vazio("Nome: ")
    email = validar_texto_nao_vazio("Email: ")
    cargo = validar_texto_nao_vazio("Cargo: ")

    try:
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO TB_COLABORADOR (NOME, EMAIL, CARGO)
            VALUES (:1, :2, :3)
            """
            cursor.execute(sql, [nome, email, cargo])
            conn.commit()
            print(f"Colaborador '{nome}' cadastrado com sucesso!")
    except oracledb.DatabaseError as e:
        # Se qualquer erro do banco ocorrer (ex: email duplicado), desfaz a transação
        print(f"Erro de banco de dados ao criar colaborador: {e}")
        conn.rollback()
    except Exception as e:
        print(f"Erro inesperado: {e}")
        conn.rollback()


# Função Listar o colaborar 
def listar_colaboradores(conn):
    print("\n--- [ Lista de Colaboradores ] ---")
    try:
        with conn.cursor() as cursor:
            sql = "SELECT ID_COLABORADOR, NOME, EMAIL, CARGO FROM TB_COLABORADOR ORDER BY NOME"
            cursor.execute(sql)
            colaboradores = cursor.fetchall()
            
            if not colaboradores:
                print("Nenhum colaborador cadastrado.")
                return
            print(f"{'ID':<5} | {'Nome':<30} | {'Email':<35} | {'Cargo':<20}")
            print("-" * 95)
            for c in colaboradores:
                print(f"{c[0]:<5} | {c[1]:<30} | {c[2]:<35} | {c[3]:<20}")
            cursor.execute(sql) 
            dados_brutos = cursor.fetchall()
            prompt_exportar_json(cursor, dados_brutos, "lista_colaboradores")

    except oracledb.DatabaseError as e:
        print(f"Erro de banco de dados ao listar colaboradores: {e}")
    except Exception as e:
       print(f"Erro inesperado: {e}")


#Função de Atualizar Colaborador 
def atualizar_colaborador(conn):
    """(Update) Atualiza dados de um colaborador existente."""
    print("\n--- [ Atualizar Colaborador ] ---")
    id_colaborador = validar_int("Digite o ID do colaborador que deseja atualizar: ")

    try:
        with conn.cursor() as cursor:
            sql_check = "SELECT NOME, EMAIL, CARGO FROM TB_COLABORADOR WHERE ID_COLABORADOR = :1"
            cursor.execute(sql_check, [id_colaborador])
            colab = cursor.fetchone() 

            if not colab:
                print(f"Erro: Colaborador com ID {id_colaborador} não encontrado.")
                return

            print(f"\nAtualizando dados de: {colab[0]}")
            print(f"Email atual: {colab[1]}")
            print(f"Cargo atual: {colab[2]}")
            novo_email = input(f"Novo Email (atual: {colab[1]}): ").strip() or colab[1]
            novo_cargo = input(f"Novo Cargo (atual: {colab[2]}): ").strip() or colab[2]
            sql_update = """
            UPDATE TB_COLABORADOR
            SET EMAIL = :1, CARGO = :2
            WHERE ID_COLABORADOR = :3
            """
            cursor.execute(sql_update, [novo_email, novo_cargo, id_colaborador])
            conn.commit()
            print(f"Dados do colaborador ID {id_colaborador} atualizados com sucesso!")

    except oracledb.DatabaseError as e:
        print(f"Erro de banco de dados ao atualizar colaborador: {e}")
        conn.rollback()
    except Exception as e:
        print(f"Erro inesperado: {e}")
        conn.rollback()

#Função para deletar Colaborador 
def deletar_colaborador(conn):
    """(Delete) Remove um colaborador do banco."""
    print("\n--- [ Deletar Colaborador ] ---")
    id_colaborador = validar_int("Digite o ID do colaborador que deseja deletar: ")
    print(f"ATENÇÃO: Deletar o colaborador ID {id_colaborador} também removerá todos os seus")
    print("check-ins, relatórios e alertas associados (devido às constraints ON DELETE CASCADE).")
    while True:
        confirm = input(f"Tem certeza que deseja continuar? (s/n): ").strip().lower()
        if confirm == 's':
            break 
        elif confirm == 'n':
            print("Operação cancelada.")
            return 
        else:
            print("Opção inválida.")
            
    try:
        with conn.cursor() as cursor:
            sql_delete = "DELETE FROM TB_COLABORADOR WHERE ID_COLABORADOR = :1"
            cursor.execute(sql_delete, [id_colaborador])
            if cursor.rowcount == 0:
                print(f"Nenhum colaborador encontrado com o ID {id_colaborador}.")
            else:
             
                conn.commit()
                print(f"Colaborador ID {id_colaborador} deletado com sucesso.")

    except oracledb.DatabaseError as e:
        print(f"Erro de banco de dados ao deletar colaborador: {e}")
        conn.rollback()
    except Exception as e:
        print(f"Erro inesperado: {e}")
        conn.rollback()
# 
#---- função para Criar Checkin ----
def criar_checkin(conn):
    """(Create) Adiciona um novo check-in de humor."""
    print("\n--- [ Novo Check-in de Humor ] ---")
    
    id_colaborador = validar_int("Digite o seu ID de Colaborador: ")
    try:
        with conn.cursor() as cursor_check:
            cursor_check.execute("SELECT NOME FROM TB_COLABORADOR WHERE ID_COLABORADOR = :1", [id_colaborador])
            colab = cursor_check.fetchone()
            if not colab:
                print(f"Erro: Colaborador com ID {id_colaborador} não encontrado.")
                return # Interrompe a função se o ID não for válido
            print(f"Registrando check-in para: {colab[0]}")
    except oracledb.DatabaseError as e:
        print(f"Erro ao verificar colaborador: {e}")
        return

    # 2. Coleta de dados do check-in
    opcoes_humor = ['Feliz','Motivado','Tranquilo','Neutro','Cansado','Estressado']
    humor = validar_opcao("Como você está se sentindo? ", opcoes_humor)
    comentario = input("Gostaria de adicionar um comentário? (opcional): ").strip()

    try:
        with conn.cursor() as cursor:
            #  Executa o INSERT
            sql = """
            INSERT INTO TB_CHECKIN (ID_COLABORADOR, HUMOR, COMENTARIO)
            VALUES (:1, :2, :3)
            """
            cursor.execute(sql, [id_colaborador, humor, comentario])
            #  Confirma (salva) o check-in
            conn.commit()
            print("Check-in de humor salvo com sucesso!")
    except oracledb.DatabaseError as e:
        print(f"Erro de banco de dados ao salvar check-in: {e}")
        conn.rollback()
    except Exception as e:
        print(f"Erro inesperado: {e}")
        conn.rollback()

#---- função para Listar Checkin ----

def listar_checkins_por_colaborador(conn):
    """(Read) Lista todos os check-ins de um colaborador específico."""
    print("\n--- [ Histórico de Check-ins por Colaborador ] ---")
    id_colaborador = validar_int("Digite o ID do Colaborador para ver o histórico: ")

    try:
        with conn.cursor() as cursor:
            #  SQL para buscar check-ins de um colaborador específico
            sql = """
            SELECT ID_CHECKIN, DATA_REGISTRO, HUMOR, COMENTARIO
            FROM TB_CHECKIN
            WHERE ID_COLABORADOR = :1
            ORDER BY DATA_REGISTRO DESC
            """
            #  Executa a consulta passando o ID como parâmetro
            cursor.execute(sql, [id_colaborador])
            registros = cursor.fetchall()

            if not registros:
                print(f"Nenhum check-in encontrado para o colaborador ID {id_colaborador}.")
                return

            #  Imprime os resultados
            print(f"\nHistórico do Colaborador ID {id_colaborador}:")
            print(f"{'ID Chk':<8} | {'Data':<20} | {'Humor':<15} | {'Comentário'}")
            print("-" * 80)
            for r in registros:
                data_formatada = r[1].strftime('%Y-%m-%d')
                print(f"{r[0]:<8} | {data_formatada:<20} | {r[2]:<15} | {r[3]}")
            
            #  Exportação JSON (Opcional)
            cursor.execute(sql, [id_colaborador])
            dados_brutos = cursor.fetchall()
            prompt_exportar_json(cursor, dados_brutos, f"historico_checkin_{id_colaborador}")

    except oracledb.DatabaseError as e:
        print(f"Erro de banco de dados ao listar check-ins: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

#---- função para Criar Alerta ----

def criar_alerta(conn):
    """(Create) Cria um novo alerta manual para um colaborador."""
    print("\n--- [ Criar Novo Alerta (Manual) ] ---")
    
    id_colaborador = validar_int("Digite o ID do Colaborador: ")
    try:
        with conn.cursor() as cursor_check:
            cursor_check.execute("SELECT NOME FROM TB_COLABORADOR WHERE ID_COLABORADOR = :1", [id_colaborador])
            colab = cursor_check.fetchone()
            if not colab:
                print(f"Erro: Colaborador com ID {id_colaborador} não encontrado.")
                return
            print(f"Criando alerta para: {colab[0]}")
    except oracledb.DatabaseError as e:
        print(f"Erro ao verificar colaborador: {e}")
        return

    #  Coleta de dados do alerta
    opcoes_alerta = ['Informativo', 'Atenção', 'Crítico', 'Aviso']
    tipo_alerta = validar_opcao("Tipo do Alerta: ", opcoes_alerta)
    descricao = validar_texto_nao_vazio("Descrição do Alerta: ")

    try:
        with conn.cursor() as cursor:
            # 3. Executa o INSERT
            # DATA_ENVIO usa o default (SYSTIMESTAMP) do banco
            sql = """
            INSERT INTO TB_ALERTA (ID_COLABORADOR, TIPO_ALERTA, DESCRICAO)
            VALUES (:1, :2, :3)
            """
            cursor.execute(sql, [id_colaborador, tipo_alerta, descricao])
            # 4. Confirma (salva) o alerta
            conn.commit()
            print("Alerta criado com sucesso!")
    except oracledb.DatabaseError as e:
        print(f"Erro de banco de dados ao criar alerta: {e}")
        conn.rollback()
    except Exception as e:
        print(f"Erro inesperado: {e}")
        conn.rollback()
#---- função para Listar Alertas  ----
def listar_alertas_por_colaborador(conn):
    """(Read) Lista todos os alertas de um colaborador."""
    print("\n--- [ Histórico de Alertas por Colaborador ] ---")
    id_colaborador = validar_int("Digite o ID do Colaborador para ver os alertas: ")

    try:
        with conn.cursor() as cursor:
            #  SQL para buscar alertas de um colaborador
            sql = """
            SELECT ID_ALERTA, TIPO_ALERTA, DESCRICAO, DATA_ENVIO
            FROM TB_ALERTA
            WHERE ID_COLABORADOR = :1
            ORDER BY DATA_ENVIO DESC
            """
            cursor.execute(sql, [id_colaborador])
            alertas = cursor.fetchall()

            if not alertas:
                print(f"Nenhum alerta encontrado para o colaborador ID {id_colaborador}.")
                return

            #  Imprime os resultados
            print(f"\nAlertas do Colaborador ID {id_colaborador}:")
            print(f"{'ID':<5} | {'Data/Hora':<20} | {'Tipo':<12} | {'Descrição'}")
            print("-" * 80)
            for a in alertas:
                # Formata o objeto 'timestamp' do Oracle para 'YYYY-MM-DD HH:MM'
                data_formatada = a[3].strftime('%Y-%m-%d %H:%M')
                print(f"{a[0]:<5} | {data_formatada:<20} | {a[1]:<12} | {a[2]}")
            
            # Exportação JSON (Opcional)
            cursor.execute(sql, [id_colaborador])
            dados_brutos = cursor.fetchall()
            prompt_exportar_json(cursor, dados_brutos, f"historico_alertas_{id_colaborador}")

    except oracledb.DatabaseError as e:
        print(f"Erro de banco de dados ao listar alertas: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

 # ---- função para Listar Relatorio----

def listar_relatorios_por_colaborador(conn):
    """(Read) Lista todos os relatórios de um colaborador."""
    print("\n--- [ Histórico de Relatórios por Colaborador ] ---")
    id_colaborador = validar_int("Digite o ID do Colaborador para ver os relatórios: ")

    try:
        with conn.cursor() as cursor:
            # SQL para buscar relatórios de um colaborador
            sql = """
            SELECT ID_RELATORIO, DATA_GERACAO, MEDIA_HUMOR, RESUMO
            FROM TB_RELATORIO
            WHERE ID_COLABORADOR = :1
            ORDER BY DATA_GERACAO DESC
            """
            cursor.execute(sql, [id_colaborador])
            relatorios = cursor.fetchall()

            if not relatorios:
                print(f"Nenhum relatório encontrado para o colaborador ID {id_colaborador}.")
                return

            # Imprime os resultados
            print(f"\nRelatórios do Colaborador ID {id_colaborador}:")
            print(f"{'<ID>':<5} | {'Data':<15} | {'Média Humor':<12} | {'Resumo'}")
            print("-" * 80)
            for r in relatorios:
                data_formatada = r[1].strftime('%Y-%m-%d')
                print(f"{r[0]:<5} | {data_formatada:<15} | {r[2]:<12.2f} | {r[3]}")
            
            # Exportação JSON (Opcional)
            cursor.execute(sql, [id_colaborador])
            dados_brutos = cursor.fetchall()
            prompt_exportar_json(cursor, dados_brutos, f"historico_relatorios_{id_colaborador}")

    except oracledb.DatabaseError as e:
        print(f"Erro de banco de dados ao listar relatórios: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

        # ---- CONSULTAS E EXPORTAÇÃO JSON ----

def consulta_humor_recente(conn):
    print("\n--- [ Consulta 1: Humor Mais Recente por Colaborador ] ---")
    
    sql = """
    SELECT c.NOME, ch.HUMOR, ch.COMENTARIO, ch.DATA_REGISTRO
    FROM TB_COLABORADOR c
    JOIN TB_CHECKIN ch
      ON ch.ID_COLABORADOR = c.ID_COLABORADOR
    WHERE ch.DATA_REGISTRO = (
      SELECT MAX(ch2.DATA_REGISTRO)
      FROM TB_CHECKIN ch2
      WHERE ch2.ID_COLABORADOR = c.ID_COLABORADOR
    )
    ORDER BY c.NOME
    """
    
    try:
        with conn.cursor() as cursor:
            # Executa a consulta complexa
            cursor.execute(sql)
            resultados = cursor.fetchall()

            if not resultados:
                print("Nenhum dado encontrado para gerar o relatório.")
                return

            # Imprime os resultados
            print(f"\n{'Nome':<30} | {'Humor':<15} | {'Data':<15} | {'Comentário'}")
            print("-" * 100)
            for r in resultados:
                data_formatada = r[3].strftime('%Y-%m-%d')
                print(f"{r[0]:<30} | {r[1]:<15} | {data_formatada:<15} | {r[2]}")
            
            # Exportação JSON (Opcional)
            cursor.execute(sql)
            dados_brutos = cursor.fetchall()
            prompt_exportar_json(cursor, dados_brutos, "consulta_humor_recente")

    except oracledb.DatabaseError as e:
        print(f"Erro de banco de dados na consulta: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

def consulta_media_geral_colaborador(conn):
    print("\n--- [ Consulta 2: Média Geral de Humor (dos Relatórios) ] ---")
    sql = """
    SELECT C.NOME, ROUND(AVG(R.MEDIA_HUMOR),2) AS MEDIA_GERAL
    FROM TB_COLABORADOR C
    JOIN TB_RELATORIO R ON C.ID_COLABORADOR = R.ID_COLABORADOR
    GROUP BY C.NOME
    ORDER BY MEDIA_GERAL DESC
    """
    
    try:
        with conn.cursor() as cursor:
            # Executa a consulta de agregação
            cursor.execute(sql)
            resultados = cursor.fetchall()

            if not resultados:
                print("Nenhum relatório encontrado para calcular médias.")
                return

            # Imprime os resultados
            print(f"\n{'Nome':<30} | {'Média de Humor (Relatórios)'}")
            print("-" * 60)
            for r in resultados:
                print(f"{r[0]:<30} | {r[1]:<12.2f}")
            
            # Exportação JSON (Opcional)
            cursor.execute(sql)
            dados_brutos = cursor.fetchall()
            prompt_exportar_json(cursor, dados_brutos, "consulta_media_humor_relatorios")

    except oracledb.DatabaseError as e:
        print(f"Erro de banco de dados na consulta: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

def consulta_colaboradores_risco(conn):
    print("\n--- [ Consulta 3: Colaboradores em Risco (Média < 7) ] ---")

    sql = """
    SELECT C.NOME, ROUND(AVG(R.MEDIA_HUMOR),2) AS MEDIA_HUMOR
    FROM TB_COLABORADOR C
    JOIN TB_RELATORIO R ON C.ID_COLABORADOR = R.ID_COLABORADOR
    GROUP BY C.NOME
    HAVING AVG(R.MEDIA_HUMOR) < 7
    ORDER BY MEDIA_HUMOR ASC
    """
    
    try:
        with conn.cursor() as cursor:
            #  Executa a consulta com filtro de agregação (HAVING)
            cursor.execute(sql)
            resultados = cursor.fetchall()

            if not resultados:
                print("Nenhum colaborador encontrado com média de humor abaixo de 7.")
                return

            #  Imprime os resultados
            print("\nColaboradores que podem precisar de atenção:")
            print(f"\n{'Nome':<30} | {'Média de Humor (Relatórios)'}")
            print("-" * 60)
            for r in resultados:
                print(f"{r[0]:<30} | {r[1]:<12.2f}")
            
            #  Exportação JSON (Opcional)
            cursor.execute(sql)
            dados_brutos = cursor.fetchall()
            prompt_exportar_json(cursor, dados_brutos, "consulta_colaboradores_risco")

    except oracledb.DatabaseError as e:
        print(f"Erro de banco de dados na consulta: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

