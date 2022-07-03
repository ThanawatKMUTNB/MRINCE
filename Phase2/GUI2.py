from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QHeaderView
import pandas as pd
import textwrap
from report import Ui_ReportWindow
from reportlab.platypus import SimpleDocTemplate,Paragraph, Spacer, Table
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
import sys
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(944, 572)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
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
        self.item_ID = QtWidgets.QLineEdit(self.centralwidget)
        self.item_ID.setMinimumSize(QtCore.QSize(0, 30))
        self.item_ID.setMaximumSize(QtCore.QSize(16777215, 30))
        self.item_ID.setFont(font)
        self.item_ID.setObjectName("item_ID")
        self.gridLayout.addWidget(self.item_ID, 3, 1, 1, 2)
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
        self.gridLayout.addWidget(self.cus_ID, 1, 1, 1, 2)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 894, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
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

        self.report_ui.pushButton.clicked.connect(self.PDF_report)

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
        self.employee_name.setPlaceholderText(_translate("MainWindow", "ใส่ชื่อพนักงาน"))

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

    def get_order_list(self) -> list:
        LIST = []
        LIST.append(['SKU', 'สินค้า', 'จำนวนที่สั่ง', 'จำนวนที่ได้'])
        for index, row in self.order_list.iterrows():
            ROW = []
            ROW.append(str(row['Item Code']))
            ROW.append(str(row['Item Name']))
            ROW.append(str(row['Item Qty']))
            ROW.append(str(row['ItemGet']))
            LIST.append(ROW)
        return LIST

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
        print('start add item funcion')
        item_ID = self.item_ID.text()
        print(f'read bar code as : {item_ID}')
        self.item_ID.clear()
        if (item_ID == "") or (len(item_ID) != 13) or (not (item_ID.isnumeric())):
            return
        SKU = self.readbarcode(item_ID)
        print(f'SKU : {SKU}')
        found = False
        for index,row in self.order_list.iterrows():
            if row['Item Code'] == SKU:
                print('SKU found in order list')
                if self.add_mode:
                    print('add item')
                    self.order_list.loc[index,'ItemGet'] += 1
                elif self.order_list.loc[index,'ItemGet'] >0:
                    print('sub item')
                    self.order_list.loc[index,'ItemGet'] -= 1
                found = True
                break
        if not found:
            print('no SKU fount in order list -> Add new order')
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
        
    def PDF_report(self):
        employee_name = self.employee_name.text()
        if employee_name == "":
            # show pop up
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("คำเตือน")
            msg.setText("กรุณาใส่ชื่อพนักงาน")
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            x = msg.exec_()

        ListOfList = self.get_order_list()
        if  len(ListOfList) == 1: return # No item found
        
        custumerName = self.customer_name.text()
        doc = SimpleDocTemplate(str(custumerName)+".pdf",pagesize=A4,
                                rightMargin=100,leftMargin=100,
                                topMargin=20,bottomMargin=20)
        pdfmetrics.registerFont(TTFont('THSarabunNew', 'THSarabunNew.ttf'))
        Story=[]
        styles=getSampleStyleSheet()
        # styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
        styles.add(ParagraphStyle(name='Normals',
                                parent=styles['Normal'],
                                fontName='THSarabunNew',
                                alignment=TA_LEFT,
                                fontSize=16,
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
        Story.append(Paragraph(custumerName, styles["Normals"]))
        Story.append(Spacer(1, 12))
        Story.append(Spacer(1, 12))
        td = Table(ListOfList,style = [  ('BACKGROUND', (0, 0), (-1,0), '#D2D2D2'),
                                        ('FONT', (0,0), (-1,-1),('THSarabunNew')),
                                        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                        ('FONTSIZE', (0,0), (-1,-1),15),
                                        ("ALIGN", (0, 0), (0, 0), "CENTER"),
                                        ],colWidths=[1*inch,4*inch,1*inch,1*inch],
                                            rowHeights=0.4*inch)
        Story.append(td)
        Story.append(Spacer(1, 12))
        Story.append(Paragraph(f'ผู้จัดลงลัง : {employee_name}', styles["Normals"]))
        doc.build(Story)
        
if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(main_window)
    main_window.show()
    sys.exit(app.exec_())