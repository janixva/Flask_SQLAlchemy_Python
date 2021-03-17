from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
#from flask_marshmallow import Marshmallow



app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/flask_warships'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/warship_c.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
#ma = Marshmallow(app)

#clases ---------------------

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




@app.route('/')
def index():
    ships = Ship.query.all()    
    return render_template('index.html', ships = ships)   



@app.route('/add_ship/', methods=['POST'])
def add_ship():
    ship = Ship(nombre=request.form['nombre'],type_class=request.form['type_class'], tier_number=request.form['tier_number'], origin=request.form['origin'], max_velocity=request.form['max_velocity'], active=False)
#la variable "ship" es una instancia de la clase, un objeto

    db.session.add(ship)
    db.session.commit()
    return redirect(url_for('index'))
    


@app.route('/delete_ship/<id>')
def delete_ship(id):
    Ship.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/tiers/')
def add_tiers():
    ships = Ship.query.all()
    tiers = Tier.query.all()
    return render_template('tiers.html', ships = ships, tiers = tiers)


# Al darle al boton invertimos el
@app.route('/active_ship/<id>')
def active_ship(id):
    ship = Ship.query.filter_by(id=int(id)).first()
    ship.active = not(ship.active)
    ship.tier_number = id
    db.session.commit()
    return redirect(url_for('add_tiers'))


@app.route('/add_types/', methods=['GET','POST'])
def create1_types():
    if request.method == 'GET':
        types = Type.query.all()
        return render_template('create_types.html', types = types)
    if request.method == 'POST':
        type_add = Type(type_class=request.form['type_class'],full_name=request.form['full_name'], video=request.form['video'], wars=request.form['wars'])
        db.session.add(type_add)
        db.session.commit()
        return redirect(url_for('index'))



@app.route('/types/')
def add_types():
    types = Type.query.all()    
    return render_template('types.html', types = types)

@app.route('/edit_types/<type_class>', methods = ['GET','POST'])
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
def delete_type(type_class):
    Type.query.filter_by(type_class=(type_class)).delete()
    db.session.commit()
    return redirect(url_for('add_types'))



@app.route('/edit_ship/<id>', methods = ['GET','POST'])
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