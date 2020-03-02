from wordcloud import WordCloud,ImageColorGenerator
import jieba
import numpy
from PIL import Image
import sys
from PyQt5.QtWidgets import QWidget, QApplication,QPushButton,QColorDialog,QTextEdit,QFileDialog,QLabel,QMessageBox
from PyQt5.QtGui import *


class WordCloudWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(600,480)
        self.setWindowTitle('WordCloud Maker')

        # 文本选择按钮
        self.chooseFileButton=QPushButton('选择文本文件',self)
        self.chooseFileButton.setGeometry(40,40,160,40)
        self.chooseFileButton.clicked.connect(self.openFile)
        # 文本预览框
        self.textContain=QTextEdit(self)
        self.textContain.setGeometry(230,40,320,150)
        self.textContain.setText('文本预览...')
        
        
        # 图片选择按钮
        self.backgroundImage=None
        self.image_colors=None
        self.chooseImageButton=QPushButton('选择图片蒙版',self)
        self.chooseImageButton.setGeometry(40,210,160,40)
        self.chooseImageButton.clicked.connect(self.openImage)
        # 图片预览框
        self.imageContain=QLabel(self)
        self.imageContain.setText('蒙版预览...\n默认为长方形')
        self.imageContain.setGeometry(230,210,320,150)
        self.imageContain.setStyleSheet("QLabel{background:white;border:1px solid grey;}")

        # 制作词云按钮
        self.makeButton=QPushButton('制作图云',self)
        self.makeButton.setGeometry(150,400,300,40)
        self.makeButton.clicked.connect(self.makeWordCloud)
        


        self.show()

    def openFile(self):
        self.filePath=QFileDialog.getOpenFileName(self,'打开文件','./')
        if self.filePath[0]:
            with open(self.filePath[0],'r') as file:
                text=file.read()
                self.textContain.setText(text)

    def openImage(self):
        imagePath=QFileDialog.getOpenFileName(self,'打开图片','','*.jpg;;*.png;;All Files(*)')
        if imagePath[0]:
            image=QPixmap(imagePath[0]).scaled(self.imageContain.width(),self.imageContain.height())
            self.imageContain.setPixmap(image)
            self.backgroundImage=numpy.array(Image.open(imagePath[0]))
            # 读取图片颜色
            self.image_colors = ImageColorGenerator(self.backgroundImage)

    def makeWordCloud(self):
        fontPath='Fonts\msyh.ttf' # 字体路径

        # 用结巴分词将语段分词
        with open(self.filePath[0]) as file:
            text=file.read()
            keyWords=''
            keyWords+=' '.join(jieba.lcut(text))


        # 制作词云
        wordcloud = WordCloud(
            background_color="white",
            mask=self.backgroundImage,
            max_words=2000,
            font_path=fontPath,
            repeat=True,
            color_func=self.image_colors,
            ).generate(keyWords)

        # 存取
        wordcloud.to_file('wordcloud.png')
        # 弹出成功提示
        self.showMessage()
    
    def showMessage(self):
        QMessageBox.about(self,'','制作完成')
        sys.exit()

                
if __name__=='__main__':
    app=QApplication(sys.argv)
    showwordcloud=WordCloudWindow()
    sys.exit(app.exec_())

