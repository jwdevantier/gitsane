import subprocess
import rich
from gitsane.config import config
import typer
from typer.main import CommandFunctionType, CommandInfo
from typing import List, Optional, Callable
import sys


def _prefix_alias_str(help: str, alias: str) -> str:
    help_lst = help.split("\n")
    help_lst[0] = f"[\033[1;35m\033[1m{alias}\033[0m] {help_lst[0]}"
    return "\n".join(help_lst)


def add_typer_with_alias(parent: typer.Typer, child: typer.Typer, name: str, alias: str, **kwargs):
    kwargs["help"] = _prefix_alias_str(kwargs.get("help", ""), alias)
    parent.add_typer(child, **kwargs, name=name)
    parent.add_typer(child, **kwargs, name=alias, hidden=True)


def command(app: typer.Typer, alias: Optional[str] = None, **kwargs)\
        -> Callable[[CommandFunctionType], CommandFunctionType]:
    def decorator(fn: CommandFunctionType) -> CommandFunctionType:
        app.registered_commands.append(
            CommandInfo(**kwargs, callback=fn)
        )
        if not alias:
            return fn

        help = getattr(fn, "__doc__", None)
        if help and not getattr(fn, "__help_str_set__", False):
            setattr(fn, "__doc__", _prefix_alias_str(help, alias))
            setattr(fn, "__help_str_set__", True)

        # merge kwargs and dict to effectively override previously defined keys
        # do NOT merge `callback=fn` -- this causes an error to occur if the
        # caller attempts setting this key - which we don't want them to do.
        cmd_info = CommandInfo(**{
            **kwargs,
            **{"name": alias,
               "hidden": True}},
                               callback=fn,
                               )
        app.registered_commands.append(cmd_info)
        return fn
    return decorator


def run(cmd, exit_on_error=True, capture=False, **kwargs) -> subprocess.CompletedProcess:
    if "dry_run" in kwargs:
        dry_run = kwargs["dry_run"]
        del kwargs["dry_run"]
    else:
        dry_run = config.dry_run

    if not "check" in kwargs:
        kwargs["check"] = True

    if capture:
        kwargs["stdout"] = subprocess.PIPE
        kwargs["stderr"] = subprocess.STDOUT

    if not "encoding" in kwargs:
        kwargs["encoding"] = "utf-8"

    if dry_run:
        rich.print(f"""[bold purple]> [/]{" ".join(cmd)} (dry run)""")
    else:
        rich.print(f"""[bold purple]> [/]{" ".join(cmd)}""")
        try:
            return subprocess.run(cmd, **kwargs)
        except subprocess.CalledProcessError as e:
            if exit_on_error:
                sys.exit(e.returncode)
            raise e
