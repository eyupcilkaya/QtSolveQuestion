import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QFrame
from PyQt5.uic import loadUi
import firebase_process
import variables
from PyQt5.QtCore import QThread
from ui.mainui import Ui_MainWindow


class ThreadClass(QThread):
    def __init__(self, parent=None, variablesObject=None, id=None):
        super(ThreadClass, self).__init__(parent)
        self.state = 0
        self.variablesObject = variablesObject
        self.id = id

    def run(self):
        while True:
            self.state = firebase_process.readFirebase(self.variablesObject, self.id)
            if (self.state == 1):
                break
            else:
                continue


class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)


        self.answer = ""
        self.variablesObject = variables.Variables()
        self.sign_in.clicked.connect(self.signInClicked)
        self.submit.clicked.connect(self.submitClicked)
        self.option_a.clicked.connect(lambda: self.save("a"))
        self.option_b.clicked.connect(lambda: self.save("b"))
        self.option_c.clicked.connect(lambda: self.save("c"))
        self.option_d.clicked.connect(lambda: self.save("d"))
        self.option_e.clicked.connect(lambda: self.save("e"))
        self.widget.setEnabled(False)
        self.show()

    def save(self, answer):
        self.answer = answer

    def signInClicked(self):
        self.id = self.enter_id.text()

        print(type(self.id))
        print(self.id)
        result = firebase_process.createFirebase(self.id)
        if result:
            self.info.setText("BİLGİ: Kayıt başarılı ile yapıldı.")
            self.enter_id.setEnabled(False)
            self.sign_in.setEnabled(False)
            self.id_text.setText(self.id)

            self.startThread()
        else:
            self.info.setText("BİLGİ: Bu numara sisteme kayıtlı.")

    def submitClicked(self):
        print("submit")
        self.widget.setEnabled(False)

        firebase_process.writeFirebase(self.answer, self.id)
        self.info.setText("BİLGİ: Yeni soru için lütfen bekleyin.")
        self.startThread()


    def refreshClicked(self):

        self.widget.setEnabled(True)
        self.clear()
        quest, a, b, c, d, e = self.variablesObject.getQuestion()
        self.question.setText(quest)
        self.option_a.setText(a)
        self.option_b.setText(b)
        self.option_c.setText(c)
        self.option_d.setText(d)
        self.option_e.setText(e)
        self.frame.setStyleSheet(f'background-image : url({"1.jpg"})')
        self.frame.setStyleSheet(
            f'border-image : url({"1.jpg"}) 0 0 0 0 strech strech')
        self.info.setText("BİLGİ: Gönderme işleminden sonra değişiklik yapılamaz.")




    def clear(self):
        self.option_a.setAutoExclusive(False)
        self.option_b.setAutoExclusive(False)
        self.option_c.setAutoExclusive(False)
        self.option_d.setAutoExclusive(False)
        self.option_e.setAutoExclusive(False)
        self.option_a.setChecked(False)
        self.option_b.setChecked(False)
        self.option_c.setChecked(False)
        self.option_d.setChecked(False)
        self.option_e.setChecked(False)
        self.option_a.setAutoExclusive(True)
        self.option_b.setAutoExclusive(True)
        self.option_c.setAutoExclusive(True)
        self.option_d.setAutoExclusive(True)
        self.option_e.setAutoExclusive(True)

    def startThread(self):
        self.threadClass = ThreadClass(variablesObject=self.variablesObject, id=self.id)
        self.threadClass.start()
        self.threadClass.finished.connect(self.refreshClicked)


app = QApplication(sys.argv)
window = MainWindow()
app.exec_()