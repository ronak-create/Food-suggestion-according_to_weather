from flask import Flask, render_template, request
import requests
from genai import food_suggestion

app = Flask(__name__)

API_KEY = "6124268d29d8547004420e70a56b4564"

def get_lat_lon(city_name, state_code, country_code, API_KEY):
    resp = requests.get(
        f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&appid={API_KEY}"
    ).json()
    # print(resp)
    data = resp[0]
    lat, lon = data.get("lat"), data.get("lon")
    return lat, lon

def get_temperature(lat,lon,API_KEY):
    resp = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric').json()
    print(resp)
    weather_data = {"main":resp.get('weather')[0].get('main'), "temp":int(resp.get('main').get('temp'))}
    return weather_data


@app.route("/", methods=["GET","POST"])
def index():
    city_name = None
    weather_manual = None
    food = None
    try:
        if request.method == "POST":
            city_name = request.form["city"]
            state_name = request.form["state"]
            country_name = request.form["country"]
            weather_manual = request.form["weather"]
            lat,lon=get_lat_lon(city_name, state_name, country_name, API_KEY)
            temp = get_temperature(lat,lon,API_KEY)
            try:
                food = food_suggestion(temp.get("main"),city_name)
            except:
                food = food_suggestion(weather_manual,city_name)
            print(food)
            # url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
            # response = requests.get(url)
            # if response.status_code == 200:
                # data = response.json()
                # temperature = data["main"]["temp"]
            # else:
            #     error_message = "City not found!"

        return render_template("index.html", city=city_name, food = food)
    except:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)