from flask import Flask, request, render_template, redirect
import os
import sqlite3
from model import Model

current_location = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__,static_url_path='/static')


UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def create_database():
    conn = sqlite3.connect(os.path.join(current_location, 'login.db'))
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users(name TEXT, email VARCHAR(100), city TEXT,purpose TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard',methods = ['GET'])
def dashboard():
    return render_template('index02.html')

@app.route('/sign_in', methods=['POST','GET'])
def sign_in():
    if request.method == 'POST'or 'GET':
        print(request.form)
        try : 
            EM = request.form['sign_in_email']
            PW = request.form['sign_in_password']
            #print(f'{EM},{PW}')
            #
            conn = sqlite3.connect(os.path.join(current_location, 'login.db'))
            cursor = conn.cursor()
            query = 'SELECT email,password FROM users WHERE email = ? AND password = ?'
            cursor.execute(query, (EM, PW))
            row = cursor.fetchone()
            conn.close()
            if row:
                return redirect('/dashboard')
            else:
                return 'Sign In first!!!'
        except KeyError : 
            return 'Missing sign-in email or password' 
@app.route('/sign_up', methods=['POST'])
def sign_up():   
    if request.method == 'POST':
        # print(request.form)
        sName = request.form['name']
        sEM = request.form['sign-up-email']
        sC = request.form['city']
        use = request.form['using']
        print(sName, sEM, sC,use)
        
        conn = sqlite3.connect(os.path.join(current_location, 'login.db'))
        cursor = conn.cursor()
        query = 'INSERT INTO users VALUES (?, ?, ?, ?)'
        cursor.execute(query, (sName, sEM, sC, use))
        conn.commit()
        conn.close()
        return redirect('/dashboard')    
    return render_template('index.html')  

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        # Save the uploaded file to the uploads folder
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        m = Model()
        prediction_o = m.prediction_result
        return render_template("index02.html",prediction = prediction_o)
if __name__ == '__main__':
    create_database()
    app.run(debug=True)
