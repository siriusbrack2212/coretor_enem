\# 📚 Corretor ENEM: Automação de Correção de Redações



\## ✨ Visão Geral do Projeto



O \*\*Corretor ENEM\*\* é uma ferramenta de automação desenvolvida em Python que simplifica o processo de avaliação de redações. Ele permite que o usuário escreva uma redação e, em seguida, envia automaticamente esse texto para múltiplos corretores online (sites e IAs) para avaliação. O grande diferencial é a capacidade de consolidar todas as notas e feedbacks recebidos em um histórico pessoal detalhado, facilitando o acompanhamento do progresso e a identificação de pontos de melhoria.



Este projeto visa otimizar o tempo de estudantes e educadores, centralizando o feedback de diversas plataformas de correção e oferecendo uma visão abrangente do desempenho em redações.



\## 🚀 Funcionalidades Principais



\-   \*\*Envio Automatizado:\*\* Envia redações para múltiplos serviços de correção online (ex: Cria.net.br, Corredação, Toda Matéria).

\-   \*\*Coleta de Feedback:\*\* Extrai notas e comentários detalhados de cada plataforma de correção.

\-   \*\*Consolidação de Dados:\*\* Agrega todos os feedbacks e notas em um formato unificado.

\-   \*\*Histórico Pessoal:\*\* Armazena o histórico de redações e avaliações em um banco de dados local (SQLite) para análise posterior.

\-   \*\*Gerenciamento de Perfil:\*\* Utiliza o Playwright para gerenciar perfis de navegador, permitindo a persistência de sessões de login (útil para sites que exigem autenticação).



\## 💻 Tecnologias Utilizadas



\-   \*\*Python:\*\* Linguagem de programação principal.

\-   \*\*Playwright:\*\* Biblioteca para automação de navegador (web scraping e interação com UI).

\-   \*\*SQLite:\*\* Banco de dados leve para armazenamento local do histórico de redações.

\-   \*\*Pandas:\*\* Biblioteca para manipulação e análise de dados (utilizada na persistência para Excel, embora o foco principal seja SQLite).

\-   \*\*Tkinter/CustomTkinter (Potencial):\*\* Importado no `main.py`, indicando um potencial para futura implementação de uma Interface Gráfica do Usuário (GUI).

\-   \*\*Pytest / Pytest-Playwright:\*\* Frameworks para testes automatizados (presentes nas dependências, indicando intenção de testar).



\## 📂 Estrutura do Projeto



```

coretor\_enem/

├── LICENSE

├── README.md

├── requirements.txt

├── tb\_redacoes.xlsx          # Exemplo de arquivo de dados (pode ser usado para exportação)

└── tests/                    # Contém os scripts principais e módulos de automação

&nbsp;   ├── \_\_pycache\_\_/          # Cache de bytecode Python

&nbsp;   ├── classe\_redacao.py     # Define a estrutura de dados da redação e funções de persistência

&nbsp;   ├── coredacao.py          # Lógica de automação para o corretor Corredação

&nbsp;   ├── cria\_codigo.py        # Lógica de automação para o corretor Cria.net.br

&nbsp;   ├── gerenciador\_perfil.py # Gerencia o navegador Playwright e perfis de usuário

&nbsp;   ├── main.py               # Ponto de entrada principal da aplicação

&nbsp;   └── toda\_materia\_codigo.py# Lógica de automação para o corretor Toda Matéria

```



\## ⚙️ Como Instalar e Rodar



Siga os passos abaixo para configurar e executar o projeto em sua máquina.



\### Pré-requisitos



\-   Python 3.8+ instalado.

\-   Navegador Google Chrome instalado (o Playwright utilizará uma versão Chromium, mas a cópia de perfil pode se beneficiar do Chrome).



\### 1. Clonar o Repositório



Abra seu terminal ou prompt de comando e execute:



```bash

git clone https://github.com/siriusbrack2212/coretor\_enem.git

cd coretor\_enem

```



\### 2. Instalar Dependências



É altamente recomendável usar um ambiente virtual para gerenciar as dependências do projeto. Isso evita conflitos com outras instalações Python.



```bash

\# Criar um ambiente virtual (se ainda não tiver um)

python -m venv venv



\# Ativar o ambiente virtual

\# No Windows:

.\\venv\\Scripts\\activate

\# No macOS/Linux:

source venv/bin/activate



\# Instalar as dependências

pip install -r requirements.txt



\# Instalar os drivers do Playwright (necessário para a primeira execução)

playwright install

```



\### 3. Configuração Inicial (Importante!)



O projeto utiliza o Playwright para automação e pode copiar dados do seu perfil de navegador existente para manter sessões de login. Siga estas instruções:



\-   \*\*Feche todas as instâncias do Google Chrome\*\* antes de executar o script para evitar conflitos de perfil.

\-   No arquivo `tests/gerenciador\_perfil.py`, na função `launch`, a linha `page = browser.launch(headless=False, copy\_profile=True)` (ou similar) controla se o perfil será copiado. \*\*Na primeira execução\*\*, defina `copy\_profile=True` para que o Playwright copie seus dados de login (cookies, etc.) do Chrome padrão para o perfil de automação. Nas execuções subsequentes, você pode definir `copy\_profile=False` para economizar tempo.

\-   Se o script indicar que o login no Google é necessário, siga as instruções no terminal para fazer o login manualmente na janela do navegador que será aberta pelo Playwright.



\### 4. Executar o Projeto



Após a instalação e configuração, você pode executar o script principal:



```bash

python tests/main.py

```



O script iniciará o navegador e executará as automações para os corretores configurados. Os resultados serão consolidados e salvos no banco de dados `redacoes\_historico.db`.



\## 📝 Como Usar



1\.  \*\*Execute o Script:\*\* Rode `python tests/main.py`.

2\.  \*\*Escreva sua Redação:\*\* O navegador abrirá automaticamente no site do Cria. Escreva sua redação diretamente na plataforma.

3\.  \*\*Automação Completa:\*\* O sistema automaticamente:

&nbsp;   - Captura o texto da redação que você escreveu no Cria

&nbsp;   - Envia essa mesma redação para os outros corretores (Corredação, Toda Matéria)

&nbsp;   - Coleta todas as notas e feedbacks

&nbsp;   - Salva tudo no banco de dados local

4\.  \*\*Verifique os Resultados:\*\* Após a execução, o arquivo `redacoes\_historico.db` será criado (ou atualizado) na raiz do projeto, contendo o histórico das suas redações e as avaliações recebidas de todos os corretores.



\## 🤝 Contribuição



Contribuições são bem-vindas! Se você tiver sugestões de melhoria, novas funcionalidades ou encontrar bugs, sinta-se à vontade para abrir uma \*issue\* ou enviar um \*pull request\*.



\## 📄 Licença



Este projeto está licenciado sob a Licença MIT. Veja o arquivo \[LICENSE](LICENSE) para mais detalhes.











