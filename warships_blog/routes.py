from flask import Flask, render_template, request, url_for, redirect, flash
from flask_login import login_user, current_user, logout_user, login_required, LoginManager #UserMixin
#from flask_login import *
from flask_user import roles_required, UserMixin

#from warships_blog import *
from warships_blog import app, db, bcrypt
from warships_blog.classes import Ship, Tier, Type, User, Role, UserRoles
from warships_blog.forms import RegistrationForm, LoginForm




#--Rutas

@app.route('/')
@login_required
@roles_required('admin')
def index():      
    if current_user.is_authenticated:
        ships = Ship.query.all()
        #tiers = Tier.query.all()
        #return render_template('tiers.html', ships = ships, tiers = tiers)
        return render_template('index.html', ships = ships)

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
            return redirect(url_for('add_tiers'))
            
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

@app.route("/account_admin/")
@login_required
@roles_required('admin')
def account_admin():
    user = User.query.all()
    userRoles = UserRoles.query.all()
    return render_template('account_admin.html', user=user, userRoles=userRoles)

    

@app.route('/new_admin/<id>')
@login_required
def new_admin(id):
    
    if (UserRoles.query.filter_by(user_id=(id)).first()):        
        admin = UserRoles.query.filter_by(user_id=(id)).first()
        admin.role_id = 1
    else:        
        admin = UserRoles(user_id=(id), role_id = 1)
        db.session.add(admin)
    
    db.session.commit()
    return redirect(url_for('account_admin'))



@app.route('/new_pueblo/<id>')
@login_required
def new_pueblo(id):
    pueblo = UserRoles.query.filter_by(user_id=(id)).first()    
    pueblo.role_id = 2
    db.session.commit()
    return redirect(url_for('account'))


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
        
        #rol = UserRoles(user_id=(user.id), role_id = 2) #asignamos el rol de pueblo
        #db.session.add(rol)
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
#@roles_required('admin')
def add_ship():
    ship = Ship(nombre=request.form['nombre'],type_class=request.form['type_class'], tier_number=request.form['tier_number'], origin=request.form['origin'], max_velocity=request.form['max_velocity'], active=False)
#--------la variable "ship" es una instancia de la clase, un OBJETO

    db.session.add(ship)
    db.session.commit()
    return redirect(url_for('index'))
    


@app.route('/delete_ship/<id>')
@login_required
@roles_required('admin')
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
@roles_required('admin')
def active_ship(id):
    ship = Ship.query.filter_by(id=int(id)).first()
    ship.active = not(ship.active)
    ship.tier_number = id
    db.session.commit()
    return redirect(url_for('add_tiers'))


@app.route('/add_types/', methods=['GET','POST'])
@login_required
@roles_required('admin')
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
@roles_required('admin')
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
@roles_required('admin')
def delete_type(type_class):
    Type.query.filter_by(type_class=(type_class)).delete()
    db.session.commit()
    return redirect(url_for('add_types'))



@app.route('/edit_ship/<id>', methods = ['GET','POST'])
@login_required
@roles_required('admin')
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