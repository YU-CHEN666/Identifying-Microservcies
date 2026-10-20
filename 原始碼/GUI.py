#GUI介面和邏輯 檔案
from PyQt6 import QtWidgets
from PyQt6.QtCore import QRect,Qt,pyqtSignal,pyqtSlot
import importlib.util
from pathlib import Path
import os,time,subprocess,threading,re
import CustomEnum
import psutil


class MainWindows(QtWidgets.QWidget):
    #信號
    setLableLightSignal = pyqtSignal(object)
    showMessageBoxSignal = pyqtSignal(object,str)
    def __init__(self):
        super().__init__()
        self.resize(600,350)
        self.setWindowTitle("控制面板")
        #伺服器運作指示，會影響GUI程式是否結束
        self.isServerRun = False
        #啟動伺服器按鈕
        self.startServerButton = QtWidgets.QPushButton("啟動伺服器")
        self.startServerButton.clicked.connect(lambda: self.Button_Click_Handler(CustomEnum.ButtonMode.Start))
        #關閉伺服器按鈕
        self.shutdownServerButton = QtWidgets.QPushButton("關閉伺服器")
        self.shutdownServerButton.clicked.connect(lambda: self.Button_Click_Handler(CustomEnum.ButtonMode.Stop))
        self.shutdownServerButton.setEnabled(False)
        #結束程式按鈕
        self.shutdownProgramButton = QtWidgets.QPushButton("結束程式")
        self.shutdownProgramButton.clicked.connect(lambda: self.close())
        #按鈕垂直佈局
        btnLayoutContainer = QtWidgets.QWidget(self)
        btnLayoutContainer.setGeometry(QRect(5,40,200,270))
        buttonLayout = QtWidgets.QVBoxLayout(btnLayoutContainer)
        buttonLayout.addWidget(self.startServerButton)
        buttonLayout.addWidget(self.shutdownServerButton)
        buttonLayout.addWidget(self.shutdownProgramButton)
        # 左 上 右 下 預設都是9 
        buttonLayout.setContentsMargins(9, 0, 9, 0)
        buttonLayout.setSpacing(30)
        buttonLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        btnLayoutContainer.setStyleSheet("""
                                          QPushButton {
                                              font-size:18px;
                                              height:60px;}
                                        """)

        #伺服器運作中指示燈
        self.serverRunLableLight = QtWidgets.QLabel()
        self.serverRunLableLight.setStyleSheet("""
                                               background-color:black;
                                               border-radius:15px;
                                               """)
        self.serverRunLableLight.setFixedSize(30, 30)
        #伺服器停止指示燈
        self.serverStopLableLight = QtWidgets.QLabel()
        self.serverStopLableLight.setStyleSheet("""
                                                background-color:red;
                                                border-radius:15px;
                                                """)
        self.serverStopLableLight.setFixedSize(30, 30)
        #Textlabl 縮放政策(SizePolicy)
        textLableSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                    QtWidgets.QSizePolicy.Policy.Expanding)
        textLableSizePolicy.setVerticalStretch(1)
        #伺服器運作中標籤
        serverRunTextLable = QtWidgets.QLabel("伺服器運作中")
        serverRunTextLable.setSizePolicy(textLableSizePolicy)
        #伺服器停止中標籤
        serverStopTextLable = QtWidgets.QLabel("伺服器停止中")
        serverStopTextLable.setSizePolicy(textLableSizePolicy)
        #指示Grid佈局
        gridLayoutContainer = QtWidgets.QWidget(self)
        gridLayoutContainer.setGeometry(QRect(230, 105, 250, 140))
        gridLayout = QtWidgets.QGridLayout(gridLayoutContainer)
        gridLayout.addWidget(self.serverRunLableLight, 0, 0)
        gridLayout.addWidget(serverRunTextLable, 0, 1)
        gridLayout.addWidget(self.serverStopLableLight, 1, 0)
        gridLayout.addWidget(serverStopTextLable, 1, 1)
        gridLayoutContainer.setStyleSheet("font-size:30px;")
        #slot連接函數
        self.setLableLightSignal.connect(self.SetLableLight)
        self.showMessageBoxSignal.connect(self.showMessageBox)
        
        
    def SetThreadManageObject(self,thread):
        #建立屬性並賦值ThreadManage物件，連結信號
        self.threadManageObject = thread
        self.threadManageObject.setLableLightSignal = self.setLableLightSignal
        self.threadManageObject.showMessageBoxSignal = self.showMessageBoxSignal
  
        
    def SetProgressDialogObject(self,windows:QtWidgets.QWidget):
        #建立屬性並賦值ProgressDialog物件
        self.progressDialogWindows = windows
 
    
    @pyqtSlot(object)
    def SetLableLight(self,serverState:CustomEnum.ServerState):
        if serverState == CustomEnum.ServerState.Run:
            self.isServerRun = True
            self.startServerButton.setEnabled(False)
            self.shutdownServerButton.setEnabled(True)
            self.shutdownProgramButton.setEnabled(False)
            self.serverRunLableLight.setStyleSheet("""
                                                    background-color: #73ff77;
                                                    border-radius:15px;
                                                    """)
            self.serverStopLableLight.setStyleSheet("""
                                                    background-color:black;
                                                    border-radius:15px;
                                                    """)
        else:
            self.isServerRun = False
            self.startServerButton.setEnabled(True)
            self.shutdownServerButton.setEnabled(False)
            self.shutdownProgramButton.setEnabled(True)
            self.serverRunLableLight.setStyleSheet("""
                                                    background-color:black;
                                                    border-radius:15px;
                                                    """)
            self.serverStopLableLight.setStyleSheet("""
                                                    background-color:red;
                                                    border-radius:15px;
                                                    """)
    
    
    @pyqtSlot(object,str)
    def showMessageBox(self,mode,message):
        if mode == CustomEnum.MessageBoxMode.Error:
            _  = QtWidgets.QMessageBox.critical(self,"發生錯誤",message)
        elif mode == CustomEnum.MessageBoxMode.Info:
            _  = QtWidgets.QMessageBox.information(self,"資訊",message)


    def Button_Click_Handler(self,mode):
        self.progressDialogWindows.show()
        if mode == CustomEnum.ButtonMode.Start:
            self.threadManageObject.StartServer()
        elif mode == CustomEnum.ButtonMode.Stop:
            self.threadManageObject.StopServer()
        
        
    def closeEvent(self,closeEvent):
        if self.isServerRun:
            closeEvent.ignore()
            self.showMessageBoxSignal.emit(CustomEnum.MessageBoxMode.Info,"請先關閉伺服器")


class ProgressDialog(QtWidgets.QWidget):
    #信號
    setCanCloseSignal = pyqtSignal()
    closeWindowsSignal = pyqtSignal()
    def __init__(self,parent):
        super().__init__(parent)
        self.setWindowTitle("訊息")
        self.resize(340, 105)
        self.setWindowFlags(Qt.WindowType.Dialog)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        #控制是否可以關閉
        self.canClose = False
        #處理中標籤
        self.textLabel = QtWidgets.QLabel("處理中...",self)
        self.textLabel.setGeometry(25, 10, 290,35)
        self.textLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.textLabel.setStyleSheet("""font-size:30px;""")
        #進度條
        progressBar = QtWidgets.QProgressBar(self)
        progressBar.move(25, 55)
        progressBar.setTextVisible(False)
        progressBar.setRange(0,0)
        #一定要寫在 QProgressBar {} 裡，才能打破原生樣式
        #border一定要寫，才能打破原生樣式
        #進度條的width一定要寫，否則進度條不會出來，因為無法計算進度條該怎麼渲染
        progressBar.setStyleSheet("""
                                  QProgressBar {
                                      border: 1px solid grey; 
                                      border-radius: 3px;
                                      width: 290px;
                                      height: 30px; }
                                  QProgressBar::chunk {
                                      background-color: #73ff77;
                                      width: 1px; }
                                   """)
        #slot連接函數
        self.setCanCloseSignal.connect(self.SetCanClose)
        self.closeWindowsSignal.connect(self.CloseWindows)
        
 
    @pyqtSlot()    
    def CloseWindows(self):
        self.close()
 
    
    @pyqtSlot()    
    def SetCanClose(self):
         self.canClose = True
 
        
    def SetThreadManageObject(self,thread):
        #建立屬性並賦值，連結信號
        self.threadManageObject = thread
        self.threadManageObject.setCanCloseProgressDialogSignal = self.setCanCloseSignal
        self.threadManageObject.closeProgressDialogSignal = self.closeWindowsSignal
        
    
    def TextLabelReset(self):
        self.textLabel.setText("處理中...")
  
    
    def closeEvent(self,closeEvent):
        if self.canClose:
            closeEvent.accept()
            self.TextLabelReset()
            self.threadManageObject.isUserStop = False
            self.canClose = False
        else:
            if self.textLabel.text() == "處理中...":
                self.textLabel.setText("停止中...")
                self.threadManageObject.isUserStop = True
            closeEvent.ignore()
    
 
class ThreadManage():
    def __init__(self):
        super().__init__()
        self.__lock = threading.Lock()
        #指示使用者是否中斷
        self.isUserStop = False
        #建立屬性存放子進程
        self.process = None
        #指示啟動模式
        self.processMode = None
        #信號，信號主體分別在MainWindows、ProgressDialog，各別透過SetThreadManageObject()賦值
        self.setLableLightSignal = None
        self.setCanCloseProgressDialogSignal = None
        self.closeProgressDialogSignal = None
        self.showMessageBoxSignal = None
        
    
    def ReadStdout(self,proc):
        # 持續讀取Stdout直到進程關閉
        for line in iter(proc.stdout.readline, ''):
            startSuccessful = re.search(r"Application startup complete",line)
            if startSuccessful:
                if self.FindFastAPIProcess():
                    self.setLableLightSignal.emit(CustomEnum.ServerState.Run)
                    self.setCanCloseProgressDialogSignal.emit()
                    self.closeProgressDialogSignal.emit()
            #print(f"{line}", end='')
        #print("讀取執行緒結束")


    def FindFastAPIEXE(self,fastapiModelPath:str) -> str|None:
        #尋找fastapi.exe 
        targetFolderName = "Scripts"
        targetFileName = "fastapi.exe"
        fastapiModelPath = Path(fastapiModelPath).resolve()
        for parent in fastapiModelPath.parents:
            if (parent/targetFolderName).exists():
                if (parent/targetFolderName/targetFileName).exists():
                    return str(parent/targetFolderName/targetFileName)
                else:
                    return None
    
            
    def KillSubprocess(self):
        #停止子進程  
        parent = psutil.Process(self.process.pid)
        children = parent.children(recursive=True)
        for childProcess in children:
            try:
                childProcess.terminate()
                childProcess.wait(timeout=3)
            except psutil.TimeoutExpired:
                childProcess.kill()
                childProcess.wait()
            except psutil.NoSuchProcess:
                pass
        try:
            self.process.terminate()
            self.process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait()
            
      
    @staticmethod    
    def FindFastAPIProcess()->bool|None:
        for targetProcess in psutil.process_iter(['pid','name']):
            if targetProcess.info['name'].lower() == "fastapi.exe":
                return True

     
    def Reset(self):
        #重設資訊
        self.process = None
        self.processMode = None
        
        
    def StartServer(self):
        thread = threading.Thread(target=self.StartServerWork, daemon=True)
        self.startServerThread = thread
        thread.start()
        

    def StartServerWork(self):
        spec = importlib.util.find_spec("fastapi")
        if not spec:
            self.setCanCloseProgressDialogSignal.emit()
            self.closeProgressDialogSignal.emit()
            self.showMessageBoxSignal.emit(CustomEnum.MessageBoxMode.Info,
                                           "請先安裝FastAPI模組。")
            return
        try:
            exePath = self.FindFastAPIEXE(spec.origin)
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            env["PYTHONUTF8"] = "1"
            cwdPath = Path(__file__).resolve().parent
            if exePath:
                self.processMode = CustomEnum.SubprocessMode.FastAPIExe
                process = subprocess.Popen(
                    [exePath,"run",str(cwdPath/"API.py")],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    encoding="utf-8",
                    errors="replace",
                    text=True,
                    env=env,
                    bufsize=1)
                time.sleep(1)
                #print(f"PID: {process.pid}")
                self.process = process
                #建立讀取stdout執行緒
                self.readStdoutThread = threading.Thread(target=self.ReadStdout, args=(process,), daemon=True)
                self.readStdoutThread.start()
                if self.isUserStop:
                    raise Exception()
            else:
                self.processMode = CustomEnum.SubprocessMode.cmd
                process = subprocess.Popen(
                    ['cmd.exe'],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    encoding="utf-8",
                    errors="replace",
                    text=True,
                    env=env,
                    bufsize=1)
                time.sleep(1)
                #print(f"PID: {process.pid}")
                self.process = process
                #建立讀取stdout執行緒
                self.readStdoutThread = threading.Thread(target=self.ReadStdout, args=(process,), daemon=True)
                self.readStdoutThread.start()
                if self.isUserStop:
                    raise Exception()
                process.stdin.write("cd {}".format(str(cwdPath)) + "\n")
                process.stdin.flush()
                time.sleep(1)
                if self.isUserStop:
                    raise Exception() 
                process.stdin.write("fastapi run API.py" + "\n")
                process.stdin.flush()
        except Exception as e:
            isUserStop = self.isUserStop
            if self.process:
                if not (self.process.poll()):    
                    self.KillSubprocess()
            self.setCanCloseProgressDialogSignal.emit()
            self.closeProgressDialogSignal.emit()
            if not isUserStop:
                self.showMessageBoxSignal.emit(CustomEnum.MessageBoxMode.Error,
                                        "伺服器啟動過程發生錯誤，導致無法啟動。")
            self.Reset()
            
            
    def StopServer(self):
        thread = threading.Thread(target=self.StopServerWork, daemon=True)
        self.stopServerThread = thread
        thread.start()
        
        
    def StopServerWork(self):
        if not (self.process.poll()):
            self.KillSubprocess()
        self.setLableLightSignal.emit(CustomEnum.ServerState.Stop)
        self.setCanCloseProgressDialogSignal.emit()
        self.closeProgressDialogSignal.emit()
        self.Reset()
    
        
if  __name__ == "__main__" :
    #測試
    threadManage = ThreadManage()
    app = QtWidgets.QApplication([])
    mainwindows = MainWindows()
    progressWindows = ProgressDialog(mainwindows)
    progressWindows.SetThreadManageObject(threadManage)
    mainwindows.SetProgressDialogObject(progressWindows)
    mainwindows.SetThreadManageObject(threadManage)
    mainwindows.show()
    app.exec()