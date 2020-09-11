# WikiGameBot
This is a Discord bot for playing "the Wikipedia game".

## Rules of the game
1. Everybody except for one person (the "interrogator") selects a Wikipedia article, reads it, 
and writes the title on a piece of paper.
2. The "interrogator" select an article picks on of the articles at random and reads the title out aloud.
3. Everybody has to act like it's their article while the interrogator has to ask questions to find out 
whose article it is.

## Usage of the bot
1. Add it to your server.
2. Select a text channel you want to play the game in by typing "!start".
3. Everybody submits their article by sending a DM with "!s \<ARTICLE TITLE\>" to the bot. 
If you want to change your submission later, you can do so by simply submitting another article. 
The bot will automatically remove the old submission.
4. Use "!draw" in the game channel to have the bot pick on of the submissions at random.
5. The interrogator asks questions and uses "!guess @User" to take a guess or "!solution" to show the solution 
(and a list of all submitted articles).

## Hosting your own instance of the bot
Since I do not host an instance of the bot for public usage 
(the bot currently doesn't support multiple concurrent games anyways), you will need to host your own instance 
by following these steps:
* [Get a bot token](https://discord.com/developers/applications)
* Specify it in `secrets.json` according to the template in `secrets.json.example`
* `pip3 install discord`
* Run `main.py`


# Inspiration
[Two of these people are lying](https://www.youtube.com/playlist?list=PLfx61sxf1Yz2I-c7eMRk9wBUUDCJkU7H0) 
by [The Technical Difficulties](https://www.techdif.co.uk/)