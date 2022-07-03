from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QHeaderView
import pandas as pd
import textwrap
from report import Ui_ReportWindow

import sys
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(944, 572)
        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.status = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.status.sizePolicy().hasHeightForWidth())
        self.status.setSizePolicy(sizePolicy)
        self.status.setMaximumSize(QtCore.QSize(150, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.status.setFont(font)
        self.status.setObjectName("label_4")
        self.gridLayout.addWidget(self.status, 0, 0, 1, 1)
        self.file_name_label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.file_name_label.sizePolicy().hasHeightForWidth())
        self.file_name_label.setSizePolicy(sizePolicy)
        self.file_name_label.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.file_name_label.setFont(font)
        self.file_name_label.setText("")
        self.file_name_label.setObjectName("label_5")
        self.gridLayout.addWidget(self.file_name_label, 0, 1, 1, 1)
        self.end_button = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.end_button.sizePolicy().hasHeightForWidth())
        self.end_button.setSizePolicy(sizePolicy)
        self.end_button.setMaximumSize(QtCore.QSize(150, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.end_button.setFont(font)
        self.end_button.setObjectName("pushButton")
        self.gridLayout.addWidget(self.end_button, 0, 2, 1, 1)
        self.select_file_button = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.select_file_button.sizePolicy().hasHeightForWidth())
        self.select_file_button.setSizePolicy(sizePolicy)
        self.select_file_button.setMinimumSize(QtCore.QSize(150, 0))
        self.select_file_button.setMaximumSize(QtCore.QSize(150, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.select_file_button.setFont(font)
        self.select_file_button.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.select_file_button, 1, 0, 1, 1)
        self.cus_ID = QtWidgets.QLineEdit(self.centralwidget)
        self.cus_ID.setMinimumSize(QtCore.QSize(0, 30))
        self.cus_ID.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.cus_ID.setFont(font)
        self.cus_ID.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.cus_ID, 1, 1, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(150, 0))
        self.label_2.setMaximumSize(QtCore.QSize(150, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.customer_name = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.customer_name.sizePolicy().hasHeightForWidth())
        self.customer_name.setSizePolicy(sizePolicy)
        self.customer_name.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.customer_name.setFont(font)
        self.customer_name.setText("")
        self.customer_name.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.customer_name.setObjectName("label_3")
        self.gridLayout.addWidget(self.customer_name, 2, 1, 1, 2)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setMinimumSize(QtCore.QSize(150, 0))
        self.label.setMaximumSize(QtCore.QSize(150, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)
        self.item_ID = QtWidgets.QLineEdit(self.centralwidget)
        self.item_ID.setMinimumSize(QtCore.QSize(0, 30))
        self.item_ID.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.item_ID.setFont(font)
        self.item_ID.setObjectName("lineEdit_3")
        self.gridLayout.addWidget(self.item_ID, 3, 1, 1, 2)
        self.add_btn = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add_btn.sizePolicy().hasHeightForWidth())
        self.add_btn.setSizePolicy(sizePolicy)
        self.add_btn.setMaximumSize(QtCore.QSize(150, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.add_btn.setFont(font)
        self.add_btn.setAutoFillBackground(False)
        self.add_btn.setObjectName("pushButton_4")
        self.add_btn.clicked.connect(lambda : self.changeMode(True))
        self.gridLayout.addWidget(self.add_btn, 4, 0, 1, 1)
        self.sub_btn = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sub_btn.sizePolicy().hasHeightForWidth())
        self.sub_btn.setSizePolicy(sizePolicy)
        self.sub_btn.setMaximumSize(QtCore.QSize(150, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.sub_btn.setFont(font)
        self.sub_btn.setObjectName("pushButton_5")
        self.gridLayout.addWidget(self.sub_btn, 4, 1, 1, 1)
        self.table = QtWidgets.QTableWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.table.setFont(font)
        self.table.setObjectName("tableWidget")
        self.table.setColumnCount(4)
        self.table.setRowCount(0)
        self.table.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem())
        self.table.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem())
        self.table.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem())
        self.table.setHorizontalHeaderItem(3, QtWidgets.QTableWidgetItem())
        self.table.horizontalHeader().setVisible(True)
        self.table.horizontalHeader().setCascadingSectionResizes(False)
        self.table.horizontalHeader().setSortIndicatorShown(False)
        self.table.verticalHeader().setVisible(False)
        self.clearBtn = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clearBtn.sizePolicy().hasHeightForWidth())
        self.clearBtn.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.clearBtn.setFont(font)
        self.clearBtn.setObjectName("clearBtn")
        self.clearBtn.clicked.connect(self.clear_data)
        self.gridLayout.addWidget(self.clearBtn, 4, 2, 1, 1)
        self.gridLayout.addWidget(self.table, 5, 0, 1, 3)
        self.MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self.MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 944, 21))
        self.menubar.setObjectName("menubar")
        self.MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self.MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.MainWindow.setStatusBar(self.statusbar)

        # button
        self.select_file_button.clicked.connect(self.load_file)
        self.end_button.clicked.connect(self.show_report_window)
        self.add_btn.clicked.connect(lambda : self.changeMode(True))
        self.sub_btn.clicked.connect(lambda : self.changeMode(False))

        # Label
        self.status.setText('สถานะ : ไม่พร้อม')

        # Line Edit
        self.cus_ID.returnPressed.connect(self.show_customer_info)
        self.item_ID.returnPressed.connect(self.add_item)

        # table
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)

        # sub window
        self.report_window = QtWidgets.QMainWindow()
        self.report_ui = Ui_ReportWindow()
        self.report_ui.setupUi(self.report_window)

        # set up variable
        self.changeMode(True)
        self.ID = None
        self.add_mode = True
        self.csv = pd.DataFrame()
        self.order_list = pd.DataFrame()
        self.all_order_list = pd.DataFrame()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.status.setText(_translate("MainWindow", "สถานะ"))
        self.end_button.setText(_translate("MainWindow", "จบ"))
        self.select_file_button.setText(_translate("MainWindow", "อัปโหลด"))
        self.label_2.setText(_translate("MainWindow", "ชื่อลูกค้า : "))
        self.label.setText(_translate("MainWindow", "รหัสสินค้า : "))
        self.add_btn.setText(_translate("MainWindow", "เพิ่ม"))
        self.sub_btn.setText(_translate("MainWindow", "ลด"))
        item = self.table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "SKU"))
        item = self.table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "สินค้า"))
        item = self.table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "จำนวนที่สั่ง"))
        item = self.table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "จำนวนที่ได้"))
        self.clearBtn.setText(_translate("MainWindow", "Clear"))

    def load_file(self) -> None:
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self.MainWindow,"QFileDialog.getOpenFileName()", "","CSV Files (*.csv)", options=options)
        if fileName:
            # load csv
            self.csv = pd.read_csv(fileName)
            self.file_name_label.setText(fileName)
            self.status.setText('สถานะ : พร้อม')
            self.set_all_order_list()
    
    def set_all_order_list(self):
        if self.csv.empty:
            return
        self.all_order_list = self.csv.drop_duplicates(subset=['Item Code']).reset_index(drop=True)[['Item Code', 'Item Name']].copy()

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
            self.table.setItem(index, 0 ,QtWidgets.QTableWidgetItem(str(row['Item Code'])))
            self.table.setItem(index, 1 ,QtWidgets.QTableWidgetItem(str(row['Item Name'])))
            self.table.setItem(index, 2 ,QtWidgets.QTableWidgetItem(str(row['Item Qty'])))
            self.table.setItem(index, 3 ,QtWidgets.QTableWidgetItem(str(row['ItemGet'])))

    def clear_data(self) -> None:
        self.table.setRowCount(0)
        self.item_ID.clear()
        self.customer_name.clear()
        self.cus_ID.clear()
        self.order_list = pd.DataFrame()

    def changeMode(self, add):
        if add:
            self.add_mode = True 
            self.add_btn.setStyleSheet("background-color : Green")
            self.sub_btn.setStyleSheet("background-color : None")
        else:
            self.add_mode = False
            self.add_btn.setStyleSheet("background-color : None")
            self.sub_btn.setStyleSheet("background-color : Red")

    def add_item(self) -> None:
        item_ID = self.item_ID.text()
        self.item_ID.clear()
        if (item_ID == "") or (len(item_ID) != 13) or not (item_ID.isnumeric()):
            return
        SKU = self.readbarcode(item_ID)
        found = False
        for index,row in self.order_list.iterrows():
            if row['Item Code'] == SKU:
                if self.add_mode:
                    self.order_list.loc[index,'ItemGet'] += 1
                elif self.order_list.loc[index,'ItemGet'] >0:
                    self.order_list.loc[index,'ItemGet'] -= 1
                found = True
                break
        if not found:
            item_name = self.all_order_list.loc[self.all_order_list['Item Code'] == SKU]['Item Name']
            row = {'Item Code':SKU, 'Item Name':item_name, 'Item Qty': 0, 'ItemGet': 1}
            self.order_list = pd.concat([self.order_list, pd.DataFrame(row)], ignore_index=True)
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
        missing_list = report[report['Status'] == 'ขาด'][['Item Name', 'Item Qty']].reset_index(drop=True)
        over_list = report[report['Status'] == 'เกิน'][['Item Name', 'Item Qty']].reset_index(drop=True)

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
    import sys

    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(main_window)
    main_window.show()
    sys.exit(app.exec_())