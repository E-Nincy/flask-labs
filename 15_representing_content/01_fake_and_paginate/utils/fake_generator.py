import random
from faker import Faker
from app import db
from app.models import User, TodoList, Todo

fake = Faker("en_US")

def generate_users(n=10):
    users = []
    for _ in range(n):
        u = User(
            username=fake.user_name(),
            email=fake.email(),
            password="password123"
        )
        db.session.add(u)
        users.append(u)
    db.session.commit()
    return users

def generate_todolists(users, num_lists=75):
    todolists = []
    for user in users:
        for _ in range(num_lists // len(users)):
            tl = TodoList(
                title=fake.sentence(nb_words=3),
                creator=user.username
            )
            db.session.add(tl)
            db.session.commit() 
            todolists.append(tl)
    return todolists

def generate_tasks(todolists):
    for tl in todolists:
        num_tasks = random.randint(3, 8)
        for _ in range(num_tasks):
            t = Todo(
                description=fake.sentence(),
                todolist_id=tl.id,
                creator=tl.creator
            )
            t.is_finished = random.choice([True, False])
            db.session.add(t)
        db.session.commit() 

def generate_all():
    """
    Generate users, todo lists, and tasks to populate the database.
    """

    from app.models import User

    # We take all existing users
    users = User.query.all()
    if not users:
        users = generate_users()

    # Generate ToDolist
    todolists = generate_todolists(users)

    # Generate TASKS
    generate_tasks(todolists)

def clear_db():
    Todo.query.delete()
    TodoList.query.delete()
    User.query.delete()
    db.session.commit()