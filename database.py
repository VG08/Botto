import sqlite3  

def initialize():
    conn = sqlite3.connect("bot.db")

    tags_table_sql = """ CREATE TABLE IF NOT EXISTS tags (
                                        author_id integer NOT NULL,
                                        title text PRIMARY KEY,
                                        uses integer NOT NULL,
                                        content text NOT NULL
                                    ); """
    c = conn.cursor()
    levels_table_sql = """ CREATE TABLE IF NOT EXISTS levels (
                                        user_id integer PRIMARY KEY,
                                        xp integer NOT NULL,
                                        lvl integer,
                                        msg_before_xp integer
                                    ); """

    c.execute(tags_table_sql)
    c.execute(levels_table_sql)

if __name__ == "__main__":
    initialize()