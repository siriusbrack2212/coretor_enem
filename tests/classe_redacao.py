
import sqlite3
import os
import datetime
arquivo = 'tb_redacoes.xlsx'
id_redacao = None
data_avaliacao = None

dados_redacao = {
        "TITULO": None,                 # Título digitado pelo usuário (opcional)
        "TEMA": None,                   # Tema da redação (extraído do site ou input)
        "DATA": data_avaliacao,         # Data e hora da avaliação
        "TEXTO_REDACAO": None,          # O texto completo da redação
        "FEEDBACK_GERAL": None,         # Feedback consolidado de todas as fontes

        # --- Notas do Corretor CRIA ---
        "NOTA_TOTAL_CRIA": None,
        "C1_CRIA": None, "C2_CRIA": None, "C3_CRIA": None, "C4_CRIA": None, "C5_CRIA": None,

    
        # --- NOVOS CAMPOS: Notas do Corretor CORREDAÇÃO ---
        "NOTA_TOTAL_CORREDACAO": None,
        "C1_CORREDACAO": None, "C2_CORREDACAO": None, "C3_CORREDACAO": None, "C4_CORREDACAO": None, "C5_CORREDACAO": None,

        # --- NOVOS CAMPOS: Notas do Corretor TODAMATERIA ---
        "NOTA_TOTAL_TODAMATERIA": None,
        "C1_TODAMATERIA": None, "C2_TODAMATERIA": None, "C3_TODAMATERIA": None, "C4_TODAMATERIA": None, "C5_TODAMATERIA": None,
        
        # Você pode adicionar mais campos se houver outras métricas específicas
    }


def atualizar_campo_redacao(dados_redacao: dict, campo: str, valor):
    
    if campo in dados_redacao:
        dados_redacao[campo] = valor
        # Opcional: print para depuração, pode ser removido em produção
        # print(f"Campo '{campo}' atualizado para '{valor}' no dicionário de redação.")
    else:
        print(f"Aviso: Campo '{campo}' não existe no dicionário de redação. Valor não adicionado.")


def salvar_redacao_banco(dados_redacao:dict):
    banco_existe = os.path.exists("redacoes_historico.db")
    
    if not banco_existe:
        conn = sqlite3.connect("redacoes_historico.db")
        cursor= conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS redacoes (
            ID INTEGER PRIMARY KEY, -- ID gerado automaticamente
            TITULO TEXT,
            TEMA TEXT,
            DATA TEXT,
            TEXTO_REDACAO TEXT,
            FEEDBACK_GERAL TEXT,
            NOTA_TOTAL_CRIA INTEGER, C1_CRIA INTEGER, C2_CRIA INTEGER, C3_CRIA INTEGER, C4_CRIA INTEGER, C5_CRIA INTEGER,
            NOTA_TOTAL_CORREDACAO INTEGER, C1_CORREDACAO INTEGER, C2_CORREDACAO INTEGER, C3_CORREDACAO INTEGER, C4_CORREDACAO INTEGER, C5_CORREDACAO INTEGER,
            NOTA_TOTAL_TODAMATERIA INTEGER, C1_TODAMATERIA INTEGER, C2_TODAMATERIA INTEGER, C3_TODAMATERIA INTEGER, C4_TODAMATERIA INTEGER, C5_TODAMATERIA INTEGER
        );
        """)    
    else:
        conn = sqlite3.connect("redacoes_historico.db")
        cursor= conn.cursor()

    colunas  = ','.join(dados_redacao.keys())
    placeholders = ', '.join(['?'] * len(dados_redacao))
    sql_de_insercao = f"INSERT INTO redacoes({colunas}) VALUES ({placeholders})"

    cursor.execute(sql_de_insercao,tuple(dados_redacao.values()))

    conn.commit()
    conn.close()
    print("redaçao preechida")