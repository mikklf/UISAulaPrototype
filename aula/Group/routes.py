from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_required
from aula.models import select_users_by_id
import sys, datetime

Group = Blueprint('Group', __name__)

@Group.route("/groups/index", methods=['GET'])
def index():
    groups = current_user.get_groups()
    return render_template('groups.html', groups=groups)

