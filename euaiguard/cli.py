# import typer

# app = typer.Typer()


# @app.callback()
# def main():
#     print("Hello from EU AI Guard")


# if __name__ == "__main__":
#     app()
import typer

app = typer.Typer()


@app.callback(invoke_without_command=True)
def main():
    print("Hello from EU AI Guard")


if __name__ == "__main__":
    app()