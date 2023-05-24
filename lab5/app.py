import requests
from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)
conn = psycopg2.connect(database="service_database",
                        user="postgres",
                        password="12365477Suka",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            if not username or not password:
                return "Одно или несколько полей являются пустыми"
            cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s",
                           (str(username), str(password) ))
            records = list(cursor.fetchall())
            if not records:
                return "Неверный логин или пароль"
            return render_template('account.html', full_name=records[0][1])
        elif request.form.get("registration"):
            return redirect("/registration/")

    return render_template('login.html')

    user_data = records[0]
    name_and_login = user_data[1] + " -- логин: " + user_data[2] + " -- пароль: " + user_data[3]
    return render_template('account.html', full_name=name_and_login)


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        if not login or not password or not name:
            return "Одно или несколько полей являются пустыми"
        if " " in login:
            return "Недопустимый символ в логине"
        cursor.execute(f"SELECT * FROM service.users WHERE login=%s", (login,))
        records = list(cursor.fetchall())

        if records:
            return "Пользователь с таким логином уже существует"

        cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);',
                       (str(name), str(login), str(password)))
        conn.commit()

        return redirect('/login/')

    return render_template('registration.html')


app.run(debug=True)
