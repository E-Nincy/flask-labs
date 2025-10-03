from flask import Blueprint, render_template, redirect, url_for, flash, request
from .forms import TodoListForm, TodoForm
from app import db
from app.models import TodoList, Todo
from app.main.forms import NewTodoListForm

main = Blueprint('main', __name__)

@main.route('/')
def index():
    form = TodoListForm()

    page = request.args.get('page', 1, type=int)
    pagination = TodoList.query.order_by(TodoList.created_at.desc()).paginate(page=page, per_page=10)
    todolists = pagination.items

    for todolist in todolists:
        open_query = Todo.query.filter_by(todolist_id=todolist.id, is_finished=False)
        finished_query = Todo.query.filter_by(todolist_id=todolist.id, is_finished=True)

        open_page = request.args.get(f'open_page_{todolist.id}', 1, type=int)
        finished_page = request.args.get(f'finished_page_{todolist.id}', 1, type=int)

        todolist.open_pagination = open_query.paginate(page=open_page, per_page=10)
        todolist.finished_pagination = finished_query.paginate(page=finished_page, per_page=10)

    return render_template('index.html', form=form, todolists=todolists, pagination=pagination)

@main.route('/new_todolist', methods=['POST'])
def new_todolist():
    form = TodoListForm()
    if form.validate_on_submit():
        flash(f"Todolist '{form.title.data}' created!", "success")
        return redirect(url_for('main.index'))
    flash("Error: could not create todolist", "danger")
    return redirect(url_for('main.index'))

from flask_login import login_required, current_user

from app.main.forms import NewTodoListForm

@main.route('/todolists', methods=['GET', 'POST'])
def todolist_overview():
    form = NewTodoListForm()
    todolists = TodoList.query.all()

    if form.validate_on_submit():
        new_list = TodoList(title=form.title.data, user_id=current_user.id)
        db.session.add(new_list)
        db.session.commit()
        return redirect(url_for('main.todolist_overview'))

    return render_template('todolists.html', current_user=current_user, form=form, todolists=todolists)


@main.route('/todolist/<int:id>')
@login_required
def show_todolist(id):
    todolist = TodoList.query.get_or_404(id)
    
    # paginate the open and finish ones
    open_todos = todolist.todos.filter_by(done=False).paginate(
        page=request.args.get('open_page', 1, type=int),
        per_page=5
    )
    finished_todos = todolist.todos.filter_by(done=True).paginate(
        page=request.args.get('finished_page', 1, type=int),
        per_page=5
    )

    form = TodoForm()

    return render_template(
        'todolist.html',
        todolist=todolist,
        open_todos=open_todos,
        finished_todos=finished_todos,
        form=form
    )
