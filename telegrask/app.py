from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    InlineQueryHandler,
    CallbackContext,
    Filters,
)
from telegram import ParseMode, Update
from .exceptions import HelpPrasingError
from .helpparser import HelpParser
from .inlinequery import InlineQuery
from .config import Config
from typing import Union, Callable, Optional, Pattern


class Telegrask:
    """Main bot class.

    Usage
    -----
        bot = Telegrask(TOKEN)

        # optional configuration
        bot.config["ATTRIBUTE_NAME"] = attribute_value
    """

    default_config = Config({"HELP_MESSAGE": True})

    def __init__(self, token: str) -> None:
        self.config = self.default_config
        self.updater = Updater(token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.help = HelpParser()

    def add_handler(self, handler) -> None:
        """Simple wrapper method to add custom handlers to dispatcher."""
        self.dispatcher.add_handler(handler)

    def command(
        self,
        commands: Union[str, list],
        help: Optional[str] = None,
        allow_without_prefix: bool = False,
    ) -> Callable:
        """Decorator for command callback function.

        Usage
        -----
            @bot.command("command_name", help="command help message")
            def callback_function(update, context):
                ...
        """

        def w(f):
            self.add_handler(CommandHandler(commands, f))
            command_name = commands[0] if type(commands) == list else commands
            if self.config["HELP_MESSAGE"]:
                if help is None:
                    raise HelpPrasingError("Help for command is not provided")
                self.help.add_command(command_name, help)

            if allow_without_prefix:
                self.message(Filters.text & ~Filters.command)(f)

        return w

    def message(self, filters: Filters) -> Callable:
        """Decorator for message callback function based on filters.

        Usage
        -----
            @bot.message(telegram.ext.filters.Filters.*)
            def callback_function(update, context):
                ...
        """

        return lambda f: self.add_handler(MessageHandler(filters, f))

    def message_regex(self, regex: Pattern) -> Callable:
        """Wrapper decorator for `self.message` used for handle messages
        by regexes.

        Usage
        -----
            @bot.message_regex("text or regex")
            def callback_function(update, context):
                ...
        """

        return lambda f: self.message(Filters.regex(regex))(f)

    def inline_query(self, f: Callable) -> None:
        """Decorator for inline query callback function.

        Usage
        -----
            @bot.inline_query
            def callback_function(query: telegrask.InlineQuery):
                # update, context = query.update, query.context
                ...
        """

        # Handle Update and CallbackContext and pass instance of InlineQuery class
        # as an argument for decorated function to avoid unnecessary code.
        self.add_handler(InlineQueryHandler(lambda u, c: f(InlineQuery(u, c))))

    def __help_command(self, update: Update, context: CallbackContext) -> None:
        """Send help message with description of each command."""

        update.message.reply_text(self.help.content, parse_mode=ParseMode.MARKDOWN)

    def custom_help_command(self, f: Callable) -> None:
        """Decorator to create custom help message instead generated by HelpParser.

        Usage
        -----
            @bot.custom_help_command
            def help_command(update, context, descriptions: dict):
                ...

            # @bot.custom_help_command is equivalent for:
            # @bot.command(["help", "start"], help="display this message")
            # with additional callback function parameter with commands descriptions
        """

        self.help.add_command("help", "display this message")
        self.add_handler(
            CommandHandler(
                ["help", "start"], lambda u, c: f(u, c, self.help.commands_descriptions)
            )
        )

    def run(self, debug: bool = False) -> None:
        """Start bot.

        Usage
        -----
            # execute at the end
            bot.run(debug=True)
        """

        if self.config["HELP_MESSAGE"]:
            self.command(["help", "start"], help="display this message")(
                self.__help_command
            )

        if debug:
            import logging

            logging.basicConfig(
                format="%(levelname)s - %(message)s", level=logging.DEBUG
            )
            logging.getLogger(__name__)

        self.updater.start_polling()
        self.updater.idle()
