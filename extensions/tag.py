import sqlite3
import hikari
import lightbulb
import aiosqlite

plugin = lightbulb.Plugin("tag")



async def create_tag( tag, content, author_id):
    db = await aiosqlite.connect("bot.db")
    sql = """INSERT INTO tags(author_id,title,uses,content) VALUES(?, ?, ?, ?) """
    await db.execute(sql, (author_id, tag,0, content))
    await db.commit()
    await db.close()

async def get_tag(title):
    db = await aiosqlite.connect("bot.db")
    sql = """SELECT * FROM tags WHERE title=?"""
    cursor = await db.execute(sql, (title,))
    row = await cursor.fetchone()
    await db.close()
    return row

async def add_use(row: sqlite3.Row):
    db = await aiosqlite.connect("bot.db")
    sql = """UPDATE tags SET uses = ? WHERE title=?"""
    await db.execute(sql, ((row[2]+1),row[1]))
    await db.commit()
    await db.close()

async def update_content(title, content):
    db = await aiosqlite.connect("bot.db")
    sql = """UPDATE tags SET content = ? WHERE title=?"""
    await db.execute(sql, (content, title))
    await db.commit()
    await db.close()

async def delete_tag(title):
    db = await aiosqlite.connect("bot.db")
    sql = """DELETE FROM tags WHERE title = ?"""
    await db.execute(sql, (title,))
    await db.commit()
    await db.close()
async def tag_list(author_id):
    db = await aiosqlite.connect("bot.db")
    sql = """SELECT * FROM tags where author_id=?"""
    cur = await db.execute(sql, (author_id,))
    await db.commit()
    rows = cur.fetchall()
    await db.close()

    return await rows
   
    


@plugin.command
@lightbulb.option("title", "Title of the tag", required=True, type=str)
@lightbulb.command("tag", "Get a tag")
@lightbulb.implements(lightbulb.PrefixCommandGroup)
async def tag(ctx: lightbulb.Context) -> None:
    row = await get_tag(ctx.options.title)
    print(row)
    if row:
        await ctx.respond(row[3])
        await add_use(row)
    else:
        await ctx.respond("Can't find a tag with that name")



@tag.child
@lightbulb.option("content", "Content of the tag", required=True, type=str, modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.option("title", "Title of the tag", required=True, type=str)
@lightbulb.command("create", "make a tag")
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def make_tag(ctx: lightbulb.Context) -> None:
    title = ctx.options.title
    content = ctx.options.content
    author_id = ctx.author.id
    print("hre")
    if await get_tag(title=title) != None:
        print("1")
        await ctx.respond(f"A tag with this name already exists")
        return
    print("2")
    print(await create_tag(title, content, author_id))
    await ctx.respond(f"created tag")


@tag.child
@lightbulb.option("title", "Title of the tag", required=True, type=str)
@lightbulb.command("info", "Get info about a tag")
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def tag_info(ctx: lightbulb.Context):
    row = await get_tag(ctx.options.title)
    print(row)
    if row:
        print("ur")
        em = hikari.Embed(
            title=f"Created by {(await ctx.bot.rest.fetch_user(row[0])).username}",
            description=f"Uses : {row[2]}",
            color=hikari.Colour.from_rgb(0, 255, 20),
        )
        print("ur")
        await ctx.respond(embed=em, reply=True)
    else:
        await ctx.respond("Can't find a tag with that name")

@tag.child
@lightbulb.option("content", "New content of the tag", required=True, type=str, modifier=lightbulb.OptionModifier.CONSUME_REST )
@lightbulb.option("title", "Name of the tag", required=True, type=str)
@lightbulb.command("edit", "Edit ur tag")
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def tag_edit(ctx: lightbulb.Context):
    row = await get_tag(ctx.options.title)
    print(row)
    if row:
        if not row[0] == ctx.author.id:
            await ctx.respond("This tag is not made by you hence you can't edit it")
        else:
            await update_content(row[1], ctx.options.content)
            await ctx.respond("Successfully updated")
    else:
        await ctx.respond("Can't find a tag with that name")

    
@tag.child
@lightbulb.option("title", "Name of the tag", required=True, type=str)
@lightbulb.command("delete", "delete ur tag")
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def tag_edit(ctx: lightbulb.Context):
    row = await get_tag(ctx.options.title)
    print(row)
    if row:
        if not row[0] == ctx.author.id:
            await ctx.respond("This tag is not made by you hence you can't edit it")
        else:
            await delete_tag(row[1])
            await ctx.respond("Successfully deleted")
    else:
        await ctx.respond("Can't find a tag with that name")


@tag.child
@lightbulb.option("member", "the member whose tags you want", type=hikari.Member, required=False)
@lightbulb.command("list", "Lists all tags of a member")
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def list_tag(ctx: lightbulb.Context):
    if ctx.options.member:
        tags = await tag_list(ctx.options.member.id)
    else:    
        tags = await tag_list(ctx.author.id)
    print(tags)
    print(type(tags))
    try:
        em = hikari.Embed(title=f"Tags", description=f" - {ctx.options.member.username}")
        for tag in tags:
            em.add_field(tag[1], f"uses : {tag[2]}")
        await ctx.respond(embed=em)
    except Exception as e:
        print(e)

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)