import os
from flask import Flask, redirect, request, url_for, render_template_string, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'super_secret_key_change_me'  # Required for sessions
app.config['SQLALCHEMY_DATABASE_URI'] =os.environ.get('DATABASE_URI', 'sqlite:///loveson.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False

db = SQLAlchemy(app)

#--Protfolio password--
PROTFOLIO_PASSKEY = '2068'

#------------------
#---DB_Model----
class Quest(db.Model):
	id = db.Column(db.Integer, primary_key= True)
	message = db.Column(db.String(200), unique=True)

# -----------------------------------------------------------------------------
with app.app_context():
	db.create_all()


@app.route('/', methods=['GET', 'POST'])
def home():
	if session.get('logged_in'):
		return redirect(url_for('profile'))
		
		
	if request.method == 'POST':
		
		password = request.form.get('password')
		if password == PROTFOLIO_PASSKEY:
			session['logged_in']= True
			return redirect(url_for('profile'))
			
		else:
			flash('⛔️ Invalid credentials', 'danger')
			return redirect('/')
	return render_template_string(html)
	
@app.route('/profile')
def profile():
	if not session.get('logged_in'):
		return redirect('/')
	return render_template_string(Main, message=message)
	
@app.route('/logout')
def logout():
	session.pop ('logged_in', None)
	return redirect('/')
	
@app.route('/message', methods=['GET', 'POST'])
def message():
	user_msg = request.form.get('message')
	if user_msg:
			new_quest= Quest(message=user_msg)
			db.session.add(new_quest)
			db.session.commit()
	return redirect('/profile')
			

if __name__ == '__main__':
    app.run(debug=True)
