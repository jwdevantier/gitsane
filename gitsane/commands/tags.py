import typer
from gitsane.utils import run, command


app = typer.Typer(no_args_is_help=True)

# NOT supporting lightweight tags
# TODO: should support creating a tag from a commit


@command(app, name="add", no_args_is_help=True)
def tags_create(tag: str = typer.Argument(..., help="name of tag"),
                message: str = typer.Argument(..., help="\"commit\" message of tag (opens editor if omitted)"),
                commit: str = typer.Argument(None, help="commit hash to tag (otherwise tagging HEAD)")):
    """tag commit"""
    cmd = ["git", "tag", "-a", tag, "-m", message]
    if commit:
        cmd.append(commit)
    run(cmd)


@command(app, name="remove", alias="rm", no_args_is_help=True)
def tags_delete(tag: str = typer.Argument(..., help="name of tag to delete"),
                remote: str = typer.Argument(None, help="if provided, delete tag on remote")):
    """remove local or remote tag"""
    if remote:
        run(["git", "push", remote, "--delete", tag])
    else:
        run(["git", "tag", "-d", tag])


@command(app, name="view", alias="v", no_args_is_help=True)
def tags_show(tag: str = typer.Argument(..., help="tag to view")):
    """view tag details (tagger, date, message etc)"""
    run(["git", "show", tag])


@command(app, name="push", alias="p", no_args_is_help=True)
def tags_push(tag: str = typer.Argument(..., help="tag to push to remote"),
              remote: str = typer.Argument(..., help="remote to push the tag to")):
    """push local tag to remote"""
    run(["git", "push", remote, tag])
