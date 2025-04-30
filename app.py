from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__, instance_relative_config=False)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Liquor(db.Model):
    __tablename__ = 'liquor'
    id = db.Column(db.Integer, primary_key=True)
    liquor_name = db.Column(db.String(100), nullable=False)
    liquor_type = db.Column(db.String(50), nullable=False)
    bottle_size = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    last_updated = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    liquors = Liquor.query.all()
    return render_template('index.html', liquors=liquors)

@app.route('/add', methods=['GET', 'POST'])
def add_liquor():
    if request.method == 'POST':
        liquor = Liquor(
            liquor_name=request.form['liquor_name'],
            liquor_type=request.form['liquor_type'],
            bottle_size=request.form['bottle_size'],
            quantity=int(request.form['quantity']),
            last_updated=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        db.session.add(liquor)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_liquor(id):
    liquor = Liquor.query.get_or_404(id)
    if request.method == 'POST':
        liquor.liquor_name = request.form['liquor_name']
        liquor.liquor_type = request.form['liquor_type']
        liquor.bottle_size = request.form['bottle_size']
        liquor.quantity = int(request.form['quantity'])
        liquor.last_updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', liquor=liquor)

@app.route('/delete/<int:id>')
def delete_liquor(id):
    liquor = Liquor.query.get_or_404(id)
    db.session.delete(liquor)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)