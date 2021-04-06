
from warships_blog import db, login_manager
from flask_login import UserMixin, login_user, current_user, logout_user, login_required, LoginManager


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class Ship(db.Model):        
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200))
    origin = db.Column(db.String(200))
    type_class = db.Column(db.String(200))
    tier_number = db.Column(db.Integer)
    max_velocity = db.Column(db.Integer)
    active = db.Column(db.Boolean)

class Tier(db.Model):
    
    tier_number = db.Column(db.String(5),  primary_key=True)
    cost_level = db.Column(db.String(200))

class Type(db.Model):
    type_class = db.Column(db.String(200), primary_key=True)
    full_name = db.Column(db.String(200))
    origin = db.Column(db.String(200))
    photo = db.Column(db.String(200))
    video = db.Column(db.String(200))
    countrys_owners = db.Column(db.String(200))
    wars = db.Column(db.String(200))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    email = db.Column(db.String(60))
    password = db.Column(db.String(50))

    def __repr__(self):
        return ("User")
        #return (f"User('{self.username}', '{self.email}')")

