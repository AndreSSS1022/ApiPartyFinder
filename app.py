"""
Archivo principal de la aplicación Flask.
Configura la conexión a MySQL, JWT y registra los blueprints de los controladores.
"""

import os
import logging
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flasgger import Swagger

from controllers.user_controller import user_bp
from controllers.bar_controller import bar_bp
from controllers.reservation_controller import reservation_bp
from controllers.availability_controller import availability_bp
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
    "title": "PartyFinder API",
    "uiversion": 3,
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "PartyFinder API",
        "description": "API RESTful para sistema de reservas de bares con Flask, SQLAlchemy y JWT.",
        "version": "2.0.0",
    },
    "basePath": "/",
    "schemes": ["http", "https"],
    "consumes": ["application/json"],
    "produces": ["application/json"],
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
# Construir la URL de conexión a MySQL con las variables de Railway
if (
    os.getenv("MYSQLHOST")
    and os.getenv("MYSQLUSER")
    and os.getenv("MYSQLPASSWORD")
    and os.getenv("MYSQLDATABASE")
):
    db_url = (
        f"mysql+pymysql://{os.getenv('MYSQLUSER')}:{os.getenv('MYSQLPASSWORD')}"
        f"@{os.getenv('MYSQLHOST')}:{os.getenv('MYSQLPORT','3306')}/{os.getenv('MYSQLDATABASE')}"
    )
else:
    # Fallback si no hay variables (por ejemplo, local)
    db_url = "sqlite:///app.db"

if not db_url:
    logger.warning("MYSQL_URL no definido. Usando SQLite local 'sqlite:///app.db'.")
    db_url = "sqlite:///app.db"

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
app.register_blueprint(bar_bp)
app.register_blueprint(reservation_bp)
app.register_blueprint(availability_bp)

logger.info("Blueprints registrados:")
logger.info("- Usuarios")
logger.info("- Electrodomésticos")
logger.info("- Bares")
logger.info("- Reservas")
logger.info("- Disponibilidad")

# =========================
# Rutas utilitarias
# =========================
@app.route("/health")
def health():
    return {"status": "ok", "version": "2.0.0"}, 200


@app.route("/")
def index():
    return (
        {
            "api": "PartyFinder API",
            "version": "2.0.0",
            "status": "OK",
            "description": "API RESTful para sistema de reservas de bares.",
            "endpoints": {
                "POST /users/register": "Registro de usuario",
                "POST /users/login": "Login y obtención de JWT",
                "GET /users/": "Listado de usuarios (requiere JWT)",
                "GET /bars/": "Listado de bares",
                "GET /bars/<id>": "Detalle de bar",
                "POST /bars/": "Crear bar (requiere JWT)",
                "POST /reservations/": "Crear reserva (requiere JWT)",
                "GET /reservations/my-reservations": "Mis reservas (requiere JWT)",
                "PUT /reservations/<id>/cancel": "Cancelar reserva (requiere JWT)",
                "POST /availability/": "Crear disponibilidad (requiere JWT)",
                "POST /availability/bulk": "Crear disponibilidad múltiple (requiere JWT)",
                "GET /availability/bar/<id>": "Consultar disponibilidad de bar",
                "GET /": "Información de la API",
                "GET /health": "Health check",
                "GET /apidocs": "Documentación Swagger"
            },
        },
        200,
    )

# =========================
# Creación de tablas
# =========================
def create_tables_if_not_exist() -> None:
    """Crea las tablas definidas en modelos que heredan de db.Model."""
    with app.app_context():
        # Importar todos los modelos antes de crear tablas
        from models.user import User
        from models.bar import Bar
        from models.availability import Availability
        from models.reservation import Reservation
        
        db.create_all()
        logger.info("Tablas creadas en la base de datos")

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