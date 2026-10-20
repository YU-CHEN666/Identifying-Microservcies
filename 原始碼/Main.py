#程式進入點 檔案
from GUI import ThreadManage,MainWindows,ProgressDialog
from PyQt6 import QtWidgets


threadManage = ThreadManage()
app = QtWidgets.QApplication([])
mainwindows = MainWindows()
progressWindows = ProgressDialog(mainwindows)
progressWindows.SetThreadManageObject(threadManage)
mainwindows.SetProgressDialogObject(progressWindows)
mainwindows.SetThreadManageObject(threadManage)
mainwindows.show()
app.exec()
