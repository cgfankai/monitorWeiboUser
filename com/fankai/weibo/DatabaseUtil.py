import sqlite3

conn = sqlite3.connect('weibo.db')
c = conn.cursor()


def createTable(tableName):
    c.execute(
        "SELECT name FROM sqlite_master WHERE type IN ('table','view') AND name NOT LIKE 'sqlite_%' UNION ALL SELECT"
        " name FROM sqlite_temp_master WHERE type IN ('table','view')")
    resultList = c.fetchall()
    if (tableName,) not in resultList:
        c.execute(
            "create table {} (user_id INTEGER NOT NULL , blog_id INTEGER NOT NULL, text TEXT, source TEXT,screen_name TEXT);".format(
                tableName))


def insert(user_id, blog_id, text, source, screen_name, table='weibo'):
    c.execute("INSERT INTO {}(user_id, blog_id,text,source,screen_name) VALUES ({},{},{},{},{})".format(table, user_id,
                                                                                                        blog_id, text,
                                                                                                        source,
                                                                                                        screen_name))
    conn.commit()


def is_have_blog_id(blog_id, user_id, table='weibo'):
    c.execute("SELECT blog_id FROM {} WHERE blog_id = {} AND user_id = {}".format(table, blog_id, user_id))
    result = len(c.fetchall())
    if result == 0:
        return False
    else:
        return True


if __name__ == "__main__":
    createTable('weibo')
    print(is_have_blog_id(33, 12))
