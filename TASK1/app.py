from flask import Flask
from flask_login import LoginManager
from models import db, User
from routes.auth import auth_bp
from routes.blog import blog_bp
from routes.comments import comments_bp

from flask import Flask, render_template

import pymysql
pymysql.install_as_MySQLdb()


app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(auth_bp)
app.register_blueprint(blog_bp)
app.register_blueprint(comments_bp)

@app.route('/')
def home():
    blog = {"title": "Sample Blog"}
    comments = [
        {"user": "Alice", "text": "Nice post!"},
        {"user": "Bob", "text": "Thanks for sharing."}
    ]
    return render_template('index.html', blog=blog, comments=comments)

if __name__ == '__main__':
    app.run(debug=True)
