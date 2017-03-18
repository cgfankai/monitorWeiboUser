import urllib.request,sqlite3,json

def get_json_blog_data():
    req = urllib.request.Request(
        'http://m.weibo.cn/container/getIndex?type=uid&value=2783743235&containerid=1076032783743235')
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
    with urllib.request.urlopen(req) as html:
        data = json.loads(html.read().decode('utf-8', 'ignore'))['cards']

    return data


if __name__ == "__main__":
    print(get_json_blog_data())
