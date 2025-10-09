"""
"""
from flask_reddit import db
from flask_reddit.users import constants as USER
from flask_reddit.threads.models import thread_upvotes, comment_upvotes
from sqlalchemy import select, and_, func


user_subscriptions = db.Table('user_subscriptions',
    db.Column('user_id', db.Integer, db.ForeignKey('users_user.id'), primary_key=True),
    db.Column('subreddit_id', db.Integer, db.ForeignKey('subreddits_subreddit.id'), primary_key=True)
)

class User(db.Model):
    """
    """
    __tablename__ = 'users_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(USER.MAX_USERNAME), unique=True)
    email = db.Column(db.String(USER.MAX_EMAIL), unique=True)
    password = db.Column(db.String(USER.MAX_PASSW))
    created_on = db.Column(db.DateTime, default=db.func.now())

    threads = db.relationship('Thread', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')
    subreddits = db.relationship('Subreddit', backref='user', lazy='dynamic')
    
    upvoted_threads = db.relationship('Thread', secondary=thread_upvotes,
                                  backref=db.backref('voters', lazy='dynamic'))

    subscriptions = db.relationship('Subreddit', secondary=user_subscriptions,
                                backref=db.backref('subscribers', lazy='dynamic'))

    status = db.Column(db.SmallInteger, default=USER.ALIVE)
    role = db.Column(db.SmallInteger, default=USER.USER)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.username)

    def get_status(self):
        """
        returns string form of status, 0 = 'dead', 1 = 'alive'
        """
        return USER.STATUS[self.status]

    def get_role(self):
        """
        analogous to above but for roles
        """
        return USER.ROLE[self.role]

    def get_thread_karma(self):
        """
         Fetch the number of upvotes this user has received on their threads,
        excluding their own votes.
        """
        thread_ids = [t.id for t in self.threads]

        if not thread_ids:
            return 0

        stmt = select(func.count()).select_from(thread_upvotes).where(
            and_(
                thread_upvotes.c.thread_id.in_(thread_ids),
                thread_upvotes.c.user_id != self.id,
                thread_upvotes.c.vote_type == 'up'
            )
        )

        result = db.session.execute(stmt).scalar()  # devuelve el número directamente
        return result or 0

    def get_comment_karma(self):
        """
        Fetch the number of upvotes this user has received on their comments,
        excluding their own votes.
        """
        comment_ids = [c.id for c in self.comments]

        if not comment_ids:
            return 0

        stmt = select(func.count()).select_from(comment_upvotes).where(
            and_(
                comment_upvotes.c.comment_id.in_(comment_ids),
                comment_upvotes.c.user_id != self.id,
                comment_upvotes.c.vote_type == 'up'
            )
        )

        result = db.session.execute(stmt).scalar()  # devuelve el número directamente
        return result or 0


