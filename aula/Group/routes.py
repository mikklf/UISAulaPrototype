from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_required
from aula.models import select_users
import sys, datetime

Group = Blueprint('Group', __name__)

@Group.route("/groups/index", methods=['GET'])
def index():
    user = select_users(5000)
    return user.address

