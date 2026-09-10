from flask import Flask, request, jsonify
from nltk.tokenize import word_tokenize
import nltk
import re
import difflib

nltk.download('punkt')
nltk.download('punkt_tab')

# --- Respostas do chatbot, por categoria ---
respostas = {
    "cumprimento": "Como posso ajudar você neste belo dia?",
    "gentileza": "Estou bem, obrigada por perguntar. Espero que você também esteja bem.",
    "nome": "Meu nome é ChatBot Guarani.",
    "funcao": "Fui criado para introduzir o estudo de Inteligência Artificial. Posso responder a perguntas simples para iniciar um diálogo com o usuário.",
    "despedida": "Tchau! Muito obrigada por testar esse serviço! Tenha um bom dia!",
    "idade": "Sou um programa de computador, não tenho idade como as pessoas — mas fui criado em 2023!",
    "agradecimento": "De nada! Fico feliz em ajudar.",
    "ajuda": "Claro! Pode me perguntar coisas como 'qual é o seu nome', 'o que você faz' ou 'tudo bem?'.",
    "criador": "Fui desenvolvida pela Maria Machado como projeto final do curso Técnico em Desenvolvimento de Sistemas.",
}

# --- Frases-gatilho de cada categoria (a frase inteira é comparada, não palavra a palavra) ---
categorias = {
    "cumprimento": ["olá", "oi", "ola", "hey", "ei", "e ai", "e aí", "bom dia", "boa tarde", "boa noite"],
    "gentileza": ["tudo bem", "como vai", "tudo certo", "como você está", "como voce esta", "beleza"],
    "nome": ["qual é o seu nome", "qual seu nome", "como você se chama", "seu nome", "quem é você", "quem e voce"],
    "funcao": ["função", "funcao", "o que você pode fazer", "o que voce pode fazer", "quais são suas habilidades",
               "funções", "o que você faz", "o que voce faz", "qual é a sua função", "para que você serve",
               "para que voce serve"],
    "despedida": ["adeus", "bye", "até logo", "ate logo", "tchau", "falou", "flw"],
    "idade": ["quantos anos você tem", "quantos anos voce tem", "qual sua idade", "qual é a sua idade",
              "que idade você tem", "que idade voce tem"],
    "agradecimento": ["obrigado", "obrigada", "valeu", "muito obrigado", "muito obrigada", "vlw"],
    "ajuda": ["ajuda", "me ajuda", "socorro", "não entendi", "nao entendi", "o que posso perguntar"],
    "criador": ["quem te criou", "quem criou você", "quem criou voce", "quem te fez", "quem é sua criadora",
                "quem e sua criadora"],
}

# Lista achatada de (palavra_individual, categoria) — usada só na etapa de correspondência aproximada
palavras_por_categoria = {
    categoria: sorted({palavra for frase in frases for palavra in frase.split()})
    for categoria, frases in categorias.items()
}

app = Flask(__name__)


@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    user_question = data['question']
    resposta = responder_pergunta(user_question)
    print(resposta)
    return jsonify({'response': resposta})


def normalizar(texto):
    """Deixa minúsculo e remove pontuação, preservando acentos."""
    texto = texto.lower().strip()
    texto = re.sub(r"[!?.,;:]+", "", texto)
    texto = re.sub(r"\s+", " ", texto)
    return texto


def responder_pergunta(pergunta):
    pergunta_normalizada = normalizar(pergunta)

    if not pergunta_normalizada:
        return "Desculpe, não entendi a pergunta."

    # 1ª etapa: a pergunta contém alguma das frases-gatilho? (comparação por frase, não palavra solta)
    for categoria, frases in categorias.items():
        for frase in frases:
            if frase in pergunta_normalizada:
                return respostas[categoria]

    # 2ª etapa: correspondência aproximada — pega erros de digitação e variações não previstas
    tokens = word_tokenize(pergunta_normalizada)
    melhor_categoria = None
    melhor_pontuacao = 0.0

    for token in tokens:
        for categoria, palavras in palavras_por_categoria.items():
            proximas = difflib.get_close_matches(token, palavras, n=1, cutoff=0.75)
            if proximas:
                pontuacao = difflib.SequenceMatcher(None, token, proximas[0]).ratio()
                if pontuacao > melhor_pontuacao:
                    melhor_pontuacao = pontuacao
                    melhor_categoria = categoria

    if melhor_categoria:
        return respostas[melhor_categoria]

    return "Desculpe, não entendi a pergunta. Tente perguntar de outra forma, ou digite 'ajuda' para ver exemplos."


if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5000)
