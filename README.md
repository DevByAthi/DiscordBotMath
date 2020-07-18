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
7. Run one of the commands the ReMBot recognizes. Currently, only the command `$chocolate` is implemented.
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

## References
https://discordpy.readthedocs.io/en/latest/index.html

http://www.cs.columbia.edu/~rjaiswal/factoring-survey.pdf

https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Practical_optimizations_and_infinite_graphs