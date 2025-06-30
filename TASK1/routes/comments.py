from flask import Blueprint, request, redirect
from models import db, Comment

comments_bp = Blueprint('comments', __name__)

@comments_bp.route('/comment/<int:blog_id>', methods=['POST'])
def add_comment(blog_id):
    text = request.form['text']
    user = request.form['user']
    comment = Comment(text=text, blog_id=blog_id, user=user)
    db.session.add(comment)
    db.session.commit()
    return redirect('/')
