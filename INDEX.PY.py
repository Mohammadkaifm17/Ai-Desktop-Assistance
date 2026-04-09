import webbrowser
import speech_recognition as sr
import os
import time
import urllib.parse
import datetime
import cv2
import requests
import random


last_site = None
jarvish_running = True
last_city = None  # remembers last city for weather follow-ups


# === BASIC SPEECH FUNCTIONS ===
def say(text):
    """Speak text using macOS say command"""
    os.system(f"say {text}")


def takeCommand():
    """Listen to microphone and return recognized text"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        print("Listening...")
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-IN")
            query = query.lower().strip()
            print(f"You said: {query}")
            return query
        except Exception:
            response = "Sorry, I could not understand you."
            print(response)
            say(response)
            return ""


# === SEARCH & WEBSITE HANDLING ===
def google_search(query, api_key, cx, num=5):
    """Return list of search result dicts from Google Custom Search."""
    base = "https://www.googleapis.com/customsearch/v1"
    params = {"key": api_key, "cx": cx, "q": query, "num": min(max(1, num), 10)}
    try:
        resp = requests.get(base, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        results = []
        for item in data.get("items", []):
            results.append({
                "title": item.get("title"),
                "link": item.get("link"),
                "snippet": item.get("snippet")
            })
        return results
    except Exception as e:
        print(f"Error in Google Search: {e}")
        return []


def open_website(query):
    """Open a website or search it on Google."""
    global last_site
    sites = {
        "youtube": "https://youtube.com",
        "google": "https://google.com",
        "facebook": "https://facebook.com",
        "twitter": "https://twitter.com",
        "openai": "https://openai.com",
        "spotify": "https://open.spotify.com"
    }

    for site in sites:
        if site in query:
            last_site = site
            say(f"Opening {site}, sir")
            webbrowser.open_new_tab(sites[site])
            return

    last_site = "google"
    say("I could not find that site, searching on Google")
    webbrowser.open_new_tab("https://www.google.com/search?q=" + urllib.parse.quote(query))


def search_in_site(site, term):
    """Search a term in a specific site"""
    if site == "google":
        url = "https://www.google.com/search?q=" + urllib.parse.quote(term)
    elif site == "youtube":
        url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(term)
    elif site == "spotify":
        url = "https://open.spotify.com/search/" + urllib.parse.quote(term)
    else:
        url = "https://www.google.com/search?q=" + urllib.parse.quote(term)

    say(f"Searching {term} on {site}")
    webbrowser.open_new_tab(url)


# === UTILITIES ===
def tell_date_time():
    now = datetime.datetime.now()
    date_str = now.strftime("%A, %d %B %Y")
    time_str = now.strftime("%I:%M %p")
    say(f"Today is {date_str} and the current time is {time_str}")
    print(f"Date: {date_str}, Time: {time_str}")


def take_selfie():
    """Take a high-quality selfie using webcam or DSLR if connected."""
    say("Opening camera for selfie, sir. Please get ready!")

    # Try to open the default webcam first
    cap = cv2.VideoCapture(0)

    # --- Try to use DSLR if available ---
    if not cap.isOpened():
        say("Default camera not found, trying to connect DSLR camera.")
        for i in range(1, 6):  # Try camera indexes 1 to 4
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                say(f"Connected to camera {i}")
                break

    if not cap.isOpened():
        say("Sorry sir, no camera detected.")
        print("Error: Cannot access any camera.")
        return

    # --- Improve image quality ---
    # Request high resolution (Full HD)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    # Some DSLR or HD webcams support even higher (like 4K)
    cap.set(cv2.CAP_PROP_FPS, 30)

    start_time = time.time()
    countdown_time = 3  # seconds

    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            print(" Failed to grab frame")
            break

        elapsed = int(time.time() - start_time)
        remaining = countdown_time - elapsed

        # Show countdown on screen
        if remaining > 0:
            cv2.putText(frame, f"Taking photo in {remaining}...", (60, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 4)
        else:
            cv2.putText(frame, "📸 Smile! Capturing now...", (60, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 4)

        cv2.imshow("Camera - Jarvish Selfie Mode", frame)

        # Capture photo when countdown finishes
        if remaining <= 0:
            filename = f"selfie_{int(time.time())}.jpg"
            # Save with MAX quality (JPEG_QUALITY = 100)
            success = cv2.imwrite(filename, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

            if success:
                say(f"Selfie captured successfully, saved as {filename}")
                print(f" High-quality selfie saved: {filename}")
            else:
                say("Sorry sir, failed to save the selfie.")
                print(" Error saving image.")
            break

        # Allow manual cancel by pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            say("Selfie cancelled, sir.")
            print(" Selfie cancelled by user.")
            break

    cap.release()
    cv2.destroyAllWindows()



# === WEATHER HANDLER ===
def get_weather(location, forecast_days=1):
    """Fetch and speak the weather for a given location using WeatherAPI."""
    api_key = "84c88866a2194e088c3190918250510"
    base_url = "https://api.weatherapi.com/v1/forecast.json"

    try:
        params = {"key": api_key, "q": location, "days": forecast_days, "aqi": "yes", "alerts": "no"}
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "error" in data:
            say(f"Sorry, I couldn't find weather information for {location}.")
            print("Error:", data["error"]["message"])
            return

        city = data["location"]["name"]
        country = data["location"]["country"]
        current = data["current"]
        condition = current["condition"]["text"]
        temp_c = current["temp_c"]
        feelslike = current["feelslike_c"]
        humidity = current["humidity"]
        wind = current["wind_kph"]
        local_time = data["location"]["localtime"]

        say(f"The current weather in {city}, {country} is {condition}. "
            f"The temperature is {temp_c} degrees Celsius, feels like {feelslike}. "
            f"Humidity is {humidity} percent, and wind speed is {wind} kilometers per hour.")

        print(f"\n🌤️  Current weather for {city}, {country} ({local_time})")
        print(f"Condition: {condition}")
        print(f"Temperature: {temp_c}°C (Feels like {feelslike}°C)")
        print(f"Humidity: {humidity}% | Wind: {wind} km/h\n")

        # Forecast for multiple days
        if forecast_days > 1 and "forecast" in data:
            say(f"Here is the {forecast_days}-day forecast for {city}.")
            for day in data["forecast"]["forecastday"]:
                date = day["date"]
                avg_temp = day["day"]["avgtemp_c"]
                condition = day["day"]["condition"]["text"]
                chance_of_rain = day["day"]["daily_chance_of_rain"]
                forecast_report = (f"On {date}, expect {condition} with an average temperature of "
                                   f"{avg_temp} degrees and {chance_of_rain} percent chance of rain.")
                print(forecast_report)
                say(forecast_report)

    except Exception as e:
        print("Error fetching weather:", e)
        say("Sorry, I couldn't get the weather right now. Please try again later.")


# === HELPER FUNCTIONS ===
def play_song_on_youtube(song_name):
    url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(song_name)}"
    say(f"Playing {song_name} on YouTube")
    webbrowser.open_new_tab(url)


def is_stop_command(query):
    stop_keywords = [["stop", "jarvish"], ["exit", "jarvish"], ["shutdown", "jarvish"], ["stop"]]
    return any(all(word in query for word in group) for group in stop_keywords)


# === MAIN PROGRAM ===
if __name__ == "__main__":
    say("Hello, I am Jarvish A.I")
    while jarvish_running:
        query = takeCommand()
        if not query:
            continue

        # --- Stop Jarvish ---
        if is_stop_command(query):
            say("Goodbye  Harry sir, shutting down now.")
            jarvish_running = False
            break

        # --- Greetings ---
        elif any(phrase in query for phrase in
                 ["hi jarvish", "hello jarvish", "hey jarvish", "how are you", "start jarvish"]):
            greetings = [
                "Hello harry  sir, nice to hear from you! What can I do today?",
                "Hi harry  sir! How can I assist you?",

            ]
            say(random.choice(greetings))

        # --- Open websites ---
        elif "open" in query:
            open_website(query)

        # --- Search ---
        elif "search" in query:
            term = query.replace("search", "").strip()
            if term:
                if last_site:
                    search_in_site(last_site, term)
                else:
                    open_website("google")
                    search_in_site("google", term)

        # --- Weather ---
        elif "weather" in query or "forecast" in query:
            forecast_days = 1
            if any(word in query for word in ["forecast", "next days", "tomorrow", "week"]):
                forecast_days = 3

            city = None
            if " in " in query:
                city = query.split(" in ")[-1].strip()
            elif " of " in query:
                city = query.split(" of ")[-1].strip()

            if not city and last_city:
                city = last_city
            elif not city:
                say("Sure sir, please tell me the city name.")
                print("Listening for city name...")
                city = takeCommand().lower().strip()

            if city:
                last_city = city
                say(f"Fetching weather for {city}")
                get_weather(city, forecast_days)
            else:
                say("Sorry, I couldn't get the city name.")

        # --- Play Song or Music ---
        elif any(word in query for word in
                 ["jarvish play song", "play music", "listen a song", "listen music", "play some music"]):
            # Try to extract the song name after keywords
            song_name = (
                query.replace("jarvish", "")
                .replace("i want to", "")
                .replace("listen to", "")
                .replace("listen a", "")
                .replace("listen", "")
                .replace("play music", "")
                .replace(" play song", "")
                .replace("play", "")
                .replace("music", "")
                .replace("song", "")
                .strip()
            )

            if song_name:
                say(f"Playing {song_name} on YouTube, sir.")
                play_song_on_youtube(song_name)
            else:
                say("Which song would you like to listen, sir?")
                song_name = takeCommand()
                if song_name:
                    play_song_on_youtube(song_name)
                else:
                    say("Sorry sir, I didn’t catch the song name.")


        # --- Date & Time ---
        elif "date" in query or "time" in query:
            tell_date_time()

        # --- Selfie ---
        elif "selfie" in query:
            take_selfie()

        else:
            say("Sorry, I didn't understand that command.")
