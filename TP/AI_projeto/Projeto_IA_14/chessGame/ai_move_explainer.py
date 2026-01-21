import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api.groq.com/openai/v1/chat/completions"
API_KEY = os.getenv("GROQ_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def explain_move_with_groq(move_san, board_fen, color="White"):
    """
    Utiliza a API Groq (modelo LLaMA) para explicar um lance de xadrez de forma simples.

    Args:
        move_san (str): O lance no formato SAN (Standard Algebraic Notation), ex: "Nf3".
        board_fen (str): O estado atual do tabuleiro no formato FEN.
        color (str, optional): A cor do jogador que realizou o lance. Default é "White".

    Returns:
        str: Explicação curta do lance ou mensagem de erro.
    """
    prompt = f"""
You're a chess teacher.
Explain this move in plain English:
{color} plays {move_san}

Board FEN: {board_fen}

Explain why this move might be smart. Keep it short and clear. Limit your answer to no more than 30 words.
"""
    data = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 120
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=data)
        response.raise_for_status()
        explanation = response.json()["choices"][0]["message"]["content"].strip()
        return explanation
    except Exception as e:
        print(f"Failed to explain move: {e}")
        return "Couldn't get explanation."
