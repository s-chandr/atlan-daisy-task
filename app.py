from flask import Flask, render_template, request , Response
from flask_sqlalchemy import SQLAlchemy
import xlwt
import io

import os
from twilio.rest import Client 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/sampledb'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'itsverysecret'




db = SQLAlchemy(app)

#create table this way : follow these commands 
# python
# from app import db
# db.create_all()
class Persons(db.Model):
    __tablename__ = 'persons'   
    id = db.Column( db.Integer, primary_key=True)
    pname = db.Column(db.String(80), unique=True, nullable=False)
    _phone_number = db.Column(db.String(80))
    phone_country_code = db.Column(db.String(20))
    income = db.Column(db.Integer)
    expenditure = db.Column(db.Integer)

    


    def __init__(self,pname, _phone_number , phone_country_code , income , expenditure):
        self.pname = pname
        self._phone_number = _phone_number
        self.phone_country_code = phone_country_code
        self.income = income
        self.expenditure = expenditure
    
#Twilio Config
account_sid = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
auth_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
client = Client(account_sid, auth_token)

# @app.route('/')
# def home():
#     return '<a href="/addperson"><button> Click here </button></a>'
errors = {} 

@app.route("/")
def addperson():
    errors = {}
    return render_template("index.html" , errors = errors)


@app.route("/personadd", methods=['POST'])
def personadd():
    errors = {}
    pname=request.form["name"]
    _phone_number = request.form["_phone_number"]
    phone_country_code = request.form["phone_country_code"]
    income = request.form["income"]
    expenditure = request.form["expenditure"]
    #add income and expenditure as well and check this at server side 
    #phonenumber validation at client side 
    
    if int(income)<int(expenditure):
        errors["err"] = ["The expenditure can't be greater then income!"]
        return render_template("index.html" , errors = errors)
    entry = Persons(   pname  , _phone_number   , phone_country_code , income, expenditure)
    db.session.add(entry)
    db.session.commit()
    message = client.messages.create(
         body='Hello {} This is a sample message !! It means you have succefully registerd'.format(pname),
         from_='+16075363224',
         to=phone_country_code+_phone_number
    )
    print(_phone_number, phone_country_code)
    return render_template("index.html" , errors = errors)

@app.route('/download/report/excel')
def download_report():
    
    result = db.session.query(Persons).filter()
    
 
    #output in bytes
    output = io.BytesIO()
    #create WorkBook object
    workbook = xlwt.Workbook()
    #add a sheet
    sh = workbook.add_sheet('Student Report')
 
    #add headers
    sh.write(0, 0, 'id')
    sh.write(0, 1, 'pname')
    sh.write(0, 2, '_phone_number')
    sh.write(0, 3, 'phone_country_code')
    sh.write(0, 4, 'income')
    sh.write(0, 5, 'expenditure')
    
 
    idx = 0
    for row in result:
        sh.write(idx+1, 0, row.id)
        sh.write(idx+1, 1, row.pname)
        sh.write(idx+1, 2, row._phone_number)
        sh.write(idx+1, 3, row.phone_country_code)
        sh.write(idx+1, 3, row.income)
        sh.write(idx+1, 3, row.expenditure)
        idx += 1
 
    workbook.save(output)
    output.seek(0)
 
    return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=student_report.xls"})

if __name__ == '__main__':
    db.create_all()
    app.run()