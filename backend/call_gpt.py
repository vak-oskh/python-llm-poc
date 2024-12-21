import requests


def query_llm(user_input, list_of_functions):
    url = "https://ollama-yggo8cggoc8k55w0w05c0s85.ovcraft.com/api/chat/completions"
    model = "qwen2.5-coder:latest"
    token = "sk-0db19bdb96794a308fb81391d4b69063"

    prompt = f"""You are an AI assistant whose job is to identify which functions 
                you should call based on a natural language prompt. 
                The functions you can all are: {list_of_functions}. 
                Your response from now on should be only a function name and the arguments 
                you think are most appropriate, if any arguments are needed. 
                Try to fully qualify the names of any TV shows and songs. 
                For example, when you are asked to play 'BoJack' you should return play_tv_show('BoJack Horseman'). 
                The string for this request is: '{user_input}'"""

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
    print(query_llm("prompt", "Func 1, 2, 3"))
