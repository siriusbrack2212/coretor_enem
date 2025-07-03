from playwright.sync_api import Page
import time
from playwright.sync_api import Page, expect # Importa Page para type hinting e expect para asserções
from classe_redacao import atualizar_campo_redacao,dados_redacao,contador
import time
def automacao_toda_materia(page: Page, texto=dados_redacao['TEXTO_REDACAO'], tema=dados_redacao['TEMA'], titulo=dados_redacao['TITULO']) -> dict:
    """
    Automatiza o processo de correção de redação no site Toda Matéria.
    
    Args:
        page (Page): Instância da página do Playwright
        texto (str): Texto da redação a ser corrigida
        tema (str): Tema da redação
        titulo (str): Título da redação (opcional)
    
    Returns:
        dict: Dados atualizados da redação com as notas
    """
    
    try:
        # Navegar para a página do corretor
        print("Acessando Toda Matéria...")
        page.goto("https://www.todamateria.com.br/corretor-de-redacao/", wait_until="networkidle")
        time.sleep(5)

        # Selecionar o tema
        print("Selecionando o tema...")
        try:
            page.wait_for_selector("#tema-selecao", timeout=15000)
            page.select_option("#tema-selecao", label="Redação de Tema Livre")
            print("Tema 'Redação de Tema Livre' selecionado.")
        except Exception as e:
            print(f"Erro ao selecionar tema: {e}")

        # Preencher o campo do tema
        if tema:
            print(f"Preenchendo tema: {tema}")
            try:
                page.wait_for_selector("input.tm-input-group-input.tm-input-group-input_title", timeout=10000)
                page.fill("input.tm-input-group-input.tm-input-group-input_title", tema)
            except Exception as e:
                print(f"Erro ao preencher tema: {e}")

        # Preencher o campo do título (opcional)
        if titulo:
            print(f"Preenchendo título: {titulo}")
            try:
                page.fill("input[placeholder='Escreva um título (opcional)']", titulo)
            except Exception as e:
                print(f"Erro ao preencher título: {e}")

        # Preencher o campo do conteúdo da redação
        print("Preenchendo conteúdo...")
        try:
            page.wait_for_selector("#redactionInput", timeout=10000)
            page.fill("#redactionInput", texto)
            print("Conteúdo preenchido com sucesso.")
        except Exception as e:
            print(f"Erro ao preencher conteúdo: {e}")
            return dados_redacao

        # Clicar no botão de correção
        print("Clicando no botão de correção...")
        try:
            botao_correcao = page.locator("button.landing-page-bottom-button")
            botao_correcao.wait_for(state="visible", timeout=10000)
            botao_correcao.scroll_into_view_if_needed()
            time.sleep(1)
            botao_correcao.click()
            print("Botão de correção clicado.")
        except Exception as e:
            print(f"Erro ao clicar no botão: {e}")
            return dados_redacao

        # Aguardar processamento da correção
        print("Aguardando processamento da correção...")
        time.sleep(15)

        # Tentar capturar as notas específicas
        print("Tentando capturar notas...")
        try:
            # Aguardar elementos de resultado aparecerem
            page.wait_for_selector(".correction-result, .result-container, .tm-correction-result, [class*='result'], [class*='correction']", timeout=60000)
            
            # Extrair nota geral
            try:
                # Procurar por elementos que contenham a nota geral
                nota_geral_element = page.locator("text=/Nota.*:.*\\d+/").first
                if nota_geral_element.is_visible():
                    nota_geral_text = nota_geral_element.text_content()
                    # Extrair número da nota (assumindo formato "Nota: X" ou "Nota geral: X")
                    import re
                    match = re.search(r'(\d+)', nota_geral_text)
                    if match:
                        nota_geral = int(match.group(1))
                        atualizar_campo_redacao(dados_redacao, "NOTA_TOTAL_TODAMATERIA", nota_geral)
                        print(f"Nota geral capturada: {nota_geral}")
            except Exception as e:
                print(f"Erro ao capturar nota geral: {e}")

            # Extrair notas das competências
            for i in range(1, 6):
                try:
                    # Procurar por elementos que contenham as competências
                    competencia_selector = f"text=/Competência.*{i}.*:.*\\d+/"
                    comp_element = page.locator(competencia_selector).first
                    
                    if comp_element.is_visible():
                        comp_text = comp_element.text_content()
                        # Extrair número da competência
                        import re
                        match = re.search(r'(\d+)', comp_text)
                        if match:
                            nota_comp = int(match.group(1))
                            campo = f"C{i}_TODAMATERIA"
                            atualizar_campo_redacao(dados_redacao, campo, nota_comp)
                            print(f"Competência {i} capturada: {nota_comp}")
                except Exception as e:
                    print(f"Erro ao capturar competência {i}: {e}")

            # Se não conseguir capturar notas específicas, tentar método alternativo
            if dados_redacao["NOTA_TOTAL_TODAMATERIA"] is None:
                print("Tentando método alternativo para capturar notas...")
                try:
                    # Capturar todo o texto da área de resultados
                    resultados_text = page.evaluate("""
                        () => {
                            const possiveisElementos = [
                                '.correction-result',
                                '.result-container', 
                                '.tm-correction-result',
                                '[class*="result"]',
                                '[class*="correction"]'
                            ];
                            
                            for (let seletor of possiveisElementos) {
                                const elemento = document.querySelector(seletor);
                                if (elemento && elemento.innerText.trim()) {
                                    return elemento.innerText;
                                }
                            }
                            
                            return document.body.innerText;
                        }
                    """)
                    
                    # Usar regex para extrair notas do texto
                    import re
                    
                    # Procurar por nota geral
                    nota_geral_match = re.search(r'nota.*geral.*?(\d+)', resultados_text, re.IGNORECASE)
                    if nota_geral_match:
                        nota_geral = int(nota_geral_match.group(1))
                        atualizar_campo_redacao(dados_redacao, "NOTA_TOTAL_TODAMATERIA", nota_geral)
                    
                    # Procurar por competências
                    for i in range(1, 6):
                        comp_match = re.search(rf'competência.*{i}.*?(\d+)', resultados_text, re.IGNORECASE)
                        if comp_match:
                            nota_comp = int(comp_match.group(1))
                            campo = f"C{i}_TODAMATERIA"
                            atualizar_campo_redacao(dados_redacao, campo, nota_comp)
                    
                    print("Método alternativo aplicado.")
                    
                except Exception as e:
                    print(f"Erro no método alternativo: {e}")

            print("Processo de captura de notas concluído.")
            
        except Exception as e:
            print(f"Erro ao capturar resultados: {e}")

        # Aguardar para visualização (opcional)
        time.sleep(10)
        
        return dados_redacao

    except Exception as e:
        print(f"Erro geral na automação Toda Matéria: {e}")
        try:
            page.screenshot(path="error_toda_materia.png")
            print("Screenshot de erro salvo como error_toda_materia.png")
        except:
            pass
        return dados_redacao


# Exemplo de uso

