from flask import Blueprint, request, redirect, render_template
from flask_login import login_required, current_user
from models import db, Blog

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/create', methods=['POST'])
@login_required
def create_blog():
    data = request.form
    blog = Blog(title=data['title'], content=data['content'], author=current_user)
    db.session.add(blog)
    db.session.commit()
    return redirect('/')
