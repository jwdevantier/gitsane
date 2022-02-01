from dataclasses import dataclass


@dataclass
class Config:
    dry_run: bool = False


config = Config()