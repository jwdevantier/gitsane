import typer
from typing import Optional

import gitsane.commands.branch
import gitsane.commands.stash
import gitsane.commands.tags
import gitsane.commands.commit
import gitsane.commands.remote
from gitsane.config import config
from gitsane.utils import run


app = typer.Typer(no_args_is_help=True)
app.add_typer(
    gitsane.commands.branch.app,
    name="branch",
    help="manage branches")

app.add_typer(
    gitsane.commands.remote.app,
    name="remote",
    help="manage remotes")

app.add_typer(
    gitsane.commands.stash.app,
    name="stash",
    help="manage stashes")


app.add_typer(
    gitsane.commands.tags.app,
    name="tags",
    help="manage tags")


app.add_typer(
    gitsane.commands.commit.app,
    name="commit",
    help="mangle commits")


@app.callback()
def _pre_command(dry_run: bool = False):
    config.dry_run = dry_run
    pass


@app.command(name="clone", no_args_is_help=True)
def git_clone(
        url: str = typer.Argument(..., help="URL of repository, whether a remote URL or local directory"),
        dest: Optional[str] = typer.Argument(None, help="name the local directory"),
        branch: Optional[str] = typer.Option(None, help="specify what branch to check out"),
        remote_name: str = typer.Option("origin", help="specify what to call the default remote"),
        with_submodules: bool = typer.Option(False, help="if true, recursively clone all submodules as well")):
    """clone repository"""
    cmd = ["git"]
    if branch is not None:
        cmd.extend(["--branch", branch])
    if remote_name:
        cmd.extend(["--origin", remote_name])
    if with_submodules:
        cmd.append("--recurse-submodules")
    cmd.append(url)
    if dest:
        cmd.append(dest)
    run(cmd)


@app.command(name="log")
def git_log(verbose: bool = typer.Option(False, help="show commit message, date and so on")):
    """display commit log"""
    if verbose:
        run(["git", "log"])
    else:
        run(["git", "--pretty=oneline", "log"])


def main():
    app()


if __name__ == "__main__":
    main()
