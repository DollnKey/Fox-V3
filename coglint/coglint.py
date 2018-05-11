import discord
from discord.ext import commands
from redbot.core import Config, checks, RedContext

from redbot.core.bot import Red

from pylint import epylint as lint
from redbot.core.data_manager import cog_data_path


class CogLint:
    """
    V3 Cog Template
    """

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=9811198108111121, force_registration=True)
        default_global = {
            "lint": True
        }
        default_guild = {}

        self.path = str(cog_data_path(self)).replace('\\', '/')

        self.counter = 0

        # self.answer_path = self.path + "/tmpfile.py"

        self.config.register_global(**default_global)
        self.config.register_guild(**default_guild)

    @commands.command()
    async def autolint(self, ctx: RedContext):
        """Toggles automatically linting code"""

    @commands.command()
    async def lint(self, ctx: RedContext, *, code):
        """Lint python code"""
        await self.lint_message(ctx.message)
        await ctx.send("Hello World")

    async def lint_code(self, code):
        self.counter += 1
        path = self.path + "/{}.py".format(self.counter)
        with open(path, 'w') as codefile:
            codefile.write(code)

        future = await self.bot.loop.run_in_executor(None, lint.py_run, path, 'return_std=True')

        if future:
            (pylint_stdout, pylint_stderr) = future
        else:
            (pylint_stdout, pylint_stderr) = None, None

        # print(pylint_stderr)
        # print(pylint_stdout)

        return pylint_stdout, pylint_stderr

    async def lint_message(self, message):
        code_blocks = message.content.split('```')[1::2]

        for c in code_blocks:
            is_python, code = c.split(None, 1)
            is_python = is_python.lower() == 'python'
            if is_python:  # Then we're in business
                linted, errors = await self.lint_code(code)
                linted = linted.getvalue()
                errors = errors.getvalue()
                await message.channel.send(linted)
                # await message.channel.send(errors)

    async def on_message(self, message: discord.Message):
        await self.lint_message(message)
