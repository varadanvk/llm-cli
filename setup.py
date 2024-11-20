from setuptools import setup

setup(
    name="llm-chat-cli",
    version="0.1.0",
    description="A CLI tool for chatting with multiple LLM providers",
    long_description="""
# llm-chat-cli

Chat with multiple LLM providers (Groq, OpenAI, Anthropic, Cerebras) through a simple CLI interface.

## Features
- Single command to start: `lmci` 
- Easy model switching
- Conversation history
- Token counting
- Multiple provider support

Full docs at: https://github.com/varadankalkunte/llm-chat-cli
    """,
    long_description_content_type="text/markdown",
    author="Varadan Kalkunte",
    author_email="varadan.vk@gmail.com", 
    url="https://github.com/varadanvk/llm-cli",
    packages=["llm_chat_cli"],
    install_requires=[
    "groq",
    "openai",
    "anthropic",
    "tiktoken",
    "prompt_toolkit",
    "termcolor",
    "rich",
    "python-dotenv",
    "cerebras_cloud_sdk",
    ],
    entry_points={
        "console_scripts": [
            "lmci=llm_chat_cli.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
)