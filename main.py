import os
from langchain_ollama import ChatOllama

ollama_host = os.environ.get('OLLAMA_HOST', 'localhost')
base_url = f'http://{ollama_host}:11434'
print(base_url)

llm = ChatOllama(
    model='qwen3:0.6b',
    base_url=base_url,
    verbose=True,
    validate_model_on_init=True,
)
print('A')

messages = [
    ("system", "You are a helpful assistant that translates English to French. Translate the user sentence."),
    ("human", "I love programming."),
]

print('B')
ai_msg = llm.invoke(messages)
print('C')

print(ai_msg)
