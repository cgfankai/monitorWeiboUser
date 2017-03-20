#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3

conn = sqlite3.connect('weibo.db')
c = conn.cursor()

def get_name_by_containerid(container_id):
    c.execute('SELECT name FROM container_ids WHERE container_id={};'.format(container_id))
    return str(c.fetchone()[0])

def get_container_id():
    resulr_is_list = [];
    for row in c.execute("SELECT container_id from container_ids;"):
        resulr_is_list.append(row[0])
    return resulr_is_list

def create_container_ids_table():
    c.execute(
        "SELECT name FROM sqlite_master WHERE type IN ('table','view') AND name NOT LIKE 'sqlite_%' UNION ALL SELECT"
        " name FROM sqlite_temp_master WHERE type IN ('table','view')")
    resultList = c.fetchall()
    if ('container_ids',) not in resultList:
        c.execute(
            "create table container_ids (container_id TEXT NOT NULL, name TEXT);")
        c.execute("CREATE INDEX containerid_index ON container_ids(container_id);")

def createTable(tableName):
    c.execute(
        "SELECT name FROM sqlite_master WHERE type IN ('table','view') AND name NOT LIKE 'sqlite_%' UNION ALL SELECT"
        " name FROM sqlite_temp_master WHERE type IN ('table','view')")
    resultList = c.fetchall()
    if (tableName,) not in resultList:
        c.execute(
            "create table {} (user_id INTEGER NOT NULL , blog_id INTEGER NOT NULL, text TEXT, source TEXT,screen_name TEXT,retweeted_status BOOLEAN);".format(
                tableName))
        c.execute('CREATE INDEX blogid_index ON weibo(blog_id,user_id);')


def insert(user_id, blog_id, text, source, screen_name, retweeted_status, table='weibo'):
    c.execute(
        "INSERT INTO {}(user_id, blog_id,text,source,screen_name,retweeted_status) VALUES (?,?,?,?,?,?);".format(
            table),(user_id, blog_id, text, source, screen_name, retweeted_status))
    conn.commit()


def is_have_blog_id(blog_id, user_id, table='weibo'):
    c.execute("SELECT blog_id FROM {} WHERE blog_id = {} AND user_id = {}".format(table, blog_id, user_id))
    result = len(c.fetchall())
    if result == 0:
        return False
    else:
        return True

def initial_data():
    c.execute("SELECT container_id FROM container_ids;")
    result = c.fetchall()
    if len(result) > 0:
        return
    c.execute("insert into container_ids values ('107603*****','****');")
    conn.commit()

if __name__ == "__main__":
    create_container_ids_table()
    #initial_data()
    ids = get_container_id()

