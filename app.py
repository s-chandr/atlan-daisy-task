from flask import Flask, render_template, request , Response
from flask_sqlalchemy import SQLAlchemy

import xlwt
import io

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/sampledb'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'itsverysecret'

db = SQLAlchemy(app)


class Persons(db.Model):
    __tablename__ = 'persons'   
    id = db.Column( db.Integer, primary_key=True)
    pname = db.Column(db.String(80), unique=True, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    field = db.Column(db.String(100))
    
    def __init__(self, pname, city , field):
        self.pname = pname
        self.city = city
        self.field = field


# @app.route('/')
# def home():
#     return '<a href="/addperson"><button> Click here </button></a>'


@app.route("/")
def addperson():
    return render_template("index.html")


@app.route("/personadd", methods=['POST'])
def personadd():
    
    pname=request.form["name"]
    city = request.form["city"] ,
    field = request.form["field"]

    entry = Persons(   pname , city , field)
    db.session.add(entry)
    db.session.commit()

    return render_template("index.html")

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
    sh.write(0, 2, 'city')
    sh.write(0, 3, 'field')
 
    idx = 0
    for row in result:
        sh.write(idx+1, 0, row.id)
        sh.write(idx+1, 1, row.pname)
        sh.write(idx+1, 2, row.city)
        sh.write(idx+1, 3, row.field)
        idx += 1
 
    workbook.save(output)
    output.seek(0)
 
    return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=student_report.xls"})

if __name__ == '__main__':
    db.create_all()
    app.run()