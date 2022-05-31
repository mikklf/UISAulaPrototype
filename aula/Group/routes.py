from flask import render_template, Blueprint, flash, redirect
from flask_login import current_user, login_required
from aula.models import get_group, insert_group
from aula.forms import CreateThreadForm, CreateGroupForm, CreatePostForm

Group = Blueprint('Group', __name__)

@Group.route("/groups", methods=['GET'])
@login_required
def groups():
    groups = current_user.get_groups_joinable()
    form = CreateGroupForm()
    return render_template('groups.html', groups=groups, form=form)

@Group.route("/groups/<int:group_id>", methods=['GET'])
@login_required
def show(group_id):
    group = get_group(group_id)
    posts = group.get_posts()
    threads = group.get_threads()
    form = CreateThreadForm()
    formpost = CreatePostForm()
    if (group is not None):
        return render_template('group_show.html', group=group, posts=posts, threads=threads, form=form, formpost=formpost)
    else:
        return f"Der findes ikke en gruppe med id {group_id}."

@Group.route("/groups/create", methods=['POST'])
@login_required
def create():
    form = CreateGroupForm()
    
    if insert_group(form.title.data, form.hidden.data):
        flash('Gruppen blev oprettet', 'success')
    else:
        flash('En gruppe med det navn findes allerede', 'danger')
    return redirect(f"/groups")