from flask import Flask
from config import Config
from models import db
from auth import auth_bp
from products import product_bp
from orders import order_bp
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(auth_bp)
app.register_blueprint(product_bp)
app.register_blueprint(order_bp)

# No decorators needed for table creation
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
