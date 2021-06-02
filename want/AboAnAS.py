from AboAnas_Server import *
ui, _ = loadUiType('Souq.ui')
class MainApp(QMainWindow, ui, QThread):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setFixedSize(799, 600)
        self.setupUi(self)
        self.Handel()
    def Handel(self):
        self.pushButton_run_2.clicked.connect(lambda: self.login())
        self.movie = QMovie(f"loading.gif")
        self.label.setMovie(self.movie)
        self.pushButton_run.clicked.connect(self.sent_in)

    def login(self):
        self.movie = QMovie("loading.gif")
        self.label.setMovie(self.movie)
        gifSize = QSize(40, 40)
        self.movie.setScaledSize(gifSize)
        self.movie.start()
        self.email = str(self.lineEdit_email.text())
        self.password = self.lineEdit_password.text()
        self.path = self.lineEdit_path.text()
        self.got = rel(em=self.email, pwd=self.password, pathh=self.path)
        self.got.nump.connect(self.ump)
        self.got.patdd.connect(self.any)
        self.got.start()
        self.pushButton_run_2.setEnabled(False)
        print('hi')
    def any(self, d):
        print(d)
        self.label.setHidden(True)
        self.label_note.setText(d)
        self.label_note.setStyleSheet("color: green")
    def sent_in(self):
        self.check = checker()
        self.check.EAN.connect(self.set_on)
        self.check.on_fire.connect(self.onfire)
        self.check.start()
    def set_on(self, txt):
        self.textEdit.append(f'{txt}')
    def onfire(self, ean):
        self.label_2.setText(f'On Fire : {ean}')

    def ump(self, nn):
        self.label_note_2.setText(f"{nn}")
def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()
if __name__ == '__main__':
    main()
