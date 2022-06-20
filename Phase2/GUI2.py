from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QPushButton, QFileDialog, QVBoxLayout
import pandas as pd
import numpy as np

import re
import sys
class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('GUI_Mrince_7.ui', self)

        # button
        self.button = self.findChild(QtWidgets.QPushButton, 'pushButton_2')
        self.button.clicked.connect(self.load_file)
        self.ok = self.findChild(QtWidgets.QPushButton, 'pushButton_3')
        self.ok.clicked.connect(self.show_customer_info)

        # Label
        self.Cus_ID = self.findChild(QtWidgets.QPlainTextEdit, 'plainTextEdit')
        self.Cus_name = self.findChild(QtWidgets.QPlainTextEdit, 'plainTextEdit_5')
        self.Tracking_number = self.findChild(QtWidgets.QPlainTextEdit, 'plainTextEdit_15')
        self.Cus_address = self.findChild(QtWidgets.QPlainTextEdit, 'plainTextEdit_6')
        self.Cus_phone = self.findChild(QtWidgets.QPlainTextEdit, 'plainTextEdit_16')
        self.Acc_No = self.findChild(QtWidgets.QPlainTextEdit, 'plainTextEdit_7')
        self.Acc_name = self.findChild(QtWidgets.QPlainTextEdit, 'plainTextEdit_17')
        self.Cus_email = self.findChild(QtWidgets.QPlainTextEdit, 'plainTextEdit_14')
        self.shipping = self.findChild(QtWidgets.QPlainTextEdit, 'plainTextEdit_18')
        self.status = self.findChild(QtWidgets.QPlainTextEdit, 'plainTextEdit_2')
        self.subtotal = self.findChild(QtWidgets.QPlainTextEdit, 'plainTextEdit_4')
        self.total = self.findChild(QtWidgets.QPlainTextEdit, 'plainTextEdit_3')

        self.csv = pd.DataFrame()
        self.show()

    def load_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","CSV Files (*.csv)", options=options)
        if fileName:
            # load csv
            self.csv = pd.read_csv(fileName)
    
    def show_customer_info(self):
        if self.csv.empty:
            return
        
        Number = self.Cus_ID.toPlainText()
        if Number.isnumeric():
            Number = int(Number)
        else:
            return
        if Number in self.csv['No.'].unique():
            info = self.csv.loc[self.csv['No.'] == Number].iloc[0]
            # clear old text
            self.Cus_name.clear()
            self.Tracking_number.clear()
            self.Cus_address.clear()
            self.Cus_phone.clear()
            self.Acc_No.clear()
            self.Acc_name.clear()
            self.Cus_email.clear()
            self.shipping.clear()
            self.status.clear()
            self.subtotal.clear()
            self.total.clear()
            # set new text
            self.Cus_name.insertPlainText(info['Customer Name'])
            self.Tracking_number.insertPlainText(f"{info['Tracking Number'] if not np.isnan(info['Tracking Number']) else ''}")
            self.Cus_address.insertPlainText(info['Customer Address'])
            self.Cus_phone.insertPlainText(info['Customer Phone'])
            self.Acc_No.insertPlainText(f"{info['Account No.'] if not np.isnan(info['Account No.']) else ''}")
            self.Acc_name.insertPlainText(f"{info['Account Name'] if not np.isnan(info['Account Name']) else ''}")
            self.Cus_email.insertPlainText(info['Customer Email'])
            self.shipping.insertPlainText(f"{info['Shipping Option'] if not np.isnan(info['Shipping Option']) else ''}")
            self.status.insertPlainText(info['Status'])
            self.subtotal.insertPlainText(f"{info['Subtotal'] if not np.isnan(info['Subtotal']) else ''}")
            self.total.insertPlainText(f"{info['Total'] if not np.isnan(info['Total']) else ''}")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()