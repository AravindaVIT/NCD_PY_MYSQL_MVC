from flask import Flask, render_template, request, url_for, redirect
from app import app
from flask_mysqldb import MySQL 
import MySQLdb.cursors

from random import randint
  

#mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Ankita@18Riya'
app.config['MYSQL_DB'] = 'ncdpython'


mysql = MySQL(app)



@app.route('/search',methods=['GET', 'POST'])
def search():
    
    primary_key=""
    records=()
    
    if request.method=="POST":

        primary_key=request.form['primary_key']
        primary_key.capitalize()
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * from patient WHERE patient_id LIKE '"+primary_key+"%' or first_name LIKE '"+primary_key+"%' or last_name LIKE '"+primary_key+"%'; ")
        records=cursor.fetchall()
        cursor.close()

    return render_template('search.html', records=records)


def making_global(aadh):
    global aadhaar
    aadhaar=aadh
    


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method=="POST":

        firstname=""
        lastname=""
        gender=""
        aadhaar=""
        phone=""
        birthday=""
        pincode=""
        total=0
        screening=""
        msg = " "
        patient_id=""

        firstname=request.form['firstname']
        lastname=request.form['lastname']
        gender=request.form['gender']
        aadhaar=request.form['aadhaar']
        phone=request.form['phone']
        birthday=request.form['birthday']
        pincode=request.form['pincode']

        firstname.capitalize()
        lastname.capitalize()

    making_global(aadhaar)

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT patient_id from patient')
    pid=cursor.fetchall()
    #print(pid)
    
    if(len(pid)>0):
        for i in pid:
            id=random_n_digits(14)
            if(id==i):
                continue
            else:
                cursor.execute('INSERT INTO patient VALUES (%s, % s, % s, % s, % s, % s, % s, % s,%s,%s)',(id,firstname, lastname, gender , aadhaar, phone, birthday, pincode, total, screening,))
                mysql.connection.commit()
                msg='You have successfully registered !'
                break
                
    else:
        id=random_n_digits(14)
        cursor.execute('INSERT INTO patient VALUES (%s,% s, % s, % s, % s, % s, % s, % s,%s,%s)',(id,firstname, lastname, gender , aadhaar, phone, birthday, pincode, total, screening))
        mysql.connection.commit()
    
    cursor.execute('SELECT patient_id from patient WHERE aadhaar_uid=%s',[aadhaar])
    patient_id= cursor.fetchone()

    return render_template('question.html',patient_id=patient_id.get('patient_id'))

def random_n_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)
    

@app.route('/submit', methods=['GET','POST'])
def ncd_rac():
    if request.method == "POST":
        total=0
        age=-1
        smoke=-1
        alcohol=-1
        waist=-1
        phy_act=-1
        fam_his=-1
        
        age = int(request.form['age'])
        if (age ==-1):
            return redirect(url_for('fail'))
        
        smoke = int(request.form['smoke'])
        if (smoke == -1):
            return redirect(url_for('fail'))

        alcohol = int(request.form['smoke'])
        if (alcohol == -1):
            return redirect(url_for('fail'))

        waist = int(request.form['waist'])
        if (waist ==-1):
            return redirect(url_for('fail'))

        phy_act = int(request.form['phy_act'])
        if (phy_act == -1):
            return redirect(url_for('fail'))

        fam_his = int(request.form['fam_his'])
        if (fam_his == -1):
            return redirect(url_for('fail'))   

        total = age + smoke + alcohol + waist + phy_act + fam_his

        res=""
        screening=""
        
        if total>4:
            res="The person may be at higher risk of NCDs and needs to be prioritized for attending screening."
            screening ="yes"
        else:
            res="The person is not at risk of NCDs and doesn't need screening."
            screening ="no"

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE patient SET score =% s,screening =% s WHERE aadhaar_uid =% s',(total,screening,aadhaar))

    mysql.connection.commit()   

    return render_template('result.html',result=res,total=total, age=age,smoke=smoke,alcohol=alcohol,
                            waist=waist,phy_act=phy_act,fam_his=fam_his)              
    

