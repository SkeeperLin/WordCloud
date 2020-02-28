from wordcloud import WordCloud
import matplotlib.pyplot as plt
import jieba
import numpy
from PIL import Image

backgroundPath='Image\img.jpg'          # 背景图片路径
fontPath='Fonts\msyh.ttf'               # 字体路径
keyWordsPath='KeyWords\CloudWords.txt'  # 文本路径

def makeWordCloud():
    # 导入背景图片
    backgroundImage=numpy.array(Image.open(backgroundPath))

    with open(keyWordsPath) as file:
        #用结巴分词将语段分词
        text = file.read()
        keyWords = ''
        keyWords += ' '.join(jieba.lcut(text))

        #制作词云
        wordcloud = WordCloud(
            background_color="white",
            mask=backgroundImage,
            max_words=2000,
            font_path=fontPath,
            ).generate(keyWords)
        
        #存取
        wordcloud.to_file('wordcloud.png')

makeWordCloud()