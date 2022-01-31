import lightbulb
import hikari
import json
import datetime


plugin = lightbulb.Plugin("modmail")




@plugin.command
@lightbulb.command("cmail", "Closes the modmail in the current channel")
@lightbulb.implements(lightbulb.SlashCommand)
async def Cmail(ctx: lightbulb.Context) -> None:
    f = open("modmails.json", "r")
    mails = json.load(f)
    m = mails.copy()
    mails_channels = m.items()
    for key, value in mails_channels:
        if value == f"{ctx.channel_id}":
            print(key)
            user = await ctx.bot.rest.fetch_user(key)
            dm = await user.fetch_dm_channel()
            em = hikari.Embed(
                title="Staff has closed this modmail thread, if you still have any problem feel free to dm me",
                color=hikari.Colour.from_rgb(255, 0, 20),
                timestamp=datetime.datetime.now(tz=datetime.timezone.utc),
            )
            guild = ctx.get_guild()
            em.set_footer(f"Staff", icon=guild.icon_url)
            await dm.send(embed=em)
            # await dm.send("Staff has closed this modmail thread, if you still have any problem feel free to dm me")
            channel = await ctx.bot.rest.fetch_channel(value)
            print(mails)
            print(mails[f"{key}"])
            mails.pop(f"{key}")

            await channel.delete()
            f = open("modmails.json", "w")
            json.dump(mails, f)
            f.close()
            return
    await ctx.respond("Not a modmail thread")


@plugin.listener(hikari.GuildMessageCreateEvent)
async def onMessage(event: hikari.GuildMessageCreateEvent):
    hpl = ["help vg", "vg help", "pybosh help", "where is vg", "vg!!"]
    for i in hpl:
        if i == event.message.content:
            await event.message.respond(
                f"<@734305495770333314>, Quick, <@{event.author_id}> needs help!"
            )
    hpl = ["help pybash", "pybash help", "pybosh help", "where is pybash", "pybash!!"]
    for i in hpl:
        if i == event.message.content:
            await event.message.respond(
                f"<@626461325744275464>, Quick, <@{event.author_id}> needs help!"
            )

    if event.is_bot or not event.content:
        return
    f = open("modmails.json", "r")
    mails = json.load(f)
    mails_channels = mails.items()
    for key, value in mails_channels:
        if value == f"{event.channel_id}":
            print(key)
            user = await plugin.bot.rest.fetch_user(key)
            dm = await user.fetch_dm_channel()
            em = hikari.Embed(
                title=event.message.content,
                color=hikari.Colour.from_rgb(0, 255, 20),
                timestamp=datetime.datetime.now(tz=datetime.timezone.utc),
            )
            guild = event.get_guild()
            em.set_footer(f"Staff", icon=guild.icon_url)
            await dm.send(embed=em)


@plugin.listener(hikari.DMMessageCreateEvent)
async def onDM(event: hikari.DMMessageCreateEvent):
    if event.is_bot or not event.content:
        return
    guild = plugin.bot.cache.get_guild(927835307989159977)
    f = open("modmails.json", "r+")
    mails = json.load(f)
    try:
        print(mails)
        print(mails[str(event.author_id)])

        f.close()
        channel = plugin.bot.cache.get_guild_channel(mails[str(event.author_id)])
    except KeyError as e:
        print(e)
        channel = await guild.create_text_channel(
            name=event.author_id,
            category=927841708392189963,
        )
        mails[f"{event.author_id}"] = f"{channel.id}"
        await event.message.respond(
            "Thanks for dming us, our staff will get to you soon"
        )
        f = open("modmails.json", "w")
        json.dump(mails, f)
        f.close()

    em = hikari.Embed(
        title=event.content,
        color=hikari.Colour.from_rgb(0, 255, 20),
        timestamp=datetime.datetime.now(tz=datetime.timezone.utc),
    )
    em.set_footer(
        f"{event.author.username}#{event.author.discriminator}",
        icon=event.author.avatar_url,
    )
    await channel.send(embed=em)



def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)