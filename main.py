from flask import Flask, render_template, request, redirect, url_for
from supabase import create_client, Client
from Classes.User import User
import json 

url: str = "https://pawhaidfyqohrcjbuuna.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBhd2hhaWRmeXFvaHJjamJ1dW5hIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDIzNzMzODksImV4cCI6MjA1Nzk0OTM4OX0.KWhRk_4rQOUowVCMTe93Au_KX3XHsEPFzIdXg0XVbKs"
supabase: Client = create_client(url, key)
user = User()
user_data = {}

def Login(eml : str, pss : str) -> bool:
    #UTF-8 Pass -> Supabase (Hash) -> Selection check.
    print(eml,pss)
    try:
        response = supabase.auth.sign_in_with_password(
        {
        "email": eml, 
        "password": pss,
        }
        )
        print(response)
        return True
    except Exception as e:
        print(e)
    return False

def SignUp(pss : str, eml: str) -> bool:
    #Currently need database to except a store of hash for security reasons
    try:
        response = supabase.auth.sign_up(
        {
        "email": eml, 
        "password": pss,
        }
        )
        print(response)
    except Exception as e:
        print(e)
    return False

app = Flask(__name__)

@app.route('/', methods = ["GET"])
def home():
    return render_template('landing.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    global user
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        if Login(email, password):
            user = User()
            user.set_dbquery(email, password)
            return redirect(url_for('dashboard'))
    return render_template("auth/login.html")

@app.route('/register', methods = ["GET", "POST"])
def signup():
    if request.method == 'POST':
        password = request.form.get("password")
        confirm_pword = request.form.get("confirm_password")
        email = request.form.get("email")
        if SignUp(password, email) and password == confirm_pword:
            return redirect(url_for('/auth/login'))
    return render_template('auth/register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('components/dashboard.html')

@app.route('/profile')
def profile():
    return render_template('components/profile.html')

@app.route('/input', methods = ["GET"])
def input():
    return render_template('components/input.html')

@app.route('/submit_data', methods=['POST'])
def submit_data():
    global user_data
    user_data = {
        "sleep": request.form.get("sleep"),
        "mood": request.form.get("mood"),
        "screen_time": request.form.get("screen_time"),
        "water": request.form.get("water"),
        "steps": request.form.get("steps"),
        "work": request.form.get("work"),
    }
    print(user_data)
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)