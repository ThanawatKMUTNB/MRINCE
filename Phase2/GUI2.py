from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QWidget, QFileDialog
import pandas as pd

import sys
class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('GUI_Mrince_7.ui', self)

        # button
        self.select_file_button = self.findChild(QtWidgets.QPushButton, 'pushButton_2')
        self.select_file_button.clicked.connect(self.load_file)
        self.end_button = self.findChild(QtWidgets.QPushButton, 'pushButton')
        self.end_button = self.findChild(QtWidgets.QPushButton, 'pushButton_4')
        self.end_button = self.findChild(QtWidgets.QPushButton, 'pushButton_5')

        # Label
        self.status = self.findChild(QtWidgets.QLabel, 'label_4')
        self.status.setText('สถานะ : ไม่พร้อม')
        self.customer_name = self.findChild(QtWidgets.QLabel, 'label_3')
        self.file_name_label = self.findChild(QtWidgets.QLabel, 'label_5')

        # Line Edit
        self.cus_ID = self.findChild(QtWidgets.QLineEdit, 'lineEdit')
        self.cus_ID.returnPressed.connect(self.show_customer_info)
        self.item_ID = self.findChild(QtWidgets.QLineEdit, 'lineEdit_3')

        # table
        self.table = self.findChild(QtWidgets.QTableWidget, 'tableWidget')
        self.table.setColumnCount(3)

        self.ID = None
        self.add_mode = True
        self.csv = pd.DataFrame()
        self.order_list = pd.DataFrame()
        self.show()

    def load_file(self) -> None:
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","CSV Files (*.csv)", options=options)
        if fileName:
            # load csv
            self.csv = pd.read_csv(fileName)
            self.file_name_label.setText(fileName)
            self.status.setText('สถานะ : พร้อม')
    
    def show_customer_info(self) -> None:
        if self.csv.empty:
            return
        
        self.ID = self.cus_ID.text()
        if self.ID.isnumeric():
            self.ID = int(self.ID)
        else:
            return
        if self.ID in self.csv['No.'].unique():
            info = self.csv.loc[self.csv['No.'] == self.ID].iloc[0]
            # clear old text
            self.customer_name.clear()
            # set new text
            self.customer_name.setText(info['Customer Name'])
            self.show_item_list()
            
    def show_item_list(self) -> None:
        if self.ID == None:
            return
        self.order_list = self.csv.loc[self.csv['No.'] == self.ID][['Item Code', 'Item Name', 'Item Qty']].reset_index(drop=True)
        self.order_list = self.order_list.assign(ItemGet=0)

        self.table.setRowCount(self.order_list.shape[0])
        for index, row in self.order_list.iterrows():
            self.table.setItem(index, 0 ,QtWidgets.QTableWidgetItem(str(row['Item Name'])))
            self.table.setItem(index, 1 ,QtWidgets.QTableWidgetItem(str(row['Item Qty'])))
            self.table.setItem(index, 2 ,QtWidgets.QTableWidgetItem(str(row['ItemGet'])))


    def get_report(DF : pd.DataFrame) -> pd.DataFrame:
        data = pd.DataFrame(columns=['Item Name', 'Status', 'Item Qty'])
        for index, row in DF.iterrows():
            n = row['Item Qty'] - row['GetItem']
            if n > 0: # ขาด
                df = pd.DataFrame(
                    {
                        'Item Name' : [row['Item Name']],
                        'Status' : ['ขาด'],
                        'Item Qty' : [n]
                    }
                )
            elif n < 0: # เกิน
                df = pd.DataFrame(
                    {
                        'Item Name' : [row['Item Name']],
                        'Status' : ['เกิน'],
                        'Item Qty' :[-n]
                    }
                )
            else:
                continue
            data = pd.concat([data,df], ignore_index=True)
        return data

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()