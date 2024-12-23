from flask import Flask
from routes.auth import auth_bp
from routes.tasks import tasks_bp

app = Flask(__name__)

# Configuración inicial
app.secret_key = "admin"

# Registrar blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(tasks_bp)

# Ruta principal
@app.route('/')
def index():
    return "Bienvenido a Task Manager"

if __name__ == '__main__':
    app.run(debug=True)
