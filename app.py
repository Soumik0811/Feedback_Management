from flask import Flask, render_template, request, redirect, url_for, flash
import re
from werkzeug.security import generate_password_hash,check_password_hash
import requests
from supabase import supabase
app = Flask(__name__)
app.config['SECRET_KEY'] = 'user=postgres.lhcpvlzksihcncnuoelx password=[LONdonwnpl.123] host=aws-0-ap-southeast-1.pooler.supabase.com port=5432 dbname=postgres'





@app.route('/')
def home():
    
    return render_template('home.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        mail = request.form['email']
        feed = request.form['feedback']
        satisfy = request.form['satisfaction']
        feedback_type = request.form['feedback-type']
        service_name = request.form['service_name']
        print(service_name)
        print(feed)
        print(mail)
        data = supabase.table('feedback').insert({"name":name,"email": mail,"feedback_text":feed, "phone":phone,"satisfaction":satisfy, "product":feedback_type,"sp_name":service_name}).execute()
        # send_feedback_email(mail, name)
        return render_template('thank_you.html')

    return render_template('feedback.html')

def send_feedback_email(recipient_email, name):
    url = "https://api.zeptomail.in/v1.1/email"
    payload = {
        "from": { "address": "pameshsharma87@gmail.com"},
        "to": [{"email_address": {"address": recipient_email, "name": name}}],
        "subject": "Test Email",
        "htmlbody": "<div><b>Test email sent successfully.</b></div>"
    }
    headers = {
        'accept': "application/json",
        'content-type': "application/json",
        'authorization': "Zoho-enczapikey PHtE6r0NELy52m4t8hlT5qW8QMGnYI56qelifVYW4opBWaBXHk1XqNAsw2O0rxwrXaNBR/6Yz4htubKc57+AJmzuMD4eCmqyqK3sx/VYSPOZsbq6x00aslkYckHdU4XsdNFo3SXWudzYNA==",
    }
    response = requests.post(url, json=payload, headers=headers)
    print(response.text)   

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        # password = generate_password_hash(request.form["password"], method='pbkdf2:sha256')
        password = request.form['password']
        data = supabase.table('users').insert({"email": email,"password": password,"username":username}).execute()
        return render_template('feedback.html')
   
@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        data = supabase.table('feedback').select('*').execute()
        feedback_data = data.get('data', []) 
        return render_template('dashboard.html', feedback_data=feedback_data)
    else:
        email = request.form['email']
        password = request.form['password']
        # Check if the email and password are 'admin'
        if email == 'admin@admin.com' and password == 'admin':
            try:
                data = supabase.table('feedback').select('*').execute()
                feedback_data = data.get('data', []) 
                return render_template('dashboard.html', feedback_data=feedback_data)
            except Exception as e:
                print(f"Error fetching data: {e}")
                flash('Failed to fetch data from the database.', 'error')
                return redirect(url_for('login_error'))
        else:
            flash('Invalid email or password', 'error')
            return redirect(url_for('login_error'))
    
@app    .route('/filter', methods=['POST'])
def filter_results():
    category = request.form['category']

    if category == 'product':
        data = supabase.table('feedback').select('*').eq('product', 'Product').execute()
    elif category == 'services':
        data = supabase.table('feedback').select('*').eq('product', 'Service').execute()
    elif category == 'none':
        data= supabase.table('feedback').select('*').execute()
    feedback_data = data.get('data', [])
    return render_template('dashboard.html', feedback_data=feedback_data)

@app.route('/loginuser', methods=['POST'])
def loginuser():
    # Get the form data from the request
    username = request.form['username']
    password = request.form['password']
    print(username)
    data= supabase.table('users').select('*').eq('username', username).execute()
    user=data.get('data', [])
    user_data = user[0]
    if user:
        if user_data['password']== password:
            return render_template('feedback.html')
        else:
            return ("invalid password")
    else:
        return "User not found"

@app.route("/delete_user", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        userid = request.form.get('userid')
        print(userid)
        try:
            supabase.table('feedback').delete().eq('id', userid).execute()
        except:
            return redirect(url_for('login'))
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)