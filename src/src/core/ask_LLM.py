from google import genai
import requests
import pandas as pd
from os import name
    

def generate_prompt(file_path: str, line:int, headers: list) -> str:
    if name == 'nt':
        sistema_operacional = 'windows'
    elif name == 'posix':
        sistema_operacional = 'Unix (linux ou macOS)'
    else:
        sistema_operacional = name

    descriptions = []
    prompt = f'''
    # INSTRUÇÕES PARA O MODELO DE IA

    ## PERSONA
    Você é um especialista em cibersegurança e automação de sistemas, focado em criar scripts de correção (patching). Sua única função é gerar um script que resolva a vulnerabilidade descrita abaixo.

    ## TAREFA
    Analise o contexto da vulnerabilidade a seguir e gere um script de shell (compatível com o sistema operacional do localhost) que, ao ser executado, corrija permanentemente a vulnerabilidade descrita.

    ## CONTEXTO DA VULNERABILIDADE\n
    Localhost OS: {sistema_operacional}\n
    '''

    df = pd.read_csv(file_path)
    for header in headers:
        content = df.loc[line, header]

        descriptions.append(content)

    for header, description in zip(headers, descriptions):
        prompt += f'{header}: {description}\n'
    
    prompt += '''
    ## REGRAS E RESTRIÇÕES DE SAÍDA
    1.  **APENAS SCRIPT:** A sua resposta deve conter ÚNICA E EXCLUSIVAMENTE o código do script.
    2.  **SEM EXPLICAÇÕES:** Não adicione nenhum comentário, explicação, introdução, ou despedida.
    3.  **SEM BLOCOS DE CÓDIGO MARKDOWN:** Não envolva o script em blocos de código como ` ```bash ` ou ` ```sh `. A resposta deve ser o texto puro do script.
    4.  **AUTOSSUFICIENTE:** O script deve ser completo, autônomo e não deve exigir interação do usuário para ser executado.
    5.  **COMPATIBILIDADE:** O script deve ser compatível com o sistema operacional especificado em 'localhost OS'. Se o sistema operacional não for especificado, assuma um sistema baseado em Linux (como Ubuntu/Debian).

    # INÍCIO DO SCRIPT DE CORREÇÃO'''

    return prompt


def ask_gemini(API_KEY: str, prompt: str):
    client = genai.Client(api_key=API_KEY)

    response = client.models.generate_content(
        model='gemini-2.0-flash', contents=prompt
    )

    return response.text


def ask_deepseek(API_KEY: str, API_URL: str, prompt: str) -> str:
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    data = {
        "model": "deepseek/deepseek-chat:free",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(API_URL, json = data, headers = headers)

    if response.status_code == 200:
        response = response.json()
        return response['choices'][0]['message']['content']
    else:
        return "Falha ao buscar dados da API. Código de status:", response.status_code