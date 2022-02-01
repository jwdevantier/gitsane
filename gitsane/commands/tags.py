import typer
from gitsane.utils import run


app = typer.Typer(no_args_is_help=True)

# NOT supporting lightweight tags
# TODO: should support creating a tag from a commit


@app.command(name="create", no_args_is_help=True)
def tags_create(tag: str = typer.Argument(..., help="name of tag"),
                message: str = typer.Argument(..., help="\"commit\" message of tag (opens editor if omitted)"),
                commit: str = typer.Argument(None, help="commit hash to tag (otherwise tagging HEAD)")):
    """create tag"""
    cmd = ["git", "tag", "-a", tag, "-m", message]
    if commit:
        cmd.append(commit)
    run(cmd)


@app.command(name="delete", no_args_is_help=True)
def tags_delete(tag: str = typer.Argument(..., help="name of tag to delete"),
                remote: str = typer.Argument(None, help="if provided, delete tag on remote")):
    """delete local or remote tag"""
    if remote:
        run(["git", "push", remote, "--delete", tag])
    else:
        run(["git", "tag", "-d", tag])


@app.command(name="show", no_args_is_help=True)
def tags_show(tag: str = typer.Argument(..., help="tag to view")):
    """show tag details (tagger, date, message etc)"""
    run(["git", "show", tag])


@app.command(name="push", no_args_is_help=True)
def tags_push(tag: str = typer.Argument(..., help="tag to push to remote"),
              remote: str = typer.Argument(..., help="remote to push the tag to")):
    """push local tag to remote"""
    run(["git", "push", remote, tag])
