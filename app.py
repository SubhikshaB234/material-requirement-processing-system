from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Define your models
class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String(20))
    description = db.Column(db.Text)

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    purpose = db.Column(db.Text)
    status = db.Column(db.String(20), default='Pending')

# Create database tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/materials')
def materials_list():
    materials = Material.query.all()
    return render_template('materials.html', materials=materials)

@app.route('/add_material', methods=['GET', 'POST'])
def add_material():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        unit = request.form['unit']
        description = request.form['description']
        new_material = Material(name=name, quantity=quantity, unit=unit, description=description)
        db.session.add(new_material)
        db.session.commit()
        return redirect(url_for('materials_list'))
    return render_template('add_material.html')

@app.route('/requests')
def requests_list():
    requests = Request.query.all()
    return render_template('requests.html', requests=requests)

@app.route('/add_request', methods=['GET', 'POST'])
def add_request():
    if request.method == 'POST':
        material_id = request.form['material']
        quantity = request.form['quantity']
        purpose = request.form['purpose']
        new_request = Request(material_id=material_id, quantity=quantity, purpose=purpose)
        db.session.add(new_request)
        db.session.commit()
        return redirect(url_for('requests_list'))
    materials = Material.query.all()
    return render_template('add_request.html', materials=materials)

if __name__ == '__main__':
    app.run(debug=True)
