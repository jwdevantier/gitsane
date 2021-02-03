import typer
from gitsane.utils import run, command
import re


def callback():
    pass


app = typer.Typer(callback=callback, no_args_is_help=True)

help_stash_id = "ID of stash (from `stash list`)"


@command(app, name="list", alias="ls")
def stash_list():
    """list existing stashes"""
    res = run(["git", "--no-pager", "stash", "list"], dry_run=False, capture=True)
    # replace 'stash{0}: <msg>' with '0: <msg>' (for stash 0)
    print(re.sub(r"^stash@{(\d+)\}:\s+(.+)$", r"\1: \2", res.stdout, flags=re.M))


@command(app, name="view", alias="v", no_args_is_help=True)
def stash_show(stash_id: int = typer.Argument(..., help=help_stash_id)):
    """show diff of given stash"""
    run(["git", "stash", "show", f"stash@{{{stash_id}}}"])


@command(app, name="remove", alias="rm", no_args_is_help=True)
def stash_drop(stash_id: int = typer.Argument(..., help=help_stash_id)):
    """drop/remove stash (careful!)"""
    run(["git", "stash", "drop", f"stash@{{{stash_id}}}"])


@command(app, name="apply", alias="a", no_args_is_help=True)
def stash_apply(stash_id: int = typer.Argument(..., help=help_stash_id)):
    """apply given stash to current working directory"""
    run(["git", "stash", "apply", f"stash@{{{stash_id}}}"])


@command(app, name="add", no_args_is_help=True)
def stash_save(message: str = typer.Argument(..., help="reminder, summary of stash contents")):
    """create stash from all uncommitted changes"""
    run(["git", "stash", "push", "-m", message])
