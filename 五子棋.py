from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys

import MyButton
import DoublePlayerGame
import SinglePlayerGame
from NetConfig import *
import NetPlayerGame


class Mainwindow(QWidget):

    

    def __init__(self,parent = None):
        super().__init__(parent)
        self.resize(760,650)
        self.setWindowTitle("我的五子棋")
        #设置窗口图标
        self.setWindowIcon(QIcon("source/icon.ico"))



        #设置背景图片
        p = QPalette(self.palette())#获得当前的调色板
        brush = QBrush(QImage("source/五子棋界面.png"))
        p.setBrush(QPalette.Background,brush)#设置调色版
        self.setPalette(p)#给窗口设置调色板


        self.singlePlayerBtn = MyButton.MyButton('source/人机对战_hover.png',
                     'source/人机对战_normal.png',
                     'source/人机对战_press.png',
                     parent=self)
        self.singlePlayerBtn.move(300,300)

        self.dancelePlayerBtn = MyButton.MyButton('source/双人对战_hover.png',
                     'source/双人对战_normal.png',
                     'source/双人对战_press.png',
                     parent=self)
        self.dancelePlayerBtn.move(300,400)
        #self.dancelePlayerBtn.clicked.connect(DoublePlayerGame)

        self.drawlePlayerBtn = MyButton.MyButton('source/联机对战_hover.png',
                     'source/联机对战_normal.png',
                     'source/联机对战_press.png',
                     parent=self)
        self.drawlePlayerBtn.move(300,500)

        #绑定开始双人游戏信号和槽函数
        self.dancelePlayerBtn.clicked.connect(self.startDoubliGame)
        self.singlePlayerBtn.clicked.connect(self.startSingleGame)
        self.drawlePlayerBtn.clicked.connect(self.startNetGame)


    def startDoubliGame(self):
        print("in")
        #构建双人对战界面
        self.doublePlayerGame = DoublePlayerGame.DoublePlayGame()
        #绑定返回界面
        self.doublePlayerGame.backSignal.connect(self.showStartGame)
        
        self.doublePlayerGame.show()#显示游戏界面
        self.close()


    def startSingleGame(self):
        self.SingleGame = SinglePlayerGame.SinglePlayerGame()
        self.SingleGame.backSignal.connect(self.showStartGame2)
        self.SingleGame.show()
        self.close()



    def startNetGame(self):
        self.netConfig = NetConfigWidget()
        self.netConfig.exit_signal.connect(self.show)
        self.netConfig.show()
        self.netConfig.config_signal.connect(self.receiveNetConfig)
        self.close()


    def receiveNetConfig(self,nettype,name,ip,port):
        '''
        接收网络配置信息
        '''
        print("net config:",nettype,name,ip,port)
        if nettype == "client":
            net_object = NetClient(name,ip,port)
        elif nettype == "server":
            net_object = NetServer(name,ip,port)
        else:
            return
        self.netPlayerGame = NetPlayerGame.NetPlayerGame(net_object=net_object)
        self.netPlayerGame.backSignal.connect(self.show)
        self.close()
        self.netPlayerGame.show()
        self.netConfig.hide()
        '''lbl = QLabel(self)
        pix = QPixmap("source/人机大战_norma.")'''

    #显示开始界面
    def showStartGame(self):
        self.show()
        self.doublePlayerGame.close()

    def showStartGame2(self):
        self.show()
        self.SingleGame.close()

    

if __name__ == "__main__":
    import cgitb
    cgitb.enable("text")
    a = QApplication(sys.argv)
    m = Mainwindow()
    m.show()
    sys.exit(a.exec_())
