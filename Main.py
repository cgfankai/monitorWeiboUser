#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import logging
import os
import sys
import time
import urllib.request
import DatabaseUtil
import Notication

logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

containerid = []


def write_img_file(img_url, filename):
    # thread = threading.Thread(target=)
    # thread.start()
    from_url_to_file(img_url, filename)


def from_url_to_file(img_url, filename):
    try:
        req = urllib.request.Request(img_url)
        req.add_header('User-Agent',
                       'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
        with urllib.request.urlopen(req) as html:
            f = open('img' + os.sep + filename, 'w+b')
            f.write(html.read())
            f.flush()
        logging.info('download img success:%s', filename)
    except:
        logging.error('send email exception:%s', sys.exc_info()[0])


def get_json_blog_data(id):
    try:
        req = urllib.request.Request(
            'http://m.weibo.cn/container/getIndex?containerid={}'.format(id))
        req.add_header('User-Agent',
                       'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
        with urllib.request.urlopen(req) as html:
            data = json.loads(html.read().decode('utf-8', 'ignore'))['cards']
        return data
    except:
        logging.error('send email exception:%s', sys.exc_info()[0])


def parse_json(cards,name):
    for card in cards:
        if card['card_type'] == 9:
            blog = card['mblog']
            if blog['created_at'] is not None and ("分钟" in blog['created_at'] or "今天" in blog['created_at']):
                data = {}
                data["blog_id"] = blog['id']
                data["text"] = blog['text']
                if 'raw_text' in blog:
                    data["text"] = blog['raw_text']
                data["source"] = blog['source']
                data["pics"] = None
                if 'pics' in blog:
                    data["pics"] = blog['pics']
                data["retweeted_status"] = False
                if 'retweeted_status' in blog:
                    data["retweeted_status"] = True

                data["user"] = blog['user']
                data["user_id"] = data["user"]['id']
                data["screen_name"] = data["user"]['screen_name']
                if not DatabaseUtil.is_have_blog_id(data["blog_id"], data["user_id"]):
                    # 保存数据库
                    DatabaseUtil.insert(data["user_id"], data["blog_id"], data["text"], data["source"],
                                        data["screen_name"], data["retweeted_status"])
                    # 下载微博图片
                    filenames = []
                    if data['pics'] is not None:
                        for i, img_json in enumerate(data['pics'], start=1):
                            img_url = img_json['url']
                            if "large" in img_json:
                                img_url = img_json['large']['url']
                            file_name = str(data["blog_id"]) + "_" + str(data["user_id"]) + str(i) + "." + \
                                        str(img_url).split('.')[-1:][0]
                            filenames.append(file_name)
                            write_img_file(img_url, file_name)
                    # send email
                    Notication.send_email(name + "    的新微博", data["text"], filenames)
                else:
                    logging.info('database has this record.')


if __name__ == "__main__":
    DatabaseUtil.createTable('weibo')
    DatabaseUtil.create_container_ids_table()
    DatabaseUtil.initial_data()
    if not os.path.exists('img'):
        os.mkdir("img")
    while True:
        containerid = DatabaseUtil.get_container_id()
        for id in containerid:
            try:
                name = DatabaseUtil.get_name_by_containerid(id)
                logging.info('now is get data of %s', name)
                cards = get_json_blog_data(id)
                parse_json(cards,name)
                logging.info("sleep 5s")
                time.sleep(5)
            except:
                logging.error('send email exception:%s', sys.exc_info()[0])
                Notication.send_email("monitorWeibo发现异常",sys.exc_info()[0],None,None)
