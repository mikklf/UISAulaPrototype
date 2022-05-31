from flask import render_template, Blueprint
from flask_login import current_user, login_required
from aula.models import get_group

Group = Blueprint('Group', __name__)

@Group.route("/groups", methods=['GET'])
@login_required
def groups():
    groups = current_user.get_groups_joinable()
    return render_template('groups.html', groups=groups)

@Group.route("/group/<int:group_id>", methods=['GET'])
@login_required
def show(group_id):
    group = get_group(group_id)
    posts = group.get_posts()
    if (group is not None):
        return render_template('group_show.html', group=group, posts=posts)
    else:
        return f"Der findes ikke en gruppe med id {group_id}."

