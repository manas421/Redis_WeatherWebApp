import streamlit as st
import requests
import redis
import json
from datetime import datetime

redis_cli = redis.Redis(host='localhost', port=6379, db=0)

#Key valid till 10th July
api_key = 'dabd5d7f3c1f455485b3c746bcb41c6d'
# img_url = "https://cdn.dribbble.com/users/2277649/screenshots/8498294/weather_dribbble_size.gif.gif"
img_url = "https://i.pinimg.com/originals/0e/f3/bb/0ef3bb66d9216fffcea9022628f7bb26.gif"

st.set_page_config(page_title = "Weather Details", page_icon = ":partly_sunny:",layout = "wide")

with st.container():
    left_column, right_column = st.columns((2,1))
    with left_column:
        st.title("Weather Details :partly_sunny:")
        st.write("[API Details >](https://www.weatherbit.io/api/weather-current)")
    with right_column:
        st.image(img_url, width = 250)

st.write("---")

user_city = st.text_input("Enter name of City :", "Bangalore")

b1 = st.button(label = "Get Data")

if b1:
    weather = redis_cli.get(f"{user_city}_weather")

    if weather is None:
        st.write("*Reading from API*")
        t1 = datetime.now()
        payload = {'Key':api_key, 'city':user_city, 'country':"India"}
        res = (requests.get('https://api.weatherbit.io/v2.0/current', params = payload)).json()
        t2 = datetime.now()

        redis_cli.set(f"{user_city}_weather", json.dumps(res)) #writing to redis cache
        #redis_cli.setex(f"{user_city}_weather", 15, json.dumps(res)) #writing to redis cache, with expiration

    else:
        st.write("*Reading from Cache*")
        t1 = datetime.now()
        res = json.loads(weather)
        t2 = datetime.now()
    
    temp = res['data'][0]['temp']
    wthr_desc = res['data'][0]['weather']['description']
    aqi = res['data'][0]['aqi']
    rel_humidity = res['data'][0]['rh']
    wind_dir = res['data'][0]['wind_cdir_full']
    wind_speed = round(res['data'][0]['wind_spd'], 2)
    
    
    col11, col12, col13 = st.columns(3)
    col11.metric("Temperature", f"{temp}°C",)
    col12.metric("Weather Description", wthr_desc)
    col13.metric("AQI", aqi)

    col21, col22, col23 = st.columns(3)
    col21.metric("Relative Humidity", f"{rel_humidity}%",)
    col22.metric("Wind Direction", wind_dir)
    col23.metric("Wind Speed", f"{wind_speed}m/s")
    

    delta_t = round((t2-t1).total_seconds()*1000,3)
    st.write(f"Time taken to get result : {delta_t} ms")
