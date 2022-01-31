import lightbulb

plugin = lightbulb.Plugin("utils")

@plugin.command
@lightbulb.command("ping", "checks the bot is alive")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context) -> None:
    # Send a message to the channel the command was used in
    await ctx.respond(
        "Pong! it took me " + str(int(ctx.bot.heartbeat_latency * 1000)) + "ms"
    )


def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)