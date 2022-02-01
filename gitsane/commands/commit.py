import typer
from gitsane.utils import run


app = typer.Typer(no_args_is_help=True)


@app.command(name="revert")
def commit_revert(hard: bool = typer.Argument(False, help="discard changes entirely if true")):
    """revert/undo commit, add --hard to discard changes permanently"""
    if hard:
        run(["git", "reset", "--hard", "HEAD~1"])
    else:
        run(["git", "reset", "--soft", "HEAD~1"])


if __name__ == "__main__":
    app()
