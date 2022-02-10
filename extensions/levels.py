import lightbulb
import hikari   
import aiosqlite

XP_FOR_LVL_1 = 50

plugin = lightbulb.Plugin("levels")

async def add_xp(row: aiosqlite.Row):
    db = await aiosqlite.connect("bot.db")
    sql = """UPDATE levels SET xp = ? WHERE user_id=?"""

    await db.execute(sql, ((row[1]+1),row[0]))
    await db.commit()
    sql = """UPDATE levels SET msg_before_xp = 0 WHERE user_id=?"""
    await db.execute(sql,(row[0],))
    await db.commit()
    await db.close()

async def get_xp(user_id) -> aiosqlite.Row:
    db = await aiosqlite.connect("bot.db")   
    sql = """SELECT * FROM levels WHERE user_id=?"""
    cursor = await db.execute(sql, (user_id,))
    row = await cursor.fetchone()
    await db.close()
    return row
    
async def give_xp_before_msg(user_id, before_msg_xp):
    db = await aiosqlite.connect("bot.db")
    sql = """UPDATE levels SET msg_before_xp = ? WHERE user_id=?"""
    await db.execute(sql, (before_msg_xp, user_id))
    await db.commit()
    await db.close()



async def add_user(user_id):
    db = await aiosqlite.connect("bot.db")
    sql = """INSERT INTO levels(user_id, xp,lvl, msg_before_xp) VALUES(?,?,?, ?) """
    await db.execute(sql, (user_id, 0,0, 1))
    await db.commit()
    await db.close()

   

@plugin.listener(hikari.GuildMessageCreateEvent)
async def on_message(event: hikari.GuildMessageCreateEvent):
    if event.author.is_bot:
        return
    author = event.author_id
    row = await get_xp(author)
    if row:
        if row[3] == 4:
            await add_xp(row)
        else:
    
            await give_xp_before_msg(author, (row[3]+1))
    else:
        await add_user(author)



@plugin.command
@lightbulb.command("xp", "Gives ur xp")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def check_xp(ctx: lightbulb.Context) -> None:
    row = await get_xp(ctx.author.id)
    await ctx.respond(
        f"You have {row[1]}xp"
    )


        


def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)