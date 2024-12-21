import requests


def query_llm(prompt):
    url = "https://ollama-yggo8cggoc8k55w0w05c0s85.ovcraft.com/api/chat/completions"
    model = "qwen2.5-coder:3b"
    token = "sk-0db19bdb96794a308fb81391d4b69063"

    headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

    payload = {
        'model': model,
        'messages': [{'role': 'user', 'content': prompt}],
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()['choices'][0]["message"]["content"]

if __name__ == "__main__":
    print(query_llm("prompt"))
