# -*- coding: utf-8 -*-
"""
### PACKAGES TO INSTALL ###
    
    discord
    chatterbot
    chatterbot_corpus

### DISCORD BOT INTENT REQUIREMENTS ###
    
    message_content

"""

import discord
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
#from chatterbot.trainers import CsvFileTrainer

import nltk

nltk.download("punkt_tab")


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

bot = ChatBot(
    "Poppy",
    preprocessors=[
        "chatterbot.preprocessors.clean_whitespace",
        "chatterbot.preprocessors.unescape_html",
        "chatterbot.preprocessors.convert_to_ascii"
        ],
    logic_adapters=[
        "chatterbot.logic.BestMatch",
        "chatterbot.logic.TimeLogicAdapter",
        "chatterbot.logic.MathematicalEvaluation"
        ]
    )

#List training
trainer = ListTrainer(bot)

trainer.train([
    "who are you",
    "My name is Poppy! I'm a chatbot made by Madeline Higson. So far there isn't much I can really do because the library that enables my speech was a hastle for Maddy to set up... But she's thinking of finding a newer library to use to improve me soon!",
    ])

trainer.train([
    "what can you do",
    "So far all I can really do is ***kind of*** talk back and forth with you. I have the capability of doing basic math and telling you the time, but to be honest I'm having a hard time figuring out when people are asking me for it..."
    ])

#Corpus training
trainer = ChatterBotCorpusTrainer(bot)

trainer.train("chatterbot.corpus.english")

"""
trainer = CsvFileTrainer(
    bot,
    field_map={
         'created_at': 0,
         'persona': 1,
         'text': 2,
         'conversation': 3
    }
)

trainer.train("training_data.csv")
"""

@client.event
async def on_ready():
    print("Logged in")
    print(f'Bot name: {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    # Activation command
    if message.content.startswith('$Poppy'):
        await message.channel.send("""What's up?""")
        
        #Conversation loop
        while True:
            
            #Get/prepare user response
            usr_message = await client.wait_for("message", timeout=60)
            usr_statement = str(usr_message.content)
            command = " "+usr_statement.lower()+" "
            
            #Check for stop command
            if " stop " in command or " nothing " in command or " never mind " in command:
                await message.channel.send("Okay! Call me if you need me!")
                break
            
            else:
                #Get bots response and send to channel
                bot_statement = bot.get_response(usr_statement)
                await message.channel.send(bot_statement)

client.run("YOUR TOKEN GOES HERE")
