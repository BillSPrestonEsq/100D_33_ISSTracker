import requests
import datetime
import smtplib

MY_LAT = 38.785809
MY_LONG = -77.187248

# Your position is within +5 or -5 degrees of the ISS position.
def iss_closeby(lat, long):
    global MY_LAT
    global MY_LONG
    print(f"MY_LAT: {MY_LAT}, MY_LONG: {MY_LONG}, \nISS_LAT: {lat},ISS_LONG: {long}")
    return((-5 <= (abs(MY_LONG) - abs(long)) <= 5) and (-5 <= (abs(MY_LAT) - abs(lat)) <= 5))

# IS it dark? (before sunrise or after sunset)
def is_dark():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = data["results"]["sunrise"].split("T")[1].split(":")
    sunset = data["results"]["sunset"].split("T")[1].split(":")

    sunrise_time = datetime.time(int(sunrise[0]), int(sunrise[1]))
    sunset_time = datetime.time(int(sunset[0]), int(sunset[1]))

    time_now = datetime.datetime.utcnow().time()
    return ((sunset_time <= time_now <= sunrise_time) or
            (time_now <= sunrise_time <= sunset_time) or
            (sunrise_time <= sunset_time <= time_now))

if is_dark():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if iss_closeby():
        my_email = "athrowaway5646@gmail.com"
        my_password = "?"
        to_address = "athrowaway5646@gmail.com"

        my_message = f"Subject: ISS is here!\n\nLook up!"

        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=my_password)
            connection.sendmail(from_addr=my_email,
                                to_addrs=to_address,
                                msg=my_message
                                )



