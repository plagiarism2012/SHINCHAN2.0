import os
import json
import requests
from replit import db
import discord
from discord.ext import commands
from jinda import keep_alive

key_weather = os.getenv('key_weather')
key_google = 'cc63cf735bmsh065960a0e61f969p194549jsnf7ed81d30f11'

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

def lets_inspire():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)

intents = discord.Intents.default()
intents.message_content = True

def find(str):
    url = "https://open-weather13.p.rapidapi.com/city/" + str

    headers = {
	     "X-RapidAPI-Key": "cc63cf735bmsh065960a0e61f969p194549jsnf7ed81d30f11",
	     "X-RapidAPI-Host": "open-weather13.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
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

def search(str):
    query = str
    url = "https://google-search72.p.rapidapi.com/search?q=" + query

    headers = {
	     "X-RapidAPI-Key": "cc63cf735bmsh065960a0e61f969p194549jsnf7ed81d30f11",
	     "X-RapidAPI-Host": "google-search72.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    print(data)
    results = data['items']
    title = results[1]['title']
    description = results[1]['snippet']
    link = results[1]['link']
    ans = [title, description, link]
    return ans

bot = commands.Bot(command_prefix='&', intents=intents)


@bot.event
async def on_ready():
    print("ab se koi gaali nhi dega")


@bot.event
async def on_message(message):
    print(message.content)
    if message.author == bot.user:
        return

    if message.content.startswith("&inspire"):
        quote = lets_inspire()
        await message.channel.send(quote)
        await message.channel.send("||inspire ho ke bhi discord chalane ka kya laabh parth||")

    # if "gaalis" in db.keys():
    #     options = db["gaalis"]
    #     if any(word in message.content for word in options):
    #         await message.channel.send("> gaali deta h madarjaat")

    if any(word in message.content for word in db["gaalis"]):
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
        await message.channel.send("> To google search something use `&search query`")
        await message.channel.send("> To get the weather of a location `&weather location`")
        await message.channel.send("> To get inspirational quotes use `&inspire`")
        await message.channel.send("> To add any bad word in directory`&add bad_word`")
        await message.channel.send("> To see the bad word directory `&list`")
        await message.channel.send("> To delete a bad word `&delete index_of_word`")


@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')


keep_alive()
my_secret = os.environ['key']
bot.run(my_secret)
