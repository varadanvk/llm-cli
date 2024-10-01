import os
import sys
import dotenv
from groq import Groq
import openai
from anthropic import Anthropic
import tiktoken
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from termcolor import colored
import textwrap

def initialize():
    dotenv.load_dotenv()
    api_keys = {
        'groq': os.getenv("GROQ_API_KEY"),
        'openai': os.getenv("OPENAI_API_KEY"),
        'anthropic': os.getenv("ANTHROPIC_API_KEY")
    }
    for provider, key in api_keys.items():
        if not key:
            print(f"Warning: {provider.upper()}_API_KEY not found in environment variables.")
    return api_keys

def create_clients(api_keys):
    clients = {}
    if api_keys['groq']:
        clients['groq'] = Groq(api_key=api_keys['groq'])
    if api_keys['openai']:
        clients['openai'] = openai.OpenAI(api_key=api_keys['openai'])
    if api_keys['anthropic']:
        clients['anthropic'] = Anthropic(api_key=api_keys['anthropic'])
    return clients

def chat_with_ai(client, provider, model, messages):
    try:
        if provider == 'groq':
            response = client.chat.completions.create(
                messages=messages,
                model=model,
            )
            return response.choices[0].message.content
        elif provider == 'openai':
            response = client.chat.completions.create(
                model=model,
                messages=messages
            )
            return response.choices[0].message.content
        elif provider == 'anthropic':
            response = client.messages.create(
                model=model,
                messages=messages
            )
            return response.content[0].text
    except Exception as e:
        print(f"Error occurred while communicating with {provider}: {str(e)}")
        return None

def count_tokens(text, model):
    if "gpt" in model:
        encoding = tiktoken.encoding_for_model(model)
    else:
        encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))

def print_wrapped_text(text, width=80, indent="  "):
    wrapped_lines = textwrap.wrap(text, width=width)
    for line in wrapped_lines:
        print(f"{indent}{line}")

def main():
    api_keys = initialize()
    clients = create_clients(api_keys)

    models = {
        'groq': ['llama-3.1-70b-versatile', 'mixtral-8x7b-32768', 'llama-3.1-8b-instant'],
        'openai': ['gpt-3.5-turbo', 'gpt-4', 'gpt-4o'],
        'anthropic': ['claude-3-5-sonnet-20240620', 'claude-3-opus-20240229', 'claude-3-sonnet-20240229']
    }

    print(colored("Welcome to the Multi-Model AI Chat CLI!", "cyan", attrs=["bold"]))
    print(colored("Available commands:", "yellow"))
    print(colored("  'change model' - Switch to a different AI model", "yellow"))
    print(colored("  'token count' - Display token count for the conversation", "yellow"))
    print(colored("  'clear history' - Clear the conversation history", "yellow"))
    print(colored("  'quit' or 'exit' - End the conversation", "yellow"))

    all_models = [model for provider_models in models.values() for model in provider_models]
    model_completer = WordCompleter(all_models)

    provider = 'groq'  # Default provider
    model = 'llama-3.1-70b-versatile'  # Default model
    conversation_history = []

    while True:
        user_input = prompt("\nYou: ", completer=model_completer).strip()

        if user_input.lower() in ['quit', 'exit']:
            print(colored("Goodbye!", "cyan"))
            break

        if user_input.lower() == 'change model':
            print(colored("\nAvailable models:", "cyan"))
            for p, m_list in models.items():
                print(colored(f"{p.capitalize()}:", "yellow"))
                for m in m_list:
                    print(colored(f"  - {m}", "green"))
            new_model = prompt("Enter the name of the new model: ", completer=model_completer).strip()
            for p, m_list in models.items():
                if new_model in m_list:
                    provider = p
                    model = new_model
                    break
            print(colored(f"Model changed to: {model} (Provider: {provider})", "cyan"))
            continue

        if user_input.lower() == 'token count':
            total_tokens = sum(count_tokens(m['content'], model) for m in conversation_history)
            print(colored(f"Current conversation token count: {total_tokens}", "cyan"))
            continue

        if user_input.lower() == 'clear history':
            conversation_history.clear()
            print(colored("Conversation history cleared.", "cyan"))
            continue

        conversation_history.append({"role": "user", "content": user_input})

        if provider not in clients:
            print(colored(f"Error: No API key available for {provider}.", "red"))
            continue

        response = chat_with_ai(clients[provider], provider, model, conversation_history)
        if response:
            print(colored(f"\n{model}:", "green", attrs=["bold"]))
            print_wrapped_text(response)
            conversation_history.append({"role": "assistant", "content": response})
        else:
            print(colored(f"Failed to get a response from {model}.", "red"))

if __name__ == "__main__":
    main()