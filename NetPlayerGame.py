from DoublePlayerGame import *
import json
from NetConfig import *
from PyQt5.QtMultimedia import QSound

class NetPlayerGame(DoublePlayGame):
    def __init__(self,net_object, parent = None):
        super().__init__(parent = parent)
        self.net_object = net_object
        self.net_object.buildConnect()#建立网络链接
        self.net_object.msg_signal.connect(self.parseData)
        self.m_color = None#玩家棋子颜色

        self.cuicuBtn = MyButton.MyButton('source/催促按钮_hover.png',
                     'source/催促按钮_normal.png',
                     'source/催促按钮_press.png',
                     parent=self)
        self.cuicuBtn.move(650,600)

        self.cuicuBtn.clicked.connect(self.cuicu)

    def cuicu(self):
        QSound.play('source/cuicu.wav')
        msg = {}
        msg['msg_type'] = 'cuicu'
        self.net_object.send(json.dumps(msg))
        pass

    def goBack(self):
        self.backSignal.emit()
        self.close()
        self.net_object.socket.close()


    def downChessman(self,point,color):
        '''
        自动落子
        :return:
        '''
        #point = self.getPoint()

        # 注意：x,y坐标对应
        chess_index = (point.y(), point.x())  # 棋子在棋盘中的下标
        pos = QPoint(50+point.x()*30, 50+point.y()*30) # 棋子在棋盘中的坐标

        self.chessman = Chessman(color=color, parent=self)
        self.chessman.setIndex(chess_index[0], chess_index[1])
        self.chessman.move(pos)
        self.chessman.show()  # 显示棋子

        # 显示标识
        self.focusPoint.move(QPoint(pos.x() - 15, pos.y() - 15))
        self.focusPoint.show()
        self.focusPoint.raise_()

        self.chessboard[chess_index[0]][chess_index[1]] = self.chessman

        # 历史记录
        self.history.append((chess_index[0], chess_index[1], self.chessman.color))

        # 改变落子颜色
        if self.turnChessColor == 'black':
            self.turnChessColor = 'white'
        else:
            self.turnChessColor = 'black'
        # 判断输赢
        result = self.isWin(self.chessman)
        if result != None:
            print(result + '赢了')
            self.showResult(result)

        pass
    '''
    {
        "msg_type":"positon",
        "x":"10",
        "y":"15",
        "color":"black"
    }
    '''
    #解析网路数据
    def parseData(self,data):
        print("pardata:",data)
        try:
            msg = json.loads(data)
        except Exception as e:
            print(e)
            
        #msg = json.loads(data)
        print("msg:",msg)
        if msg["msg_type"] == "position":
            self.downChessman(QPoint(int(msg["x"]),int(msg["y"])),msg["color"])
            pass

        elif msg["msg_type"] == "restart":
            result = QMessageBox.information(None,'五子棋_提示消息','请求开始游戏',QMessageBox.Yes |QMessageBox.No)
            if result == QMessageBox.Yes:
                self.restartGame()#白子
                self.m_color = 'white'
                msg = {}
                msg['msg_type'] = "response"
                msg['action_type'] = 'restart'
                msg['action_result'] = 'yes'
                self.net_object.send(json.dumps(msg))

            else:
                msg = {}
                msg['msg_type'] = "response"
                msg['action_type'] = 'restart'
                msg['action_result'] = 'no'
                self.net_object.send(json.dumps(msg))
        elif msg['msg_type'] == 'response':
            if msg['action_type'] == 'restart':
                if msg['action_result'] == 'yes':
                    self.restartGame()
                    self.m_color = 'balck'
                else:
                    QMessageBox.information(self,'五子棋_提示消息','对方拒绝游戏')
            elif msg['action_type'] == 'huiqi':
                if msg['action_result'] == 'Yes':
                    self.huiqigame()
                else:
                    QMessageBox.information(self,'五子棋_提示消息','对方拒绝悔棋',QMessageBox.Yes |QMessageBox.No)


        elif msg['msg_type'] == 'huiqi':
            result = QMessageBox.information(self,'五子棋_提示消息','对方请求悔棋',QMessageBox.Yes |QMessageBox.No)
            if result == QMessageBox.Yes:  
                msg = {}
                msg['msg_type'] = "response"
                msg['action_type'] = 'huiqi'
                msg['action_result'] = 'Yes'
                self.net_object.send(json.dumps(msg))
                self.huiqigame()
            else:
                msg = {}
                msg['msg_type'] = "response"
                msg['action_type'] = 'huiqi'
                msg['action_result'] = 'No'
                self.net_object.send(json.dumps(msg))
        elif msg['msg_type'] == 'lose':
            show.showResult(self.m_color)

        elif msg['msg_type'] == 'cuicu':
            QSound.play('source/cuicu.wav')
            QMessageBox.window(self,'0')


                



    def restartGame(self):

        for i in range(19):
            for j in range(19):
                if self.chessboard[i][j] != None:
                    self.chessboard[i][j].close()
                    self.chessboard[i][j] = None
                    self.focusPoint.close()
                else:
                    pass
        self.lbl = None
        if self.lbl != None:
            self.lbl.close() 

        self.gameStatu = True 
        self.focusPoint.hide()
        self.turnChessColor="black"
            

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        if self.m_color != self.turnChessColor:
            return
        if self.gameStatu == False:
            return None
        pos,chess_index = self.reversePos(a0)
        if pos is None:
            return
        if self.chessboard[chess_index[1]][chess_index[0]] != None:
            return

        self.chess = Chessman(color=self.turnChessColor,parent=self)
        self.chess.setIndex(chess_index[1], chess_index[0])
        self.chess.move(pos)
        self.chess.show()#显示棋子
        self.history.append(self.chess)
        self.history2.append(self.focusPoint)

        self.focusPoint.move(QPoint(pos.x()-15,pos.y()-15))
        self.focusPoint.show()
        self.focusPoint.raise_()

        print("棋盘交点位置：",chess_index)

        #放入棋盘
        self.chessboard[chess_index[1]][chess_index[0]] = self.chess
        #发送落子信息
        msg = {}
        msg["msg_type"] = "position"
        msg["x"] = chess_index[1]
        msg["y"] = chess_index[0]
        msg["color"] = self.turnChessColor
        self.net_object.send(json.dumps(msg))
       

        if self.turnChessColor=="black":
            self.turnChessColor="white"
        else:
            self.turnChessColor="black"
        
        self.lbl = None
        result = self.isWin(self.chess)
        if result != None:
            print(result + '赢了') 
            self.showResult(result)


    def huiqi(self):
        if self.gameStatu == None:
            QMessageBox.warning(self,'五子棋提示','游戏没有开始，不能悔棋')
        if self.m_color != self.turnChessColor:
            QMessageBox.warning(self,'五子棋提示','不是你的回合')
        msg = {}
        msg['msg_type'] = 'huiqi'
        self.net_object.send(json.dumps(msg))

    def huiqigame(self):
        if self.gameStatu == False:
            return
        m = self.history.pop()
        a = self.history2.pop()
        self.chessboard[m.y][m.x] = None
        m.close()  
        a.close() 
        if self.turnChessColor=="black":
            self.turnChessColor="white"
        else:
            self.turnChessColor="black"

    def restar(self):
        msg = {}
        msg["msg_type"] = "restart"
        self.net_object.send(json.dumps(msg))



def lose(self):
        if self.gameStatu == False:
            QMessageBox.warning(None,'五子棋','游戏没有开始')
        if self.m_color == "black":
            self.lbl = QLabel(self)
            self.lbl.setPixmap(QPixmap("source/白棋胜利.png"))
            self.lbl.move(150,150)
            self.lbl.show()
        elif self.m_color == "white":
            self.lbl = QLabel(self)
            self.lbl.setPixmap(QPixmap("source/黑棋胜利.png"))
            self.lbl.move(150,150)
            self.lbl.show()
        else:
            return
        msg = {}
        msg['msg_type'] = "lose"
        #msg['action_type'] = 'restart'
        #msg['action_result'] = 'no'
        self.net_object.send(json.dumps(msg))
        


if __name__ == '__main__':
    import cgitb
    cgitb.enable("text")
    a = QApplication(sys.argv)
    m = NetPlayerGame()
    m.show()
    sys.exit(a.exec_())
    pass
