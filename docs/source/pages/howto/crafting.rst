Crafting your Commands
======================

As show in the :ref:`getting_started` session, designing your own application is pretty
straightforward. In this section it will be further explained how to design commands
that suite your needs.

Functions and methods
---------------------

cmdcraft supports both free functions and class methods as callables.

Typing
------

It is highly recommended to use annotations in the callable parameters. This way, the
prompt will be cast to types.