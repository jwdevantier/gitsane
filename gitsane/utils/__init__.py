import subprocess
import rich
from gitsane.config import config
import typer
from typing import List
import sys


def add_typer_with_aliases(parent: typer.Typer, child: typer.Typer, name: str, aliases: List[str], **kwargs):
    parent.add_typer(child, **kwargs, name=name)
    for alias in aliases:
        parent.add_typer(child, **kwargs, name=alias, hidden=True)


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
