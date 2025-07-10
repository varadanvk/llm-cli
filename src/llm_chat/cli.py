import sys
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from .utils import print_available_models
from termcolor import colored
from .config import (
    initialize,
    load_config,
    save_config,
)  # Import the necessary functions from config
from .clients import create_clients
from .chat import chat_with_ai
from .utils import count_tokens, create_typing_animation, stream_with_markdown_chunks
from .setup import setup
from .tools import execute_terminal_command


def print_help_menu():
    """Print the help menu with available commands."""
    print(colored("Available commands:", "yellow"))
    print(colored("  'change model' - Switch to a different AI model", "yellow"))
    print(
        colored("  'token count' - Display token count for the conversation", "yellow")
    )
    print(colored("  'clear history' - Clear the conversation history", "yellow"))
    print(colored("  'quit' or 'exit' - End the conversation", "yellow"))
    print(colored("  'default' - Set a default model", "yellow"))
    print(colored("  'help' - Show menu options", "yellow"))
    print(colored("\n Use --- for a multi-line prompt", "yellow"))


def handle_commands(
    user_input,
    models,
    model_completer,
    conversation_history,
    provider,
    model,
    default_provider,
    default_model,
):
    """
    Handle CLI commands and their execution.

    Returns:
        tuple: (bool, provider, model, default_provider, default_model)
    """
    if user_input.lower() == "change model":
        print_available_models(models)
        new_model = prompt(
            "Enter the name of the new model: ", completer=model_completer
        ).strip()
        for p, m_list in models.items():
            if new_model in m_list:
                provider = p
                if new_model == "custom" and p == "openrouter":
                    custom_model = prompt(
                        "Enter the OpenRouter model name (e.g., 'openai/gpt-4-turbo'): "
                    ).strip()
                    if custom_model:
                        model = custom_model
                        print(
                            colored(f"Using custom OpenRouter model: {model}", "cyan")
                        )
                    else:
                        print(
                            colored(
                                "No model specified. Keeping current model.", "yellow"
                            )
                        )
                        return True, provider, model, default_provider, default_model
                else:
                    model = new_model
                break
        else:
            print(colored(f"Model '{new_model}' not found. Please try again.", "red"))
            return True, provider, model, default_provider, default_model
        print(colored(f"Model changed to: {model} (Provider: {provider})", "cyan"))
        return True, provider, model, default_provider, default_model

    if user_input.lower() == "default":
        print_available_models(models)
        new_default_model = prompt(
            "Enter the name of the new default model: ", completer=model_completer
        ).strip()
        new_default_provider = None
        for p, m_list in models.items():
            if new_default_model in m_list:
                new_default_provider = p
                break
        if new_default_provider:
            default_provider = new_default_provider
            if new_default_model == "custom" and new_default_provider == "openrouter":
                custom_model = prompt(
                    "Enter the OpenRouter model name (e.g., 'openai/gpt-4-turbo'): "
                ).strip()
                if custom_model:
                    default_model = custom_model
                    print(
                        colored(
                            f"Using custom OpenRouter model: {default_model}", "cyan"
                        )
                    )
                else:
                    print(
                        colored(
                            "No model specified. Keeping current default.", "yellow"
                        )
                    )
                    return True, provider, model, default_provider, default_model
            else:
                default_model = new_default_model
            save_config(
                {"default_provider": default_provider, "default_model": default_model}
            )  # Save both provider and model
            print(
                colored(
                    f"Default model set to: {default_model} (Provider: {default_provider})",
                    "cyan",
                )
            )
        else:
            print(
                colored(
                    f"Model '{new_default_model}' not found. Please try again.", "red"
                )
            )
        return True, provider, model, default_provider, default_model

    if user_input.lower() == "help":
        print_help_menu()
        return True, provider, model, default_provider, default_model

    if user_input.lower() == "token count":
        total_tokens = sum(
            count_tokens(m["content"], model) for m in conversation_history
        )
        print(colored(f"Current conversation token count: {total_tokens}", "cyan"))
        return True, provider, model, default_provider, default_model

    if user_input.lower() == "clear history":
        conversation_history.clear()
        print(colored("Conversation history cleared.", "cyan"))
        return True, provider, model, default_provider, default_model

    # Handle terminal command execution
    if user_input.lower().startswith("exec ") or user_input.startswith("! "):
        # Extract the command to execute
        if user_input.lower().startswith("exec "):
            command = user_input[5:].strip()
        else:  # Starts with "! "
            command = user_input[2:].strip()

        if command:
            # Execute the command
            execute_terminal_command(command)
        else:
            print(
                colored(
                    "Error: No command specified. Use 'exec <command>' or '! <command>'.",
                    "red",
                )
            )
        return True, provider, model, default_provider, default_model

    return False, provider, model, default_provider, default_model


def main():
    """Main CLI entry point."""
    if len(sys.argv) > 1 and sys.argv[1] == "setup":
        setup()
        return

    api_keys = initialize()  # Load API keys using the initialize function from config
    clients = create_clients(api_keys)
    print(colored("Initialization Successful.", "green"))

    models = {
        "groq": [
            "llama-3.1-70b-versatile",
            "mixtral-8x7b-32768",
            "llama-3.1-8b-instant",
        ],
        "openai": ["gpt-4o", "gpt-4.1", "o3"],
        "anthropic": [
            "claude-sonnet-4",
            "claude-opus-4",
            "claude-3.7-sonnet",
        ],
        "cerebras": ["llama3.1-8b", "llama-3.3-70b"],
        "openrouter": ["google/gemini-2.5-pro", "x-ai/grok-3", "x-ai/grok-4", "custom"],
    }

    print(colored("Welcome to the Multi-Model AI Chat CLI!", "cyan", attrs=["bold"]))
    print_help_menu()

    all_models = [
        model for provider_models in models.values() for model in provider_models
    ]
    model_completer = WordCompleter(all_models, ignore_case=True)

    # Load saved configuration using the load_config function from config
    config = load_config()
    default_provider = config.get(
        "default_provider", "openai"
    )  # Default provider if not in config
    default_model = config.get(
        "default_model", "gpt-4o"
    )  # Default model if not in config
    provider = default_provider  # Set to default provider
    model = default_model  # Set to default model
    conversation_history = []

    while True:
        user_input = prompt("\nYou: ").strip()
        if user_input.lower() == "---":
            lines = []
            while True:
                line = prompt("").strip()
                if line.lower() == "---":
                    break
                lines.append(line)
            user_input = "\n".join(lines)

        print("\n" + "–" * 70)

        if user_input.lower() in ["quit", "exit"]:
            print(colored("\nGoodbye!", "cyan"))
            break

        handled, provider, model, default_provider, default_model = handle_commands(
            user_input,
            models,
            model_completer,
            conversation_history,
            provider,
            model,
            default_provider,
            default_model,
        )

        if handled:
            continue

        conversation_history.append({"role": "user", "content": user_input})

        if provider not in clients:
            print(colored(f"Error: No API key available for {provider}.", "red"))
            continue

        # Use the default model if no model is currently selected
        if not model:
            model = default_model
            provider = default_provider

        # Show thinking animation before getting response
        create_typing_animation(f"Getting response from {model}")

        response = chat_with_ai(
            clients[provider], provider, model, conversation_history, stream=True
        )

        if response:
            print(colored(f"\n{model}:", "green", attrs=["bold"]))

            # Stream the response with special handling for code blocks
            full_response = stream_with_markdown_chunks(response)

            print("\n" + "–" * 70)
            # Store the actual complete response in conversation history
            conversation_history.append({"role": "assistant", "content": full_response})
        else:
            print(colored(f"Failed to get a response from {model}.", "red"))


if __name__ == "__main__":
    main()
