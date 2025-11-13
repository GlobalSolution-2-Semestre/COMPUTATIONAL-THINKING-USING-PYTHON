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


#Função de Atualizar o Colaborador 
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
        
#Função para deletar o Colaborador 
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
