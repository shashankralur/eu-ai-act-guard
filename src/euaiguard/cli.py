import typer

from src.euaiguard.commands.init import init
from src.euaiguard.commands.report import report

app = typer.Typer()

app.command()(init)
app.command()(report)

if __name__ == "__main__":
    app()