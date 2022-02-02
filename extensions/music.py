import hikari
from youtube_search import YoutubeSearch
import lightbulb
from songbird import YtdlError, ytdl, Driver, Queue
import songbird
from songbird.hikari import Voicebox
import datetime
import miru

plugin = lightbulb.Plugin("music")


# Components
class MyView(miru.View):

    @miru.button(emoji="⏭️", style=hikari.ButtonStyle.PRIMARY)
    async def rock_button(self, button: miru.Button, interaction: miru.Interaction):
        await interaction.send_message(content="Paper!")

    @miru.button(emoji="⏯️", style=hikari.ButtonStyle.PRIMARY)
    async def paper_button(self, button: miru.Button, interaction: miru.Interaction):
        await interaction.send_message(content="Scissors!")

    @miru.button( emoji="⏮️", style=hikari.ButtonStyle.PRIMARY)
    async def scissors_button(self, button: miru.Button, interaction: miru.Interaction):
        await interaction.send_message(content="Rock!")

    @miru.button(emoji="❌", style=hikari.ButtonStyle.DANGER, row=2)
    async def stop_button(self, button: miru.Button, interaction: miru.Interaction):
        self.stop()  # Stop listening for interactions


queues: dict[int, Queue] = {}


async def on_fail(driver: Driver, video):
    print("fish")


#     track_handle = await voice.play_source(await ytdl("https://www.youtube.com/watch?v=SlPhMPnQ58k"))

#     await sleep(5)
#     # Doesn't need to be awaited!
#     track_handle.pause()
#     await sleep(5)
#     track_handle.play()

@plugin.command
@lightbulb.option("song", "song/name of song", required=False, type=str)
@lightbulb.command("play", "play a song", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def play(ctx: lightbulb.Context) -> None:
    try:
        if not ctx.options.song:
            queues[ctx.guild_id].track_handle.play()
            await ctx.respond("Music resumed")
        else:
            try:
                song = await ytdl(ctx.options.song)

                queues[ctx.guild_id] += [song]
                await ctx.respond(f"Added {(await song.metadata()).title}")
            except YtdlError:
                results = YoutubeSearch(ctx.options.song, max_results=1).to_dict()
                song = await ytdl(f"https://youtube.com" + results[0]["url_suffix"])
                queues[ctx.guild_id].append(song)
                await ctx.respond(f"Adding {(await song.metadata()).title}")
    except:
        if not ctx.options.song:
            await ctx.respond("song is a required argument that is missing")
        states = ctx.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
        voice_state = [
            state
            async for state in states.iterator().filter(
                lambda i: i.user_id == ctx.author.id
            )
        ]
        if not voice_state:
            print(type(voice_state))
            print(voice_state)
            await ctx.respond("You need to be in a voice channel to do that")

        else:

            try:
                voice = await Voicebox.connect(plugin.bot, ctx.guild_id, voice_state[0].channel_id)
                queues[ctx.guild_id] = Queue(voice)
                song = await ytdl(ctx.options.song)
                queues[ctx.guild_id].append(song)
                print(queues[ctx.guild_id].running)

                await ctx.respond(f"Playing {(await song.metadata()).title}")
            except songbird.YtdlError as e:
                results = YoutubeSearch(ctx.options.song, max_results=1).to_dict()
                song = await ytdl(f"https://youtube.com" + results[0]["url_suffix"])
                queues[ctx.guild_id].append(song)
                await ctx.respond(f"Playing {(await song.metadata()).title}")


@plugin.command
@lightbulb.command("pause", "pause the music")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def pause(ctx: lightbulb.Context) -> None:
    try:
        print(queues[ctx.guild_id])
        queues[ctx.guild_id].track_handle.pause()
        await ctx.respond("Music Paused")

    except Exception as e:
        await ctx.respond("Music not playing")


@plugin.command
@lightbulb.command("skip", "skip the song")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def skip(ctx: lightbulb.Context) -> None:
    try:
        print(queues[ctx.guild_id])
        queues[ctx.guild_id].skip()
        await ctx.respond("song skipped")
    except Exception as e:
        await ctx.respond("Music not playing")


@plugin.command
@lightbulb.command("queue", "see the queue")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def queue(ctx: lightbulb.Context) -> None:
    try:
        queue = (queues[ctx.guild_id])
        em = hikari.Embed(
            title="Currently Playing",
            description=queue.track_handle.metadata.title,
            color=hikari.Colour.from_rgb(255, 0, 20),
            timestamp=datetime.datetime.now(tz=datetime.timezone.utc),
        )
        guild = ctx.get_guild()
        em.set_footer(f"Botto", icon=ctx.bot.application.icon_url)
        view = MyView(ctx.bot, timeout=120)
        for index, i in enumerate(queue):
            em.add_field(name=f"{index + 1}. {(await i.metadata()).title}", value=(await i.metadata()).artist)
        await ctx.respond(embed=em, components=view.build())
    except Exception as e:

        await ctx.respond(e)


@plugin.command
@lightbulb.command("leave", "leave the music channel")
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def leave(ctx: lightbulb.Context) -> None:
    pass
    # TODO: make a leave command, haven't made till now because can't figure out how
    await ctx.respond("not implemented yet")


def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)
