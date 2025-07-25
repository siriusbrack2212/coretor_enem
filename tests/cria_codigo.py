# c:/Users/Nicolas/Desktop/playwright_project/tests/cria_codigo.py

from playwright.sync_api import Page, expect # Importa Page para type hinting e expect para asserções
import time
from classe_redacao import atualizar_campo_redacao,dados_redacao
import pandas as pd
from datetime import date



titulo = str
tema_texto = str
texto_redacao = str

def automacao_cria(page: Page) -> dict:
    


    """
    Realiza a automação específica para o site Cria.net.br.
    Recebe uma instância 'page' já inicializada e logada.
    """
    print(f"\n--- Iniciando Automação para Cria.net.br ---")
    print(f"Navegando para: https://web.cria.net.br/?pagina=1")
    page.goto("https://web.cria.net.br/escolha-tema-redacao", wait_until="load") 
    tema_redacao = page.locator('div.css-1nwihwa').locator('p.css-d29un8')
    tema_texto = None

    tema_redacao.wait_for(state="visible",timeout=(6000000))
    tema_texto = tema_redacao.text_content()


    if tema_texto and tema_texto.strip(): 
        print(f"Tema da redação: '{tema_texto}'")
        hoje = date.today()
        atualizar_campo_redacao(dados_redacao, 'DATA',hoje.strftime('%d/%m/%Y'))
        atualizar_campo_redacao(dados_redacao, 'TEMA',tema_texto)
        
        
        

    else:
        print("O elemento do tema está visível, mas o texto está vazio.")
        tema_texto = None # Redefine para None se estiver vazio

    print("\n--- Etapa de Escrita da Redação ---")
    print("O usuário agora pode escrever o título e a redação nos campos do site.")
    print("Por favor, digite 'sim' (ou 's') no console quando terminar de escrever sua redação e título.")

    resposta_usuario = ""
    while resposta_usuario.lower() not in ['sim', 's']:
        resposta_usuario = input("Você terminou de escrever sua redação e corigiu sua readaçao serio tem que ta corigida ? (sim/s): ").strip()

    campo_titulo = page.locator('#tituloRedacao')
    campo_titulo.wait_for(state='visible',timeout=50000)
    titulo = campo_titulo.input_value()


    if titulo and titulo.strip():
        print(f"titulo: '{tema_texto}'")
        titulo = campo_titulo.input_value()
        atualizar_campo_redacao(dados_redacao,'TITULO',titulo)

    else:
        titulo = ""

    textoarea = page.locator('#textArea')

    textoarea.wait_for(state= 'visible',timeout=100000)
    texto_redacao = None
    texto_redacao = textoarea.input_value()


    if texto_redacao and texto_redacao.strip():
       texto_redacao = textoarea.input_value() 
       atualizar_campo_redacao(dados_redacao,"TEXTO_REDACAO",texto_redacao)
    else:
        print('cade o texto')
        texto_redacao = None

    # Captura a nota total (como número inteiro)
    nota_total = int(page.locator('p.css-11eepfb').first.inner_text().replace('pts', '').strip())
    atualizar_campo_redacao(dados_redacao, 'NOTA_TOTAL_CRIA', nota_total)

# Captura as notas das competências (C1 a C5) como inteiros
    notas_competencias = page.locator('p.css-11eepfb').all()

    for i, nota in enumerate(notas_competencias[1:6], start=1):  # pula a nota total
        valor = int(nota.inner_text().replace('pts', '').strip())
        campo = f'C{i}_CRIA'
        atualizar_campo_redacao(dados_redacao, campo, valor)
        

    time.sleep(9) # Para visualização, remova em produção ou use esperas mais inteligentes
    
    return {"status": "success", "message": "Navegação para Cria.net.br concluída"}

