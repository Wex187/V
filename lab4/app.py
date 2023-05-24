import requests
from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)
conn = psycopg2.connect(database="service_database",
                        user="postgres",
                        password="12365477Suka",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()


@app.route('/login/', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return "Одно или несколько полей являются пустыми"
    cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
    records = list(cursor.fetchall())

    if not records:
        return "Неверный логин или пароль"

    user_data = records[0]
    # name_and_login = user_data[1] + " -- логин: " + user_data[2] + " -- пароль: " + user_data[3]
    name_and_login = f"{user_data[1]} -- логин: {user_data[2]} -- пароль: {user_data[3]}"
    return render_template('account.html', full_name=name_and_login)


@app.route('/login/', methods=['GET'])
def index():
    return render_template('login.html')


app.run(debug=True)
