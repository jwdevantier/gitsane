import subprocess
import rich
from gitsane.config import config


def run(cmd, *args, **kwargs) -> subprocess.CompletedProcess:
    if "dry_run" in kwargs:
        dry_run = kwargs["dry_run"]
        del kwargs["dry_run"]
    else:
        dry_run = config.dry_run

    if not "check" in kwargs:
        kwargs["check"] = True

    if kwargs.get("capture"):
        del kwargs["capture"]
        kwargs["stdout"] = subprocess.PIPE
        kwargs["stderr"] = subprocess.STDOUT

    if not "encoding" in kwargs:
        kwargs["encoding"] = "utf-8"

    if dry_run:
        rich.print(f"""[bold purple]> [/]{" ".join(cmd)} (dry run)""")
    else:
        rich.print(f"""[bold purple]> [/]{" ".join(cmd)}""")
        return subprocess.run(cmd, *args, **kwargs)
