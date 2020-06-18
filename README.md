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


## References
https://discordpy.readthedocs.io/en/latest/index.html

http://www.cs.columbia.edu/~rjaiswal/factoring-survey.pdf