from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_required
from aula.models import select_users_by_id
import sys, datetime

Group = Blueprint('Group', __name__)

@Group.route("/groups/index", methods=['GET'])
def index():
    user = select_users_by_id(5000)
    groups = user.get_groups()
    for group in groups:
        print(group.name)
    return "hej"

