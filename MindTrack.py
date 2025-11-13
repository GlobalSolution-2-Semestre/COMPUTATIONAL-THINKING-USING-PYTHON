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
