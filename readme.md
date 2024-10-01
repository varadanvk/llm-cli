# Multi-Model AI Chat CLI

This is a command-line interface (CLI) application that allows users to interact with multiple AI models from different providers.

## Features

- Supports multiple AI providers: Groq, OpenAI, and Anthropic
- Allows switching between different AI models
- Keeps track of conversation history
- Provides token count for the conversation
- Offers command completion for model names

## Prerequisites

- Python 3.x
- API keys for the AI providers you want to use

## Installation

1. Clone this repository
2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Create a .env file in the root directory of the project and add your API keys:

```bash
GROQ_API_KEY=your_groq_api_key
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

4. Run the script:

```bash
python main.py
```

Available commands:

- 'change model' - Switch to a different AI model
- 'token count' - Display token count for the conversation
- 'clear history' - Clear the conversation history
- 'quit' or 'exit' - End the conversation

Supported Models

- Groq: llama-3.1-70b-versatile, mixtral-8x7b-32768, llama-3.1-8b-instant
- OpenAI: gpt-3.5-turbo, gpt-4, gpt-4o
- Anthropic: claude-3-5-sonnet-20240620, claude-3-opus-20240229, claude-3-sonnet-20240229
