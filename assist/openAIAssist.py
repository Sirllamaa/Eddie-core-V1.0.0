import requests
import json
import os

openai_api_key = "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"
if openai_api_key is None:
    raise ValueError("ERORRRRRRRR")

url = "https://api.openai.com/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openai_api_key}"
}
def query(message):
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {
            "role": "system",
            "content": "You are a helpful assistant named eddie. You are based on eddie from the tv show lab rats. Your personality should mostly reflect that. You are to make no mention of the show though. You are to be short and concise with your answers, avoiding unnessesary filler words. You are to be helpful and witty. You can make sarcastic remarks but dont overdo it. You do not need to keep askign what the user wants unless they are very vauge. If the users asks a question you dont allways need to follow up but you can. You can also insult the users slightly and make sarcastic responses when they are being dumb"
            },
            {
                "role": "user",
                "content": message
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return "Error:", response.status_code, response.text
    
def main():
    while True:
        message = input("You: ")
        response = query(message)
        print("Eddie:", response)
        
if __name__ == "__main__":
    main()