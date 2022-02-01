import typer
from gitsane.utils import run

app = typer.Typer(no_args_is_help=True)


@app.command(name="list")
def remote_list(verbose: bool = typer.Option(True, help="show fetch & push urls")):
    if verbose:
        run(["git", "remote", "--verbose"], dry_run=False)
    else:
        run(["git", "remote"], dry_run=False)


@app.command(name="add")
def remote_add(name: str = typer.Argument(..., help="name of remote"),
               url: str = typer.Argument(..., help="URL of remote")):
    run(["git", "remote", "add", name, url])


@app.command(name="remove")
def remote_remove(remote: str = typer.Argument(..., help="name of remote")):
    run(["git", "remote", "remove", remote])


@app.command(name="rename")
def remote_rename(remote: str = typer.Argument(..., help="name of existing remote"),
                  new: str = typer.Argument(..., help="new name of remote")):
    """rename remote (remote rename <remote> <new-name>)"""
    run(["git", "remote", "rename", remote, new])
