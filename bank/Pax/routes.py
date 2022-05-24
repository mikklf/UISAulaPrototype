from flask import render_template, url_for, flash, redirect, request, Blueprint
from bank import app, conn, bcrypt
from bank.forms import AddEmployeeForm
from flask_login import login_user, current_user, logout_user, login_required
from bank.models import select_all_Employees, insert_Employees

Pax = Blueprint('Pax', __name__)

posts = [{}]


@Pax.route("/test", methods=['GET', 'POST'])
def test():
    form = AddEmployeeForm()
    # Nedenstånde kode køres kun ved POST-forespørgsler:
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        id=form.id.data
        name=form.username.data
        password=hashed_password
        insert_Employees(id, name, password)
        flash('Employee has been created! The employee is now able to log in', 'success')
        return redirect(url_for('Login.home'))
    # Og denne køres GET-forespørgsler:
    employees = select_all_Employees()
    return render_template('test.html', title='Hej med dig', emp=employees, form=form)
