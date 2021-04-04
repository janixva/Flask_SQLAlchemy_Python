from flask import Flask, render_template, request, url_for, redirect, flash #jsonify
from flask_sqlalchemy import SQLAlchemy
#from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
#--flask wtf
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from flask_login import UserMixin, login_user, current_user, logout_user, login_required, LoginManager



#from flask_login import login_user, current_user, logout_user, login_required




app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/flask_warships'
app.config['SECRET_KEY'] = '8456984at5b1ace7gfs578fhdjs129e8'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/warship_jan.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#ma = Marshmallow(app)
bcrypt =Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


#clases ---------------------


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
        return f"User('{self.username}', '{self.email}')"



#-- Forms para login/register


#-Estas clases con variables las llamaremos en las paguinas que queramos hacer un formulario

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired("Introduce un nombre de usuario valido")])
    #email = StringField('Email', validators=[DataRequired("Introduce un mail valido"), Email()])
    password = PasswordField('Password', validators=[DataRequired("Contraseña")])
    submit = SubmitField('Login')
    
class RegistrationForm(FlaskForm):    
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign_Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            flash('Error Register. El USERNAME ya esta siendo usado, selecciona otro', 'danger')#este msg sale en el html del cliente,, lo de danger es el tipo de error, en danger saldra de color rojo, info azul etc...
            raise ValidationError('El USERNAME ya esta siendo usado, selecciona otro')#este msg sale en la terminal

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            flash('Error Register. El EMAIL ya esta siendo usado, selecciona otro', 'danger')
            raise ValidationError('El EMAIL ya esta siendo usado, selecciona otro.')





#--Rutas

@app.route('/')
@login_required
def index():      
    if current_user.is_authenticated:
        ships = Ship.query.all()
        return render_template('index.html', ships = ships)
    #return render_template('index.html', ships = ships)

@app.route("/login/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            #next_page = request.args.get('next')
            #return redirect(next_page) if next_page else redirect(url_for('index'))
            return redirect(url_for('index'))
            
            print(form.errors)
            
        else:
            flash('Error Login. El user/contrasenya no se han introducido correctamente', 'danger')
            print(form.errors)
    print(form.errors)#imprimira los errores que me devuelve del form que he llamado antes!! Imporante ya que asi veremos desde la terminal si tenemos algo mal
    #la idea es poner condicionales para usar mensajes flash para dar feedback al usuario y que pueda correg el error sin ver la pantalla fea de errores
    return render_template('login.html', form=form)

@app.route("/account/")
@login_required
def account():
    return render_template('account.html')

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/register", methods=['GET', 'POST'])
def register():    

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    
    if form.validate_on_submit(): #esto actua como un condicional de cuando usamos el metodo POST
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        #print(hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8'))
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        #flash('Tu cuenta ha sido creada!', 'success')
        return redirect(url_for('login'))
        #return redirect(url_for('/tiers/'))
    print(form.errors)#imprimira los errores que me devuelve del form que he llamado antes!! Imporante ya que asi veremos desde la terminal si tenemos algo mal
    #la idea es poner condicionales para usar mensajes flash para dar feedback al usuario y que pueda correg el error sin ver la pantalla fea de errores
    #if form.is_submitted():
    #    print ("SE añade") #cada vez que le demos al boton submit entrara en este condicional
    return render_template('register.html', form=form)

@app.route('/delete_user/<id>')
@login_required
def delete_user(id):
    User.query.filter_by(id=(id)).delete()
    db.session.commit()
    return redirect(url_for('register'))

@app.route('/add_ship/', methods=['POST'])
@login_required
def add_ship():
    ship = Ship(nombre=request.form['nombre'],type_class=request.form['type_class'], tier_number=request.form['tier_number'], origin=request.form['origin'], max_velocity=request.form['max_velocity'], active=False)
#--------la variable "ship" es una instancia de la clase, un OBJETO

    db.session.add(ship)
    db.session.commit()
    return redirect(url_for('index'))
    


@app.route('/delete_ship/<id>')
@login_required
def delete_ship(id):
    Ship.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/tiers/')
@login_required
def add_tiers():
    ships = Ship.query.all()
    tiers = Tier.query.all()
    return render_template('tiers.html', ships = ships, tiers = tiers)


# Al darle al boton invertimos el
@app.route('/active_ship/<id>')
@login_required
def active_ship(id):
    ship = Ship.query.filter_by(id=int(id)).first()
    ship.active = not(ship.active)
    ship.tier_number = id
    db.session.commit()
    return redirect(url_for('add_tiers'))


@app.route('/add_types/', methods=['GET','POST'])
@login_required
def create1_types():
    if request.method == 'GET':
        types = Type.query.all()
        return render_template('create_types.html', types = types)
    if request.method == 'POST':
        type_add = Type(type_class=request.form['type_class'],full_name=request.form['full_name'], video=request.form['video'], wars=request.form['wars'])
        db.session.add(type_add)
        db.session.commit()
        return redirect(url_for('add_types'))



@app.route('/types/')
@login_required
def add_types():
    types = Type.query.all()    
    return render_template('types.html', types = types)

@app.route('/edit_types/<type_class>', methods = ['GET','POST'])
@login_required
def edit_type(type_class):
      
    if request.method == 'GET':
        types = Type.query.filter_by(type_class=(type_class)).all()      
        return render_template('edit_types.html', types = types)

    if request.method == 'POST':
        typeed = Type.query.filter_by(wars=request.form['oldwars'], full_name=request.form['oldfull_name'], origin=request.form['oldorigin'],video=request.form['oldvideo'], photo=request.form['oldphoto']).first()
        typeed.full_name = request.form.get("newfull_name")
        typeed.wars = request.form.get("newwars")
        typeed.origin = request.form.get("neworigin")
        typeed.video = request.form.get("newvideo")
        typeed.photo = request.form.get("newphoto")
        

        db.session.commit()
        return redirect(url_for('add_types'))

@app.route('/delete_type/<type_class>')
@login_required
def delete_type(type_class):
    Type.query.filter_by(type_class=(type_class)).delete()
    db.session.commit()
    return redirect(url_for('add_types'))



@app.route('/edit_ship/<id>', methods = ['GET','POST'])
@login_required
def edit_ship(id):
    #ships = Ship.query.all()    
    if request.method == 'GET':
        ships = Ship.query.filter_by(id=int(id)).all()      
        return render_template('edit_ships.html', ships = ships)

    if request.method == 'POST':
        ship = Ship.query.filter_by(nombre=request.form['oldname'], origin=request.form['oldorigin'], type_class=request.form['oldtype_class'], tier_number=request.form['oldtier_number'],max_velocity=request.form['oldmax_velocity']).first()
        ship.nombre = request.form.get("newname")
        ship.origin = request.form.get("neworigin")
        ship.type_class = request.form.get("newtype_class")
        ship.tier_number = request.form.get("newtier_number")
        ship.max_velocity = request.form.get("newmax_velocity")
        #ship.active = request.form.get("newactive")

        
        db.session.commit()
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port = 8082, debug = True)