Handlers Decorators
===================

Each handler decorator is a child method of ``Telegrask`` class, so you need to have an object of this class first.

.. code-block:: python

    from telegram import Update
    from telegram.ext import CallbackContext

    bot = Telegrask("TOKEN")

@command
--------

Handler for commands (messages starting with ``/`` prefix, e.g. ``/cmd``).

.. code-block:: python

    @bot.command("command_name", help="command help message")
    def callback_function(update: Update, context: CallbackContext):
        pass

Parameters:
    * ``commands: Union[str, list]`` - command or list of commands which will use this function as callback
    * ``help: str`` - description for command which will be included in automaticly generated ``/help`` command message
    * ``allow_without_prefix: bool = False`` - handle command also without ``/`` prefix, e.g. ``/cmd`` and ``cmd``


@message
--------

Handler for messages.

.. code-block:: python

    from telegram.ext import Filters

    @bot.message(...)
    def callback_function(update: Update, context: CallbackContext):
        pass

Parameters:
    * ``filters: Filters`` - any combination of ``Filters`` from python-telegram-bot library


@message_regex
--------------

Handler for messages by regexes instead of filters.

.. code-block:: python

    @bot.message_regex(r"regex or just text")
    def callback_function(update: Update, context: CallbackContext):
        pass

Parameters:
    * ``regex: Pattern`` - regular expression to filter a message or just text


@inline_query
-------------

Handler for inline queries.

.. code-block:: python

    from telegrask import InlineQuery

    @bot.inline_query
    def inline(query: InlineQuery):
        pass