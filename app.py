from flask import Flask, request, flash, redirect, url_for, render_template, session
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from wtforms import validators, SubmitField, TextField
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
app.config['SECRET_KEY'] = 'dfihhbgcuii82fer'
db = SQLAlchemy(app)

class Calendar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(20), default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.id

class AddForm(FlaskForm):
    event = TextField('Event', validators=(validators.DataRequired(),))
    date = DateField('Date', format="%Y-%m-%d", validators=(validators.DataRequired(),))
    submit = SubmitField('Submit')

class EditForm(FlaskForm):
    event = TextField('Event', validators=(validators.DataRequired(),))
    date = DateField('Date', format="%Y-%m-%d", validators=(validators.DataRequired(),))
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
   return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        eventName = request.form['event']
        eventDate = request.form['date']
        newEvent = Calendar(event = eventName, date = eventDate)
        try:
            db.session.add(newEvent)
            db.session.commit()
            return redirect(url_for('calendar'))
        except:
            return 'There was an error while inserting to the database'
    form = AddForm()
    return render_template('add.html', form=form, title='Add Event')

@app.route('/calendar', methods=['GET', 'POST'])
def calendar():
    return render_template('calendar.html', events=Calendar.query, title='Calendar')

@app.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        EventEdit = Calendar.query.filter_by(id=id).first()
        EventEdit.event = request.form['event']
        EventEdit.date = request.form['date']
        try:
            db.session.commit()
            return redirect(url_for('calendar'))
        except:
            return 'There was an error while editing the event'
    form = EditForm()
    return render_template('edit.html', Calendar=Calendar, form=form, id=id, title='Edit Event')

@app.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete(id):
    Calendar.query.filter_by(id=id).delete()   
    db.session.commit() 
    return redirect(url_for('calendar'))

@app.route("/<int:id>/view")
def view(id):
    eventView = Calendar.query.filter_by(id=id).first()
    return render_template('view.html', eventView=eventView, title='View Event')

if __name__ == '__main__':
    app.run(debug=True)