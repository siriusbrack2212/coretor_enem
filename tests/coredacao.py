
from playwright.sync_api import Page, expect # Importa Page para type hinting e expect para asserções
from classe_redacao import atualizar_campo_redacao,dados_redacao,contador
import time


def automacao_coredacao(page:Page,texto=dados_redacao['TEXTO_REDACAO'],titulo=dados_redacao['TITULO'])->dict:
    page.goto("https://aluno.coredacao.com/escrever?tema=tema-livre")
    if titulo != None:
        page.locator('input[placeholder="Título (Opcional)"]').fill(titulo)
    else:
        pass

    page.locator('div[role="textbox"]').fill(texto)
    botao_corigir = page.locator('button:has-text("Corrigir")')
    botao_corigir.click(timeout=10000)
    page.get_by_text("Sim, corrigir").click(timeout=10000)
    page.wait_for_selector('text= Nota geral',timeout=70000000)
     
    for i in range(1, 6):
         page.wait_for_selector(f'div:has-text("Competência {i}")')

    nota_geral =  page.locator('text=Nota geral').locator('..').locator('h3').first.text_content()
    atualizar_campo_redacao(dados_redacao, "NOTA_TOTAL_CORREDACAO", int(nota_geral.strip()))
    for i in range(1, 6):
        nota =  page.locator(f'div:has-text("Competência {i}")').locator('h4').first.text_content()
        campo = f"C{i}_CORREDACAO"
        atualizar_campo_redacao(dados_redacao, campo, int(nota.strip()))
        print(dados_redacao)
    time.sleep(15)
    