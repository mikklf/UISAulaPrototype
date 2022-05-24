from flask import render_template, url_for, flash, redirect, request, Blueprint
from bank import app, conn, bcrypt
from aula.forms import TransferForm, DepositForm, AddCustomerForm
from flask_login import current_user, login_required
import sys, datetime

Group = Blueprint('Threads', __name__)

@login_required()
@Group.route("threads/index", methods=['GET'])
def index():
    return render_template()
