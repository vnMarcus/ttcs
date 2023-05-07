from flask import Flask, render_template, request, redirect
import pyodbc


app = Flask(__name__)


def connection():
    DRIVER_NAME = 'SQL SERVER'
    SERVER_NAME = 'VINH\CSDLPT6'
    DATABASE_NAME = 'QLKS'
    USER_NAME = 'sa'
    PASSWORD = '1234'
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + SERVER_NAME + ';DATABASE=' +
                          DATABASE_NAME + ';UID=' + USER_NAME + ';PWD=' + PASSWORD)
    return conn


@app.route("/")
def index():
    return render_template("home.html")



@app.route("/display")
def showAllBranch():
    branches = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM [QLKS].[dbo].[Hotel]")
    for row in cursor.fetchall():
        branches.append({"id": row[0], "location": row[1], "name": row[2], "owner": row[3]})
    conn.close()
    return render_template("display.html", branches=branches)


@app.route("/addBranch", methods = ['GET','POST'])
def addcar():
    if request.method == 'GET':
        return render_template("addBranch.html")
    if request.method == 'POST':
        id = int(request.form["id"])
        location = request.form['location']
        name = request.form["name"]
        owner = request.form['owner']
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("insert into Hotel values (?,?,?,?);", id, location,name, owner)
        conn.commit()
        conn.close()
        return redirect('/')


@app.route("/changeOwner", methods = ['GET', 'POST'])
def updateOwner():
    if request.method == 'GET':
        return render_template("changeOwner.html")
    if request.method == 'POST':
        id = request.form["id"]
        owner = request.form["owner"]

        conn = connection()
        cursor = conn.cursor()
        cursor.execute("update hotel set owner_name = ? where hotel_id = ?;",  owner,id)
        conn.commit()
        conn.close()
        return redirect('/')



if(__name__ == "__main__"):
    app.run()


