
from conversor import *
from cripto import *
import urllib3
import json
import sys
from PyQt5.QtWidgets import ( QMessageBox)
urllib3.disable_warnings()


def  connexionSenales(self):
    self.actionDescargar_Datos.triggered.connect(self.descarga)
    self.lineEdit_1.textEdited['QString'].connect(self.edit1_cambio)
    self.lineEdit_2.textEdited['QString'].connect(self.edit2_cambio)
    self.comboBox_1.activated[str].connect(self.edit1_cambio)
    self.comboBox_2.activated[str].connect(self.edit2_cambio)
    self.actionAcerca_de.triggered.connect(self.acercaDe)
    self.actionIr_a_conversor.triggered.connect(self.abrir)




def descarga(self):
    http = urllib3.PoolManager()  # se pone esto pk este objeto maneja todos los detalles de la agrupacion de conexiones
    try:
        r = http.request('GET', 'http://data.fixer.io/api/latest?access_key=d1ad8e64023dafa68c6b1ac182507b0d&format=1',
                         retries=False)

        # valor determinado eur


        data = r.data.decode('ascii')
        print('Download Successfully!')  # mensaje bien
        self.actionDescargar_Datos.setEnabled(False)  # Lo desabilito para que no se pueda descargar mas datos
        r.close()

        data = json.loads(data)
        self.rates = data['rates']
        for key, value in self.rates.items():
            baseIndex = self.comboBox_1.findText(data['base'])
            self.comboBox_1.setCurrentIndex(baseIndex)
            self.comboBox_2.setCurrentIndex(baseIndex)

            self.comboBox_1.addItem(key)
            self.comboBox_2.addItem(key)
    except urllib3.exceptions.NewConnectionError:
        QtWidgets.QMessageBox.critical(MainWindow, 'Error', 'Download failed!', QtWidgets.QMessageBox.Ok)


def edit1_cambio(self):
    key1 = self.comboBox_1.currentText()
    key2 = self.comboBox_2.currentText()
    rate = self.rates[key2] / self.rates[key1]
    amount = float(self.lineEdit_1.text()) * rate
    self.lineEdit_2.setText('{:.2f}'.format(amount))


def edit2_cambio(self):
    key1 = self.comboBox_1.currentText()
    key2 = self.comboBox_2.currentText()
    rate = self.rates[key1] / self.rates[key2]
    amount = float(self.lineEdit_2.text()) * rate
    self.lineEdit_1.setText('{:.2f}'.format(amount))
#abrir cripto
def abrir(self):
    self.ventana=QtWidgets.QMainWindow()
    self.ui=Ui_cripto()
    self.ui.setupUi(self.ventana)
    self.ventana.show()

#acerca de
def acercaDe(self):
    mensaje = QMessageBox()
    mensaje.setIcon(QMessageBox.Information)
    mensaje.setInformativeText("<p>Sencillo conversor con: < / p > < p > - PyQt < / p > < p > - Qt  Designer < / p > < p > - "
                               "Python < / p > < / p > < p > - iconos https://www.flaticon.com/ y Freepik < / p >< / p > < p > - "
                               "image Nicholas Cappello < / p >")
    mensaje.setWindowTitle("Acerca del Editor de Texto")
    mensaje.exec_()



Ui_MainWindow.connexionSenales = connexionSenales
Ui_MainWindow.descarga = descarga
Ui_MainWindow.edit1_cambio = edit1_cambio
Ui_MainWindow.edit2_cambio = edit2_cambio
Ui_MainWindow.acercaDe = acercaDe
Ui_MainWindow.abrir = abrir



if __name__ == "__main__":


    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.connexionSenales()
    MainWindow.show()
    sys.exit(app.exec_())