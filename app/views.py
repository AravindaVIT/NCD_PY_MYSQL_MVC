from app import app

from flask import render_template, request



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')



@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/searchpage')
def searchpage():
    return render_template('search.html')


    

@app.route('/fail')
def fail():
    str="Please answer all the questions."
    return render_template('error.html',str=str)

#back to registration.html page
@app.route('/back',methods=['POST','GET'])
def back():
    if request.method=='POST':
        return render_template('registration.html')

