from playwright.sync_api import Page, expect
from classe_redacao import atualizar_campo_redacao, dados_redacao
import time

def automacao_coredacao(page:Page,texto,titulo=None)->dict:
    page.goto("https://aluno.coredacao.com/escrever?tema=tema-livre")
    if titulo is not None and titulo.strip():
        page.locator('input[placeholder="Título (Opcional)"]').fill(titulo)
    else:
        pass

    page.locator('div[role="textbox"]').fill(texto)
    botao_corigir = page.locator('button:has-text("Corrigir")')
    botao_corigir.click(timeout=10000)
    page.get_by_text("Sim, corrigir").click(timeout=10000)
    page.wait_for_selector('text=Nota geral',timeout=70000000)
      
    for i in range(1, 6):
        page.wait_for_selector(f'div:has-text("Competência {i}")')

    nota_geral = page.locator('text=Nota geral').locator('..').locator('h3').first.text_content()
    # As funções `atualizar_campo_redacao` e `dados_redacao`
    # devem ser acessíveis neste escopo.
    # Assumindo que elas são importadas de `classe_redacao`.
    # Adicionando imports para simulação, se necessários
    atualizar_campo_redacao(dados_redacao, "NOTA_TOTAL_CORREDACAO", int(nota_geral.strip()))

    for i in range(1, 6):
        # Correção no seletor para pegar a nota correta de cada competência
        nota_competencia_locator = page.locator(f'div.v-card:has-text("Competência {i}")').locator('div.ml-auto.py-2.md\\:\\!py-3 h4').first
        nota = nota_competencia_locator.text_content()
        campo = f"C{i}_CORREDACAO"
        atualizar_campo_redacao(dados_redacao, campo, int(nota.strip()))
        print(dados_redacao)
    time.sleep(15)
    return {"status": "success", "message": "Automação Corredaço concluída"}