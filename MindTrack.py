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