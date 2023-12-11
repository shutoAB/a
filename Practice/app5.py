from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# ホームページ
@app.route('/')
def index():
    return render_template('index.html')

# 入力値の表示ページ
@app.route('/result', methods=['GET', 'POST'])
def result():
    # index.htmlのinputタグ内にあるname属性itemを取得し、textに格納した
    number = request.form.getlist('id')
    text = request.form.getlist('name')
    radio = request.form.getlist('sex')
    # もしPOSTメソッドならresult.htmlに値textと一緒に飛ばす
    if request.method == 'POST':
        return render_template('result.html', txt = text)
    # POSTメソッド以外なら、index.htmlに飛ばす
    else:
        return render_template('index.html')

@app.route('/output', methods=['GET', 'POST'])
def output():
    number = request.form.getlist('id')
    text = request.form.getlist('name')
    radio = request.form.getlist('sex')
    return render_template('output.html')

#おまじない
if __name__=='__main__':
    app.debug = True
    app.run(host = "localhost")

import MySQLdb

con = MySQLdb.connect(
    host = "localhost",
    user = "root",
    passwd = "2001reoAB",
    db = "sample"
)
cur = con.cursor()

cur.execute("""
            CREATE TABLE sample.user(
                id MEDIUMINT NOT NULL AUTO_INCREMENT,
                name VARCHAR(30),
                sex VARCHAR(10),
                age int(3),
                po int(3),
                place VARCHAR(30),
                PRIMARY KEY(id)
            )
""")

con.commit()

con.close()