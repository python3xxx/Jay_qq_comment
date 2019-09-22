from random import randint
from matplotlib import pyplot as plt
from wordcloud import WordCloud
import jieba

def random_color(word=None, font_size=None, position=None,  orientation=None, font_path=None, random_state=None):

    """Random Color func"""
    r = randint(30, 255)
    g = randint(30, 180)
    b = int(100.0 * float(randint(60, 120)) / 255.0)
    return "rgb({:.0f}, {:.0f}, {:.0f})".format(r, g, b)


content = open('jay_comment.txt', encoding='utf-8').read()
cut = jieba.cut(content)
cut_text = '/'.join(cut)

wordcloud = WordCloud(background_color="white",
                      width=1000,
                      height=600,
                      max_font_size=90,
                      font_path='C:\Windows\Fonts\Simhei.ttf', # 需要根据实际操作系统更换路径
                      color_func=random_color)
wordcloud.generate_from_text(cut_text)
plt.imshow(wordcloud)
plt.axis("off")
plt.savefig('jay.png', format='png', dpi=200)