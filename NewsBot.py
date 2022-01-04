import discord
import json
import requests
import random
import os

TOKEN = os.environ.get("TOKEN")          # token in environment variable.

newsApi = os.environ.get("newsApi")    # Api-key in environment variable 

weatherApi = os.environ.get("weatherApi")

client = discord.Client()


# For news and queries
def get_news(country, query):
    if query == None:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={newsApi}")
    else:
        r = requests.get(f"https://newsapi.org/v2/everything?q={query}&apiKey={newsApi}")
    parsed = json.loads(r.text)

    if parsed['articles']:
        news_choice = random.choice(parsed['articles'])
        news = news_choice['title'] + "\n" + news_choice['url']
        return news
    else:
        sent = "Could not found anything related."
        return sent


# For weather
def get_weather(place):
    r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={place}&appid={weatherApi}")
    parsed = json.loads(r.text)

    if parsed['cod'] == 200:
        weather = "**Atmosphere:** " + parsed['weather'][0]['description'].capitalize() + "\n**Current temperature:** " \
                  + str(round((parsed['main']['temp_min'] - 273), 2)) + " C" + "\n**Wind speed:** " + \
                  str(round(parsed['wind']['speed'], 2)) + " m/s"
        return weather
    else:
        weather = f"{place.capitalize()} not found. Try again with a correct name."
        return weather


# For forecasting weather
def get_forecast_weather(place):
    r = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={place}&appid={weatherApi}")
    parsed = json.loads(r.text)

    if int(parsed['cod']) == 200:
        text = "> Forecast for the next three days are: \n"

        forecast = str(parsed['list'][7]['dt_txt']) + " --> " + str(
            round((parsed['list'][7]['main']['temp'] - 273), 2)) + " C\n" + str(
            parsed['list'][15]['dt_txt']) + " --> " + str(
            round((parsed['list'][15]['main']['temp'] - 273), 2)) + " C\n" + str(
            parsed['list'][23]['dt_txt']) + " --> " + str(round((parsed['list'][23]['main']['temp'] - 273), 2)) + " C"

        return text + forecast

    else:
        forecast = f"{place.capitalize()} not found. Try again with a correct name."
        return forecast


# client.event runs the event continously.
@client.event
async def on_ready():
    print('{0.user}'.format(client) + ' is online now.')


# Async is used to call the function when something else happens.

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith('$hello') or message.content.lower().startswith('$hi'):
        await message.channel.send('Hello! ' + message.author.mention + ' I am News Bot.\nFor help, type **$help**.' )

    if message.content.lower().startswith('$bye') or message.content.lower().startswith(
            '$thank you') or message.content.lower().startswith('$thanks'):
        await message.channel.send('Have a nice day ' + message.author.mention +' !')

        
    if message.content.lower().startswith('$help'):
        embed = discord.Embed(title=" > **News Bot**",  color=0xff00ff)
        embed.add_field(name="$top news", value="For top headlines of India.", inline=False)
        embed.add_field(name="$top news us", value="For top headlines of US.", inline=False)
        embed.add_field(name="$top news uk ", value="For top headlines of UK.", inline=False)
        embed.add_field(name="$search for [topic you want to search] ", value="Provides best news articles for the topic you are interested in.", inline=False)
        embed.add_field(name="$current weather for [name of the location] ", value="Provides current weather of the location.", inline=False)
        embed.add_field(name="$forecast weather for [name of the location]", value="Provides weather forecast of the next three days for the location.", inline=False)

        await message.channel.send(embed=embed)

        
    if message.content.lower().startswith('$top news us'):
        msg = get_news("us", None)
        await message.channel.send(message.author.mention+ '\n' + msg)

    elif message.content.lower().startswith('$top news uk'):
        msg = get_news("gb", None)
        await message.channel.send(message.author.mention+ '\n' + msg)

    elif message.content.lower().startswith('$top news'):
        msg = get_news("in", None)
        await message.channel.send(message.author.mention+ '\n' + msg)

    elif message.content.lower().startswith('$search for '):
        msg = get_news(None, message.content.lower().split("for ")[1])
        await message.channel.send(message.author.mention+ '\n' + msg)

    elif message.content.lower().startswith('$current weather for '):
        msg = get_weather(message.content.lower().split("for ")[1])
        await message.channel.send(message.author.mention+ '\n' + msg)

    elif message.content.lower().startswith('$forecast weather for '):
        msg = get_forecast_weather(message.content.lower().split("for ")[1])
        await message.channel.send(message.author.mention+ '\n' + msg)


client.run(TOKEN)
