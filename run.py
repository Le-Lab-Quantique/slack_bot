import os

from src import flask_app

if __name__ == "__main__":
    flask_app.run(port=int(os.environ.get("PORT", 3100)), debug=True)
