import os
from flask import Flask, redirect, request, url_for, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
QUIZ_DATA = {
      1: [
       {"id": 1, "text": "Where does Mt. Everest lie?", "ans": "Nepal"},
       {"id": 2, "text": "Which district is known as the 'Gateway to Everest'?", "ans": "Solukhumbu"},
       {"id": 3, "text": "Which is the deepest gorge in the world located in Nepal?", "ans": "Kali Gandaki Gorge"},
       {"id": 4, "text": "In which national park is the one-horned rhinoceros primarily found in Nepal?", "ans": "Chitwan National Park"},
       {"id": 5, "text": "What is the highest lake in Nepal and the world?", "ans": "Tilicho Lake"},
       {"id": 6, "text": "Which mountain is known as the 'Killer Mountain' (Mt. Manaslu) or Chomolungma?", "ans": "Mt. Everest (or Manaslu)"},
       {"id": 7, "text": "Which river is the longest river in Nepal?", "ans": "Karnali River"},
       {"id": 8, "text": "Which city in Nepal is known as the 'City of Temples'?", "ans": "Kathmandu"},
       {"id": 9, "text": "Which city is known as the 'City of Fine Arts'?", "ans": "Lalitpur (Patan)"},
       {"id": 10, "text": "Which conservation area is the largest protected area in Nepal?", "ans": "Annapurna Conservation Area"},
       {"id": 11, "text": "What is the national bird of Nepal?", "ans": "Danphe (Himalayan Monal)"},
       {"id": 12, "text": "What is the national flower of Nepal?", "ans": "Rhododendron (Lali Gurans)"},
       {"id": 13, "text": "What is the national animal of Nepal?", "ans": "Cow"},
       {"id": 14, "text": "Which waterfall is known as the deepest waterfall in Nepal (David's Fall/Devi's Fall)?", "ans": "Devi's Fall (Pokhara)"},
       {"id": 15, "text": "Which is the second-highest peak in Nepal?", "ans": "Mt. Kangchenjunga"},
       {"id": 16, "text": "Which valley is famously known as the 'Valley of Apples' in Nepal?", "ans": "Marpha (Mustang)"},
       {"id": 17, "text": "Rara Lake lies in which district of Nepal?", "ans": "Mugu"},
       {"id": 18, "text": "Shey Phoksundo Lake is located in which national park?", "ans": "Shey Phoksundo National Park"},
       {"id": 19, "text": "Which district in Nepal touches both China and India?", "ans": "None touch both directly, but Taplejung and Darchula border India and China respectively (Mechi/Mahakali regions)."},
       {"id": 20, "text": "What is the total number of districts in Nepal?", "ans": "77"},
       {"id": 21, "text": "How many provinces are there in federal Nepal?", "ans": "7"},
       {"id": 22, "text": "Which pass is the highest trade pass between Nepal and Tibet?", "ans": "Nangpa La (or Larke Pass)"},
       {"id": 23, "text": "Arun Valley is famous for being what kind of geographical feature?", "ans": "Deepest valley in the world"},
       {"id": 24, "text": "Which Himalayan peak is locally known as 'The Goddess Mother of the World' (Chomolungma)?", "ans": "Mt. Everest"},
       {"id": 25, "text": "Which is the smallest district in Nepal by area?", "ans": "Bhaktapur"}
   ],
   2: [
       {"id": 26, "text": "Where does the Taj Mahal lie? (Context link: South Asia)", "ans": "India"},
       {"id": 27, "text": "Who was the first king of a unified Nepal?", "ans": "King Prithvi Narayan Shah"},
       {"id": 28, "text": "In which year was Nepal declared a Federal Democratic Republic?", "ans": "2008 AD (2065 BS)"},
       {"id": 29, "text": "Where was Gautam Buddha (Light of Asia) born?", "ans": "Lumbini, Nepal"},
       {"id": 30, "text": "Who is known as the 'National Light' (Mahayugapurusha) of Nepal?", "ans": "Sankhadhar Sakhwa"},
       {"id": 31, "text": "Which treaty ended the Anglo-Nepal War in 1816?", "ans": "Treaty of Sugauli"},
       {"id": 32, "text": "Who was the first martyr of Nepal?", "ans": "Lakhan Thapa (or Shukra Raj Shastri / Dasharath Chand etc.)"},
       {"id": 33, "text": "What is the traditional Newari harvest and new year festival called?", "ans": "Nepal Sambat / Mha Puja"},
       {"id": 34, "text": "Which ancient script is indigenous to the Kathmandu Valley's Newar community?", "ans": "Ranjana script (Prachalit Nepal)"},
       {"id": 35, "text": "Who unified the Kathmandu Valley during the Gorkha expansion?", "ans": "King Prithvi Narayan Shah"},
       {"id": 36, "text": "What is the name of the traditional Gurung cultural dance performed in rounds?", "ans": "Rodhi / Sorhai"},
       {"id": 37, "text": "Which historical palace features 55 windows in Bhaktapur?", "ans": "Pachpann Jhyale Durbar"},
       {"id": 38, "text": "Who wrote the national anthem of Nepal 'Sayaun Thunga Phulka Hami'?", "ans": "Byakul Maila"},
       {"id": 39, "text": "Who composed the music for the modern Nepali national anthem?", "ans": "Amber Gurung"},
       {"id": 40, "text": "What is the traditional Newari feast served on a long leaf called?", "ans": "Bhoj / Samay Baji"},
       {"id": 41, "text": "Which historical fort was the site of the famous battle during the Anglo-Nepal War led by Bal Bhadra Kunwar?", "ans": "Nalapani Fort"},
       {"id": 42, "text": "Who was the Prime Minister of Nepal during the democratic movement of 1951 (End of Ranas)?", "ans": "Mohan Shumsher Jung Bahadur Rana / Matrika Prasad Koirala"},
       {"id": 43, "text": "Which dynasty ruled Nepal before the Licchavi dynasty according to chroniclers?", "ans": "Kirat Dynasty"},
       {"id": 44, "text": "In which district is the historic Gorkha Durbar located?", "ans": "Gorkha"},
       {"id": 45, "text": "What is the traditional Newari musical instrument made of clay called?", "ans": "Dey Baji / Madal / Damru / Naykhin"},
       {"id": 46, "text": "Who was the first elected Prime Minister of Nepal (1959)?", "ans": "Bishweshwar Prasad Koirala (B.P. Koirala)"},
       {"id": 47, "text": "What historic event occurred on June 1, 2001, at the Narayanhiti Royal Palace?", "ans": "Nepalese Royal Massacre"},
       {"id": 48, "text": "Which Nepalese ruler introduced the 'Muluki Ain' (Civil Code) of 1854?", "ans": "Jung Bahadur Rana"},
       {"id": 49, "text": "What is the name of the ancient script found in Changunarayan inscription, the oldest in Nepal?", "ans": "Brahmi script (Manadeva inscription)"},
       {"id": 50, "text": "Which festival marks the celebration of sisters putting Tika on their brothers in Nepal?", "ans": "Bhai Tika (Tihar)"}
   ],
   3: [
       {"id": 51, "text": "Where does Paris lie? (General GK)", "ans": "France", "image": None},
       {"id": 52, "text": "Which is the highest altitude lake in Nepal?", "ans": "Tilicho Lake (or Cholachumbu)", "image": None},
       {"id": 53, "text": "What is the traditional fermented vegetable dish eaten in Nepal called?", "ans": "Gundruk", "image": None},
       {"id": 54, "text": "Which indigenous ethnic group is famous for mountaineering and scaling Everest?", "ans": "Sherpa", "image": None},
       {"id": 55, "text": "What is the staple food dish of Nepal consisting of lentil soup and rice?", "ans": "Dal Bhat", "image": None},
       {"id": 56, "text": "Which festival is celebrated with red powder and water to welcome spring in Nepal?", "ans": "Holi (Fagu Purnima)", "image": None},
       {"id": 57, "text": "What is the traditional Newari New Year celebration festival called?", "ans": "Mha Puja / New Year Jatra", "image": None},
       {"id": 58, "text": "Which musical instrument is the national instrument of Nepal?", "ans": "Madal", "image": None},
       {"id": 59, "text": "What is the name of the traditional alcoholic drink made from fermented millet in hilly Nepal?", "ans": "Tongba (or Chhyang)", "image": None},
       {"id": 60, "text": "Which dance form is famously performed by masked dancers representing deities in Buddhist monasteries?", "ans": "Cham Dance (Mani Rimdu)", "image": None},
       {"id": 61, "text": "What is the currency of Nepal?", "ans": "Nepalese Rupee (NPR)", "image": None},
       {"id": 62, "text": "Which city is known as the lake city or tourist capital of Nepal?", "ans": "Pokhara", "image": None},
       {"id": 63, "text": "What is the highest mountain pass motorable road in Nepal?", "ans": "Thorong La Pass", "image": None},
       {"id": 64, "text": "Which animal is sacrificed heavily during the grand Hindu festival of Dashain?", "ans": "Goat / Buffalo (He-goats)", "image": None},
       {"id": 65, "text": "What is the traditional dress worn by Nepali men consisting of a tunic and tight trousers?", "ans": "Daura Suruwal", "image": None},
       {"id": 66, "text": "What is the traditional dress worn by Nepali women?", "ans": "Gunyo Cholo (Sari)", "image": None},
       {"id": 67, "text": "Which river flows right through the holy Pashupatinath Temple premises?", "ans": "Bagmati River", "image": None},
       {"id": 68, "text": "What is the name of the chariot festival held annually in Patan dedicated to the God of Rain?", "ans": "Rato Machhindranath Jatra", "image": None},
       {"id": 69, "text": "Which famous temple in Kathmandu features thousands of eyes painted on its four sides?", "ans": "Boudhanath Stupa (or Swayambhunath)", "image": None},
       {"id": 70, "text": "What is the name of the highest commercial airport in Nepal located in Lukla?", "ans": "Tenzing-Hillary Airport", "image": None},
       {"id": 71, "text": "Which district is famous for producing high-quality orthodox tea in eastern Nepal?", "ans": "Ilam", "image": None},
       {"id": 72, "text": "Which national park in Nepal is famous for swamp deer and bird watching near the Indian border?", "ans": "Shuklaphanta National Park", "image": None},
       {"id": 73, "text": "What is the traditional flatbread made of rice flour popular in Tharu communities called?", "ans": "Roti / Dhikri", "image": None},
       {"id": 74, "text": "Which mountain peak is famously nicknamed 'The Killer Mountain' due to climbing difficulty?", "ans": "Mount Manaslu", "image": None},
       {"id": 75, "text": "What is the official language of Nepal specified in the constitution?", "ans": "Nepali", "image": None}
   ],
   4: [
       {"id": 76, "text": "Identify this landmark: What is the highest peak shown in the picture?", "ans": "Mount Everest", "image": "https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcRF6PG8Zw2LMyBJv4856C1_ySnsfTpavctBCEAHUFzNxQOuHAqGjNJGECN8pdfkwbdVHL8EmkS0BpGFyt0"},
       {"id": 77, "text": "Identify this UNESCO World Heritage site featuring a massive golden spire in Kathmandu.", "ans": "Boudhanath Stupa", "image": "https://encrypted-tbn2.gstatic.com/licensed-image?q=tbn:ANd9GcSYKZf4yN-EWx3YUMH_dO5bGQ0BhcvlBneiSR78StBjFY5Xpu_U_2RqNFMfBtYlm1lXM7jL68FtFOXJDfw"},
       {"id": 78, "text": "Identify this sacred Hindu temple situated on the banks of Bagmati River.", "ans": "Pashupatinath Temple", "image": "https://encrypted-tbn2.gstatic.com/licensed-image?q=tbn:ANd9GcTQ61Ons2S4kRAPeZOkIuvziRf3CCLleuKrmNbfkfDePjK4_MbpCsAV6HBIeiapFAsEKWXePIMCP0QGkfY"},
       {"id": 79, "text": "Identify this famous square in Kathmandu filled with ancient pagodas and palaces.", "ans": "Kathmandu Durbar Square", "image": "https://encrypted-tbn3.gstatic.com/licensed-image?q=tbn:ANd9GcTcSfG0rO2XpLQEvGHNiVkD1HG81URZ-1WmixvWyY36CurkMiFkv2EQftaV1MIwamr5UtBGeuYx1j_qzhM"},
       {"id": 80, "text": "Identify this tranquil lake reflecting the Annapurna mountain range in Pokhara.", "ans": "Phewa Lake", "image": "https://encrypted-tbn3.gstatic.com/licensed-image?q=tbn:ANd9GcTMvnTXXSRKp_nr2WdzCZ5reSWYRkwEkrsiGMdYw6bHC4mEeSbNGauxbLWrPq7-_VE13pcqY4CjBgke74M"},
       {"id": 81, "text": "Identify this birthplace of Lord Buddha marked by the Ashoka Pillar.", "ans": "Maya Devi Temple, Lumbini", "image": "https://encrypted-tbn2.gstatic.com/licensed-image?q=tbn:ANd9GcQlQMTL_zp7zLuJiV5LCmfoGUzrMoE6BBXA4y49115o4aO3gW6T7ynbkGbZezuUlsto2a5k4gaZcUuAziQ"},
       {"id": 82, "text": "Identify this wildlife reserve famous for elephant safaris and one-horned rhinos.", "ans": "Chitwan National Park", "image": "https://encrypted-tbn3.gstatic.com/licensed-image?q=tbn:ANd9GcSaJzUudKxckyrDpLvFjWDvIjKV7ObPkGcYZmUhN6_m46sqVZ2bkAhPYKYadWB_a61iP5uaQdt01Z-QNTE"},
       {"id": 83, "text": "Identify this historic multi-tiered pagoda temple located in Bhaktapur Durbar Square.", "ans": "Nyatapola Temple", "image": "https://encrypted-tbn2.gstatic.com/licensed-image?q=tbn:ANd9GcRVRQirjTvGIQHKZpkGn1FLnH5N9LYhkR4oF1iE05hh3_oCUckdKZLodxyvg3pLp3MBoIVat-ed1MZEMo8"},
       {"id": 84, "text": "Identify this ancient hilltop monkey temple overlooking the Kathmandu valley.", "ans": "Swayambhunath Stupa", "image": "https://encrypted-tbn3.gstatic.com/licensed-image?q=tbn:ANd9GcStGZ9vplCwVyG_wHKyPwxN9Omr692bL_xXhnp3e_oeXKFUCdWodSHhIWo9xUpraDOwFhgBk3-hUhCD94M"},
       {"id": 85, "text": "Identify this dramatic suspension bridge crossing a deep river gorge in Parbat district.", "ans": "Kushma Suspension Bridge", "image": "https://encrypted-tbn3.gstatic.com/licensed-image?q=tbn:ANd9GcTx3GbtkjHF0vqGA9hVUFp_OqMaFmJ_GVG9aD3me-Gsj94CfLQs9FJ06IvpcmNlTRJV1N9emNbDrqwUZfg"},
       {"id": 86, "text": "Identify this pristine freshwater lake nestled in Mugu district.", "ans": "Rara Lake", "image": "https://encrypted-tbn3.gstatic.com/licensed-image?q=tbn:ANd9GcTs8DnfETlcGNNT6kHRsdRV_cz4K43CkqqQ8EyyHOUusxpXDHufZuz6D4rdNlihS9N5Ih8J_KoqjffapXo"},
       {"id": 87, "text": "Identify this deep blue high-altitude lake located in Dolpa district.", "ans": "Shey Phoksundo Lake", "image": "https://encrypted-tbn1.gstatic.com/licensed-image?q=tbn:ANd9GcTAn0iE6JCH9cfEWrwSgJTJYo3lzGyu-RxeQv6-vDcusyUowWXRjKoNX0mZPlQGMI0q0xZx6evy8p000Qw"},
       {"id": 88, "text": "Identify this iconic fish-tail mountain backdrop visible from Pokhara valley.", "ans": "Machhapuchhre (Mt. Fishtail)", "image": "https://encrypted-tbn3.gstatic.com/licensed-image?q=tbn:ANd9GcQsxnZTUQOddvmU3myKiaVwn9uy4m98WmQ9i2jTZqD-s7OZpa4ebJSuK43tQyTtSrHMQXiiO2QDhZuuX9A"},
       {"id": 89, "text": "Identify this historical stone water spout complex found across Kathmandu valley.", "ans": "Dhunge Dhara (Hiti)", "image": "https://encrypted-tbn2.gstatic.com/licensed-image?q=tbn:ANd9GcQdhmd6ZwKvo7U3Mz22zfBJSJlGtq2aEaqr036v-qW0uUjVtda1L1HyTNAEcCrO3hXkOAGEshekRZnwt8g"},
       {"id": 90, "text": "Identify this traditional water-driven grinding mill commonly found in rural streams.", "ans": "Pani Ghatta", "image": "https://encrypted-tbn3.gstatic.com/licensed-image?q=tbn:ANd9GcSCckJ60ObvtWiX9LUru3j5cFqSE-6Alfk5GG76H5Rbl49Fa0GA06P5IHOTH9BRybACKedx_e4l7aP71WI"},
       {"id": 91, "text": "Identify this historic battle site where Gorkhali forces fought during the Anglo-Nepal war.", "ans": "Nalapani Fort", "image": "https://upload.wikimedia.org/wikipedia/commons/8/85/Death_of_Rollo_Gillespie_%28Cassell%27s_illustrated_history_of_India%29.png"},
       {"id": 92, "text": "Identify this traditional mud home structure common in Terai region.", "ans": "Tharu Mud Hut", "image": "https://encrypted-tbn1.gstatic.com/licensed-image?q=tbn:ANd9GcQmrQT3ZOUHgYH8l6-FuOy46Icpb-lva8KAkO8SJVAnnJcuQkwOhMWA30PHAx_CBcAAxzLeWopPZSRk01g"},
       {"id": 93, "text": "Identify this famous cascading waterfall located near Pokhara city.", "ans": "Devi's Fall (David's Fall)", "image": "https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcR6IepoYFEGRW35SE0Q8pEhZlzEMlxPf-As7HFWfr6me2BieUwjAKRNH72PwXW6mIDazBvM58b34pekqac"},
       {"id": 94, "text": "Identify this high mountain pass marked by prayer flags on the Annapurna Circuit.", "ans": "Thorong La Pass", "image": "https://encrypted-tbn2.gstatic.com/licensed-image?q=tbn:ANd9GcRciFMR-XBiExGSrbTZb65EKCVXjUU1nMey_vtgRlccYQdkKZEOQ0SmOdh16jCv67ll4JN674I_Jorx7Iw"},
       {"id": 95, "text": "Identify this iconic palace complex featuring the 55-Window Palace in Bhaktapur.", "ans": "Bhaktapur Durbar Square", "image": "https://encrypted-tbn2.gstatic.com/licensed-image?q=tbn:ANd9GcRYtsTWaiNLoavgwSPqE5IEgxBqL_tMPC10XC5KmUpS_CaFpft-wb8Kcm0WSTle3rjConD_dlU68WriyD8"},
       {"id": 96, "text": "Identify this sacred cave temple located near Pokhara.", "ans": "Gupteshwor Mahadev Cave", "image": "https://encrypted-tbn1.gstatic.com/licensed-image?q=tbn:ANd9GcTx1mT9TrNORN25_4K3Yrqu9oZXNm4qJDl5FuZLFwhTyZ2BBnxbNfjmBI6Czv55k20ON3il3e_jv-g_cMQ"},
       {"id": 97, "text": "Identify this glacial lake lying at the foot of Imja glacier in Everest region.", "ans": "Imja Tsho Glacial Lake", "image": "https://encrypted-tbn3.gstatic.com/licensed-image?q=tbn:ANd9GcRJll26-TErpeNe0oAXIH3eIg5W6zz3F6KE718BIP6hqFoGxIyDNeEyiMu5aZIFNKfgWxHmovi_8q0wMjQ"},
       {"id": 98, "text": "Identify this sacred temple with 108 water spouts in Mustang district.", "ans": "Muktinath Temple", "image": "https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcQHz7HOSLSkhqK34w4ECE90tDQ2aEVDCbZWLPr-JeP2EAwLmAmTiNnOGN5nXK4VKlRKa8R9VnlK4vDenUw"},
       {"id": 99, "text": "Identify this multi-tiered architecture style prominent in historic Nepali temples.", "ans": "Pagoda Style Architecture", "image": "https://encrypted-tbn2.gstatic.com/licensed-image?q=tbn:ANd9GcR0lHL8eO2NVzpTvzeR0Mp8hpyHZTkF_bLyZzo5elXtD2iNYtonW6PuBmfsmWC-Qq_ry2cwTNm5Dp2fjes"},
       {"id": 100, "text": "Identify this non-rectangular national symbol of Nepal.", "ans": "National Flag of Nepal", "image": "https://encrypted-tbn3.gstatic.com/licensed-image?q=tbn:ANd9GcSyJ8Nu7VuPP6ziBc2h8YFSuXMP4kJ-KSnOic3H4up5dj4-CFemft3EaaeAssI53jss8MV5Pk7gGX3wMtI"}
   ]
}
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
number = None
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

@app.route('/score', methods=['GET', 'POST'])
def score():
    global number
   
    if request.method=='POST':
    	number = int(request.form['number'])
    
    return render_template('Score.html', teams=teams, number=number)		

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
@app.route('/quiz')
def quiz():
	if 'teams' not in session:
		session['teams'] = {"Team A": 0, "Team B":0}
	round_num = request.args.get('round', 1, type=int)
	q_id = request.args.get('q_id', type=int)
	reveal = request.args.get('reveal', type=int)
	reset_scores = request.args.get('reset_scores', type=int)
	
	scoring_team = request.args.get('team')
	pts = request.args.get('pts', type=int)
	
	if reset_scores:
		session['teams'] = {team: 0 for team in session['teams']}
		session.modified = True
		
	if scoring_team and pts is not None and scoring_team in session['teams']:
		session['teams'][scoring_team] += pts
		session.modified = True
		
	rounds = list(QUIZ_DATA.keys()) 
	CRQ = QUIZ_DATA.get(round_num, [])
		
	active_question = None
	if q_id:
		for q in CRQ:
			if q['id'] == q_id:
				active_question = q
				break
	return render_template(
	Quiz.html,
	rounds=rounds,
	current_round = round_num,
	questions = CRQ,
	active_question = active_question,
	reveal=reveal
	)
	
@app.route('/add-team', methods=['POST'])
def add_team():
		team_name = request.form.get('team_name', '').strip()
		if team_name:
			if 'teams' not in session:
					session['teams'] = {}
			if team_name not in session['teams']:
			  session['teams'][team_name] = 0
			  session.modified = True
		
		return redirect(url_for('quiz'))
					
@app.route('/remove-team')
def remove_team():
	team_name = request.args.get('team')
	if 'teams' in session and team_name in session['teams']:
		del session['teams'][team_name]
		session.modified = True
	return redirect(url_for('quiz'))	
if __name__ == '__main__':
    app.run(debug=True)
