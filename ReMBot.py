#! /usr/bin/env python3

# --------------------------------
# ----- ADMINISTRATIVE SETUP -----
# --------------------------------
# This file allows the bot to operate in a discord server. A bot itself doesn't actually
# need to be a class. Instead, it exists as a set of callback functions which are triggered
# whenever certain events occur within the server. This file contains only the code which
# directly pertains to ReMBot listening for events. All functions managing specific event-related
# actions are defined in ReMBot_events.py. Additionally, some global variables and the start-up
# event are defined in ReMBot_starter.py

import discord
import asyncio
import numpy as np

from factory import reachAllCustomers
from parseTopLevel import readFileIntoString

from chocolate.chocolateBar import breakBar
from schedule.scheduling import *
from schedule.errors import *
from snakesequence.snake_seq_solver import getLongestSnakeSequence
from golf import parseGolf, golfClasses
from enum import Enum

from factory.graphClasses import *
from factory.generateGraph import parse_into_graph
from factory.reachAllCustomers import *
from factory.shortestShippingPath import findCheapestShippingPath

client = discord.Client()
botTestingServer = []
generalTextChannel = []


class ServerIDs(Enum):
    TOKEN = 'NzIxNzc5NDc1MDIwNTEzMzkx.XuZfkg.LnP80sKgvtyEVSSYwbK2t5nmeJo'
    SERVER_ID = 708142506012966993
    GENERAL_ID = 708142506520608828
    CHOCOLATE_ID = 726816875899650109
    CHOCOLATE_SHIPPING_ID = 738445964087656600
    SNAKE_ID = 732026639512240229
    GOLF_ID = 732954147380265040


# Sanity check event which prints a message to the terminal when the bot is online.
# It should appear after ./ReMBot.py is run.
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    # Get the guild object. This is the object representing the server we are using to develop this bot.
    # It is used to allow us deeper programmatic control, such as sending messages to specific channels within the server.
    global botTestingServer
    global generalTextChannel
    botTestingServer = client.get_guild(ServerIDs.SERVER_ID.value)
    generalTextChannel = botTestingServer.get_channel(ServerIDs.GENERAL_ID.value)


# ---------------------------------------------
# ----- EVENT HELPER FUNCTION DEFINITIONS -----
# ---------------------------------------------
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
    await chocolateProblemSolver(barLength, barHeight, numSquares)


async def chocolateProblemSolver(barLength, barHeight, numSquares):
    # Function that actually initiates the solving of the chocolate problem. It is implemented as a separate function
    # so that it can be integrated with the async framework, which does not employ the same thorough user dialogue as
    # the standalone chocolate problem solver.

    # Sa: The chocolate problem has been solved and the solution steps have been printed to the #chocolate channel.
    chocolateChannel = botTestingServer.get_channel(ServerIDs.CHOCOLATE_ID.value)
    await chocolateChannel.send('Now breaking up a new bar for you!\n')
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


async def scheduleForBreak(message):
    message_str = message.content[:].split()
    duration = 30
    if len(message_str) != 2:
        await generalTextChannel.send("One value for desired break duration expected!")
        return
    else:
        try:
            duration_user = int(message_str[1])
            if not (0 <= duration_user < 480):
                generalTextChannel.send("Desired break duration must be a nonnegative number under 480 minutes")
                raise ValueError()
        except ValueError:
            await generalTextChannel.send("Invalid input for desired break duration!")
        else:
            duration = duration_user

    if message.attachments:
        f = await discord.Attachment.to_file(message.attachments[0])

        # Check that attachment is a .txt file
        file_name = str(f.filename).split('.')
        if len(file_name) < 2 or file_name[1].lower() != "txt":
            # S_nil2: File is not a .txt file
            print(file_name)
            await generalTextChannel.send("You need to attach a .txt file!")
            return

        # File text is read into a string
        s = f.fp.read().decode("utf-8")

        try:
            # String is parsed to yield sorted list of Section objects
            section_dict = retrieveSections(s)
            sorted_list = sectionSort(section_dict)
            resulting_schedule = generateSchedule(sorted_list, duration)
            if len(resulting_schedule) == 0:
                # See scheduling.generateSchedule, POSTCONDITION 2
                # Sa: No schedules exist to fulfill constraints
                await generalTextChannel.send(
                    "There exists no schedule that will accommodate your desired break time of " + str(
                        duration) + " minutes")
            else:
                # See scheduling.generateSchedule, POSTCONDITION 1a-d
                # Sb: Schedule existing fulfilling constraints
                await generalTextChannel.send("Your schedule is as follows: ")
                for elem in resulting_schedule:
                    await generalTextChannel.send(elem)
                await generalTextChannel.send("And then you'll have time for a nice break!")
        except errors.TimeFormatError as err:
            await generalTextChannel.send(err.message)
        except errors.ScheduleFormatError as err:
            await generalTextChannel.send(err.message)
    else:
        # S_nil: No file is attached
        await generalTextChannel.send("No file attached!")
        await generalTextChannel.send("Please attach a .txt file in the format of `input_format.txt` on GitHub")
        await generalTextChannel.send("To do this, press the plus icon, select the .txt file you'd like and type "
                                      "$schedule in the same message")


def checkAsyncInput(an_input):
    # Helper function for checking the action inputs and associated parameters. This has to be hard coded for each
    # action due to the wide range of possible actions the bot might perform.
    # Precondition: an_input should be a list of strings, where an_input[0] specifies the action and an_input[1:]
    #               specifies input parameters required for that action.
    # Postcondition: 0 has been returned if no faults were found in the input, XOR -1 was returned if a fault was found.

    action = an_input[0]
    parameters = an_input[1:]

    # TODO: Simplify this using a dictionary mapping keywords to a list of parameters numbers

    if action == 'help':
        if len(parameters) != 0:
            return -1
    elif action == 'chocolate':
        if len(parameters) != 3:
            return -1
        try:
            int(parameters[0])
            int(parameters[1])
            int(parameters[2])
        except ValueError:
            return -1
    elif action == 'dm':
        if len(parameters) < 2:
            return -1
    elif action == 'hello':
        if parameters:
            return -1
    else:
        return 0


# Global variables here are manually maintained to work with the concurrency framework. It isn't really the best
# solution since it must be scaled manually, but it is the easiest solution for short-term proof of concept.
valid_concurrent_keywords = [
    'help',
    'chocolate',
    'dm',
    'hello']

help_message = ('$async command documentation:\n'
                'The $async command allows you to ask me to perform multiple actions at once. In order to do this, '
                'you must provide me with certain inputs that are specific to the action you want me to perform. '
                'Below are examples showing how to format inputs for each action I can perform for you through this '
                'command. You may provide these commands in any order, as long as they follow the patterns below.\n\n'
                '-help\n    Display this help message.\n'
                '-chocolate L H M\n    Solve the chocolate problem for bar length L, bar height H, and desired area M, where L, H, and M are all integers.\n'
                '-hello\n    Send a greeting into the general chat.\n'
                '-dm user text\n    Send a dm to the server member specified by user, containing the text specified by text.\n\n\n'
                'Example usage:\n   $async -chocolate 8 9 17 -hello -dm flubblemolubble you are cool')


async def performConcurrentActions(a_message):
    # Abstract: This function provides a flexible framework for performing numerous actions in response to one query by
    # a user. Through use of this function, the user can ask ReMBot to solve more than one math puzzle at once and/or
    # perform other simple actions as well.

    # Example input: $async -chocolate 8 9 17 -hello -dm @flubblemolubble you're a nerd

    # Intent: Complete all actions detailed in a_message concurrently
    # Precondition: a_message is a string describing all desired actions and required input parameters.
    # Postcondition: For each action described in a_message, a task to perform that action has begun.

    # Sa: a_message has been parsed to extract the described actions/inputs
    # -XOR-
    # A "help" message has been printed to guide the user in providing proper inputs AND this function has returned.

    # Transform the input string into an easily parse-able form.
    a_message_text = a_message.content
    a_message_text = a_message_text[8:].split(' -')
    a_message_text = [item.split() for item in a_message_text]
    if not a_message_text[0]:
        await generalTextChannel.send('Please specify at least one action.')
        return

    for i in range(len(a_message_text)):
        # At each step, check if the action is valid. If it isn't, print the help text for the concurrent framework.
        if not (a_message_text[i][0] in valid_concurrent_keywords):
            await generalTextChannel.send(
                'I don\'t know what {} is! Please check the doc message for available actions.'.format(
                    a_message_text[i][0]))
            await generalTextChannel.send(help_message)
            return

        # Use helper function to check specific input parameters
        result = checkAsyncInput(a_message_text[i])
        if result == -1:
            await generalTextChannel.send('Whoops! I caught some bad input parameters. Please check the doc message.')
            await generalTextChannel.send(help_message)
            return

    # Sb: task_list has been created, where task_list := an array of asyncio.Task objects, wherein each asyncio.Task
    # object attains one of the actions described by a_message, and each action described by a_message has one
    # corresponding task in task_list.

    # We have parsed the inputs and confirmed their correctness, so we can create the specific tasks incrementally.
    # Tasks are created as Task objects via asyncio.ensure_future(). These Tasks will later be run concurrently.
    # Note that the states listed below are optional in that a user's request to the async framework may or may not
    # ask for some action to be performed. However, at least one of the Sb_* states will be accomplished.
    task_list = []
    for i in range(len(a_message_text)):
        if a_message_text[i][0] == 'help':
            # Sb_1: Task t_1 has been created, where t_1 achieves the printing of an async framework documentation
            # message to the #general text channel in the discord server.
            task_list.append(asyncio.ensure_future(
                generalTextChannel.send(help_message)))
        elif a_message_text[i][0] == 'chocolate':
            # Sb_2: Task t_2 has been created, where t_2 achieves the solving of the chocolate problem and the printing
            # of the solution to the #chocolate text channel in the discord server.
            task_list.append(asyncio.ensure_future(
                chocolateProblemSolver(int(a_message_text[i][1]), int(a_message_text[i][2]),
                                       int(a_message_text[i][3]))))
        elif a_message_text[i][0] == 'hello':
            # Sb_3: Task t_3 has been created, where t_3 achieves the sending of a message containing a friendly
            # greeting to the #general text channel in the discord server.
            task_list.append(asyncio.ensure_future(
                generalTextChannel.send('Hello!')))
        elif a_message_text[i][0] == 'dm':
            # Sb_4: Task t_4 has been created, where t_4 achieves the goal of sending a direct message to a named user
            # containing the provided text.
            task_list.append(asyncio.ensure_future(
                directMessageUser(a_message_text[i][1], ' '.join(a_message_text[i][2:]))))

    # Sc: Each task described in task_list has started.
    # The asyncio.gather function runs all tasks provided to it concurrently, so this one line is all we need.
    await asyncio.gather(*task_list)


async def snakeSequenceTask():
    # If the user wants to find the longest snake sequence, ask them for the grid of numbers to use, then call
    # the snake sequence solver. Right now this function assumes perfect input because I'm too lazy to do input
    # checking.

    snakeChannel = botTestingServer.get_channel(ServerIDs.SNAKE_ID.value)
    await generalTextChannel.send(
        'Let me find the longest snake sequence in a grid for you! Please provide your grid as a single message.')
    grid = await client.wait_for('message')
    grid = grid.content
    grid = grid.split('\n')
    for i in range(len(grid)):
        grid[i] = grid[i].split(' ')
        grid[i] = list(map(int, grid[i]))
    grid = np.array(grid)
    longest_seq = getLongestSnakeSequence(grid)
    await generalTextChannel.send('Perfect! Meet me in the #snake channel for your solution.')
    await snakeChannel.send('I\'ve got an answer for you! First, here\'s your grid again:')
    await snakeChannel.send(str(grid))
    await snakeChannel.send('The longest snake sequence in your grid is: ' + str(longest_seq))


async def codeGolfHelper(message):
    # If the user wants ReMBot to play some code golf, query them for the input grid, and ask if they have a preferred
    # optimization for ReMBot to use. Finally, call the code golf solver and return the output as a message in the
    # discord #codegolf text channel.

    golfChannel = botTestingServer.get_channel(ServerIDs.GOLF_ID.value)
    await generalTextChannel.send('Let me play some code golf for you!')
    graph = None
    grid = None
    if message.attachments:
        f = await discord.Attachment.to_file(message.attachments[0])

        # Check that attachment is a .txt file
        file_name = str(f.filename).split('.')
        if len(file_name) < 2 or file_name[1].lower() != "txt":
            # S_nil2: File is not a .txt file
            print(file_name)
            await generalTextChannel.send("You need to attach a .txt file!")
            return
        rows = []
        try:
            # File text is read into a string
            rows = f.fp.read().decode("utf-8").split('\n')
        except BlockingIOError as err:
            print(err.filename)
            await generalTextChannel.send("Could not read attached file")
            return
        grid = parseGolf.readIntoGrid(rows)
        graph = golfClasses.GolfGraph(grid)
        graph.a_star_greedy()
        print(graph.path)
    else:
        await generalTextChannel.send("Please attach a .txt file representing the golf course!")
        return

    if graph is None or grid is None:
        await generalTextChannel.send("Hmmm seems we weren't able to find a path.")
        await generalTextChannel.send("Check that you've given a file in the appropriate format.")
        return

    await generalTextChannel.send('Perfect! Meet me in the #codegolf channel for your optimal series of hits.')
    await golfChannel.send('I\'ve got a route for you! First, here\'s your golf course terrain again:')
    for row in grid:
        # Format printed row to have equal spacing
        await golfChannel.send('`' + "".join(["{:=5}".format(elem) for elem in row]) + '`')
    await golfChannel.send('The route you should take to optimize for this terrain' + ' is:\n' + str(graph.path))


async def chocolateShippingHelper(message):
    # If the user wants to figure out some logistics related to shipping chocolate, find out their
    # use case (customer vs factory planner) and call the appropriate solver.
    chocolateShippingChannel = botTestingServer.get_channel(ServerIDs.CHOCOLATE_SHIPPING_ID.value)

    if message.attachments:
        f = await discord.Attachment.to_file(message.attachments[0])

        # Check that attachment is a .txt file
        file_name = str(f.filename).split('.')
        if len(file_name) < 2 or file_name[1].lower() != "txt":
            # S_nil2: File is not a .txt file
            print(file_name)
            await generalTextChannel.send("You need to attach a .txt file!")
            return
        try:
            # File text is read into a string
            rows = f.fp.read().decode("utf-8").strip().split('\n')
            graph = parse_into_graph(rows)
        except BlockingIOError as err:
            print(err.filename)
            await generalTextChannel.send("Could not read attached file")
            return
        except ValueError as err:
            await generalTextChannel.send(str(err))
            return
        except TypeError as err:
            await generalTextChannel.send(str(err))
            return
    else:
        await generalTextChannel.send("Please attach a .txt file representing the chocolate shipping network as a graph!")
        return

    await generalTextChannel.send('Let\'s do some chocolate business. Firstly, are you a customer or planner?')
    await generalTextChannel.send('Please respond either `customer` or `planner`.')
    useCase = await client.wait_for('message')
    useCase = useCase.content
    while not ((useCase == 'customer') or (useCase == 'planner')):
        await generalTextChannel.send('Please respond either `customer` or `planner`.')
        useCase = await client.wait_for('message')
        useCase = useCase.content

    if useCase == 'customer':
        await generalTextChannel.send(('So, you\'re a chocolate-hungry customer. Let\'s look at your shipping network '
                                       'and decide which factory you should order from to minimize shipping costs.'))
        await generalTextChannel.send(('But first, please tell me the name of the Customer in your shipping network '
                                       'which you would like to ship chocolate to.'))
        customerNode = await client.wait_for('message')
        customerNode = customerNode.content

        # TODO: This loop does not terminate until proper input is provided
        i = 0
        while not (customerNode in graph.vertices and graph.vertices[customerNode].type == 'C'):
            await generalTextChannel.send(('I couldn\'t find a Customer with that name in your shipping network. '
                                           'Please try again.'))
            customerNode = await client.wait_for('message')
            customerNode = customerNode.content
            i += 1
            if i > 3:
                # Prevent infinite loop if user submits graph with no customer nodes.
                await generalTextChannel.send('Too many failed attempts. Please submit $shipping again and retry.')

        await generalTextChannel.send('Great! Meet me in the #chocolate-factory channel for your solution.')
        cheapestFactory = findCheapestShippingPath(graph, customerNode)
        await chocolateShippingChannel.send('Hello, customer! I\'ve found the factory with cheapest shipping cost to you.')
        await chocolateShippingChannel.send('The factory you should order from is: ' + cheapestFactory[0])
        await chocolateShippingChannel.send('The total shipping cost to you will be: ' + str(cheapestFactory[1]))
        await chocolateShippingChannel.send('Enjoy your cheap chocolate!')
    else:
        await generalTextChannel.send(('So, you\'re a ruthless chocolate businessperson. Let\'s look at your shipping network '
                                       'and decide between a few locations to build your factory to minimize shipping costs ' 
                                       'to all the customers in your network.'))
        # Call MST solver for factory-builder and print output
        potential_factory = await client.wait_for('message')
        potential_factory = potential_factory.content
        # Code segment is in a try-except block in case the user
        # does not provide a valid potential factory name
        try:
            minimum_tree_dict = reachAllCustomers.prims_algorithm(graph, potential_factory)
            parsed_customer_paths = parse_mst_dict(minimum_tree_dict)
            await generalTextChannel.send("Go to the #chocolate-shipping channel to see the result of your query")
            await chocolateShippingChannel.send("From the potential factory site {}, the following paths must be "
                                                "taken to reach these customers".format(potential_factory))
            for path in parsed_customer_paths:
                await chocolateShippingChannel.send("`" + path + "`")
        except TypeError as err:
            await generalTextChannel.send(str(err))
            return


# -----------------------------
# ----- EVENT DEFINITIONS -----
# -----------------------------
# Here the events which define how ReMBot actually interacts with the server are defined.

# Here we create an event which triggers whenever a text message is sent in the server.
# We can parse messages sent by users and perform whatever actions we want depending
# on the message.
@client.event
async def on_message(message):
    # Ignore all messages sent by ReMBot itself to avoid potential infinite chat loops.
    if message.author == client.user:
        return

    # Simple message reply to demonstrate concept of interacting with the bot.
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    # If the user wants to solve the chocolate bar problem, query them for the required input,
    # solve the problem, and return the result.
    if message.content.startswith('$chocolate'):
        await chocolateProblem(message)

    # The user is requesting to run multiple events at once. Launch the framework to parse the event inputs
    # and run them concurrently.
    if message.content.startswith('$async'):
        await performConcurrentActions(message)

    # The user would like ReMBot to send a direct message to a named member of the server.
    if message.content.startswith('$dm'):
        message = message.content
        a_user = message[4:].split(' ')[0]
        a_message = ' '.join(message[4:].split(' ')[1:])
        await directMessageUser(a_user, a_message)

    if message.content.startswith('$schedule'):
        await scheduleForBreak(message)

    # The user would like ReMBot to find the longest snake sequence in a grid.
    if message.content.startswith('$snake'):
        await snakeSequenceTask()

    # The user would like ReMBot to play some code golf.
    if message.content.startswith('$golf'):
        await codeGolfHelper(message)

    # The user would like to figure out some shipping logistics for the chocolate economy.
    if message.content.startswith('$shipping'):
        await chocolateShippingHelper(message)


# This line is used for authentication purposes to allow interaction with the Discord api, and to begin the
# asynchronous event loop that allows all these lines of code to actually run.
client.run(ServerIDs.TOKEN.value)
