import mysql.connector
import requests, json

#API za OpenWeather
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
API_KEY = "a2f20235363fec07f91366bdf3e4a2f0"

start_lat = 46.041900
start_lng = 14.499725

try:
    connection = mysql.connector.connect(host='localhost',
                                         database='mestadb',
                                         user='admin',
                                         password='admin')
    cursor = connection.cursor()
    cursor.execute("SELECT city, lat, lng, (6371 * acos(cos(radians(%s)) * cos(radians(lat))* cos(radians(lng) - radians(%s)) + sin (radians(%s)) * sin(radians(lat)))) AS distance FROM city HAVING distance < 1000 ORDER BY distance LIMIT 0, 20", (start_lat, start_lng, start_lat))

    # get all records
    records = cursor.fetchall()

    for row in records:
        city = row[0]
        lat = row[1]
        lng = row[2]

        CITY = city
        # upadting the URL
        URL = BASE_URL + "q=" + CITY + "&appid=" + API_KEY
        # HTTP request
        response = requests.get(URL)

        if response.status_code == 200:
            data = response.json()
            main = data['main']
            report = data['weather']
            print(f"{CITY:-^30}")
            print(f"Weather Report: {report[0]['description']}")
        else:
            print("Error in the HTTP request")

        print("city = ", row[0], )
        print("lat = ", row[1], )
        print("lng = ", row[2], "\n")


except mysql.connector.Error as e:
    print("Error reading data from MySQL table", e)
finally:
    if connection.is_connected():
        connection.close()
        cursor.close()
        print("MySQL connection is closed")
