import os
from flask import Flask, redirect, request, url_for, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'super_secret_key_change_me'  # Required for sessions
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///loveson.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -- Portfolio password --
PROTFOLIO_PASSKEY = '2068'

# ------------------
teams = [
    {"id": 1, "name": "Team A", "score": 0}
]
next_team_id = 2

# --- DB Model ----
class Quest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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
            session['logged_in'] = True
            return redirect(url_for('profile'))
        else:
            flash('⛔️ Invalid credentials', 'danger')
            return redirect(url_for('home'))
            
    return render_template('Login_Page.html')
	
@app.route('/profile')
def profile():
    if not session.get('logged_in'):
        return redirect(url_for('home'))
    
    # FIX: Fetch all messages from the database to pass to the template
    messages = Quest.query.all()
    return render_template('Protfolio_Page.html', messages=messages)
	
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))
	
@app.route('/message', methods=['POST'])
def message():
    if request.method == 'POST':
        user_msg = request.form.get('message')
        if user_msg:
            # Prevent duplicate message errors due to unique=True in the DB model
            existing = Quest.query.filter_by(message=user_msg).first()
            if not existing:
                new_quest = Quest(message=user_msg)
                db.session.add(new_quest)
                db.session.commit()
                flash('Message sent!', 'success')
            else:
                flash('That message already exists!', 'warning')
    return redirect(url_for('profile'))
	
@app.route('/send')
def send():
    return render_template('About.html')

@app.route('/score')
def score():
    # FIX: Pass the teams list so Score.html can render them
    return render_template('Score.html', teams=teams)				

@app.route('/add_team', methods=['POST'])
def add_team():
    global next_team_id
    teams.append({
        "id": next_team_id,
        "name": f"Team {chr(64 + len(teams) + 1) if len(teams) < 26 else next_team_id}",
        "score": 0
    })
    next_team_id += 1
    return redirect(url_for('score'))

@app.route('/update_team/<int:team_id>', methods=['POST'])
def update_team(team_id):
    new_name = request.form.get('team_name', '').strip()
    for team in teams:
        if team['id'] == team_id and new_name:
            team['name'] = new_name
            break
    return redirect(url_for('score'))

@app.route('/add_score/<int:team_id>', methods=['POST'])
def add_score(team_id):
    try:
        points = int(request.form.get('points', 0))
    except ValueError:
        points = 0
        
    for team in teams:
        if team['id'] == team_id:
            team['score'] += points
            break
    return redirect(url_for('score'))

@app.route('/reset_score/<int:team_id>', methods=['POST'])
def reset_score(team_id):
    for team in teams:
        if team['id'] == team_id:
            team['score'] = 0
            break
    return redirect(url_for('score'))

@app.route('/delete_team/<int:team_id>', methods=['POST'])
def delete_team(team_id):
    global teams
    teams = [t for t in teams if t['id'] != team_id]
    return redirect(url_for('score'))

if __name__ == '__main__':
    app.run(debug=True)
