import typer

app = typer.Typer()

@app.command()
def init(
    project_name: str,
    verbose: bool = False
):
    """
    Initialize a new AI project for compliance tracking.
    """

    print(f"Project: {project_name}")
    
@app.command()
def report():
    print("Report Generating...")


if __name__ == "__main__":
    app()