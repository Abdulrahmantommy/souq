from AboAnas_Server import *
from main import Sheet
ui, _ = loadUiType('Souq.ui')
class MainApp(QMainWindow, ui, QThread):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        #self.setFixedSize(799, 600)
        self.setMaximumSize(799, 600)
        self.setMinimumSize(252, 598)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'logo.ico'))
        self.Handel()
    def Handel(self):
        self.pushButton_run_2.clicked.connect(lambda: self.login())
        try:
            r.get('http://127.0.0.1:5000')
        except CA:
            print(CA)
        self.movie = QMovie(f"loading.gif")
        self.label.setMovie(self.movie)
        self.pushButton_run.clicked.connect(self.sent_in)
        self.pushButton_browser.clicked.connect(self.openFileNamesDialog)
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
        self.label_note.setStyleSheet("color: rgb(85, 255, 0);")
        if d == ' ':
            self.pushButton_run_2.setEnabled(True)
        elif d != ' ':
            self.pushButton_run_2.setEnabled(False)
            self.label_note.setStyleSheet("color: red;")

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"Set CSV File For Checker", "","CSV Files (*.csv);;All Files (*)", options=options)
        if files:
            self.path_file = files[0]
            self.lineEdit_file_csv.setText(self.path_file)
            self.csv = self.lineEdit_file_csv.text()
            self.get()
        return self.csv
    def sent_in(self):
        try:
            print(self.path_file)
            print(self.csv)
            self.check = checker(csv=str(self.path_file))
            self.check.EAN.connect(self.set_on)
            self.check.on_fire.connect(self.onfire)
            self.check.start()
            app = QApplication(sys.argv)
            s = Sheet()
            s.show()
            sys.exit(app.exec_())
        except:
            QMessageBox.information(self, 'Error', 'Please Select CSV File.')

    def set_on(self, txt):
        self.textEdit.append(f'{txt}')
    def onfire(self, ean):
        self.label_2.setText(f'On Fire : {ean}')

    def ump(self, nn):
        self.label_note_2.setText(f"{nn}")


    def get(self):
        data = pd.read_csv(self.path_file)







def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()
if __name__ == '__main__':
    main()
