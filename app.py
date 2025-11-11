import os
import logging
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flasgger import Swagger

from controllers.user_controller import user_bp
from models.db import db

# =========================
# Carga de entorno y logging
# =========================
load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

logger.info("Inicializando la aplicación Flask")
app = Flask(__name__)

# =========================
# Configuración Swagger
# =========================
app.config["SWAGGER"] = {
    "title": "FlaskAPIExample",
    "uiversion": 3,
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "FlaskAPIExample",
        "description": "API RESTful con Flask, SQLAlchemy, JWT y estructura modular.",
        "version": "1.0.0",
    },
    "basePath": "/",
    "schemes": ["http", "https"],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Usa 'Authorization: Bearer <token>'",
        }
    },
}
swagger = Swagger(app, template=swagger_template)

# =========================
# Configuración DB y JWT
# =========================
# Railway: usa MYSQL_URL directamente
db_url = os.getenv("MYSQL_URL")

if not db_url:
    logger.warning("Variable MYSQL_URL no definida. Usando SQLite local 'sqlite:///app.db'.")
    db_url = "sqlite:///app.db"
else:
    # Ajustar formato a SQLAlchemy (usa mysql+pymysql://)
    if db_url.startswith("mysql://"):
        db_url = db_url.replace("mysql://", "mysql+pymysql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "tu_clave_secreta_jwt")

jwt = JWTManager(app)
logger.info(f"Conexión a la base de datos: {app.config['SQLALCHEMY_DATABASE_URI']}")

# Inicializar extensiones
db.init_app(app)
logger.info("SQLAlchemy inicializado")

# =========================
# Blueprints
# =========================
app.register_blueprint(user_bp)
logger.info("Blueprint de usuarios registrado")

# =========================
# Rutas utilitarias
# =========================
@app.route("/health")
def health():
    return {"status": "ok"}, 200


@app.route("/")
def index():
    return (
        {
            "api": "FlaskAPIExample",
            "status": "OK",
            "description": "API RESTful con Flask, SQLAlchemy, JWT y estructura modular.",
            "author": "afmirandad",
            "endpoints": {
                "POST /users/register": "Registro de usuario",
                "POST /users/login": "Login y obtención de JWT",
                "GET /users/": "Listado de usuarios (requiere JWT)",
                "GET /": "Información de la API",
                "GET /health": "Health check",
            },
        },
        200,
    )

# =========================
# Creación de tablas
# =========================
def create_tables_if_not_exist() -> None:
    with app.app_context():
        db.create_all()
        logger.info("Tablas creadas en la base de datos (db.Model)")

create_tables_if_not_exist()

# =========================
# Manejo básico de errores
# =========================
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not Found", "msg": "Recurso no encontrado"}), 404

@app.errorhandler(500)
def server_error(e):
    logger.exception("Error interno no controlado")
    return jsonify({"error": "Internal Server Error", "msg": "Ocurrió un error interno"}), 500

if __name__ == "__main__":
    logger.info("Ejecutando como script principal")
