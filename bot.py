import os
import lightbulb
import database
database.initialize()
if os.name != "nt":
    import uvloop

    uvloop.install()

with open("token", "r") as f:
    token = f.read()

bot = lightbulb.BotApp(
    token=token, prefix="b!", default_enabled_guilds=927835307989159977
)
for file in os.listdir("extensions"):
    if file.endswith("py"):
        ext = file[:-3]
        print(ext)
        bot.load_extensions(f"extensions.{ext}")


# Error Handling
@bot.listen(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.CommandErrorEvent):
    if isinstance(event.exception, lightbulb.CommandNotFound):
        pass
    elif isinstance(event.exception, lightbulb.NotEnoughArguments):
        await event.context.respond(f"A required arguement is missing, try b!help {event.context.command.name}")
    else:
        raise event.exception


bot.run()