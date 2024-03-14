from src.slack import actions
from src.slack import commands
from src.slack import shortcuts
from src.slack import views


def register_listeners(app):
    actions.register(app)
    commands.register(app)
    shortcuts.register(app)
    views.register(app)
