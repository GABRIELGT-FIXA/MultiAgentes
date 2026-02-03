# CrewAI: Gerador de Post para LinkedIn (Busca → Redação → Edição)

Este projeto usa **CrewAI** para orquestrar 3 agentes (Buscador, Redator e Editor) que trabalham em sequência para criar um post de LinkedIn sobre um tema:

1. **Buscador de Conteúdo**: pesquisa na web e coleta informações.
2. **Redator de Conteúdo**: escreve um texto divertido e factualmente correto.
3. **Editor de Conteúdo**: ajusta o tom e revisa o texto final.

> Ferramentas usadas: `SerperDevTool` (pesquisa) e `ScrapeWebsiteTool` (raspagem).

---

## ✅ Requisitos

- Python **3.10+**
- Chaves de API:
  - **OPENAI_API_KEY** (OpenAI)
  - **SERPER_API_KEY** (Serper)

---

## 📦 Instalação (pip)

Crie e ative um ambiente virtual (recomendado):

### Windows (PowerShell)
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### macOS / Linux
```bash
python -m venv .venv
source .venv/bin/activate
```

Instale as dependências:
```bash
pip install -U crewai crewai-tools
```

> Se você estiver no Google Colab, normalmente isso funciona também (veja seção Colab).

---

## 🔑 Configurando as variáveis de ambiente (Local)

Você pode exportar as chaves no terminal:

### macOS / Linux
```bash
export OPENAI_API_KEY="SUA_CHAVE_OPENAI"
export SERPER_API_KEY="SUA_CHAVE_SERPER"
export OPENAI_MODEL_NAME="gpt-4o-mini"
```

### Windows (PowerShell)
```powershell
$env:OPENAI_API_KEY="SUA_CHAVE_OPENAI"
$env:SERPER_API_KEY="SUA_CHAVE_SERPER"
$env:OPENAI_MODEL_NAME="gpt-4o-mini"
```

> **Dica:** você pode trocar `OPENAI_MODEL_NAME` por outro modelo que esteja disponível para sua conta.

---

## 🔑 Configurando no Google Colab (opcional)

Se você estiver no Colab, pode usar o `google.colab.userdata` como no seu notebook:

1. Vá em **Colab → (ícone de chave/Secrets)** e adicione:
   - `OPENAI_API_KEY`
   - `SERPER_API_KEY`

2. No código:
```python
from google.colab import userdata
import os

os.environ["OPENAI_API_KEY"] = userdata.get("OPENAI_API_KEY")
os.environ["SERPER_API_KEY"] = userdata.get("SERPER_API_KEY")
os.environ["OPENAI_MODEL_NAME"] = "gpt-4o-mini"
```

---

## ▶️ Como executar

### 1) Salve o script

Crie um arquivo, por exemplo `main.py`, e cole o código do projeto.

Estrutura sugerida:
```text
.
├── main.py
└── README.md
```

### 2) Rode no terminal

```bash
python main.py
```

Ao executar, você verá logs do CrewAI (por causa do `verbose=True`) e no final o **resultado** gerado.

---

## 🧠 Exemplo de código (main.py)

> Este é o mesmo fluxo que você enviou (com pequenos ajustes só para rodar fora do Colab também).

```python
import os
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

# --- CONFIG: defina suas variáveis de ambiente antes de rodar ---
# OPENAI_API_KEY
# SERPER_API_KEY
# OPENAI_MODEL_NAME (opcional, padrão abaixo)

os.environ.setdefault("OPENAI_MODEL_NAME", "gpt-4o-mini")

search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

# 1 - Buscador de Conteúdo
buscador = Agent(
    role='Buscador de Conteúdo',
    goal='Busque conteúdo online sobre {tema}',
    backstory=(
        'Você está trabalhando na criação de artigos para o Linkedin sobre o {tema}. '
        'Você vai fazer uma busca sobre informações na internet, coletá-las e agrupá-las. '
        'Seu trabalho servirá de base para o redator de Conteúdo.'
    ),
    tools=[search_tool, scrape_tool],
    verbose=True
)

# 2 - Redator de Conteúdo
redator = Agent(
    role='Redator de Conteúdo',
    goal='Escreva um texto divertido e factualmente correto para o LinkedIn sobre {tema}',
    backstory=(
        'Você está trabalhando na redação de um artigo para o Linkedin sobre {tema}. '
        'Você vai utilizar os dados coletados pelo Buscador de conteúdo para escrever um texto '
        'interessante, divertido e factualmente correto para o LinkedIn. '
        'Dê opniões sobre o {tema}, mas ao fazê-lo, deixe claro que são opniões pessoais.'
    ),
    tools=[search_tool, scrape_tool],
    verbose=True
)

# 3 - Editor de Conteúdo
editor = Agent(
    role='Editor de Conteúdo',
    goal='Editar um texto de LinkedIn para que ele tenha um tom mais informal.',
    backstory=(
        'Você está trabalhando na edição de um artigo para o Linkedin. '
        'Você vai receber um texto do redator de conteúdo e editá-lo para o tom de voz '
        'do Fabrício Carrara, que é mais divertido.'
    ),
    tools=[search_tool, scrape_tool],
    verbose=True
)

# --- Tarefas ---
buscar = Task(
    description=(
        '1. Priorize as ultimas tendências, os principais atores e as notícias mais relevantes sobre {tema}.\n'
        '2. Identifique o público-alvo, considerando seus interesses e pontos de dor.\n'
        '3. Inclua palavras-chave de SEO e dados ou fontes relevantes.'
    ),
    agent=buscador,
    expected_output='Plano de tendências sobre {tema} com palavras relevantes de SEO e últimas notícias.',
)

redigir = Task(
    description=(
        '1. Use os dados coletados de conteúdos para criar um post de LinkedIn atraente sobre {tema}.\n'
        '2. Incorporar palavras-chave de SEO de forma natural.\n'
        '3. Certifique-se de que o post esteja estruturado de forma cativante, com uma conclusão que faça o leitor refletir.'
    ),
    agent=redator,
    expected_output='Um texto de LinkedIn sobre {tema}.',
)

editar = Task(
    description=(
        'Revisar a postagem do LinkedIn em questão quanto a erros gramaticais e alinhamento com voz pessoal do Whinderson Nunes'
    ),
    agent=editor,
    expected_output=(
        'Um texto de LinkedIn pronto para publicação, seguindo o tom de voz esperado. '
        'O texto está separado em parágrafos e não usa bullet point.'
    ),
)

# --- Crew ---
equipe = Crew(
    agents=[buscador, redator, editor],
    tasks=[buscar, redigir, editar],
    verbose=True
)

if __name__ == "__main__":
    tema_do_artigo = "O uso da IA para o mundo corporativo"
    entradas = {"tema": tema_do_artigo}
    resultado = equipe.kickoff(inputs=entradas)
    print("\n===== RESULTADO FINAL =====\n")
    print(resultado)
```

---

## 🧪 Personalizando o tema

Basta alterar:
```python
tema_do_artigo = "O uso da IA para o mundo corporativo"
```

Ou receber via terminal (opcional), por exemplo:
```python
import sys
tema_do_artigo = sys.argv[1] if len(sys.argv) > 1 else "IA no mundo corporativo"
```

E rodar:
```bash
python main.py "CrewAI no marketing B2B"
```

---

## 🛠️ Problemas comuns

### 1) Erro de chave / autenticação
Verifique se você definiu:
- `OPENAI_API_KEY`
- `SERPER_API_KEY`

### 2) Modelo não encontrado
Tente trocar:
```bash
export OPENAI_MODEL_NAME="gpt-4o-mini"
```
por outro modelo disponível para sua conta.

### 3) Ambiente do Colab vs Local
No Colab você usa `userdata.get(...)`.
No local você usa variáveis de ambiente no terminal.

---

## 📄 Licença
Escolha uma licença (ex: MIT) e adicione um arquivo `LICENSE` no repositório.

---

## ⭐ Créditos
- CrewAI (orquestração de agentes)
- Serper (pesquisa web)
- Ferramentas CrewAI Tools (scraping e search)
****
