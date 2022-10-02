from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QHeaderView

from reportlab.platypus import SimpleDocTemplate,Paragraph, Spacer, Table, PageBreak
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import  TA_LEFT
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4

import sys
import os
import re
import pandas as pd
import textwrap
import traceback
import functools
from report import Ui_ReportWindow

def err(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try: 
            value = func(*args, **kwargs)
            return value
        except Exception as e:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.setMinimumHeight(350)
            error_dialog.setMinimumWidth(700)
            message = traceback.format_exc().replace('\n', '<br>')
            error_dialog.showMessage(message)
            error_dialog.exec_()
    return wrapper

def get_weight(name):
    # search for unit in item name
    bracket = re.search(r"\((\d+).+\)", name)
    if bracket != None:
        u = re.search(r'\d+', bracket.group()[1:-1])
        if u != None: 
            unit = u.group()
        else:
            unit = 100
    else:
        unit = 100
    return unit

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(944, 572)

        font = QtGui.QFont()
        font.setPointSize(14)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.select_file_button = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.select_file_button.sizePolicy().hasHeightForWidth())
        self.select_file_button.setSizePolicy(sizePolicy)
        self.select_file_button.setMinimumSize(QtCore.QSize(150, 0))
        self.select_file_button.setMaximumSize(QtCore.QSize(150, 30))
        self.select_file_button.setFont(font)
        self.select_file_button.setObjectName("select_file_button")
        self.gridLayout.addWidget(self.select_file_button, 1, 0, 1, 1)

        self.customer_name = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.customer_name.sizePolicy().hasHeightForWidth())
        self.customer_name.setSizePolicy(sizePolicy)
        self.customer_name.setMaximumSize(QtCore.QSize(16777215, 30))
        self.customer_name.setFont(font)
        self.customer_name.setText("")
        self.customer_name.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.customer_name.setObjectName("customer_name")
        self.gridLayout.addWidget(self.customer_name, 2, 1, 1, 1)

        self.add_btn = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add_btn.sizePolicy().hasHeightForWidth())
        self.add_btn.setSizePolicy(sizePolicy)
        self.add_btn.setMaximumSize(QtCore.QSize(150, 30))
        self.add_btn.setFont(font)
        self.add_btn.setAutoFillBackground(False)
        self.add_btn.setObjectName("add_btn")
        self.gridLayout.addWidget(self.add_btn, 4, 0, 1, 1)

        self.sub_btn = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sub_btn.sizePolicy().hasHeightForWidth())
        self.sub_btn.setSizePolicy(sizePolicy)
        self.sub_btn.setMaximumSize(QtCore.QSize(150, 30))
        self.sub_btn.setFont(font)
        self.sub_btn.setObjectName("sub_btn")
        self.gridLayout.addWidget(self.sub_btn, 4, 1, 1, 1)

        self.table = QtWidgets.QTableWidget(self.centralwidget)
        self.table.setFont(font)
        self.table.setObjectName("table")
        self.table.setColumnCount(5)
        self.table.setRowCount(0)
        self.table.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem('SKU'))
        self.table.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem('สินค้า'))
        self.table.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem('จำนวนที่สั่ง'))
        self.table.setHorizontalHeaderItem(3, QtWidgets.QTableWidgetItem('จำนวนที่ได้'))
        self.table.setHorizontalHeaderItem(4, QtWidgets.QTableWidgetItem('กล่องที่'))
        self.table.horizontalHeader().setVisible(True)
        self.table.horizontalHeader().setCascadingSectionResizes(False)
        self.table.horizontalHeader().setSortIndicatorShown(False)
        self.table.verticalHeader().setVisible(False)
        self.gridLayout.addWidget(self.table, 6, 0, 1, 3)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setMinimumSize(QtCore.QSize(150, 0))
        self.label.setMaximumSize(QtCore.QSize(150, 30))
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)

        self.clearBtn = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clearBtn.sizePolicy().hasHeightForWidth())
        self.clearBtn.setSizePolicy(sizePolicy)
        self.clearBtn.setMaximumSize(QtCore.QSize(150, 30))
        self.clearBtn.setFont(font)
        self.clearBtn.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.clearBtn.setObjectName("clearBtn")
        self.gridLayout.addWidget(self.clearBtn, 4, 2, 1, 1)

        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        
        self.item_ID = QtWidgets.QLineEdit(self.centralwidget)
        self.item_ID.setMinimumSize(QtCore.QSize(0, 30))
        self.item_ID.setMaximumSize(QtCore.QSize(16777215, 30))
        self.item_ID.setFont(font)
        self.item_ID.setObjectName("item_ID")
        self.horizontalLayout_4.addWidget(self.item_ID)

        self.quantity_edit_text = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.quantity_edit_text.sizePolicy().hasHeightForWidth())
        self.quantity_edit_text.setSizePolicy(sizePolicy)
        self.quantity_edit_text.setMaximumSize(QtCore.QSize(150, 16777215))
        self.quantity_edit_text.setFont(font)
        self.quantity_edit_text.setText("")
        self.quantity_edit_text.setMaxLength(32765)
        self.quantity_edit_text.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.quantity_edit_text.setObjectName("quantity_edit_text")
        self.horizontalLayout_4.addWidget(self.quantity_edit_text)
        self.gridLayout.addLayout(self.horizontalLayout_4, 3, 1, 1, 2)

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(150, 0))
        self.label_2.setMaximumSize(QtCore.QSize(150, 30))
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.employee_name = QtWidgets.QLineEdit(self.centralwidget)
        self.employee_name.setFont(font)
        self.employee_name.setObjectName("employee_name")
        self.gridLayout.addWidget(self.employee_name, 2, 2, 1, 1)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.status = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.status.sizePolicy().hasHeightForWidth())
        self.status.setSizePolicy(sizePolicy)
        self.status.setMinimumSize(QtCore.QSize(0, 30))
        self.status.setMaximumSize(QtCore.QSize(150, 30))
        self.status.setFont(font)
        self.status.setAlignment(QtCore.Qt.AlignCenter)
        self.status.setObjectName("status")
        self.horizontalLayout_2.addWidget(self.status)

        self.file_name_label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.file_name_label.sizePolicy().hasHeightForWidth())
        self.file_name_label.setSizePolicy(sizePolicy)
        self.file_name_label.setMaximumSize(QtCore.QSize(16777215, 30))
        self.file_name_label.setFont(font)
        self.file_name_label.setText("")
        self.file_name_label.setObjectName("file_name_label")
        self.horizontalLayout_2.addWidget(self.file_name_label)

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.id_add_label = QtWidgets.QLabel(self.centralwidget)
        self.id_add_label.setFont(font)
        self.id_add_label.setText("ID : ")
        self.id_add_label.setObjectName("id_add_label")
        self.horizontalLayout_3.addWidget(self.id_add_label)

        self.end_button = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.end_button.sizePolicy().hasHeightForWidth())
        self.end_button.setSizePolicy(sizePolicy)
        self.end_button.setMinimumSize(QtCore.QSize(30, 0))
        self.end_button.setMaximumSize(QtCore.QSize(150, 30))
        self.end_button.setFont(font)
        self.end_button.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.end_button.setObjectName("end_button")
        self.horizontalLayout_2.addWidget(self.end_button)

        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 3)
        self.cus_ID = QtWidgets.QLineEdit(self.centralwidget)
        self.cus_ID.setMinimumSize(QtCore.QSize(0, 30))
        self.cus_ID.setMaximumSize(QtCore.QSize(16777215, 40))
        self.cus_ID.setFont(font)
        self.cus_ID.setObjectName("cus_ID")
        self.gridLayout.addWidget(self.cus_ID, 1, 1, 1, 1)

        self.box_no = QtWidgets.QLineEdit(self.centralwidget)
        self.box_no.setFont(font)
        self.box_no.setObjectName("box_no")
        self.gridLayout.addWidget(self.box_no, 1, 2, 1, 1)

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setFont(font)
        self.pushButton.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_3.addWidget(self.pushButton)
        self.gridLayout.addLayout(self.horizontalLayout_3, 8, 2, 1, 1)

        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 894, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.MainWindow.setStatusBar(self.statusbar)

        # button
        self.select_file_button.clicked.connect(self.load_file)
        self.end_button.clicked.connect(self.show_report_window)
        self.add_btn.clicked.connect(lambda : self.changeMode(True))
        self.sub_btn.clicked.connect(lambda : self.changeMode(False))
        self.clearBtn.clicked.connect(self.clear_data)
        self.pushButton.clicked.connect(self.end_of_program)

        # Label
        self.status.setText('สถานะ : ไม่พร้อม')

        # Line Edit
        self.cus_ID.returnPressed.connect(self.show_customer_info)
        self.item_ID.returnPressed.connect(self.add_item)

        # table
        header = self.table.horizontalHeader()
        for i in [0, 2, 3, 4]:
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)

        # sub window
        self.report_window = QtWidgets.QMainWindow()
        self.report_ui = Ui_ReportWindow()
        self.report_ui.setupUi(self.report_window)

        self.report_ui.pushButton.clicked.connect(lambda: self.PDF_report(False))
        self.report_ui.pushButton_2.clicked.connect(lambda: self.PDF_report(True))

        # set up variable
        self.changeMode(True)
        self.ID = None
        self.add_mode = True
        self.csv = pd.DataFrame()
        self.order_list = pd.DataFrame()
        self.all_order_list = pd.DataFrame()
        self.list_by_item = {}
        self.carton_count = {}
        self.Item_set = set()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        if not os.path.exists('./file'):
            os.mkdir('./file')

        self.cartons_table_style = [('BACKGROUND', (0, 0), (-1,0), '#D2D2D2'),
                                    ('FONT', (0,0), (-1,-1),('THSarabunNew')),
                                    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                    ('FONTSIZE', (0,0), (-1,-1),15),
                                    ("ALIGN", (0, 0), (0, 0), "CENTER"),
                                    ]

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
        self.clearBtn.setText(_translate("MainWindow", "Clear"))
        self.employee_name.setPlaceholderText(_translate("MainWindow", "ใส่ชื่อพนักงาน"))
        self.box_no.setPlaceholderText(_translate("MainWindow", "กล่องที่"))
        self.pushButton.setText(_translate("MainWindow", "End of Program"))
        self.quantity_edit_text.setPlaceholderText(_translate("MainWindow", "จำนวน"))

    @err
    def load_file(self, *args, **kwargs) -> None:
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self.MainWindow,"QFileDialog.getOpenFileName()", "","CSV Files (*.csv)", options=options)
        if fileName:
            # load csv
            self.csv = pd.read_csv(fileName)
            self.set_all_order_list(fileName)

    @err
    def set_all_order_list(self, fileName, *args, **kwargs):
        if self.csv.empty:
            return
        try:
            self.all_order_list = self.csv.drop_duplicates(subset=['Item Code']).reset_index(drop=True)[['Item Code', 'Item Name']].copy()
            self.status.setText('สถานะ : พร้อม')
            self.file_name_label.setText(fileName)
        except:
            self.csv = pd.DataFrame()
            # show pop up
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("คำเตือน")
            msg.setText("กรุณาเลือกไฟล์ที่ถูกต้อง")
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            x = msg.exec_()
            return

    @err
    def show_customer_info(self, *args, **kwargs) -> None:
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
            ID = self.cus_ID.text()
            self.clear_data()
            self.cus_ID.setText(ID)
            # set new text
            self.customer_name.setText(info['Customer Name'])
            self.get_customer_item_list()
            self.show_item_list()

    @err        
    def get_customer_item_list(self, *args, **kwargs) -> None: 
        self.order_list = self.csv.loc[self.csv['No.'] == self.ID][['Item Code', 'Item Name', 'Item Qty', 'Item Price']].reset_index(drop=True)
        self.order_list = self.order_list.assign(ItemGet=0)
        self.order_list['BoxNo'] = [set() for i in range(len(self.order_list))]
        weight = []
        for name in self.order_list['Item Name']:
            weight.append(get_weight(name))
        self.order_list['Weight'] = weight
        for SKU in self.order_list['Item Name']:
            self.Item_set.add(SKU)

    @err
    def show_item_list(self, *args, **kwargs) -> None:
        self.table.setRowCount(0)
        self.table.setRowCount(self.order_list.shape[0])
        for index, row in self.order_list.iterrows():
            self.table.setItem(index, 0 ,QtWidgets.QTableWidgetItem(str(row['Item Code'])))
            self.table.setItem(index, 1 ,QtWidgets.QTableWidgetItem(str(row['Item Name'])))
            self.table.setItem(index, 2 ,QtWidgets.QTableWidgetItem(str(row['Item Qty'])))
            self.table.setItem(index, 3 ,QtWidgets.QTableWidgetItem(str(row['ItemGet'])))
            if row['Item Name'] in self.carton_count.keys():
                BoxNo = ', '.join(self.carton_count[row['Item Name']])
                self.table.setItem(index, 4, QtWidgets.QTableWidgetItem(BoxNo))

    @err
    def get_order_list(self, cartons=False, *args, **kwargs) -> list:
        LIST = []
        if cartons:
            LIST.append(['SKU', 'สินค้า', 'กล่องที่'])
            for index, row in self.order_list.iterrows():
                ROW = []
                ROW.append(str(row['Item Code']))
                ROW.append(str(row['Item Name']))
                if len(row['BoxNo']) == 0:
                    ROW.append('')
                else:
                    ROW.append(f"{sorted(row['BoxNo'])}".replace("'","")[1:-1])
                LIST.append(ROW)
        else:
            count = get = total_price = 0
            LIST.append(['SKU', 'สินค้า', 'จำนวนที่สั่ง', 'จำนวนที่ได้', 'ราคาต่อชิ้น', 'ราคารวม'])
            for index, row in self.order_list.iterrows():
                count += row['Item Qty']
                get += row['ItemGet']
                price = row['ItemGet'] * row['Item Price']
                total_price += price
                ROW = []
                ROW.append(str(row['Item Code']))
                ROW.append(str(row['Item Name']))
                ROW.append(row['Item Qty'])
                ROW.append(row['ItemGet'])
                ROW.append(row['Item Price'])
                ROW.append(price)
                LIST.append(ROW)
            LIST.append(['', 'Total', count, get, '', total_price])
        return LIST

    @err
    def clear_data(self, *args, **kwargs) -> None:
        self.table.setRowCount(0)
        self.item_ID.clear()
        self.customer_name.clear()
        self.cus_ID.clear()
        self.employee_name.clear()
        self.carton_count = {}
        self.order_list = pd.DataFrame()
        self.Item_set = set()

    def changeMode(self, add, *args, **kwargs):
        if add:
            self.add_mode = True 
            self.add_btn.setStyleSheet("background-color : Green")
            self.sub_btn.setStyleSheet("background-color : None")
        else:
            self.add_mode = False
            self.add_btn.setStyleSheet("background-color : None")
            self.sub_btn.setStyleSheet("background-color : Red")

    @err
    def add_item(self, *args, **kwargs) -> None:
        item_ID = self.item_ID.text().strip()
        self.item_ID.clear()
        if (item_ID == "") or (len(item_ID) != 13) or (not (item_ID.isnumeric())) or self.all_order_list.empty:
            return
        SKU = self.readbarcode(item_ID)

        n = self.get_quantity()
        if n == 0:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("คำเตือน")
            msg.setText("ช่องจำนวนสามารถใส่ได้แค่เพียงตัวเลขเท่านั้น")
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            x = msg.exec_()
            self.quantity_edit_text.clear()

        if len(self.all_order_list.loc[self.all_order_list['Item Code'] == SKU].reset_index(drop=True)) == 0 : return               # no item match with SKU in CSV
        item_name = self.all_order_list.loc[self.all_order_list['Item Code'] == SKU].reset_index(drop=True).iloc[0]['Item Name']    # select match item
        found = False
        carton_code = self.box_no.text().strip()
        if carton_code == '' : return           # no carton code defind
        for index,row in self.order_list.iterrows():
            if row['Item Code'] == SKU:
                # add mode
                if self.add_mode:
                    self.order_list.loc[index,'ItemGet'] += n           # add quantity
                    self.order_list.loc[index,'BoxNo'].add(carton_code) # add carton code to set

                    # add Carton Count
                    if item_name not in self.carton_count.keys():
                        self.carton_count[item_name] = {
                            carton_code : n
                        }
                    else:
                        if carton_code not in self.carton_count[item_name].keys():  # no carton code found in carton count
                            self.carton_count[item_name][carton_code] = n           # create carton count
                        else:
                            self.carton_count[item_name][carton_code] += n          # add carton count

                    if '' in self.order_list.loc[index,'BoxNo']:
                        self.order_list.loc[index,'BoxNo'].remove('')
                    self.add_list_by_item(SKU, item_name, carton_code, n)

                # sub mode
                elif self.order_list.loc[index,'ItemGet'] > 0:
                    if item_name in self.carton_count.keys():                       # found in carton count
                        if carton_code in self.carton_count[item_name].keys(): 

                            self.carton_count[item_name][carton_code] -= n
                            if self.carton_count[item_name][carton_code] < 0: self.carton_count[item_name][carton_code] = 0

                            self.order_list.loc[index,'ItemGet'] -= n
                            if self.order_list.loc[index,'ItemGet'] < 0: self.order_list.loc[index,'ItemGet'] = 0

                            if self.carton_count[item_name][carton_code] == 0: 
                                self.carton_count[item_name].pop(carton_code, None) # remove carton if = 0
                                if (item_name not in self.Item_set) and (sum(self.carton_count[item_name].values()) == 0):  # item not in original order list
                                    self.order_list.drop([index], axis=0, inplace=True)

                        if len(self.carton_count[item_name].keys()) == 0 : self.carton_count.pop(item_name, None)
                    if item_name in self.Item_set:
                        if self.order_list.loc[index,'ItemGet'] == 0:
                            self.order_list.loc[index,'BoxNo'] = set([''])
                    self.sub_list_by_item(SKU, n)
                found = True
                
                break
        if (not found) and self.add_mode:
            row = {
                'Item Code':SKU,
                'Item Name':item_name,
                'Item Qty': 0,
                'ItemGet': 1,
                'Weight': int(get_weight(item_name))
            }
            if not self.order_list.empty:
                df = pd.DataFrame(row, index=[0])
                df['BoxNo'] = [set([carton_code])]
                self.order_list = pd.concat([self.order_list, df], ignore_index=True)
                if item_name not in self.carton_count.keys():
                    self.carton_count[item_name] = {
                        carton_code : 1
                    }
                else:
                    self.carton_count[item_name][carton_code] = 1
                self.add_list_by_item(SKU, item_name, carton_code)
        self.show_item_list()

    @err
    def add_list_by_item(self, SKU, item_name, carton_code, n:int, *args, **kwargs):
        if self.ID not in self.list_by_item.keys():
            self.list_by_item[self.ID] = {}
            self.list_by_item[self.ID][SKU] = {
                'Item' : item_name,
                'carton code' : set(carton_code),
                'Qty' : n
            }
        else:
            if SKU not in self.list_by_item[self.ID].keys():
                self.list_by_item[self.ID][SKU] = {
                'Item' : item_name,
                'carton code' : set(carton_code),
                'Qty' : n
            }
            else:
                self.list_by_item[self.ID][SKU]['Qty'] += n
                self.list_by_item[self.ID][SKU]['carton code'].add(carton_code)
        self.id_add_label.setText(f'ID : {self.ID} ถูกเพิ่ม')

    @err
    def sub_list_by_item(self, SKU, n, *args, **kwargs):
        if self.ID in self.list_by_item.keys():
            if SKU in self.list_by_item[self.ID].keys():
                if self.list_by_item[self.ID][SKU]['Qty'] > 0:

                    self.list_by_item[self.ID][SKU]['Qty'] -= n
                    if self.list_by_item[self.ID][SKU]['Qty'] < 0 : self.list_by_item[self.ID][SKU]['Qty'] = 0

                    if self.list_by_item[self.ID][SKU]['Qty'] == 0: self.list_by_item[self.ID][SKU]['carton code'] = set()

                    self.id_add_label.setText(f'ID : {self.ID} ถูกลด')

    @err
    def end_of_program(self, *args, **kwargs):
        df = pd.DataFrame(
            columns=['SKU', 'Item', 'carton number', 'carton code', 'Qty (Pcs)', 'unit (g)', 'total (g)'],
        )
        for cartons_number in self.list_by_item:
            for SKU in self.list_by_item[cartons_number]:
                item_name = self.list_by_item[cartons_number][SKU]['Item']
                qty = self.list_by_item[cartons_number][SKU]['Qty']
                unit = get_weight(item_name)

                if len(self.list_by_item[cartons_number][SKU]['carton code']) == 0:
                    continue
                carton_code = f"{sorted(list(self.list_by_item[cartons_number][SKU]['carton code']))}".replace("'","")[1:-1]
                row = {
                    'SKU' : SKU,
                    'Item' : re.sub('\(.*\)', '', item_name),
                    'carton number' : cartons_number,
                    'carton code' : carton_code,
                    'Qty (Pcs)' : qty,
                    'unit (g)' : unit,
                    'total (g)' : qty*unit
                }
                df = pd.concat([df, pd.DataFrame(row, index=[0])], ignore_index=True)
        df = df.sort_values(by=['carton code'])
        row = {
            'SKU' : 'Total',
            'Item' : '',
            'carton number' : '',
            'carton code' : len(df.groupby('carton code').count()),
            'Qty (Pcs)' : df['Qty (Pcs)'].sum(),
            'unit (g)' : df['unit (g)'].sum(),
            'total (g)' : df['total (g)'].sum(),
        }
        df = pd.concat([df, pd.DataFrame(row, index=[0])], ignore_index=True)
        df.to_excel('./file/Packing list by item.xlsx', engine='openpyxl', index=False)

    @err
    def readbarcode(self, num : str, *args, **kwargs) -> str:
        if num == "6979700123456":return "EOF"  #End of file
        num = num[:-1]
        while num[-1] != "0": num = num[:-1]
        num = num[:-1]      #detect trash digits
        chr_list = []
        alpha = textwrap.wrap(num[:-4],2)       #split digit for character
        for c in alpha: chr_list.append(str(chr(int(c))))   
        return str("".join(chr_list)+num[-4:])

    @err
    def get_report(self, *args, **kwargs) -> pd.DataFrame:
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

    @err
    def show_report_window(self, *args, **kwargs):
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

    @err    
    def PDF_report(self, cartons=False, *args, **kwargs):
        employee_name = self.employee_name.text()
        if employee_name == "":
            # show pop up
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("คำเตือน")
            msg.setText("กรุณาใส่ชื่อพนักงาน")
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            x = msg.exec_()
            return

        custumerName = self.customer_name.text()
        ListOfList = self.get_order_list(cartons)
        if len(ListOfList) == 1: return # No item found
        if not cartons:
            self.save_to_csv(ListOfList[1:], custumerName)
            return
        
        if cartons:
            file_name = f"./file/{custumerName} cartons.pdf"
        else:
            file_name = f"./file/{custumerName}.pdf"
        doc = SimpleDocTemplate(file_name,pagesize=(150*mm, 100*mm),
                                rightMargin=100,leftMargin=100,
                                topMargin=15,bottomMargin=15)
        pdfmetrics.registerFont(TTFont('THSarabunNew', './src/THSarabunNew.ttf'))
        Story=[]
        styles=getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Normals',
                                parent=styles['Normal'],
                                fontName='THSarabunNew',
                                alignment=TA_LEFT,
                                fontSize=20,
                                leading=0,
                                textColor=colors.black,
                                borderPadding=0,
                                leftIndent=0,
                                rightIndent=0,
                                spaceAfter=0,
                                spaceBefore=0,
                                splitLongWords=True,
                                spaceShrinkage=0.05,
                                ))
        Story.append(Paragraph(f'{self.ID} : {custumerName}', styles["Normals"]))
        Story.append(Spacer(1, 24))
        if cartons:
            td = Table(ListOfList,style = self.cartons_table_style
                                            ,colWidths=[20*mm, 100*mm, 20*mm],
                                            rowHeights=0.4*inch,
                                            repeatRows=1)
        else:
            td = Table(ListOfList,style = self.cartons_table_style,
                                            colWidths=[0.8*inch,3.5*inch,0.8*inch,0.8*inch,0.8*inch,0.8*inch],
                                            rowHeights=0.4*inch,
                                            repeatRows=1)
        Story.append(td)
        Story.append(Spacer(1, 24))
        Story.append(Paragraph(f'ผู้จัดลงลัง : {employee_name}', styles["Normals"]))
        if cartons:
            Story.append(PageBreak())
            carton_dict = {}
            for index, row in self.order_list.iterrows():
                carton = row['BoxNo']
                for c in carton:
                    if c not in carton_dict.keys():
                        carton_dict[c] = set([row['Item Name']])
                    else:
                        carton_dict[c].add(row['Item Name'])
            for c in carton_dict:
                Story.append(Paragraph(f'{self.ID} : {custumerName}', styles["Normals"]))
                Story.append(Spacer(1, 24))
                Story.append(Paragraph(f"Cartons Code : {c}", styles["Normals"]))
                Story.append(Spacer(1, 24))
                ListOfList = []
                ListOfList.append(['Item', 'Qty(Pcs)'])
                Qty = 0
                for ItemName in carton_dict[c]:
                    item = self.order_list.loc[self.order_list['Item Name'] == ItemName].iloc[0]
                    Qty += self.carton_count[ItemName][c]
                    ListOfList.append([item['Item Name'], self.carton_count[ItemName][c]])
                ListOfList.append(['total', f'{Qty}'])
                td = Table(ListOfList,style = self.cartons_table_style,
                                                colWidths=[120*mm, 20*mm],
                                                rowHeights=0.4*inch,
                                                repeatRows=1)
                Story.append(td)
                Story.append(PageBreak())
            # Add nan page
            nan_list = self.order_list.loc[self.order_list['ItemGet'] == 0]
            if len(nan_list) > 0:
                Story.append(Paragraph(f'{self.ID} : {custumerName}', styles["Normals"]))
                Story.append(Spacer(1, 24))
                Story.append(Paragraph(f"Cartons Code : nan", styles["Normals"]))
                Story.append(Spacer(1, 24))
                ListOfList = []
                ListOfList.append(['Item', 'Qty(Pcs)'])
                for index, row in self.order_list.loc[self.order_list['ItemGet'] == 0].iterrows():
                    ListOfList.append([row['Item Name'], '0'])
                ListOfList.append(['total', '0'])
                td = Table(ListOfList,style = self.cartons_table_style,
                                                colWidths=[120*mm, 20*mm],
                                                rowHeights=0.4*inch,
                                                repeatRows=1)
                Story.append(td)
        try:
            doc.build(Story)
        except PermissionError:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("คำเตือน")
            msg.setText("กรุณาปิดไฟล์ PDF ก่อนทำการ save")
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            x = msg.exec_()
        except:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("คำเตือน")
            msg.setText("ไม่สามารถทำการเขียนไฟล์ PDF ได้")
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            x = msg.exec_()

    @err
    def get_str_carton(self, series : pd.Series, *args, **kwargs):
        s = []
        for carton in series:
            if len(carton) == 0:
                text = ''
            else:
                text = f"{[x for x in carton]}".replace("'","")[1:-1]
            s.append(text)
        return s

    def save_to_csv(self, ListOfList, custumerName):
        df = pd.DataFrame(ListOfList, columns = ['SKU', 'สินค้า', 'จำนวนที่สั่ง', 'จำนวนที่ได้', 'ราคาต่อชิ้น', 'ราคารวม'])
        df.to_csv(f'./file/{custumerName}.csv', encoding='utf-8', index=False)

    def get_quantity(self) -> int:
        text = self.quantity_edit_text.text().strip()
        if len(text) == 0: return 1
        if re.match(r'^\d+$', text):
            return int(text)
        else: return 0
        
if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(main_window)
    main_window.show()
    sys.exit(app.exec_())
