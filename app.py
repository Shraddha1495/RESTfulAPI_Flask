from flask import Flask, render_template, url_for, request
import pyodbc
import os

app = Flask(__name__)

# connections

hostname = "sk14.database.windows.net"
database = "shraddha"
username = "shraddha"
password ="Ai_09876"
driver= '{ODBC Driver 17 for SQL Server}'
# driver= '{SQL Server}'
connection = pyodbc.connect('DRIVER='+driver+';SERVER='+hostname+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = connection.cursor()

@app.route("/")
def start():
    cursor.execute("Select studentid from studentdata")
    resultID=cursor.fetchall()
    cursor.execute("Select * from studentdata")
    resultRead=cursor.fetchall()
    return render_template("index.html",output=resultRead,output1=resultID)

@app.route("/insert", methods=["GET", "POST"])
def insertData():
    stid = int(request.form['id'])
    fname = str(request.form['fname'])
    lname = str(request.form['lname'])
    dob = str(request.form['dob'])
    amount = int(request.form['amount'])
    print((stid,fname,lname,dob,amount))
    sql=cursor.execute("Insert into studentdata values(?,?,?,?,?)",(stid,fname,lname,dob,amount))
    print(sql)
    cursor.execute("Select * from studentdata")
    resultRead=cursor.fetchall()
    cursor.execute("Select studentid from studentdata")
    resultID=cursor.fetchall()
    return render_template("index.html",output=resultRead,output1=resultID,message="Data Inserted Successfully")

@app.route("/updateselect", methods=["GET", "POST"])
def updateSelect():
    stid=int(request.form.get('id'))
    cursor.execute("Select * from studentdata where studentid = ?",(stid))
    resultupdate=cursor.fetchall()
    return render_template("update.html",output=resultupdate)

@app.route("/update", methods=["GET", "POST"])
def update():
    stid = int(request.form['id'])
    fname = str(request.form['fname'])
    lname = str(request.form['lname'])
    dob = str(request.form['dob'])
    amount = int(request.form['amount'])
    print((stid,fname,lname,dob,amount))
    sql=cursor.execute("Update studentdata set firstname=?, lastname=?, dob=?, amountdue=? where studentid =?",(fname,lname,dob,amount,stid))
    print(sql)
    cursor.execute("Select * from studentdata")
    resultRead=cursor.fetchall()
    cursor.execute("Select studentid from studentdata")
    resultID=cursor.fetchall()
    return render_template("index.html",output=resultRead,output1=resultID,message="Data Updated Successfully")


@app.route('/delete',methods=["POST"])
def delete():
        stid=int(request.form.get('id'))
        print(stid)
        sql=cursor.execute("Delete from studentdata where studentid = ?",(stid))
        cursor.execute("Select studentid from studentdata")
        resultID=cursor.fetchall()
        cursor.execute("Select * from studentdata")
        resultRead=cursor.fetchall()
        return render_template("index.html",output=resultRead,output1=resultID,message="Data Deleted Successfully for "+str(stid))

if __name__ == "__main__":
    app.debug=True
    app.run(host="0.0.0.0")

