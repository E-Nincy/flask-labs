import random
from faker import Faker
from app import db
from app.models import User, TodoList, Todo

fake = Faker("en_US")

def clear_db():
    Todo.query.delete()
    TodoList.query.delete()
    User.query.delete()
    db.session.commit()

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

def generate_todolists(users, num_lists=100):
    todolists = []
    for _ in range(num_lists):
        user = random.choice(users)
        tl = TodoList(
            title=fake.sentence(nb_words=3),
            creator=user.username
        )
        db.session.add(tl)
        todolists.append(tl)
    db.session.commit()
    return todolists

def generate_tasks(todolists, min_tasks=5, max_tasks=75):
    for tl in todolists:
        for _ in range(random.randint(min_tasks, max_tasks)):
            t = Todo(
                description=fake.sentence(),
                todolist_id=tl.id,
                creator=tl.creator
            )
            t.is_finished = random.choice([True, False])
            db.session.add(t)
    db.session.commit()

def generate_all():
    clear_db()
    users = generate_users(10)
    todolists = generate_todolists(users, 200)
    generate_tasks(todolists, 5, 75)
    print("✅ Database filled successfully.")
