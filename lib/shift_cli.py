from ai_client import OllamaChatClient
from brief_builder import HandoffBriefBuilder


class ShiftBriefCLI:
    """Command-line workflow for generating and revising shift handoff briefs."""

    def __init__(self, ai_client, brief_builder=None):
        """Initialize the CLI application."""
        self.ai_client = ai_client
        self.brief_builder = brief_builder or HandoffBriefBuilder()
        self.running = True

    def display_welcome(self):
        """Print a welcome message and command guidance."""
        print("Welcome to the Shift Handoff Brief CLI.")
        print(self.command_help())

    def command_help(self):
        """Return command guidance as a string."""
        return (
            "Available commands:\n"
            "  brief <shift notes>   Create a new shift handoff brief\n"
            "  revise <feedback>     Revise the previous brief\n"
            "  history               Show the conversation message count\n"
            "  reset                 Clear the conversation history\n"
            "  help                  Show this help message\n"
            "  exit                  Quit the application\n"
            "  quit                  Quit the application"
        )

    def handle_command(self, raw_input):
        """Route a user command."""
        if not isinstance(raw_input, str) or not raw_input.strip():
            return "Input Error: Please enter a command. Type help for options."

        parts = raw_input.strip().split(maxsplit=1)
        command = parts[0].lower()
        payload = parts[1].strip() if len(parts) > 1 else ""

        try:
            if command == "brief":
                if not payload:
                    return "Input Error: Please include your shift notes after brief."
                return self.brief_builder.create_brief(self.ai_client, payload)

            if command == "revise":
                if not payload:
                    return "Input Error: Please include your revision feedback after revise."
                return self.brief_builder.revise_brief(self.ai_client, payload)

            if command == "history":
                count = self.ai_client.message_count()
                return f"Conversation messages: {count}"

            if command == "reset":
                self.ai_client.reset()
                return "Conversation reset. History cleared."

            if command == "help":
                return self.command_help()

            if command in ("exit", "quit"):
                self.running = False
                return "Goodbye!"

            return (
                f"Input Error: Unknown command '{command}'. "
                "Type help to see available commands."
            )
        except ValueError as error:
            return f"Input Error: {error}"
        except RuntimeError as error:
            return f"Service Error: {error}"

    def run(self):
        """Run the CLI input loop."""
        self.display_welcome()

        while self.running:
            try:
                user_input = input("> ")
            except EOFError:
                print("Goodbye!")
                break

            print(self.handle_command(user_input))


def main():
    client = OllamaChatClient(model_name="llama3.2")
    app = ShiftBriefCLI(client)
    app.run()


if __name__ == "__main__":
    main()
