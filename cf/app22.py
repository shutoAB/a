from flask import Flask, request, render_template
from datetime import timedelta, datetime
from geopy.geocoders import Nominatim
import html, secrets, MySQLdb, requests, json, urllib, folium

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)
app.permanent_session_lifetime = timedelta(minutes=60)

def connect():
    con = MySQLdb.connect(
        host = "localhost",
        user = "root",
        passwd = "2001reoAB",
        db = "sample",
        use_unicode = True,
        charset = "utf8"
    )
    return con

#ある地点の5日間の気象情報を返す関数
def get_weather(api_key, place):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': place,
        'appid': api_key,
        'units': 'metric',
        "lang": "ja",
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    return data

def get_coordinates(Address):
    geolocator = Nominatim(user_agent="shutoAB")
    location = geolocator.geocode(Address)
    return location.latitude, location.longitude

def get_city_map(city_name):
    # ここで地図データを取得するためのAPIリクエストを作成し、適切な処理を行う
    # この例ではOpenStreetMap Nominatim APIを使用しています
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': city_name,
        'format': 'json',
    }
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]  # 最初の結果を返す
    return None

@app.route("/", methods=["GET"])
def index():
    return render_template('loginA.html')

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template('loginA.html')
    elif request.method == "POST":
        name = request.form["name"]
        con = connect()
        cur = con.cursor()
        cur.execute("""
            SELECT place FROM userC WHERE name=%(name)s
        """,{"name":name})
        data = []
        for row in cur:
            data.append(row)
        con.commit()
        place = cur.fetchone()
        try:
            api_key = "f4354b232b86f1e1069e58b14b228ee9"
            weather_data = get_weather(api_key, place)
            loc = get_coordinates(place)
            lat, lon = loc
            city_map = get_city_map(place)
            con.close()
            return render_template("successA.html",name=name, place=place, lat=lat, lon=lon, city_map=city_map,
                                    temperature=weather_data['main']['temp'],
                                    description=weather_data['weather'][0]['description'],
                                    humidity=weather_data['main']['humidity']
                                    )
        except Exception as err:
            return render_template("loginA.html",msg="新規作成してください。")

@app.route("/other", methods=["GET", "POST"])
def other():
    if request.method == "GET":
        return render_template('otherA.html')
    if request.method == "POST":
        place = request.form["other"]
        try:
            api_key = "f4354b232b86f1e1069e58b14b228ee9"
            weather_data = get_weather(api_key, place)
            loc = get_coordinates(place)
            lat, lon = loc
            city_map = get_city_map(place)
            return render_template("outA.html", place=place, lat=lat, lon=lon, city_map=city_map,
                                temperature=weather_data['main']['temp'],
                                description=weather_data['weather'][0]['description'],
                                humidity=weather_data['main']['humidity']
                                )
        except Exception as err:
            return render_template("otherA.html",msg="検索できない地点名です。他の地名で検索してください。")

@app.route("/make", methods = ["GET", "POST"])
def make():
    if request.method == "GET":
        return render_template("makeA.html")
    elif request.method == "POST":
        name = request.form["name"]
        place = request.form["place"]
        con = connect()
        cur = con.cursor()
        cur.execute("""
            SELECT * FROM userC WHERE name=%(name)s
        """,{"name":name})
        data = []
        for row in cur:
            data.append(row)
        if len(data) != 0:
            return render_template("makeA.html", msg="既に存在する名前です")
        con.commit()
        con.close()
        con = connect()
        cur = con.cursor()
        cur.execute("""
            INSERT INTO userC (name,place)
            VALUES (%(name)s,%(place)s)
        """,{
            "name":name, "place":place
        })
        con.commit()
        con.close()
        return render_template("infoA.html", name=name, place=place)

# おまじない
if __name__=='__main__':
    app.debug = True
    app.run(host = "localhost")