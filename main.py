import discord
import os
import json
import requests
from replit import db
from jinda import keep_alive

key_weather = os.getenv('key_weather')
key_google = os.getenv('google_api_key')


def lets_inspire():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)


def find(str):
    url = "https://community-open-weather-map.p.rapidapi.com/weather"

    querystring = {
        "q": str,
        "lat": "0",
        "lon": "0",
        "callback": "",
        "id": "",
        "lang": "null",
        "units": "metric",
        "mode": ""
    }

    headers = {
        'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
        'x-rapidapi-key': key_weather
    }

    response = requests.request("GET",
                                url,
                                headers=headers,
                                params=querystring)
    if response.status_code != 200:
        return "false"
    data = response.json()
    main = data['main']
    temp = main['temp']
    humidity = main['humidity']
    pressure = main['pressure']
    report = data['weather']

    ans = [temp, humidity, pressure, report[0]['description']]
    return ans


def add_gaali(gaali):
    if "gaalis" in db.keys():
        gaalis = db["gaalis"]
        gaalis.append(gaali)
        db["gaalis"] = gaalis

    else:
        db["gaalis"] = [gaali]


def delete_gaali(index):
    gaalis = db["gaalis"]
    if len(gaalis) > index:
        del gaalis[index]
        db["gaalis"] = gaalis


def search(str):
    query = str
    url = "https://google-search3.p.rapidapi.com/api/v1/search/q=" + query

    headers = {
        'x-user-agent': "desktop",
        'x-proxy-location': "US",
        'x-rapidapi-host': "google-search3.p.rapidapi.com",
        'x-rapidapi-key': key_google
    }

    response = requests.request("GET", url, headers=headers)
    data = response.json()
    results = data['results']
    title = results[0]['title']
    description = results[0]['description']
    link = results[0]['link']
    ans = [title, description, link]
    return ans


bad_words = ["land", "loda", "bsdk", "bkl", "bc", "bisi", "fuck", "chutiya"]

client = discord.Client()


@client.event
async def on_ready():
    print("ab se koi gaali nhi dega")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("&inspire"):
        quote = lets_inspire()
        await message.channel.send(quote)
        await message.channel.send(
            "||inspire ho ke bhi insta chalane ka kya laabh parth||")

    if "gaalis" in db.keys():
        options = db["gaalis"]
        if any(word in message.content for word in options):
            await message.channel.send("> gaali deta h madarjaat")

    if any(word in message.content for word in bad_words):
        await message.channel.send("> gaali deta h madarjaat")

    if message.content.startswith("&add"):
        new_gaali = message.content.split("&add ", 1)[1]
        add_gaali(new_gaali)
        await message.channel.send("`added " + new_gaali + " 👍" + "`")

    if message.content.startswith("&delete"):
        gaalis = []
        if "gaalis" in db.keys():
            old_gaali = int(message.content.split("&delete ", 1)[1])
            delete_gaali(old_gaali)
            gaalis = db["gaalis"]
        await message.channel.send(gaalis)

    if message.content.startswith("&list"):
        gaalis = []
        if "gaalis" in db.keys():
            gaalis = db["gaalis"]
        await message.channel.send(gaalis)

    if message.content.startswith("&weather"):
        str1 = message.content.split("&weather ", 1)[1]
        msg = find(str1)
        if (msg == "false"):
            await message.channel.send("`> sahi sahi likh na bro`")
        else:
            await message.channel.send("`> Temprature: " + str(msg[0]) + "`")
            await message.channel.send("`> Humidity: " + str(msg[1]) + "`")
            await message.channel.send("`> Pressure: " + str(msg[2]) + "`")
            await message.channel.send("`> Weather: " + str(msg[3]) + "`")

    if message.content.startswith("&search"):
        str1 = message.content.split("&search ", 1)[1]
        msg = search(str1)
        await message.channel.send("```> " + msg[0] + "```")
        await message.channel.send("```" + msg[1] + "```")
        await message.channel.send(msg[2])

    if message.content.startswith("&help"):
        await message.channel.send(
            "> To google search something use `&search query`")
        await message.channel.send(
            "> To get the weather of a location `&weather location`")
        await message.channel.send(
            "> To get inspirational quotes use `&inspire`")
        await message.channel.send(
            "> To add any bad word in directory`&add bad_word`")
        await message.channel.send("> To see the bad word directory `&list`")
        await message.channel.send(
            "> To delete a bad word `&delete index_of_word`")


keep_alive()
my_secret = os.environ['key']
client.run(my_secret)

# we can implement something to stop spamming in discord channels
# to do so we have to keep count of the same message in some 
# interval of time and check if it crosses the limit.
# if it does so then we will ask the admin to weather keep it or # delete it from all channels.
