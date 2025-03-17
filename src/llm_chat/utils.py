"""
Utility functions for LLM Chat
"""

import tiktoken
import textwrap
import time
import sys
from rich.console import Console
from rich.markdown import Markdown
from termcolor import colored


def count_tokens(text, model):
    """
    Count tokens in the given text.

    Args:
        text (str): The text to count tokens for
        model (str): The model name (currently unused, but kept for future model-specific counting)

    Returns:
        int: Number of tokens in the text
    """
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))


def print_wrapped_text(text, width=80, indent="  "):
    """
    Print text with proper wrapping.

    Args:
        text (str): The text to wrap and print
        width (int): Maximum line width
        indent (str): Indentation string to prepend to each line
    """
    wrapped_lines = textwrap.wrap(text, width=width)
    for line in wrapped_lines:
        print(f"{indent}{line}")


def render_markdown(text, clear=False):
    """
    Render text as markdown.

    Args:
        text (str): The markdown text to render
        clear (bool): Whether to clear the previous output
    """
    console = Console()
    md = Markdown(text)
    console.print(md)


def print_available_models(models):
    print(colored("\nAvailable models:", "cyan"))
    for p, m_list in models.items():
        print(colored(f"{p.capitalize()}:", "yellow"))
        for m in m_list:
            print(colored(f"  - {m}", "green"))


def create_typing_animation(text="Thinking", color="cyan"):
    """
    Create a typing animation effect.

    Args:
        text (str): The text to display before the animation
        color (str): The color to use for the animation
    """
    animations = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]
    i = 0
    start_time = time.time()
    sys.stdout.write(colored(f"{text} ", color))
    sys.stdout.flush()

    while time.time() - start_time < 1.5:  # Show animation for 1.5 seconds
        sys.stdout.write(colored(f"\r{text} {animations[i % len(animations)]}", color))
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1

    sys.stdout.write(colored(f"\r{text}   \n", color))
    sys.stdout.flush()
