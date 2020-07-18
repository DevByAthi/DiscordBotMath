# DiscordBotMath
We present ReMBot, the Recreational Mathematics Bot, for Discord. 
Discord is a free communication platform that allows users to create _bots_, 
automated chatbots that can perform pre-defined tasks. When added to a server, ReMBot will allow the user to
 enter commands to solve mathematical puzzles and games. The first puzzle is given below

## Setup and Run
1. Create a folder to store a local version of this repo on your machine
2. Clone the repo to your local machine via the command `git clone https://github.com/TheRogueDalek/DiscordBotMath.git`
3. Create a discord account [here](https://discordapp.com/)
4. Join our server dedicated to testing ReMBot [here](https://discord.gg/awFeeb5)
5. Run ReMBot.py on your local machine. On the command line, this is done by going to the _DiscordMathBot_ directory and running the command `python ReMBot.py`
6. Check on the testing server that ReMBot is online by clicking on "Member List" in the top-right of Discord
7. Run one of the commands the ReMBot recognizes.
8. Follow ReMBot's instructions and have fun with math!

## The Chocolate Bar Problem
The first command we've implemented allows users to play with the Chocolate Bar Problem, which is defined as follows.
You are given a rectangular chocolate bar composed of square pieces of chocolate. The width and height are given.
You are asked to break apart the chocolate bar to obtain a desired number of squares to eat. The desired number of squares is given.

The only valid way to break up a chocolate bar is by splitting it along the grooves
between the squares. **You cannot divide an individual square. You cannot partially break a chocolate bar**; 
the break must run the full length of the bar, splitting it in two.

Your task (or ReMBot's, really) is to find the minimum number of breaks needed to obtain the desired number of squares.
ReMBot is not great at drawing, so it will verbally describe the steps needed 
for you to break apart the chocolate bar and get your desired amount. 
If it is not possible to obtain the desired number of squares, ReMBot will tell you in so many words.

To give the width and height of a chocolate bar and ask ReMBot to help you get a particular amount of chocolate,
run the command `$chocolate` in the test server, and follow the directions. Enjoy!

### Divide and Conquer

The divide-and-conquer method is applied to the Chocolate Bar Problem in a 
special case where one can create sub-problems of the Chocolate Bar Problem. Oftentimes, a user will request a
desired area that _cannot_ be obtained in a single break (this would occur if the desired area is a multiple of at least one of the side lengths).
When this occurs, we first attempt to take as large a piece of the side of the original chocolate bar as possible. 
We reduce the desired area by this reduced amount in preparation for the sub-problem.

In this sub-problem, we take the remaining, unused portion of the original chocolate bar
and attempt to obtain the remaining desired area for it. The "conquering" part of the method is where we combine the 
first break with the number of breaks needed in the sub-problem to determine the total number of breaks needed.

To see this divide-and-conquer method in action, give ReMBot an input of a 5-by-7 chocolate bar and a desired area of 32.

### Concurrency Framework

ReMBot provides a framework for carrying out numerous actions concurrently. These actions include a number of puzzles
and administrative tasks. This allows users to query ReMBot for multiple things at once in case they are short on time,
for example. In order to initiate this framework, query ReMBot with `$async`. ReMBot will guide you through the 
rest of the required steps.

### Meeting Scheduler

ReMBot provides users with a convenient interface for figuring out which meetings to attend during a given work day.
Users with a packed schedule may have to choose between many meetings on any given day, and they may struggle to find
a break in their schedule to relax for a moment. Users query this interface by sending a message saying
`$schedule N`, where N is the length of the desired break in minutes. Additionally, the user must attach a text
file to this message containing the start and end times of all the meetings on their calendar. For an example
of how to format this text file, see the sample1.txt file in the DiscordBotMath GitHub repository. Once
provided with this information, ReMBot will return a planned-out schedule allowing the user to fit in as many
meetings as possible while still leaving time for a break of the specified length. If there exists no possible
schedule which accommodates the desired break length, ReMBot will let the user know.

### Snake Problem Solver

In the Snake Problem, one is provided with a rectangular grid of numbers and tasked with finding the longest sequence
of adjacent numbers such that for each number, the number either to the right of or below the current number is 
+1 or -1 the value of the current number. Such a sequence is known as a Snake Sequence. ReMBot provides a solver
for the Snake Problem, which a user may utilize by calling `$snake` and then, in a follow-up message, providing a
rectangular grid of numbers as a single message. Once ReMBot has solved the problem, it will re-print the grid
for convenience and then print the longest Snake Sequence found in the grid. If the grid contains two
or more Snake Sequences with identical length longer than any other Snake Sequences, one of those sequences
will be printed at random.

### Code Golf

ReMBot loves to golf, and ReMBot loves to help golfers of all kinds optimize their paths through a golf course.
For the sake of this problem, a golf course is represented by a grid of integers which one may think of as a top-down
view onto the terrain of the course. The x and y positions are the terrain locations, and the value of the grid
at a given location is the height of the terrain. A golf ball always begins at the top-left of the terrain grid, and 
the hole is always at the bottom-right of the terrain grid. When standing at a position on the terrain grid, a golfer
can only see as far as the next piece of terrain which is higher than the golfer's current height. Thus, 
the golfer has limited information at any given square. The golfer may be very lazy, in which case they will want to 
avoid hitting to terrain with a height much higher than their own, even if it means they take more overall hits to 
get to the end of the course. Alternatively, the golfer may be very strong, in which case they won't care about
hitting over a mountain if it gets them closer to the end of the course. ReMBot allows the user to specify which of 
these two types of golfer they are. Based on this specification, ReMBot will attempt to optimize for a different goal. 
The user may query ReMBot for this service by calling `$golf`. ReMBot will then ask the user to provide a grid of
numbers representing the golf course terrain, followed by a specification of what to optimize for: 
`-hits` or `-effort`. ReMBot will return a list of tuples representing which squares the user
should hit towards to achieve their solution of the course.

## References
https://discordpy.readthedocs.io/en/latest/index.html

http://www.cs.columbia.edu/~rjaiswal/factoring-survey.pdf