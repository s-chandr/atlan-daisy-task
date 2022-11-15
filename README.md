![alt text](https://github.com/s-chandr/atlan-daisy-task/blob/master/atlan-logo.jpg "Atlan")



# Atlan-Backend-Challenge

## :bookmark_tabs: What This Document is all about atlan's Internship hiring challenge 


## Database Model. 
```shell 
class Persons(db.Model):
    __tablename__ = 'persons'   
    id = db.Column( db.Integer, primary_key=True)
    pname = db.Column(db.String(80), nullable=False)
    _phone_number = db.Column(db.String(80))
    phone_country_code = db.Column(db.String(20))
    income = db.Column(db.Integer)
    expenditure = db.Column(db.Integer)
```
I have performed all the tasks as services provided by a web application. 
Flask is the framework used.

## :rocket: Task 1 
 ```shell
One of our clients wanted to search for slangs (in local language) for an answer to a text question
on the basis of cities (which was the answer to a different MCQ question).

```
### Various Approches/ideas : -
1. Since this is an mcq questions answer we will defince common slands and can see if that option is being selected by the user or not.


## :rocket: Task 2 
 ```shell
A market research agency wanted to validate responses coming in against a set of business rules 
(eg. monthly savings cannot be more than monthly income) and send the response back to the data collector 
to fix it when the rules generate a flag.
```
### Various Approches/ideas : -
There can be two approached : 
1 . Checking during insertion: 
``` shell 
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
        return render_template("base.html" , errors = errors)

```
2. Checking after data is collected : We can loop over the data in database. 
``` shell
@app.route('/mistakes')
def mistakes():
    
    result = db.session.query(Persons).filter()
    person = {"details":[]} 
    for row in result:
        if(row.income<row.expenditure):
            person["details"].append( "{} has incorerect entry income={} and expenditure={}".format(row.pname , row.income, row.expenditure))
    return render_template("index.html" , person = person)
```



## :rocket: Task 3 
 ```shell
A very common need for organizations is wanting all their data onto Google Sheets, wherein they could
connect their CRM, and also generate graphs and charts offered by Sheets out of the box. In such cases,
each response to the form becomes a row in the sheet, and questions in the form become columns. 
```
### Various Approches/ideas : -

``` shell 
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
        sh.write(idx+1, 4, row.income)
        sh.write(idx+1, 5, row.expenditure)
        idx += 1
 
    workbook.save(output)
    output.seek(0)
 
    return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=student_report.xls"})

```

## :rocket: Task 4 
 ```shell
A recent client partner wanted us to send an SMS to the customer whose details are
collected in the response as soon as the ingestion was complete reliably. The content
of the SMS consists of details of the customer, which were a part of the answers in 
the response. This customer was supposed to use this as a “receipt” for them having 
participated in the exercise



```
### Various Approches/ideas : -
For this i have used twilio api. So as soon as the form gets submitted one sms is sent to the user on successfull submissions containing filled details by him.
```shell 
#Twilio Config
account_sid = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
auth_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
client = Client(account_sid, auth_token)
message = client.messages.create(
         body='Hello {} This is a sample message !! It means you have succefully registerd'.format(pname),
         from_='+16075363224',
         to=phone_country_code+_phone_number
 )
```

## :ballot_box: Modules Used
 ```shell
   xlwt , Twilio , flask , flask_sqlalchemy , io , os 
  
   ```

## :memo: License
Licensed under the [MIT License](./LICENSE).

## :purple_heart: Thanks
Thanks to all the smart people at Atlan for reviewing my project.
