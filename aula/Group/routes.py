from flask import render_template, Blueprint, flash, redirect
from flask_login import current_user, login_required
from aula.models import get_group, insert_group, group_exist
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
    
    # Make sure we dont try to create group with same name as others
    # Since name has UNIQUE constraint.
    if group_exist(form.title.data):
        flash('En gruppe med det navn findes allerede', 'danger')
        return redirect(f"/groups")

    group = insert_group(form.title.data, form.mandatory.data)
    current_user.join_group(group.group_id)
    flash('Gruppen blev oprettet', 'success')
    return redirect(f"/groups")

@Group.route("/groups/join/<int:group_id>", methods=['GET'])
def join(group_id):
    group = get_group(group_id)

    current_user.join_group(group_id)
    flash(f'Du er nu tilmeldt {group.name} gruppen', 'success')
    return redirect(f"/groups/{group_id}")

@Group.route("/groups/leave/<int:group_id>", methods=['GET'])
def leave(group_id):
    group = get_group(group_id)

    current_user.leave_group(group_id)
    flash(f'Du er frameldt {group.name} gruppen', 'success')
    return redirect(f"/groups")