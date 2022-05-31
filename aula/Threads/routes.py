from flask import render_template, Blueprint
from flask_login import login_required, current_user
from aula.models import get_thread

Threads = Blueprint('Threads', __name__)

@Threads.route("/threads", methods=['GET'])
@login_required
def threads():
    threads_data = current_user.get_threads()
    return render_template("threads.html", threads=threads_data)

@Threads.route("/threads/<int:thread_id>", methods=['GET'])
@login_required
def show(thread_id):
    thread = get_thread(thread_id)
    if thread is None:
        return f"Der findes ikke en tråd med id {thread_id}."
    elif not current_user.in_thread(thread_id):
        return f"Du har ikke adgang til tråden med id {thread_id}."
    else:
        return render_template("thread_show.html", thread=thread, messages=thread.get_messages())
