from flask import Flask, request, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2

app = Flask(__name__)

# 데이터베이스 연결
conn = psycopg2.connect(database="mydatabase", user="myuser", password="mypassword", host="localhost", port="5432")
cur = conn.cursor()

# 회원 등록 페이지
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 입력된 정보를 데이터베이스에 저장
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')
        cur.execute("INSERT INTO users (name, email, username, password) VALUES (%s, %s, %s, %s)", (name, email, username, hashed_password))
        conn.commit()
        return redirect(url_for('login'))
    else:
        return render_template('register.html')

# 로그인 페이지
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 입력된 정보를 데이터베이스와 비교하여 로그인 처리
        username = request.form['username']
        password = request.form['password']
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        if user is not None and check_password_hash(user[4], password):
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid username or password')
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 입력된 정보를 데이터베이스에 저장
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        # 사용자 이름 중복 체크
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        if user is not None:
            return render_template('register.html', error='Username already exists')

        # 비밀번호 해싱하여 저장
        hashed_password = generate_password_hash(password, method='sha256')
        cur.execute("INSERT INTO users (name, email, username, password) VALUES (%s, %s, %s, %s)", (name, email, username, hashed_password))
        conn.commit()
        return redirect(url_for('login'))
    else:
        return render_template('register.html')



if __name__ == '__main__':
    app.run(debug=True)


