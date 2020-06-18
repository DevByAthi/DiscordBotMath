# This file allows the bot to operate in a discord server. A bot itself doesn't actually
# need to be a class. Instead, it exists as a set of callback functions which are triggered
# whenever certain events occur within the server. 

import discord
from chocolate.chocolateBar import breakBar

client = discord.Client()

# Sanity check event which prints a message to the terminal when the bot is online.
# It should appear after ./ReMBot.py is run.
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# Here we create an event which triggers whenever a text message is sent in the server.
# We can parse messages sent by users and perform whatever actions we want depending
# on the message.
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Simple message reply to demonstrate concept of interacting with the bot.
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    # If the user wants to solve the chocolate bar problem, query them for the required input,
    # solve the problem, and return the result.
    if message.content.startswith('$chocolate'):
        await message.channel.send('Let me break down a chocolate bar for you! First, how big is your starting bar?')
        barSize = await client.wait_for('message')
        barSize = barSize.content.split(' ')

        # The input must be provided correctly
        while len(barSize) != 2 and (not barSize[0].isdecimal()) and (not barSize[1].isdecimal()):
            await message.channel.send('Please provide your bar dimensions as two integer numbers separated by a space.')
            barSize = await client.wait_for('message')
            barSize = barSize.content.split(' ')

        await message.channel.send('Your bar is ' + barSize[0] + ' squares tall and ' + barSize[1] + ' squares long. How many squares do you want to eat?')
        numSquares = await client.wait_for('message')

        while not numSquares.content.isdecimal():
            await message.channel.send('Please provide your desired number of squares as a single integer with no other characters.')
            numSquares = await client.wait_for('message')

        numSquares = int(numSquares.content)
        barHeight = int(barSize[0])
        barLength = int(barSize[1])
        
        await message.channel.send('Sounds good. Let me show you how to break that up.')

        # insert chocolate bar problem solving function here
        sequence = []
        chocolateBarSolution = breakBar(barLength, barHeight, numSquares, sequence, 2)
        for step in sequence:
            await message.channel.send(step )

# This line is used for authentication purposes to allow interaction with the Discord api
client.run('NzIxNzc5NDc1MDIwNTEzMzkx.XuZfkg.LnP80sKgvtyEVSSYwbK2t5nmeJo')