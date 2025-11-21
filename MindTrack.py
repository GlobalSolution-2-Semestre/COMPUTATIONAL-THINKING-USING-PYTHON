
"""
NOME: Guilherme Macedo Martins | RM: 562396 | TURMA: 1TDSPF
NOME: Pedro Henrique Luiz Alves Duarte | RM: 563405 | TURMA: 1TDSPF

Projeto: MindTrack - Plataforma de Monitoramento de Bem-Estar e Saúde Mental no Trabalho
Global Solution 2025 - Computational Thinking Using Python
"""

import oracledb
import json
from datetime import datetime

# --- CONFIGURAÇÃO DE CONEXÃO ORACLE ---
ORACLE_USER = "rm563405"
ORACLE_PASS = "250307"
ORACLE_DSN = "oracle.fiap.com.br:1521/orcl"


# --- FUNÇÃO DE CONEXÃO COM O BANCO ---

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
        print("Verifique usuário, senha, DSN e se o banco está acessível.")
        return None
    except Exception as e:
        print(f"Erro inesperado na conexão: {e}")
        return None


# --- FUNÇÕES DE VALIDAÇÃO DE ENTRADA ---

def validar_int(prompt, min_val=None, max_val=None):
    while True:
        try:
            valor_str = input(prompt)
            valor_int = int(valor_str)

            if min_val is not None and valor_int < min_val:
                print(f"Valor inválido. O mínimo é {min_val}.")
            elif max_val is not None and valor_int > max_val:
                print(f"Valor inválido. O máximo é {max_val}.")
            else:
                return valor_int
        except ValueError:
            print("Entrada inválida. Por favor, digite um número inteiro.")


def validar_texto_nao_vazio(prompt):
    while True:
        texto = input(prompt).strip()
        if texto:
            return texto
        print("Este campo não pode ficar vazio. Por favor, digite um valor.")


def validar_opcao(prompt, opcoes_validas):
    opcoes_lower = [str(opt).lower() for opt in opcoes_validas]
    while True:
        print(f"Opções válidas: {', '.join(opcoes_validas)}")
        texto = input(prompt).strip().lower()

        if texto in opcoes_lower:
            indice = opcoes_lower.index(texto)
            return opcoes_validas[indice]
        print("Opção inválida. Por favor, escolha uma das opções listadas.")


def validar_email(prompt):
    while True:
        email = input(prompt).strip()
        if "@" in email and "." in email and len(email) >= 5:
            return email
        print("Email inválido. Digite um email válido (ex: usuario@dominio.com).")


# --- FUNÇÕES DE EXPORTAÇÃO JSON ---

def formatar_resultados_para_json(cursor, dados_brutos):
    colunas = [col[0].lower() for col in cursor.description]
    resultados = []
    for linha in dados_brutos:
        resultados.append(dict(zip(colunas, linha)))
    return resultados


def exportar_para_json(dados, nome_arquivo):
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False, default=str)
        print(f"Sucesso! Dados exportados para '{nome_arquivo}'.")
    except IOError as e:
        print(f"Erro ao escrever o arquivo JSON: {e}")
    except Exception as e:
        print(f"Erro inesperado ao exportar JSON: {e}")


def prompt_exportar_json(cursor, dados_brutos, nome_base_arquivo):
    while True:
        escolha = input("Deseja exportar estes resultados para JSON? (s/n): ").strip().lower()
        if escolha == 's':
            dados_formatados = formatar_resultados_para_json(cursor, dados_brutos)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"{nome_base_arquivo}_{timestamp}.json"
            exportar_para_json(dados_formatados, nome_arquivo)
            break
        elif escolha == 'n':
            break
        else:
            print("Opção inválida. Digite 's' ou 'n'.")


# --- CRUD COLABORADOR ---
def criar_colaborador(conn):
    print("\n---- Cadastrar Novo Colaborador ----")
    nome = validar_texto_nao_vazio("Nome: ")
    email = validar_email("Email: ")
    cargo = validar_texto_nao_vazio("Cargo: ")

    try:
        with conn.cursor() as cursor:
            sql = '''
            INSERT INTO TB_COLABORADOR (NOME, EMAIL, CARGO)
            VALUES (:1, :2, :3)
            '''
            cursor.execute(sql, [nome, email, cargo])
            conn.commit()
            print(f"Colaborador '{nome}' cadastrado com sucesso!")
    except oracledb.DatabaseError as e:
        print(f"Erro de banco de dados ao criar colaborador: {e}")
        conn.rollback()
    except Exception as e:
        print(f"Erro inesperado: {e}")
        conn.rollback()


def listar_colaboradores(conn):
    print("\n---  Lista de Colaboradores  ---")
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

            prompt_exportar_json(cursor, colaboradores, "lista_colaboradores")

    except oracledb.DatabaseError as e:
        print(f"Erro de banco de dados ao listar colaboradores: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")


def atualizar_colaborador(conn):
    print("\n---  Atualizar Colaborador  ---")
    id_colaborador = validar_int("Digite o ID do colaborador que deseja atualizar: ", min_val=1)

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

            novo_email_input = input(f"Novo Email (ENTER para manter '{colab[1]}'): ").strip()
            if novo_email_input:
                novo_email = validar_email("Confirme o novo Email: ")
            else:
                novo_email = colab[1]

            novo_cargo = input(f"Novo Cargo (ENTER para manter '{colab[2]}'): ").strip() or colab[2]

            sql_update = '''
            UPDATE TB_COLABORADOR
            SET EMAIL = :1, CARGO = :2
            WHERE ID_COLABORADOR = :3
            '''
            cursor.execute(sql_update, [novo_email, novo_cargo, id_colaborador])
            conn.commit()
            print(f"Dados do colaborador ID {id_colaborador} atualizados com sucesso!")

    except oracledb.DatabaseError as e:
        print(f"Erro de banco de dados ao atualizar colaborador: {e}")
        conn.rollback()
    except Exception as e:
        print(f"Erro inesperado: {e}")
        conn.rollback()


def deletar_colaborador(conn):
    print("\n---  Deletar Colaborador  ---")
    id_colaborador = validar_int("Digite o ID do colaborador que deseja deletar: ", min_val=1)

    print("\nATENÇÃO: Se o colaborador tiver check-ins, relatórios ou alertas associados,")
    print("a exclusão poderá falhar devido a restrições de integridade do Oracle (por exemplo, ORA-02292).")
    while True:
        confirm = input("Tem certeza que deseja continuar? (s/n): ").strip().lower()
        if confirm == 's':
            break
        elif confirm == 'n':
            print("Operação cancelada.")
            return
        else:
            print("Opção inválida. Digite 's' ou 'n'.")

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


# --- CHECK-INS ---

def criar_checkin(conn):

    print("\n---  Check-in de Humor  ---")

    id_colaborador = validar_int("Digite o seu ID de Colaborador: ", min_val=1)
    try:
        with conn.cursor() as cursor_check:
            cursor_check.execute("SELECT NOME FROM TB_COLABORADOR WHERE ID_COLABORADOR = :1", [id_colaborador])
            colab = cursor_check.fetchone()
            if not colab:
                print(f"Erro: Colaborador com ID {id_colaborador} não encontrado.")
                return
            print(f"Registrando check-in para: {colab[0]}")
    except oracledb.DatabaseError as e:
        print(f"Erro ao verificar colaborador: {e}")
        return

    opcoes_humor = ['Feliz', 'Motivado', 'Tranquilo', 'Neutro', 'Cansado', 'Estressado']
    humor = validar_opcao("Como você está se sentindo? ", opcoes_humor)
    comentario = input("Gostaria de adicionar um comentário? (opcional): ").strip()

    try:
        with conn.cursor() as cursor:
            sql = '''
            INSERT INTO TB_CHECKIN (ID_COLABORADOR, HUMOR, COMENTARIO)
            VALUES (:1, :2, :3)
            '''
            cursor.execute(sql, [id_colaborador, humor, comentario])
            conn.commit()
            print("Check-in de humor salvo com sucesso!")
    except oracledb.DatabaseError as e:
        print(f"Erro de banco de dados ao salvar check-in: {e}")
        conn.rollback()
    except Exception as e:
        print(f"Erro inesperado: {e}")
        conn.rollback()


def listar_checkins_por_colaborador(conn):
    print("\n---  Histórico de Check-ins por Colaborador ---")
    id_colaborador = validar_int("Digite o ID do Colaborador para ver o histórico: ", min_val=1)

    try:
        with conn.cursor() as cursor:
            sql = '''
            SELECT ID_CHECKIN, DATA_REGISTRO, HUMOR, COMENTARIO
            FROM TB_CHECKIN
            WHERE ID_COLABORADOR = :1
            ORDER BY DATA_REGISTRO DESC
            '''
            cursor.execute(sql, [id_colaborador])
            registros = cursor.fetchall()

            if not registros:
                print(f"Nenhum check-in encontrado para o colaborador ID {id_colaborador}.")
                return

            print(f"\nHistórico do Colaborador ID {id_colaborador}:")
            print(f"{'ID Chk':<8} | {'Data':<20} | {'Humor':<15} | {'Comentário'}")
            print("-" * 80)
            for r in registros:
                data_formatada = r[1].strftime('%Y-%m-%d')
                print(f"{r[0]:<8} | {data_formatada:<20} | {r[2]:<15} | {r[3]}")

            prompt_exportar_json(cursor, registros, f"historico_checkin_{id_colaborador}")

    except oracledb.DatabaseError as e:
        print(f"Erro de banco de dados ao listar check-ins: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")


# --- ALERTAS ---

def criar_alerta(conn):
    print("\n--- Criar Novo Alerta  ---")

    id_colaborador = validar_int("Digite o ID do Colaborador: ", min_val=1)
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

    opcoes_alerta = ['Informativo', 'Atenção', 'Crítico', 'Aviso']
    tipo_alerta = validar_opcao("Tipo do Alerta: ", opcoes_alerta)
    descricao = validar_texto_nao_vazio("Descrição do Alerta: ")

    try:
        with conn.cursor() as cursor:
            sql = '''
            INSERT INTO TB_ALERTA (ID_COLABORADOR, TIPO_ALERTA, DESCRICAO)
            VALUES (:1, :2, :3)
            '''
            cursor.execute(sql, [id_colaborador, tipo_alerta, descricao])
            conn.commit()
            print("Alerta criado com sucesso!")
    except oracledb.DatabaseError as e:
        print(f"Erro de banco de dados ao criar alerta: {e}")
        conn.rollback()
    except Exception as e:
        print(f"Erro inesperado: {e}")
        conn.rollback()


def listar_alertas_por_colaborador(conn):
    print("\n---  Histórico de Alertas por Colaborador  ---")
    id_colaborador = validar_int("Digite o ID do Colaborador para ver os alertas: ", min_val=1)

    try:
        with conn.cursor() as cursor:
            sql = '''
            SELECT ID_ALERTA, TIPO_ALERTA, DESCRICAO, DATA_ENVIO
            FROM TB_ALERTA
            WHERE ID_COLABORADOR = :1
            ORDER BY DATA_ENVIO DESC
            '''
            cursor.execute(sql, [id_colaborador])
            alertas = cursor.fetchall()

            if not alertas:
                print(f"Nenhum alerta encontrado para o colaborador ID {id_colaborador}.")
                return

            print(f"\nAlertas do Colaborador ID {id_colaborador}:")
            print(f"{'ID':<5} | {'Data/Hora':<20} | {'Tipo':<12} | {'Descrição'}")
            print("-" * 80)
            for a in alertas:
                data_formatada = a[3].strftime('%Y-%m-%d %H:%M')
                print(f"{a[0]:<5} | {data_formatada:<20} | {a[1]:<12} | {a[2]}")

            prompt_exportar_json(cursor, alertas, f"historico_alertas_{id_colaborador}")

    except oracledb.DatabaseError as e:
        print(f"Erro de banco de dados ao listar alertas: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")


# --- RELATÓRIOS ---

def listar_relatorios_por_colaborador(conn):
    print("\n---  Histórico de Relatórios por Colaborador  ---")
    id_colaborador = validar_int("Digite o ID do Colaborador para ver os relatórios: ", min_val=1)

    try:
        with conn.cursor() as cursor:
            sql = '''
            SELECT ID_RELATORIO, DATA_GERACAO, MEDIA_HUMOR, RESUMO
            FROM TB_RELATORIO
            WHERE ID_COLABORADOR = :1
            ORDER BY DATA_GERACAO DESC
            '''
            cursor.execute(sql, [id_colaborador])
            relatorios = cursor.fetchall()

            if not relatorios:
                print(f"Nenhum relatório encontrado para o colaborador ID {id_colaborador}.")
                return

            print(f"\nRelatórios do Colaborador ID {id_colaborador}:")
            print(f"{'ID':<5} | {'Data':<15} | {'Média Humor':<12} | {'Resumo'}")
            print("-" * 80)
            for r in relatorios:
                data_formatada = r[1].strftime('%Y-%m-%d')
                print(f"{r[0]:<5} | {data_formatada:<15} | {r[2]:<12.2f} | {r[3]}")

            prompt_exportar_json(cursor, relatorios, f"historico_relatorios_{id_colaborador}")

    except oracledb.DatabaseError as e:
        print(f"Erro de banco de dados ao listar relatórios: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")


# --- CONSULTAS E EXPORTAÇÃO JSON ---

def consulta_humor_recente(conn):
    print("\n---  Humor Mais Recente por Colaborador ---")

    sql = '''
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
    '''

    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            resultados = cursor.fetchall()

            if not resultados:
                print("Nenhum dado encontrado para gerar o relatório.")
                return

            print(f"{'Nome':<30} | {'Humor':<15} | {'Data':<15} | {'Comentário'}")
            print("-" * 100)
            for r in resultados:
                data_formatada = r[3].strftime('%Y-%m-%d')
                print(f"{r[0]:<30} | {r[1]:<15} | {data_formatada:<15} | {r[2]}")

            prompt_exportar_json(cursor, resultados, "consulta_humor_recente")

    except oracledb.DatabaseError as e:
        print(f"Erro de banco de dados na consulta: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")


def consulta_media_geral_colaborador(conn):
    print("\n---  Média Geral de Humor (dos Relatórios)  ---")

    sql = '''
    SELECT C.NOME, ROUND(AVG(R.MEDIA_HUMOR),2) AS MEDIA_GERAL
    FROM TB_COLABORADOR C
    JOIN TB_RELATORIO R ON C.ID_COLABORADOR = R.ID_COLABORADOR
    GROUP BY C.NOME
    ORDER BY MEDIA_GERAL DESC
    '''

    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            resultados = cursor.fetchall()

            if not resultados:
                print("Nenhum relatório encontrado para calcular médias.")
                return

            print(f"{'Nome':<30} | {'Média de Humor (Relatórios)'}")
            print("-" * 60)
            for r in resultados:
                print(f"{r[0]:<30} | {r[1]:<12.2f}")

            prompt_exportar_json(cursor, resultados, "consulta_media_humor_relatorios")

    except oracledb.DatabaseError as e:
        print(f"Erro de banco de dados na consulta: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")


def consulta_colaboradores_risco(conn):
    print("\n---   Colaboradores em Risco (Média < 7)  ---")

    sql = '''
    SELECT C.NOME, ROUND(AVG(R.MEDIA_HUMOR),2) AS MEDIA_HUMOR
    FROM TB_COLABORADOR C
    JOIN TB_RELATORIO R ON C.ID_COLABORADOR = R.ID_COLABORADOR
    GROUP BY C.NOME
    HAVING AVG(R.MEDIA_HUMOR) < 7
    ORDER BY MEDIA_HUMOR ASC
    '''

    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            resultados = cursor.fetchall()

            if not resultados:
                print("Nenhum colaborador encontrado com média de humor abaixo de 7.")
                return

            print("Colaboradores que podem precisar de atenção:")
            print(f"{'Nome':<30} | {'Média de Humor (Relatórios)'}")
            print("-" * 60)
            for r in resultados:
                print(f"{r[0]:<30} | {r[1]:<12.2f}")

            prompt_exportar_json(cursor, resultados, "consulta_colaboradores_risco")

    except oracledb.DatabaseError as e:
        print(f"Erro de banco de dados na consulta: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")


# --- MENUS DE NAVEGAÇÃO ---

def menu_consultas(conn):
    while True:
        print("\n---  Menu de Consultas e Relatórios  ---")
        print("1. Ver Humor Mais Recente por Colaborador")
        print("2. Ver Média de Humor (dos Relatórios) por Colaborador")
        print("3. Ver Colaboradores em Risco (Média < 7)")
        print("4. Voltar ao Menu Principal")

        escolha = validar_int("\nEscolha uma opção: ", 1, 4)

        if escolha == 1:
            consulta_humor_recente(conn)
        elif escolha == 2:
            consulta_media_geral_colaborador(conn)
        elif escolha == 3:
            consulta_colaboradores_risco(conn)
        elif escolha == 4:
            break

        input("\nPressione Enter para continuar...")


def menu_gerenciar_colaboradores(conn):
    while True:
        print("\n----  Gerenciar Colaboradores  ----")
        print("1. Cadastrar Novo Colaborador")
        print("2. Listar Todos os Colaboradores")
        print("3. Atualizar Dados de Colaborador")
        print("4. Deletar Colaborador")
        print("5. Voltar ao Menu Principal")

        escolha = validar_int("\nEscolha uma opção: ", 1, 5)

        if escolha == 1:
            criar_colaborador(conn)
        elif escolha == 2:
            listar_colaboradores(conn)
        elif escolha == 3:
            atualizar_colaborador(conn)
        elif escolha == 4:
            deletar_colaborador(conn)
        elif escolha == 5:
            break

        input("\nPressione Enter para continuar...")


def menu_gerenciar_checkins(conn):
    while True:
        print("\n---- Gerenciar Check-ins de Humor  ----")
        print("1. Adicionar Novo Check-in ")
        print("2. Ver Histórico de Check-ins por Colaborador ")
        print("3. Voltar ao Menu Principal")

        escolha = validar_int("\nEscolha uma opção: ", 1, 3)

        if escolha == 1:
            criar_checkin(conn)
        elif escolha == 2:
            listar_checkins_por_colaborador(conn)
        elif escolha == 3:
            break

        input("\nPressione Enter para continuar...")


def menu_gerenciar_outros(conn):
    while True:
        print("\n---- Gerenciar Relatórios e Alertas  ----")
        print("1. Ver Histórico de Relatórios por Colaborador ")
        print("2. Criar Alerta Manual")
        print("3. Ver Histórico de Alertas por Colaborador")
        print("4. Voltar ao Menu Principal")

        escolha = validar_int("\nEscolha uma opção: ", 1, 4)

        if escolha == 1:
            listar_relatorios_por_colaborador(conn)
        elif escolha == 2:
            criar_alerta(conn)
        elif escolha == 3:
            listar_alertas_por_colaborador(conn)
        elif escolha == 4:
            break

        input("\nPressione Enter para continuar...")


def main_menu():
    print("=" * 50)
    print("   Plataforma de Monitoramento de Bem-Estar")
    print("                (Global Solution)")
    print("=" * 50)

    conn = get_connection()
    if not conn:
        print("\nFalha crítica na conexão com o banco de dados.")
        print("Verifique as configurações no início do script (USER, PASS, DSN).")
        input("Pressione Enter para sair...")
        return

    print("\nConexão com o Oracle Database estabelecida com sucesso!")

    while True:
        print("\n----  Menu Principal  ----")
        print("1. Gerenciar Colaboradores")
        print("2. Gerenciar Check-ins de Humor")
        print("3. Gerenciar Relatórios e Alertas")
        print("4. Consultas e Relatórios (com JSON)")
        print("5. Sair")

        escolha = validar_int("\nEscolha uma opção: ", 1, 5)

        if escolha == 1:
            menu_gerenciar_colaboradores(conn)
        elif escolha == 2:
            menu_gerenciar_checkins(conn)
        elif escolha == 3:
            menu_gerenciar_outros(conn)
        elif escolha == 4:
            menu_consultas(conn)
        elif escolha == 5:
            print("Encerrando a conexão...")
            conn.close()
            print("Programa finalizado.")
            break


if __name__ == "__main__":
    main_menu()
