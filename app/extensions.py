from flask_selfdoc import Autodoc
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
cache = Cache()
auto = Autodoc()
jwt = JWTManager()
