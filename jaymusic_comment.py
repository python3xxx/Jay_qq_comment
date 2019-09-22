import requests, json, time, pymongo, re

class JayMusicComment:
    def __init__(self, url=None):
        self.url = url
        self.comment = ''
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db = self.client['jay']
        self.col = self.db['comment']
        self.last_comment_id = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'Referer': 'https://y.qq.com/n/yqq/song/001qvvgF38HVc4.html?ADTAG=baiduald&play=1'
        }

    # 获取评论
    def get_comment(self, url):
        response = json.loads(requests.get(url, headers=self.headers).text)
        arr = []
        for i in response['comment']['commentlist']:
            # 评论id
            comment_id = i['commentid']
            if i['middlecommentcontent'] or self.is_exist(comment_id):
                continue
            # 评论内容
            comment_content_arr = re.findall(r'[\u4e00-\u9fa5]+', i['rootcommentcontent'])
            comment_content = ''.join(comment_content_arr)
            if not comment_content:
                continue
            self.write_txt(comment_content)
            # 点赞数
            praise_num = i['praisenum']
            # 昵称
            nick = i['nick']
            create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(i['time']))
            arr.append(comment_id)
            self.last_comment_id = comment_id
            # 保存
            self.save(comment_id, comment_content, nick, praise_num, create_time)
        print('last_comment_id: ' , comment_id)
        return self.last_comment_id


    # 保存数据
    def save(self, comment_id, comment_content, nick, praise_num, create_time):
        self.col.insert_one({
            '_id': comment_id,
            'comment_content': comment_content,
            'nick': nick,
            'praise_num': praise_num,
            'create_time': create_time
        })

    # 写入文本
    def write_txt(self, comment_content):
        with open('jay_comment.txt', 'a+', encoding='utf-8') as f:
            f.write(comment_content + '\n')

    def is_exist(self, comment_id):
        result = self.col.count({
            "_id": comment_id
        })
        return result

    # 启动
    def run(self):
        last_comment_id = self.get_comment(self.url)
        pagesiz = 1
        while 1:
            url = 'https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg?g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=GB2312&notice=0&' \
                  'platform=yqq.json&needNewCode=0&cid=205360772&reqtype=2&biztype=1&topid=237773700&cmd=8&needmusiccrit=0&pagenum=' + str(pagesiz) + \
                  '&pagesize=25&lasthotcommentid=' + last_comment_id + '&domain=qq.com&ct=24&cv=10101010'
            print('url == ', url)
            last_comment_id = self.get_comment(url)
            self.last_comment_id = last_comment_id
            pagesiz += 1



if __name__ == '__main__':
    jay = JayMusicComment('https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg?g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=GB2312&notice=0&platform=yqq.json&needNewCode=0&cid=205360772&reqtype=2&biztype=1&topid=237773700&cmd=8&needmusiccrit=0&pagenum=0&pagesize=25&lasthotcommentid=&domain=qq.com&ct=24&cv=10101010')
    jay.run()









