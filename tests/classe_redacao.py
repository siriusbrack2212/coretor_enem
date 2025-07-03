import pandas as pd
import os
contador = 0
arquivo = 'tb_redacoes.xlsx'
id_redacao = None
data_avaliacao = None

dados_redacao = {
        "ID": id_redacao,
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



def salvar_redacao_excel(dados_redacao, nome_arquivo="tb_redacoes.xlsx", modo="auto"):
    """
    Salva dados de redação em uma planilha Excel.
    
    Args:
        dados_redacao (dict): Dicionário com os dados da redação
        nome_arquivo (str): Nome do arquivo Excel (padrão: "essays.xlsx")
        modo (str): Como lidar com campos diferentes:
                   - "auto": Adiciona campos automaticamente (padrão)
                   - "sobrescrever": Sobrescreve o arquivo com nova estrutura
                   - "manter_existente": Mantém apenas campos que já existem
    
    Returns:
        bool: True se salvou com sucesso, False caso contrário
    """
    try:
        # Converte o dicionário em DataFrame
        df_nova_redacao = pd.DataFrame([dados_redacao])
        
        # Verifica se o arquivo já existe
        if os.path.exists(nome_arquivo):
            try:
                # Tenta carregar o arquivo existente
                df_existente = pd.read_excel(nome_arquivo)
                
                # Verifica se há diferenças nos campos
                campos_existentes = set(df_existente.columns)
                campos_novos = set(dados_redacao.keys())
                
                # Campos que só existem no arquivo atual
                campos_so_existentes = campos_existentes - campos_novos
                # Campos que só existem nos novos dados
                campos_so_novos = campos_novos - campos_existentes
                
                if campos_so_existentes or campos_so_novos:
                    print(f"\n  DIFERENÇAS DETECTADAS NOS CAMPOS:")
                    if campos_so_existentes:
                        print(f"   Campos apenas no arquivo existente: {list(campos_so_existentes)}")
                    if campos_so_novos:
                        print(f"   Campos apenas nos novos dados: {list(campos_so_novos)}")
                
                # Lida com as diferenças baseado no modo escolhido
                if modo == "auto":
                    # Adiciona campos faltantes com valores None
                    for campo in campos_so_existentes:
                        if campo not in df_nova_redacao.columns:
                            df_nova_redacao[campo] = None
                    
                    for campo in campos_so_novos:
                        if campo not in df_existente.columns:
                            df_existente[campo] = None
                    
                    # Reorganiza as colunas para manter consistência
                    todas_colunas = list(campos_existentes.union(campos_novos))
                    df_existente = df_existente.reindex(columns=todas_colunas)
                    df_nova_redacao = df_nova_redacao.reindex(columns=todas_colunas)
                    
                    df_final = pd.concat([df_existente, df_nova_redacao], ignore_index=True)
                    print(f"   ✅ Campos adicionados automaticamente")
                
                elif modo == "sobrescrever":
                    df_final = df_nova_redacao
                    print(f"   ⚠️  Arquivo sobrescrito com nova estrutura")
                
                elif modo == "manter_existente":
                    # Mantém apenas campos que já existem no arquivo
                    campos_comuns = campos_existentes.intersection(campos_novos)
                    df_nova_redacao_filtrada = df_nova_redacao[list(campos_comuns)]
                    df_final = pd.concat([df_existente, df_nova_redacao_filtrada], ignore_index=True)
                    print(f"   ℹ  Mantidos apenas campos existentes: {list(campos_comuns)}")
                    if campos_so_novos:
                        print(f"   ⚠️  Campos ignorados: {list(campos_so_novos)}")
                
            except Exception as e:
                print(f"⚠️  Erro ao ler arquivo existente: {str(e)}")
                print("   Criando novo arquivo...")
                df_final = df_nova_redacao
        else:
            # Se não existe, usa apenas a nova redação
            df_final = df_nova_redacao
            print(f"   📁 Criando novo arquivo '{nome_arquivo}'")
        
        # Salva no Excel com configurações para quebra de linha
        with pd.ExcelWriter(nome_arquivo, engine='openpyxl') as writer:
            df_final.to_excel(writer, index=False, sheet_name='Redações')
            
            # Acessa a planilha para configurar quebra de linha
            worksheet = writer.sheets['Redações']
            
            # Configura quebra de linha para todas as células
            for row in worksheet.iter_rows():
                for cell in row:
                    cell.alignment = cell.alignment.copy(wrap_text=True)
            
            # Ajusta a largura das colunas (opcional)
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                
                # Define largura máxima para evitar colunas muito largas
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
            
            # Configura altura das linhas para acomodar quebras de linha
            for row in worksheet.iter_rows():
                worksheet.row_dimensions[row[0].row].height = None  # Auto altura
        
        print(f"Redação salva com sucesso em '{nome_arquivo}'!")
        return True
        
    except Exception as e:
        print(f"Erro ao salvar redação: {str(e)}")
        return False
