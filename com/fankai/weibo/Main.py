import urllib.request,json
import com.fankai.weibo.DatabaseUtil

def get_json_blog_data():
    req = urllib.request.Request(
        'http://m.weibo.cn/container/getIndex?type=uid&value=6058872024&containerid=1076036058872024')
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
    with urllib.request.urlopen(req) as html:
        data = json.loads(html.read().decode('utf-8', 'ignore'))['cards']
    return data

def parse_json(cards):
    for card in cards:
        if card['card_type'] == 9:
            blog = card['mblog']
            print(blog)
            if blog['created_at'] is not None and "分钟" in blog['created_at']:
                data = {}

                data["blog_id"] = blog['id']
                data["text"] = blog['text']
                if 'raw_text' in blog:
                    data["text"] = blog['raw_text']
                data["source"] = blog['source']
                data["pics"] = None
                if 'pics' in blog:
                    data["pics"] = blog['pics']
                data["retweeted_status"] = None
                if 'retweeted_status' in blog:
                    data["retweeted_status"] = blog['retweeted_status']
                data["user"] = blog['user']
                data["user_id"] = data["user"]['id']
                data["screen_name"] = data["user"]['screen_name']
                if not com.fankai.weibo.DatabaseUtil.is_have_blog_id(blog_id,user_id):
                    #send email
                    com.fankai.weibo.DatabaseUtil.insert(user_id,blog_id)
                    print(text)
                else:
                    print("recorded")



if __name__ == "__main__":
    com.fankai.weibo.DatabaseUtil.createTable('weibo')
    cards = get_json_blog_data()
    parse_json(cards)
