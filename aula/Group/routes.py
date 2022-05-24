from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_required
from aula.models import select_users_by_id
import sys, datetime

Group = Blueprint('Group', __name__)

@Group.route("/groups", methods=['GET'])
def index():
    current_user.join_group(1000)
    groups = current_user.get_groups()
    return render_template('groups.html', groups=groups)

