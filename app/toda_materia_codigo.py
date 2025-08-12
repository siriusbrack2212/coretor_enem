from playwright.sync_api import Page, expect
import time
import re

# Assume que atualizar_campo_redacao e dados_redacao são importados de classe_redacao
# from classe_redacao import atualizar_campo_redacao, dados_redacao

def _extrair_notas_toda_materia(page: Page) -> dict:
    notas_coletadas = {'NOTA_TOTAL': None, 'C1': None, 'C2': None, 'C3': None, 'C4': None, 'C5': None}
    
    try:
        page.locator('div.corrector-results-tab-general').wait_for(state="visible", timeout=60000)
    except Exception as e:
        return notas_coletadas

    try:
        nota_geral_locator = page.locator('div.corrector-results-tab-general').locator('span.corrector-results-tab-general-value')
        if nota_geral_locator.is_visible():
            nota_geral_text = nota_geral_locator.text_content().strip()
            match = re.search(r'(\d+)', nota_geral_text)
            if match:
                notas_coletadas['NOTA_TOTAL'] = int(match.group(1))
    except Exception as e:
        pass # Erro de extração de nota geral

    try:
        page.locator('div.corrector-results-tab-competencies').wait_for(state="visible", timeout=10000)
    except Exception as e:
        pass # Container de Competências não visível

    for i in range(1, 6):
        competencia_label = f"Competência {i}"
        
        try:
            competencia_container_locator = page.locator(f'div.corrector-results-tab-competencies-item:has-text("{competencia_label}")')
            nota_competencia_locator = competencia_container_locator.locator('span.corrector-results-tab-competencies-item-results-value')
            
            nota_competencia_locator.wait_for(state="visible", timeout=5000)
            
            nota_texto = nota_competencia_locator.text_content().strip()
            
            if nota_texto.isdigit():
                notas_coletadas[f'C{i}'] = int(nota_texto)
            else:
                pass # Nota não numérica
        except Exception as e:
            pass # Erro ao extrair competência

    return notas_coletadas

def automacao_toda_materia(page: Page, texto: str, tema: str, titulo: str | None = None) -> dict:
    try:
        page.goto("https://www.todamateria.com.br/corretor-de-redacao/", wait_until="networkidle")
        time.sleep(5)

        if tema:
            page.wait_for_selector("input.tm-input-group-input.tm-input-group-input_title", timeout=10000)
            page.fill("input.tm-input-group-input.tm-input-group-input_title", tema)

        if titulo:
            page.fill("input[placeholder='Escreva um título (opcional)']", titulo)

        page.wait_for_selector("#redactionInput", timeout=10000)
        page.fill("#redactionInput", texto)

        botao_correcao = page.locator("button.landing-page-bottom-button")
        botao_correcao.wait_for(state="visible", timeout=10000)
        botao_correcao.scroll_into_view_if_needed()
        time.sleep(1)
        botao_correcao.click()

        time.sleep(15) # Aguardar processamento da correção

        notas_do_site = _extrair_notas_toda_materia(page)

        if notas_do_site:
            # As funções `atualizar_campo_redacao` e `dados_redacao`
            # devem ser acessíveis neste escopo.
            from classe_redacao import atualizar_campo_redacao, dados_redacao 
            
            atualizar_campo_redacao(dados_redacao, "NOTA_TOTAL_TODAMATERIA", notas_do_site.get('NOTA_TOTAL'))
            atualizar_campo_redacao(dados_redacao, "C1_TODAMATERIA", notas_do_site.get('C1'))
            atualizar_campo_redacao(dados_redacao, "C2_TODAMATERIA", notas_do_site.get('C2'))
            atualizar_campo_redacao(dados_redacao, "C3_TODAMATERIA", notas_do_site.get('C3'))
            atualizar_campo_redacao(dados_redacao, "C4_TODAMATERIA", notas_do_site.get('C4'))
            atualizar_campo_redacao(dados_redacao, "C5_TODAMATERIA", notas_do_site.get('C5'))
        
        return {"status": "success", "message": "Automação Toda Matéria concluída"}

    except Exception as e:
        return {"status": "error", "message": f"Erro na automação: {e}"}