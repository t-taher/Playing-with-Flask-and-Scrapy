from itsdangerous import TimedJSONWebSignatureSerializer as srial
from mysite import db, login_manager,app
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    p_img = db.Column(db.String(8), nullable=False, default="3zma.jpg")
    posts = db.relationship("Post", backref='author', lazy=True)

    def rest(self, sec=1800):
        s = srial(app.config['SECRET_KEY'], sec)
        return s.dumps({'user_id': self.id}).decode("utf-8")

    @staticmethod
    def verify(token):
        s = srial(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    post = db.Column(db.String(250), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
