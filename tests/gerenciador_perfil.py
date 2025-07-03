from playwright.sync_api import sync_playwright, BrowserContext, Page
import os
import platform
import time
import shutil

class PlaywrightBrowser:
    _instance = None # Para implementar o padrão Singleton (uma única instância)
    _playwright_context: BrowserContext = None
    _playwright_page: Page = None
    _playwright_instance = None # Armazena a instância do sync_playwright

    def __new__(cls):
        # Implementa o padrão Singleton
        if cls._instance is None:
            cls._instance = super(PlaywrightBrowser, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'): # Garante que __init__ só rode uma vez
            self._initialized = True
            self._playwright_instance = None # Será inicializado em .launch()
            print("PlaywrightBrowser inicializado. Chame .launch() para abrir o navegador.")

    def _get_profile_paths(self):
        sistema = platform.system()
        home_dir = os.path.expanduser("~")
        
        playwright_user_data_dir = os.path.join(home_dir, "PlaywrightAutomationProfile")
        
        chrome_original_user_data_root = ""
        profile_name_to_use = "Default" # <<< AJUSTE AQUI SE VOCÊ TEM UM PERFIL DEDICADO!

        if sistema == "Windows":
            chrome_original_user_data_root = os.path.join(home_dir, r"AppData\Local\Google\Chrome\User Data")
        elif sistema == "Darwin":
            chrome_original_user_data_root = os.path.join(home_dir, "Library/Application Support/Google/Chrome")
        elif sistema == "Linux":
            chrome_original_user_data_root = os.path.join(home_dir, ".config/google-chrome")
        else:
            raise Exception(f"Sistema operacional {sistema} não suportado.")
        
        chrome_original_profile_dir = os.path.join(chrome_original_user_data_root, profile_name_to_use)
        os.makedirs(playwright_user_data_dir, exist_ok=True)
        os.makedirs(os.path.join(playwright_user_data_dir, profile_name_to_use), exist_ok=True)
        
        return playwright_user_data_dir, chrome_original_profile_dir, profile_name_to_use

    def _copy_profile_data(self, playwright_data_dir, original_chrome_profile_dir, profile_name):
        dest_profile_path_inside_playwright_dir = os.path.join(playwright_data_dir, profile_name)
        os.makedirs(dest_profile_path_inside_playwright_dir, exist_ok=True)
        
        files_to_copy = ["Cookies", "Login Data", "Web Data", "Local Storage/leveldb"]

        print("Copiando dados do perfil...")
        for filename in files_to_copy:
            src_path = os.path.join(original_chrome_profile_dir, filename)
            dest_path = os.path.join(dest_profile_path_inside_playwright_dir, filename)
            
            if os.path.isdir(src_path):
                if os.path.exists(dest_path):
                    shutil.rmtree(dest_path)
                try:
                    shutil.copytree(src_path, dest_path)
                except shutil.Error as e:
                    print(f"Aviso ao copiar pasta '{filename}': {e}")
            elif os.path.exists(src_path):
                try:
                    shutil.copy2(src_path, dest_path)
                except shutil.Error as e:
                    print(f"Aviso ao copiar arquivo '{filename}': {e}")
            
    def launch(self, headless=False, copy_profile=False):
        """Inicia o navegador e configura a página principal."""
        self._playwright_instance = sync_playwright().start()
        
        playwright_user_data_dir, chrome_original_profile_dir, profile_name = self._get_profile_paths()

        if copy_profile:
            self._copy_profile_data(playwright_user_data_dir, chrome_original_profile_dir, profile_name)

        self._playwright_context = self._playwright_instance.chromium.launch_persistent_context(
            user_data_dir=playwright_user_data_dir,
            headless=headless,
            channel="chrome",
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized",
                "--disable-dev-shm-usage",
                "--no-sandbox"
            ]
        )
        self._playwright_page = self._playwright_context.new_page()
        self._playwright_page.set_viewport_size({"width": 1920, "height": 1080})

        print("Verificando login Google...")
        self._playwright_page.goto("https://accounts.google.com", wait_until="networkidle")
        time.sleep(2)
        
        if "myaccount.google.com" not in self._playwright_page.url and "accounts.google.com" in self._playwright_page.url:
            print("Não está logado no Google. Faça login manualmente.")
            self._playwright_page.screenshot(path="login_google_required_on_launch.png")
            input("Pressione Enter após fazer login manual no Google...")
        else:
            print("Já está logado no Google.")
        
        return self._playwright_page

    def get_page(self):
        """Retorna a página principal do navegador."""
        if not self._playwright_page:
            raise Exception("Navegador não iniciado. Chame .launch() primeiro.")
        return self._playwright_page

    def new_page(self):
        """Cria e retorna uma nova aba no navegador."""
        if not self._playwright_context:
            raise Exception("Contexto do navegador não iniciado. Chame .launch() primeiro.")
        new_page_instance = self._playwright_context.new_page()
        new_page_instance.set_viewport_size({"width": 1920, "height": 1080})
        return new_page_instance

    def close(self):
        """Fecha o contexto do navegador e a instância do Playwright."""
        if self._playwright_context:
            self._playwright_context.close()
            print("Navegador e contexto fechados.")
        if self._playwright_instance:
            self._playwright_instance.stop() # Garante que o Playwright termine o processo
            print("Instância do Playwright parada.")
        PlaywrightBrowser._instance = None # Reseta o singleton
        self._playwright_context = None
        self._playwright_page = None
        self._playwright_instance = None
        self._initialized = False

# --- Função auxiliar para verificar Chrome rodando ---
def verificar_chrome_fechado_manual():
    print("\n================================================")
    print("⚠️  ATENÇÃO: FECHE TODAS AS INSTÂNCIAS DO CHROME MANUALMENTE ANTES DE EXECUTAR.")
    print("            Isso evita conflitos de perfil.")
    print("================================================\n")
    input("Pressione Enter APÓS fechar todas as janelas do Chrome e verificar no Gerenciador de Tarefas...")

# --- Teste da classe (apenas para verificar se a classe funciona sozinha) ---
if __name__ == "__main__":
    verificar_chrome_fechado_manual()
    
    browser = PlaywrightBrowser()
    page = None
    try:
        # Inicia o navegador (headless=False para ver)
        # copy_profile=True para copiar os dados do seu perfil padrão para o perfil de automação
        # Faça copy_profile=True APENAS na primeira execução ou quando precisar atualizar os logins.
        # Depois, pode usar copy_profile=False para economizar tempo.
        page = browser.launch(headless=False, copy_profile=True)
        
        print("\nNavegador iniciado. Testando navegação...")
        page.goto("https://www.google.com")
        page.wait_for_load_state("networkidle")
        print(f"Página atual: {page.url}")

        print("\nAbrindo nova aba...")
        new_page = browser.new_page()
        new_page.goto("https://www.bing.com")
        new_page.wait_for_load_state("networkidle")
        print(f"Nova página: {new_page.url}")
        time.sleep(5) # Para visualizar

        new_page.close()
        print("Nova aba fechada.")
        
    except Exception as e:
        print(f"Erro durante o teste da classe: {e}")
        if page:
            try:
                page.screenshot(path="test_error.png")
            except: pass
    finally:
        # Garante que o navegador seja fechado, a menos que o usuário queira mantê-lo aberto
        if browser._playwright_context:
            resposta = input("\nDeseja manter o navegador aberto para verificação? (s/n): ")
            if resposta.lower() not in ['s', 'sim', 'y', 'yes']:
                browser.close()
            else:
                print("Navegador mantido aberto. Feche manualmente ao terminar.")