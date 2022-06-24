from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
import pandas as pd
import textwrap
from report import Ui_ReportWindow

import sys
class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('GUI_Mrince_7.ui', self)

        # button
        self.select_file_button = self.findChild(QtWidgets.QPushButton, 'pushButton_2')
        self.select_file_button.clicked.connect(self.load_file)
        self.end_button = self.findChild(QtWidgets.QPushButton, 'pushButton')
        self.end_button.clicked.connect(self.show_report_window)
        self.add_btn = self.findChild(QtWidgets.QPushButton, 'pushButton_4')
        self.add_btn.clicked.connect(lambda : self.changeMode(True))
        self.sub_btn = self.findChild(QtWidgets.QPushButton, 'pushButton_5')
        self.sub_btn.clicked.connect(lambda : self.changeMode(False))

        # Label
        self.status = self.findChild(QtWidgets.QLabel, 'label_4')
        self.status.setText('สถานะ : ไม่พร้อม')
        self.customer_name = self.findChild(QtWidgets.QLabel, 'label_3')
        self.file_name_label = self.findChild(QtWidgets.QLabel, 'label_5')

        # Line Edit
        self.cus_ID = self.findChild(QtWidgets.QLineEdit, 'lineEdit')
        self.cus_ID.returnPressed.connect(self.show_customer_info)
        self.item_ID = self.findChild(QtWidgets.QLineEdit, 'lineEdit_3')
        self.item_ID.returnPressed.connect(self.add_item)

        # table
        self.table = self.findChild(QtWidgets.QTableWidget, 'tableWidget')
        self.table.setColumnCount(3)

        # sub window
        self.report_window = QtWidgets.QMainWindow()
        self.report_ui = Ui_ReportWindow()
        self.report_ui.setupUi(self.report_window)

        # set up variable
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
            self.get_customer_item_list()
            self.show_item_list()
            
    def get_customer_item_list(self) -> None: 
        self.order_list = self.csv.loc[self.csv['No.'] == self.ID][['Item Code', 'Item Name', 'Item Qty']].reset_index(drop=True)
        self.order_list = self.order_list.assign(ItemGet=0)

    def show_item_list(self) -> None:
        self.table.setRowCount(0)
        self.table.setRowCount(self.order_list.shape[0])
        for index, row in self.order_list.iterrows():
            self.table.setItem(index, 0 ,QtWidgets.QTableWidgetItem(str(row['Item Name'])))
            self.table.setItem(index, 1 ,QtWidgets.QTableWidgetItem(str(row['Item Qty'])))
            self.table.setItem(index, 2 ,QtWidgets.QTableWidgetItem(str(row['ItemGet'])))

    def changeMode(self, add):
         self.add_mode = True if add else  False

    def add_item(self) -> None:
        item_ID = self.item_ID.text()
        self.item_ID.clear()
        if item_ID == "":
            return
        SKU = self.readbarcode(item_ID)
        for index,row in self.order_list.iterrows():
            if row['Item Code'] == SKU:
                if self.add_mode:
                    self.order_list.loc[index,'ItemGet'] += 1
                elif self.order_list.loc[index,'ItemGet'] >0:
                    self.order_list.loc[index,'ItemGet'] -= 1
                break
        self.show_item_list()

    def readbarcode(self, num : str) -> str:
        if num == "6979700123456":return "EOF"  #End of file
        num = num[:-1]
        while num[-1] != "0": num = num[:-1]
        num = num[:-1]      #detect trash digits
        chr_list = []
        alpha = textwrap.wrap(num[:-4],2)       #split digit for character
        for c in alpha: chr_list.append(str(chr(int(c))))   
        return str("".join(chr_list)+num[-4:])

    def get_report(self) -> pd.DataFrame:
        data = pd.DataFrame(columns=['Item Name', 'Status', 'Item Qty'])
        for index, row in self.order_list.iterrows():
            n = row['Item Qty'] - row['ItemGet']
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

    def show_report_window(self):
        # getting report data
        report = self.get_report()
        missing_list = report[report['Status'] == 'ขาด'][['Item Name', 'Item Qty']]
        over_list = report[report['Status'] == 'เกิน'][['Item Name', 'Item Qty']]

        # clear old table
        self.report_ui.tableWidget_2.setRowCount(0)
        self.report_ui.tableWidget_2.setRowCount(0)

        # insert data
        self.report_ui.tableWidget_1.setRowCount(missing_list.shape[0])
        for index, row in missing_list.iterrows():
            self.report_ui.tableWidget_1.setItem(index, 0 ,QtWidgets.QTableWidgetItem(str(row['Item Name'])))
            self.report_ui.tableWidget_1.setItem(index, 1 ,QtWidgets.QTableWidgetItem(str(row['Item Qty'])))
        self.report_ui.tableWidget_2.setRowCount(over_list.shape[0])
        for index, row in over_list.iterrows():
            self.report_ui.tableWidget_2.setItem(index, 0 ,QtWidgets.QTableWidgetItem(str(row['Item Name'])))
            self.report_ui.tableWidget_2.setItem(index, 1 ,QtWidgets.QTableWidgetItem(str(row['Item Qty'])))

        self.report_window.show()
        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()