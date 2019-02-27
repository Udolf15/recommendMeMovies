from flask import Flask, render_template , request
from flaskext.mysql import MySQL

app = Flask(__name__)

# configuring DB
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'recommendmemovies'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql = MySQL()
mysql.init_app(app)


# webcode = open('webcode.html').read() - not needed

@app.route('/')
def webprint():
    return render_template('index.html') 

@app.route('/login' , methods= ['GET','POST'])
def login():
    if(request.method== 'POST'):
        userDetail = request.form
        userName = userDetail['username']
        userPassword = userDetail['password']

        conn = mysql.connect()
        curr = conn.cursor()
        curr.execute("SELECT * FROM users WHERE user_name = %s AND password = %s ",(userName,userPassword))
        data = curr.fetchone()
        if(data == None):
            return 'Error bitch'
        else:
            return render_template('loggedin.html',userName = userName)

    return render_template('login.html')

@app.route('/signup', methods = ['GET','POST'])
def signup():
    if(request.method == 'POST'):
        userDetails = request.form
        userName = userDetails['username']
        userPassword = userDetails['password']
        userEmail = userDetails['email']
        conn = mysql.connect()
        curr = conn.cursor()
        curr.execute("INSERT INTO users (user_name , email, password) VALUES(%s,%s,%s)",(userName,userEmail,userPassword))
        conn.commit()
        curr.close()
        return 'success dude'
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 3000)