import openai

openai.api_key = "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"
openai.api_base = "https://api.groq.com/openai/v1"

def explain_move_with_groq(move_san, board_fen, color="White"):
    prompt = f"""
You're a chess teacher.
Explain this move in plain English:
{color} plays {move_san}

Board FEN: {board_fen}

Explain why this move might be smart. Keep it short and clear. Limit your answer to no more than 30 words.
"""

    try:
        response = openai.ChatCompletion.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=120,
        )

        explanation = response.choices[0].message.content.strip()
        return explanation

    except Exception as e:
        print(f"❌ Failed to explain move: {e}")
        return "Couldn't get explanation."
