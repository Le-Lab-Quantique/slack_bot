import os

from src import create_app

app = create_app()

if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 3100)), debug=True)
