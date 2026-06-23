import typer

app = typer.Typer()

@app.command()
def init():
    print("Welcome to Eu AI Guard")
    
@app.command()
def report():
    print("Report Generating...")


if __name__ == "__main__":
    app()