from app import create_app, db
from app.user_model import User
from app.task_model import Task

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Task': Task, 'User': User}