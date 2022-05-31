from flask import render_template, Blueprint, flash, redirect
from flask_login import current_user, login_required
from aula.models import insert_post
from aula.forms import CreatePostForm

Post = Blueprint('Post', __name__)

@Post.route("/posts/create", methods=['POST'])
@login_required
def create():
    form = CreatePostForm()
    insert_post(form.group_id.data, form.author_id.data, form.title.data, form.content.data)
    flash('Opslag blev oprettet', 'success')
    return redirect(f"/groups/{form.group_id.data}")