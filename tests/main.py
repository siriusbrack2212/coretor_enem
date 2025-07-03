# c:/Users/Nicolas/Desktop/playwright_project/tests/main.py

from playwright.sync_api import Page # Para type hinting
import time
from classe_redacao import dados_redacao,salvar_redacao_excel
import pandas as pd
# CORREÇÃO: Importação da classe e função de verificação.
# Assumindo que 'gerenciador_perfil.py' está na pasta raiz do projeto,
# e 'main.py' está em 'tests/'.
from gerenciador_perfil import PlaywrightBrowser, verificar_chrome_fechado_manual 

# CORREÇÃO: Importação da função de automação específica do site 'cria_codigo.py'
# Assumindo que 'cria_codigo.py' está no mesmo diretório 'tests/'.
from cria_codigo import automacao_cria
from coredacao import automacao_coredacao
from toda_materia_codigo import automacao_toda_materia
# --- Bloco de execução principal ---
if __name__ == "__main__":
    # 1. Chamar a função de verificação (agora com parênteses!)
    verificar_chrome_fechado_manual()

    # 2. Obter a instância do gerenciador de navegador (Singleton)
    browser_manager = PlaywrightBrowser()
    page = None # Inicializa 'page' como None, para ser seguro no 'finally'

    try:
        # 3. Iniciar o navegador e obter a página principal
        # Lembre-se: copy_profile=True APENAS NA PRIMEIRA EXECUÇÃO
        # para copiar dados do seu perfil real. Depois, mude para False.
        print("\nIniciando navegador através do browser_manager...")
        page = browser_manager.launch(headless=False, copy_profile=False) 
        
        print("\nNavegador pronto para automações!")

        # 4. Chamar a função de automação do Cria.net.br, passando a 'page' real
        resultado_cria = automacao_cria(page)
        print("\nResultado da automação Cria.net.br:", resultado_cria)

        


        resultado_coredacao = automacao_coredacao(page=page,texto=dados_redacao['TEXTO_REDACAO'],titulo=dados_redacao['TITULO'])

        #resultado_toda_materia = automacao_toda_materia(page=page,texto=dados_redacao['TEXTO_REDACAO'],tema=dados_redacao['TEMA'],titulo=dados_redacao['TITULO'])

        salvar_redacao_excel(dados_redacao=dados_redacao,modo="sobreescrever")
        

        # --- AQUI VOCÊ PODE CHAMAR OUTRAS FUNÇÕES DE AUTOMAÇÃO ---
        # Exemplo:
        # from automacao_site_toda_materia import automacao_toda_materia
        # tema_redacao = "A importância da tecnologia"
        # conteudo_redacao = "..."
        # resultado_toda = automacao_toda_materia(page, tema_redacao, conteudo_redacao)
        # print("\nResultado Toda Matéria:", resultado_toda)

        # Se precisar de uma nova aba:
        # new_tab_page = browser_manager.new_page()
        # new_tab_page.goto("https://www.google.com")
        # print(f"Nova aba aberta para: {new_tab_page.url}")
        # time.sleep(3)
        # new_tab_page.close()


    except Exception as e:
        print(f"\nUm erro ocorreu durante a execução do script principal: {e}")
        if page: # Se a página foi criada, tenta tirar um screenshot
            try:
                page.screenshot(path="fatal_error_main_script.png")
            except: pass
    finally:
        # 5. Fechar o navegador no final de TUDO
        if browser_manager: # Garante que o objeto existe
            browser_manager.close()
            print("\nAutomações concluídas e navegador fechado.")