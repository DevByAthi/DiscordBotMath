#! /usr/bin/env python3

# ----- ADMINISTRATIVE SETUP -----
# This file allows the bot to operate in a discord server. A bot itself doesn't actually
# need to be a class. Instead, it exists as a set of callback functions which are triggered
# whenever certain events occur within the server. 

import discord
import asyncio
from chocolate.chocolateBar import breakBar

client = discord.Client()

# Get the guild object. This is the object representing the server we are using to develop this bot.
# It is used to allow us deeper programmatic control, such as sending messages to specific channels within the server.
botTestingServer = client.get_guild(708142506012966993)
generalTextChannel = botTestingServer.get_channel(708142506520608828)

# ----- EVENT HELPER FUNCTION DEFINITIONS -----
# ReMBot is capable of a number of actions. Oftentimes these actions involve checking/confirming user input.
# The code specific to each action is listed here.

async def chocolateProblem(message):
    # Code for checking user input to the chocolate problem and calling the solver to the problem.
    await message.channel.send('Let me break down a chocolate bar for you! First, how big is your starting bar?')
    barSize = await client.wait_for('message')
    barSize = barSize.content.split(' ')

    # The input must be provided correctly
    while len(barSize) != 2 and (not barSize[0].isdecimal()) and (not barSize[1].isdecimal()):
        await message.channel.send('Please provide your bar dimensions as two integer numbers separated by a space.')
        barSize = await client.wait_for('message')
        barSize = barSize.content.split(' ')

    await message.channel.send('Your bar is ' + barSize[0] + ' squares tall and ' + barSize[
        1] + ' squares long. How many squares do you want to eat?')
    numSquares = await client.wait_for('message')

    while not numSquares.content.isdecimal():
        await message.channel.send(
            'Please provide your desired number of squares as a single integer with no other characters.')
        numSquares = await client.wait_for('message')

    numSquares = int(numSquares.content)
    barHeight = int(barSize[0])
    barLength = int(barSize[1])

    await message.channel.send('Sounds good. Let me show you how to break that up. Meet me in the #chocolate channel!')
    chocolateChannel = botTestingServer.get_channel(726816875899650109)

    # chocolate bar problem solving occurs here
    sequence = []
    chocolateBarSolution = breakBar(barLength, barHeight, numSquares, sequence, 2)
    for step in sequence:
        await chocolateChannel.send(step)
    if chocolateBarSolution != -1:
        await chocolateChannel.send('A total of {} breaks were needed'.format(chocolateBarSolution))

async def chocolateProblemAsync(barLength, barHeight, numSquares):
    # A slightly modified version of the chocolateProblem function, for use with the asynchronous problem-solving
    # framework in performConcurrentActions().

    # Sa: The inputs have been converted from strings to integers.
    barLength = int(barLength)
    barHeight = int(barHeight)
    numSquares = int(numSquares)

    # Sb: The chocolate problem has been solved and the solution steps have been printed to the #chocolate channel.
    chocolateChannel = botTestingServer.get_channel(726816875899650109)
    sequence = []
    chocolateBarSolution = breakBar(barLength, barHeight, numSquares, sequence, 2)
    for step in sequence:
        await chocolateChannel.send(step)
    if chocolateBarSolution != -1:
        await chocolateChannel.send('A total of {} breaks were needed'.format(chocolateBarSolution))

async def directMessageUser(a_user, a_message):
    # Precondition: a_user is a string which is the username of a member of the discord server ReMBot is in. a_message
    # is a string.
    # Postcondition: a_message has been sent by ReMBot as a direct message to a_user XOR a_user has not been found
    # and ReMBot communicated this in the #general text channel.

    userToMessage = discord.utils.get(botTestingServer.members, name=a_user)
    if userToMessage is None:
        await generalTextChannel.send('No user with name {} was found!'.format(a_user))
    else:
        await userToMessage.send(a_message)

async def checkAsyncInput(an_input):
    # Helper function for checking the action inputs and associated parameters. This has to be hard coded for each
    # action due to the wide range of possible actions the bot might perform.
    # Precondition: an_input should be a list of strings, where an_input[0] specifies the action and an_input[1:]
    #               specifies input parameters required for that action.
    # Postcondition: 0 has been returned if no faults were found in the input, XOR -1 was returned if a fault was found.

    action = an_input[0]
    parameters = an_input[1:]

    if action == 'help':
        if len(parameters) != 0:
            return -1
    elif action == 'chocolate':
        if len(parameters) != 3:
            return -1
        elif not (x.isdecimal() for x in parameters):
            return -1
    elif action == 'google':
        if len(parameters) == 0:
            return -1
    elif action == 'dm':
        if len(parameters) < 2:
            return -1
    else:
        return 0

valid_concurrent_keywords = [
    'help',
    'chocolate',
    'dm',
    'google']

help_message = ('$async command documentation:\n'
                'The $async command allows you to ask me to perform multiple actions at once. In order to do this, '
                'you must provide me with certain inputs that are specific to the action you want me to perform. '
                'Below are examples showing how to format inputs for each action I can perform for you through this '
                'command. You may provide these commands in any order, as long as they follow the patterns below.\n\n'
                '-help              Display this help message.\n'
                '-chocolate l h m   Solve the chocolate problem for bar length l, bar height h, and desired area m, where l, h, and m are all integers.\n'
                '-google text       Perform a google image search for the string given by text, and return the top result.\n'
                '-dm user text      Send a dm to the server member specified by user, containing the text specified by text.\n\n\n'
                'Example usage:\n   $async -chocolate 8 9 17 -google dog wearing hat -dm flubblemolubble you are cool')

async def performConcurrentActions(a_message):
    # Abstract: This function provides a flexible framework for performing numerous actions in response to one query by
    # a user. Through use of this function, the user can ask ReMBot to solve more than one math puzzle at once and/or
    # perform other simple actions as well. The states/tasks described in this function's comments are somewhat vague in
    # terms of the actions actually being carried out, because those actions will vary depending on the content of the
    # user input.

    # Example input: $async -chocolate 8 9 17 -google dog wearing hat -dm @flubblemolubble you're a nerd

    # Intent: Complete all actions detailed in a_message concurrently
    # Precondition: a_message is a string describing all desired actions and required input parameters.
    # Postcondition: For each action described in a_message, a task to perform that action has begun.

    # Sa: a_message has been parsed to extract the described actions/inputs
    # -XOR-
    # A "help" message has been printed to guide the user in providing proper inputs AND this function has returned.

    # Transform the input string into an easily parse-able form.
    a_message_text = a_message.content
    a_message_text = a_message_text[7:].split(' -')
    a_message_text = [item.split() for item in a_message_text]

    for i in range(len(a_message_text)):
        # At each step, check if the action is valid. If it isn't, print the help text for the concurrent framework.
        if not (a_message_text[i][0] in valid_concurrent_keywords):
            await generalTextChannel.send(help_message)
            return

        # Use helper function to check specific input parameters
        result = checkAsyncInput(a_message_text[i])
        if result == -1:
            await generalTextChannel.send(help_message)
            return

    # Sb: task_list has been created, where task_list := an array of asyncio.Task objects, wherein each asyncio.Task
    # object attains one of the actions described by a_message, and each action described by a_message has one
    # corresponding task in task_list.

    # We have parsed the inputs and confirmed their correctness, so we can create the specific tasks incrementally.
    # Note that the states listed below are optional in that a user's request to the async framework may or may not
    # ask for some action to be performed. However, at least one of the Sb_* states will be accomplished.
    task_list = []
    for i in range(len(a_message_text)):
        if a_message_text[i][0] == 'help':
            # Sb_1: Task t_1 has been created, where t_1 achieves the printing of an async framework documentation
            # message to the #general text channel in the discord server.
            task_list.append(asyncio.create_task(
                generalTextChannel.send(help_message)))
        elif a_message_text[i][0] == 'chocolate':
            # Sb_2: Task t_2 has been created, where t_2 achieves the solving of the chocolate problem and the printing
            # of the solution to the #chocolate text channel in the discord server.
            task_list.append(asyncio.create_task(
                chocolateProblemAsync(a_message_text[i][1], a_message_text[i][2], a_message_text[i][3])))
        elif a_message_text[i][0] == 'google':
            # Sb_3: Task t_3 has been created, where t_3 achieves the searching of Google Images for a given query
            # and the printing of the image in the #google text channel in the discord server.
            print('placeholder')
            # Holding off on implementing this for now, since it might be more effort than it's worth at this point.
        elif a_message_text[i][0] == 'dm':
            # Sb_4: Task t_4 has been created, where t_4 achieves the goal of sending a direct message to a named user
            # containing the provided text.
            task_list.append(asyncio.create_task(
                directMessageUser(a_message_text[i][1], ' '.join(a_message_text[i][2:]))))

    # Sc: Each task described in task_list has started.
    # The asyncio.gather function runs all tasks provided to it concurrently, so this one line is all we need.
    await asyncio.gather(task_list)


# ----- EVENT DEFINITIONS -----
# Here the events which define how ReMBot actually interacts with the server are defined.

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
        await chocolateProblem(message)

# This line is used for authentication purposes to allow interaction with the Discord api, and to begin the
# asynchronous event loop that allows all these lines of code to actually run.
client.run('NzIxNzc5NDc1MDIwNTEzMzkx.XuZfkg.LnP80sKgvtyEVSSYwbK2t5nmeJo')