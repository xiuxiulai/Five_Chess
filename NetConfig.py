from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import *
import socket
import threading
class NetConfigWidget(QWidget):
    config_signal = pyqtSignal([str,str,str,str])
    exit_signal = pyqtSignal()
    def __init__(self,parent = None):
        super().__init__(parent = parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("网络配置")
        self.name_label = QLabel("姓名：",self)
        self.name_input = QLineEdit("玩家1",self)
        self.ip_label = QLabel("IP:",self)
        self.ip_input = QLineEdit("127.0.0.1",self)
        self.port_label = QLabel("Prot:",self)
        self.port_input = QLineEdit("10086",self)
        self.client_button = QPushButton("链接主机",self)
        self.server_button = QPushButton("我是主机",self)
        

        gridLayout = QGridLayout()
        gridLayout.addWidget(self.name_label,0,0)
        gridLayout.addWidget(self.name_input,0,1)
        gridLayout.addWidget(self.ip_label,1,0)
        gridLayout.addWidget(self.ip_input,1,1)
        gridLayout.addWidget(self.port_label,2,0)
        gridLayout.addWidget(self.port_input,2,1)
        gridLayout.addWidget(self.client_button,3,0)
        gridLayout.addWidget(self.server_button,3,1)
        self.setLayout(gridLayout)

        self.client_button.clicked.connect(self.client_btn_signal)
        self.server_button.clicked.connect(self.server_btn_signal)

    def server_btn_signal(self):
        self.config_signal.emit("server",self.name_input.text(),self.ip_input.text(),self.port_input.text())
    
    def client_btn_signal(self):
        self.config_signal.emit("client",self.name_input.text(),self.ip_input.text(),self.port_input.text())

    def closeEvent(self,a0:QtGui.QCloseEvent):
        self.close()
        self.exit_signal.emit()

class NetClient(QObject):
    msg_signal = pyqtSignal([str])
    def __init__(self,name,ip,port):
        super().__init__()
        self.name = name
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def buildConnect(self):
        '''建立链接'''
        self.socket.connect((self.ip,int(self.port)))
        threading.Thread(target=self.recv).start()
        pass

    def send(self,data):
        '''发送数据
        data(发送的数据)字符串类型'''
        self.socket.send(data.encode())
        pass

    def recv(self):
        '''接收数据'''
        while True:
            try:
                data  = self.socket.recv(4096).decode()
                self.msg_signal.emit(data)
            except:
                pass

class NetServer(QObject):
    msg_signal = pyqtSignal([str])
    def __init__(self,name,ip,port):
        super().__init__()
        self.name = name
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.cli_socket = None

    def buildConnect(self):
        self.socket.bind(("",int(self.port)))
        self.socket.listen(1)
        threading.Thread(target=self.__acceptConnect).start()


    def __acceptConnect(self):
        try:
            self.cli_socket,cli_addr = self.socket.accept()
        except:
            pass
        
        while True:
            try:
                data = self.cli_socket.recv(4096).decode()
                self.msg_signal.emit(data)
            except Exception as e:
                print(e)

    def send(self,data):
        if self.cli_socket == None:
            return
        self.cli_socket.send(data.encode())

        


if __name__ == "__main__":
    import sys
    import cgitb
    cgitb.enable("text")
    a = QApplication(sys.argv)
    m = NetConfigWidget()
    m.show()
    sys.exit(a.exec_())
    pass
