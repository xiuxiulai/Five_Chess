
from DoublePlayerGame import *

class SinglePlayerGame(DoublePlayGame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle('五子棋-单机模式')

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):

        if self.gameStatu == False:
            return None
        print(a0.pos())
        print("x:",a0.x())
        print("y:",a0.y())
        pos,chess_index = self.reversePos(a0)
        if pos is None:
            return

        if self.chessboard[chess_index[1]][chess_index[0]] != None:
            return
        # 玩家落子
        super().mouseReleaseEvent(a0)
            # 电脑落子
        self.autoDown()

    def getPointScore(self, x, y, color):
        '''
        返回每个点的得分
        y:行坐标
        x:列坐标
        color：棋子颜色
        :return:
        '''
        # 分别计算点周围5子以内，空白、和同色的分数
        blank_score = 0
        color_score = 0

        # 记录每个方向的棋子分数
        blank_score_plus = [0, 0, 0, 0]  # 横向 纵向 正斜线 反斜线
        color_score_plus = [0, 0, 0, 0]

        # 横线
        # 右侧
        i = x  # 横坐标
        j = y  # 纵坐标
        while i < 19:
            if self.chessboard[j][i] is None:
                blank_score += 1
                blank_score_plus[0] += 1
                break
            elif self.chessboard[j][i].color == color:
                color_score += 1
                color_score_plus[0] += 1
            else:
                break
            if i >= x + 4:
                break
            i += 1
        # print('123123')
        # 左侧
        i = x  # 横坐标
        j = y  # 纵坐标
        while i >= 0:
            if self.chessboard[j][i] is None:
                blank_score += 1
                blank_score_plus[0] += 1
                break
            elif self.chessboard[j][i].color == color:
                color_score += 1
                color_score_plus[0] += 1
            else:
                break
            if i <= x - 4:
                break
            i -= 1

        # 竖线
        # 上方
        i = x  # 横坐标
        j = y  # 纵坐标
        while j >= 0:
            if self.chessboard[j][i] is None:
                blank_score += 1
                blank_score_plus[1] += 1
                break
            elif self.chessboard[j][i].color == color:
                color_score += 1
                color_score_plus[1] += 1
            else:
                break
            if j <= y - 4:
                break
            j -= 1
        # 竖线
        # 下方
        i = x  # 横坐标
        j = y  # 纵坐标
        while j < 19:
            if self.chessboard[j][i] is None:
                blank_score += 1
                blank_score_plus[1] += 1
                break
            elif self.chessboard[j][i].color == color:
                color_score += 1
                color_score_plus[1] += 1
            else:
                break

            if j >= y + 4:  # 最近五个点
                break
            j += 1
        # 正斜线
        # 右上
        i = x
        j = y
        while i < 19 and j >= 0:
            if self.chessboard[j][i] is None:
                blank_score += 1
                blank_score_plus[2] += 1
                break
            elif self.chessboard[j][i].color == color:
                color_score += 1
                color_score_plus[2] += 1
            else:
                break

            if i >= x + 4:  # 最近五个点
                break
            i += 1
            j -= 1
        # 左下
        i = x
        j = y
        while j < 19 and i >= 0:
            if self.chessboard[j][i] is None:
                blank_score += 1
                blank_score_plus[2] += 1
                break
            elif self.chessboard[j][i].color == color:
                color_score += 1
                color_score_plus[2] += 1
            else:
                break

            if j >= y + 4:  # 最近五个点
                break
            i -= 1
            j += 1
        # 反斜线
        # 左上
        i = x
        j = y
        while i >= 0 and j >= 0:
            if self.chessboard[j][i] is None:
                blank_score += 1
                blank_score_plus[3] += 1
                break
            elif self.chessboard[j][i].color == color:
                color_score += 1
                color_score_plus[3] += 1
            else:
                break
            if i <= x - 4:
                break
            i -= 1
            j -= 1
        # 右上
        i = x
        j = y
        while i < 19 and j < 19:
            if self.chessboard[j][i] is None:
                blank_score += 1
                blank_score_plus[3] += 1
                break
            elif self.chessboard[j][i].color == color:
                color_score += 1
                color_score_plus[3] += 1
            else:
                break
            if i >= x + 4:
                break
            i += 1
            j += 1

        for k in range(4):
            if color_score_plus[k] >= 5:
                return 100

        # color_score *= 5
        return max([x + y for x, y in zip(color_score_plus, blank_score_plus)])

    def getPoint(self):
        '''
        返回落子位置
        :return:
        '''
        # 简单实现：返回一个空白交点
        # for i in range(19):
        #     for j in range(19):
        #         if self.chessboard[i][j] == None:
        #             return QPoint(j, i)
        #
        #  没有找到合适的点
        white_score = [ [ 0 for i in range(19) ] for j in range(19)]
        black_score = [ [ 0 for i in range(19) ] for j in range(19)]

        for i in range(19):
            for j in range(19):
                if self.chessboard[i][j] != None:
                    continue
                # 模拟落子
                self.chessboard[i][j] = Chessman(color='white',parent=self)
                white_score[i][j] = self.getPointScore(j, i, 'white')
                self.chessboard[i][j].close()
                self.chessboard[i][j] = None
                self.chessboard[i][j] = Chessman(color='black',parent=self)
                black_score[i][j] = self.getPointScore(j, i, 'black')
                self.chessboard[i][j].close()
                self.chessboard[i][j] = None


        print('----------------')
        # 将二维坐标转换成以为进行计算
        r_white_score =  []
        r_black_score = []
        for i in white_score:
            r_white_score.extend(i)
        for i in black_score:
            r_black_score.extend(i)

        # 找到分数最大值
        score = [ max(x,y) for x,y in zip(r_white_score,r_black_score) ]

        # 找到分数做大的下标
        chess_index = score.index(max(score))

        print(score,'\n',max(score))

        y = chess_index //19
        x = chess_index % 19

        return QPoint(x,y)

    def autoDown(self):
        '''
        自动落子
        :return:
        '''
        point = self.getPoint()

        # 注意：x,y坐标对应
        chess_index = (point.y(), point.x())  # 棋子在棋盘中的下标
        pos = QPoint(50+point.x()*30, 50+point.y()*30) # 棋子在棋盘中的坐标

        self.chessman = Chessman(color=self.turnChessColor, parent=self)
        self.chessman.setIndex(chess_index[1], chess_index[0])
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

if __name__ == '__main__':

    import cgitb
    cgitb.enable('text')

    a = QApplication(sys.argv)
    m = SinglePlayerGame()
    m.show()
    sys.exit(a.exec_())
