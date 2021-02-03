import typer
from gitsane.utils import run

app = typer.Typer(no_args_is_help=True)


@app.command(name="list")
def remote_list(verbose: bool = typer.Option(True, help="show fetch & push urls")):
    """display a list of configured remotes"""
    if verbose:
        run(["git", "remote", "--verbose"], dry_run=False)
    else:
        run(["git", "remote"], dry_run=False)


@app.command(name="add", no_args_is_help=True)
def remote_add(name: str = typer.Argument(..., help="name of remote"),
               url: str = typer.Argument(..., help="URL of remote")):
    """add remote to repository"""
    run(["git", "remote", "add", name, url])


@app.command(name="remove", no_args_is_help=True)
def remote_remove(remote: str = typer.Argument(..., help="name of remote")):
    """remove remote from repository"""
    run(["git", "remote", "remove", remote])


@app.command(name="rename", no_args_is_help=True)
def remote_rename(remote: str = typer.Argument(..., help="name of existing remote"),
                  new: str = typer.Argument(..., help="new name of remote")):
    """change the name used to refer to remote"""
    """rename remote (remote rename <remote> <new-name>)"""
    run(["git", "remote", "rename", remote, new])


@app.command(name="fetch")
def remote_fetch(remote: str = typer.Argument(None, help="name of remote to fetch from (all if omitted)")):
    """fetch (but do not apply) changes from remote"""
    if remote:
        run(["git", "fetch", remote])
    else:
        run(["git", "fetch", "--all"])
