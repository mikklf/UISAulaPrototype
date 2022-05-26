from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_required
from aula.models import *
import sys, datetime

Group = Blueprint('Group', __name__)

@Group.route("/groups", methods=['GET'])
def index():
    groups = current_user.get_groups_joinable()
    return render_template('groups.html', groups=groups)

@Group.route("/group/<int:group_id>", methods=['GET'])
def show(group_id):
    group = get_group(group_id)
    if (group is not None):
        return render_template('group_show.html', group=group)
    else:
        return "Der findes ingen gruppe med det id"

