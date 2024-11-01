.. _getting_started:

Getting started
===============

Installation
------------

To install using ``pip``, use the following command:

::

    pip install cmdcraft

Your first application
----------------------

Once the package is properly installed on your system, you are ready to start
the first application using cmdcraft.

Start a new Python file (i.e. ``main.py``) with the following code snippet:

.. code:: python

    import asyncio
    from cmdcraft import Prompter

    async def test_input(prompt: str) -> None:
        print(f'The input is: {prompt}')

    async def main():
        prompt = Prompter()
        prompt.register_command(test_input)
        await prompt.run()

    asyncio.run(main())

Then, run the application:

::

    python main.py

You will be greet by the prompt in your terminal. Begin typing the command described by
the function ``test_input`` and you will see a autocomplete suggestion for the command.
Accept by pressing ``tab`` your finish typing. Then the parameter ``prompt`` might pop
as the next suggestion. You may then enter ``prompt=Hello``, or simply ``Hello``, as
this is a positional parameter. Upon pressing enter, the function output will be printed
on screen.