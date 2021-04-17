from warships_blog import db, login_manager, app
from flask_login import login_user, current_user, logout_user, login_required, LoginManager #UserMixin
from flask_user import SQLAlchemyAdapter, UserManager, UserMixin
from flask_user import roles_required

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
    roles = db.relationship('Role', secondary='user_roles',
            backref=db.backref('users', lazy='dynamic'))



class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))

    #db_adapter = SQLAlchemyAdapter(db,  User)
    #user_manager = UserManager(db_adapter, app)

    #if not User.query.filter(User.username=='admin').first():
    #    user1 = User(username='admin', email='admin@gmail.com', active=True,
    #            password=user_manager.hash_password('admin'))
    #    user1.roles.append(Role(name='admin'))
    #    db.session.add(user1)
    #    db.session.commit()    


    def __repr__(self):
        return ("User")
        #return (f"User('{self.username}', '{self.email}')")

