from crewai import Agent, Task, Crew

import os
from google.colab import userdata

os.environ["OPENAI_API_KEY"] = userdata.get('OPENAI_API_KEY')
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o-mini'
os.environ["SERPER_API_KEY"] = userdata.get('SERPER_API_KEY')

from re import search
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

"""
1 - Buscador de Conteúdo
2 - Redator de Conteúdo
3 - Editor de Conteúdo
"""

buscador = Agent(
    role =      'Buscador de Conteúdo',
    goal =  	  'Busque conteúdo online sobre {tema}',
    backstory = 'Você está trabalhando na criação de artigos para o Linkedin sobre o {tema}.'
                'Você vai fazer uma busca sobre informações na internet, coletá-las e agrupá-las.'
                'Seu trabalho servirá de base para o redator de Conteúdo.',
    tools = [search_tool, scrape_tool],
    verbose = True
)

redator = Agent(
    role = 'Redator de Conteúdo',
    goal = 'Escreva um texto divertido e factualmente correto para o LinkedIn sobre {tema}',
    backstory = 'Você está trabalhando na redação de um artigo para o Linkedin sobre {tema}.'
                'Você vai utilizar os dados coletados pelo Buscador de conteúdo para escrever um texto.'
                'interessante, divertido e factualmente correto para o LinkedIn.'
                'Dê opniões sobre o {tema}, mas ao fazê-lo, deixe claro que são opniões pessoais.',
    tools = [search_tool, scrape_tool],
    verbose = True
)

editor = Agent(
    role = 'Editor de Conteúdo',
    goal = 'Editar um texto de LinkedIn para que ele tenha um tom mais informal.',
    backstory = 'Você está trabalhando na edição de um artigo para o Linkedin.'
                'Você vai receber um texto do redator de conteúdo e editá-lo para o tom de voz'
                'do Fabrício Carrara, que é mais divertido.',
    tools = [search_tool, scrape_tool],
    verbose = True
)

"""Tarefas"""

buscar = Task(
    description = '1. Priorizeas ultimas tendências, os principais atores e as notícias mais relevantes sobre {tema}.\n'
                  '2. Identifique o público-alvo, considerando seus interesses e pontos de dor.\n'
                  '3. Inclua palavras-chave de SEO e dados ou fontes relevantes.',
    agent = buscador,
    expected_output = 'plano de tentências sobre {tema} com as palavras mais relevantes de SEO e as ultimas notícias.',
)

redigir = Task(
    description = '1. Use os dados coletados de conteúdos para criar um post de LinkedIn atraente sobre {tema}.\n'
                  '2. Incorporar palabras-chave de SEO de forma natural.\n'
                  '3. Certifique-se de que o post esteja estruturado de forma cativante, com uma conclusão que faça o leitor refletir.',
    agent = redator,
    expected_output = 'Um texto de LinkedIn sobre {tema}.',
)

editar = Task(
    description = 'Revisar a postagem do LinkedIn em questão quanto a erros gramaticais e alinhamento com voz pessoal do Whinderson Nunes',
    agent = editor,
    expected_output = 'Um texto de LinkedIn pronto para publicação, seguindo o tom de voz esperado'
                      'O texto está separado em parágrafos e não usa bullet point',
)

"""Crew - equipe"""

equipe = Crew(
    agents = [
        buscador,
        redator,
        editor
    ],
    tasks = [
        buscar,
        redigir,
        editar
    ],
    verbose = True
)

"""Rodando o Crew"""

tema_do_artigo = 'O uso da IA para o mundo corporativo'

entradas = {"tema": tema_do_artigo}
resultado = equipe.kickoff(inputs=entradas)
