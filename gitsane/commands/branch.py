from typing import Optional
import typer
from gitsane.utils import run


def callback():
    # typer.echo("branch callback")
    pass


app = typer.Typer(callback=callback, no_args_is_help=True)


@app.command(name="rename", no_args_is_help=True)
def branch_rename(existing: str = typer.Argument(..., help="current name of branch"),
                  new: str = typer.Argument(..., help="new name of branch"),
                  remote: Optional[str] = typer.Argument(None, help="(if provided) rename remote instead of local branch")):
    """rename local or remote branch"""
    if remote:
        # TODO: verify!
        run(["git", "push", remote, f":{existing}", new])
    else:
        run(["git", "branch", "-m", existing, new])


@app.command(name="push", no_args_is_help=True)
def branch_push(branch: str = typer.Argument(..., help="branch to push"),
                remote: str = typer.Argument(..., help="remote to push branch to"),
                alias: Optional[str] = typer.Argument(None, help="(if provided) alternate name of branch on remote"),
                force: bool = typer.Option(False, help="force operation, even if otherwise rejected")):
    """push branch to remote"""
    cmd = ["git", "push"]
    if force:
        cmd.append("--force")
    cmd.append(remote)
    cmd.append(f"{branch}:{alias}" if alias else branch)
    run(cmd)


@app.command(name="new", no_args_is_help=True)
def branch_new(branch: str = typer.Argument(..., help="name of new branch"),
               remote: Optional[str] = typer.Argument(None, help="remote"),
               from_branch: Optional[str] = typer.Argument(None, help="(if provided) name of branch on remote")):
    """create new branch from current or some remote branch.

    \b
    * `gitsane branch new <branch>`
        * create branch `new` from current branch
    * `gitsane branch new <branch> <remote>`
        * checkout branch <branch> from remote <remote> to <branch>
    * `gitsane branch new branch remote <from-branch>`
        * checkout branch <from-branch> from remote <remote> to <branch>

    NOTE: to create a branch from another local branch, see `gitsane branch cp <old> <new>`"""
    if remote:
        run(["git", "checkout", "-b", branch, f"{remote}/{from_branch or branch}"])
    else:
        run(["git", "checkout", "-b", branch])


@app.command(name="fork", no_args_is_help=True)
def branch_fork(source: str = typer.Argument(..., help="name of existing branch or tag"),
                name: str = typer.Argument(..., help="name of new branch")):
    """create new branch from (different, not current) existing branch"""
    run(["git", "checkout", "-b", name, source])


@app.command(name="checkout", no_args_is_help=True)
def branch_checkout(branch: str):
    """switch to different (existing) branch."""
    run(["git", "checkout", branch])


@app.command(name="delete", no_args_is_help=True)
def branch_delete(branch: str = typer.Argument(..., help="name of branch to remove"),
                  remote: Optional[str] = typer.Argument(None, help="(if provided) remove branch from remote instead of locally")):
    """delete local or remote branch"""
    if remote:
        run(["git", "push", remote, "--delete", branch])
    else:
        run(["git", "branch", "-D", branch])


@app.command(name="list")
def branch_list(all: bool = typer.Option(False, help="show both local and remote branches")):
    """list existing branches"""
    if all:
        run(["git", "branch", "--all"], dry_run=False)
    else:
        run(["git", "branch"], dry_run=False)


if __name__ == "__main__":
    app()
