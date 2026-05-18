Crafting your Commands
======================

As show in the :ref:`getting_started` session, designing your own application is pretty
straightforward. In this section it will be further explained how to design commands
that suite your needs.

Recommendations
===============

Typing
------

It is highly recommended to use annotations in the callable parameters, so the prompt
arguments can be cast into said types. This will help you control and validate the input
your user inputs.

Command Grouping
================

Commands do not need to stay in a flat namespace. If your application has several
commands that would otherwise need long aliases such as ``project_status`` and
``project_config_set``, you may register them under a semantic path instead.

Both ``register_group()`` and ``register_command()`` treat whitespace as a path
separator:

- ``register_group("project config")`` means "register the group ``config`` under
  the group ``project``".
- ``register_command(set_value, alias="project config set")`` means "register the
  command ``set`` under the group path ``project -> config``".
- Registering the same group path more than once reuses the existing group,
  which lets sibling groups share the same parent naturally.
- Registering a command or group on a path that is already occupied raises
  ``ValueError``.

.. code:: python

    import asyncio
    from cmdcraft import Prompter

    async def start() -> None:
      print("project started")

    async def status() -> None:
      print("project status shown")

    async def show() -> None:
      print("project configuration shown")

    async def set_value(key: str, value: str) -> None:
      print(f"project configuration updated: {key}={value}")

    async def list_profiles() -> None:
      print("profiles: dev, test, prod")

    async def main() -> None:
        prompt = Prompter()

      project = prompt.register_group("project", doc="Project commands.")
      project.register_command(start)
      project.register_command(status)

      config = prompt.register_group(
        "project config",
        doc="Project configuration commands.",
      )
      config.register_command(show)
      prompt.register_command(set_value, alias="project config set")

      profiles = prompt.register_group(
        "project profile",
        doc="Project profile commands.",
      )
      profiles.register_command(list_profiles, alias="list")

        await prompt.run()

    asyncio.run(main())

This produces grouped commands such as ``project start``, ``project status``,
``project config show``, ``project config set theme dark`` and
``project profile list``. Re-registering grouped paths such as
``project config`` and ``project profile`` reuses the same ``project`` parent
group automatically.

The group path can be written either explicitly by chaining
``register_group()`` calls or with a spaced alias such as
``prompt.register_group("project config")``.

The runnable example in ``examples/group_commands.py`` demonstrates both styles.
