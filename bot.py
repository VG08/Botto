# Imports
import os
import lightbulb
import database

if os.name != "nt":
    import uvloop
    
    uvloop.install()

# Bot setup 
database.initialize()
with open("token", "r") as f:
    TOKEN = f.read()

bot = lightbulb.BotApp(
    token = TOKEN,
    prefix = "b!",
    default_enabled_guilds = (927835307989159977, 872490089731723365)
)

# NOTE TO VG08:
# Add the token to a .py file, this is useful since you can add more secrets later and
# is especially more useful when you deal with secrets that are not of type: str

for file in os.listdir("extensions"):
    if file.endswith("py"):
        ext = file[:-3]
        print(ext)
        bot.load_extensions(f"extensions.{ext}")


# Error Handling
@bot.listen(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.CommandErrorEvent):

    if isinstance(event.exception, lightbulb.CommandNotFound):
        # Runs when a command does not exist.
        pass

    elif isinstance(event.exception, lightbulb.NotEnoughArguments):
        # Runs when all required arguments are not specified correctly.
        await event.context.respond(f"A required arguement is missing, try b!help {event.context.command.name}")
    
    else:
        raise event.exception


bot.run()