import csv
from email.policy import strict
from PyQt5 import QtWidgets, uic,QtGui
import sys
import os
# import QtGui
from numpy import save
import DataManager
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QPushButton, QFileDialog, QVBoxLayout
import PandasModel

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('GUI_Mrince.ui', self)
        
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.options = ('Get File Name', 'Get File Names', 'Get Folder Dir', 'Save File Name')

        self.combo = QComboBox()
        self.combo.addItems(self.options)
        layout.addWidget(self.combo)
        
        self.clearAll()
        
        self.pushButton.clicked.connect(self.getPathExportByProduct)
        self.pushButton.setStyleSheet("background-color : blue;color : white")
        
        self.pushButton_2.clicked.connect(self.getPathExportByCustomer)
        self.pushButton_2.setStyleSheet("background-color : blue;color : white")
        
        self.pushButton_3.clicked.connect(self.getBarcodeCopy) #1
        self.pushButton_3.setStyleSheet("background-color : #FC6238;color : white")
        
        self.pushButton_4.clicked.connect(self.getProductType) #2
        self.pushButton_4.setStyleSheet("background-color : #74737A;color : white")
        
        #3
        self.pushButton_5.setStyleSheet("background-color : #0065A2;color : white")
        
        self.pushButton_6.clicked.connect(self.getDurianCrate) #4
        self.pushButton_6.setStyleSheet("background-color : #FFBF65;color : white")
        
        self.pushButton_7.clicked.connect(self.getParcelCover) #5
        self.pushButton_7.setStyleSheet("background-color : #6C88C4;color : white")
        
        self.pushButton_11.clicked.connect(self.getParcelCover_3Copy) #5*3
        self.pushButton_11.setStyleSheet("background-color : #C05780;color : white")
        
        
        self.pushButton_9.clicked.connect(self.ExportDupCSV) #6
        self.pushButton_9.setStyleSheet("background-color : #00A5E3 ;color : white")
        
        self.pushButton_8.clicked.connect(self.CustomerProduct) #7
        self.pushButton_8.setStyleSheet("background-color : #4DD091 ;color : white")
        
        self.pushButton_10.setStyleSheet("background-color : #FF5768 ;color : white")
        self.pushButton_10.clicked.connect(self.clearAll) #7
        # font-size: 24px;
        # self.CustomerProductBT = self.findChild(QtWidgets.QPushButton, 'pushButton_8') #7
        # self.CustomerProductBT.clicked.connect(self.CustomerProduct)
        # self.showFullScreen()
        self.showMaximized()
        #setFixedSize
    
    def clearAll(self):
        self.ExportByProductPath = ""
        self.ExportByCustomerPath = ""
        
        self.ExportByProductTable = ""
        self.ExportByCustomerTable = ""
        
        self.label_4.clear()
        self.label.clear()
        
        self.label_3.setText("No choose file")
        self.label_3.setStyleSheet("color : red")
        
        self.label_2.setText("No choose file")
        self.label_2.setStyleSheet("color : red")
        #5678910 Need Export by Product
        
        self.label_5.setText("Need Export by Product")
        self.label_5.setStyleSheet("color : black")
        
        self.label_6.setText("Need Export by Customer")
        self.label_6.setStyleSheet("color : black")
        
        self.label_7.setText("Need Export by Product")
        self.label_7.setStyleSheet("color : black")
        
        self.label_8.setText("Need Export by Product")
        self.label_8.setStyleSheet("color : black")
        
        self.label_9.setText("Need Export by Product")
        self.label_9.setStyleSheet("color : black")
        
        self.label_10.setText("Need Export by Product")
        self.label_10.setStyleSheet("color : black")
        
        self.label_11.setText("Need Export by Customer")
        self.label_11.setStyleSheet("color : black")
        
        self.lineEdit.clear()
        
        self.tableView_2.setModel(None)
        self.tableView.setModel(None)
        
        
    def getBarcodeCopy(self): #1
        sdm = DataManager.dm()
        if self.ExportByProductPath != "":
            self.label_7.setText("Waiting...")
            self.label_7.setStyleSheet("color : red;")
            sdm.Barcode_Copy(self.ExportByProductTable)
            self.label_7.setText("Compleate")
            self.label_7.setStyleSheet("color : green;")
            
    def getProductType(self): #2
        sdm = DataManager.dm()
        if self.ExportByProductPath != "":
            self.label_10.setText("Waiting...")
            self.label_10.setStyleSheet("color : red;")
            sdm.Product_type(self.ExportByProductTable)
            self.label_10.setText("Compleate")
            self.label_10.setStyleSheet("color : green;")
            
    #3
    
    def getDurianCrate(self): #4
        sdm = DataManager.dm()
        if self.ExportByProductPath != "":
            self.label_9.setText("Waiting...")
            self.label_9.setStyleSheet("color : red;")
            sdm.new_Durian_crate_PDF(self.ExportByProductTable,self.ExportByProductPath)
            self.label_9.setText("Compleate")
            self.label_9.setStyleSheet("color : green;")
    
    def getParcelCover(self): #5
        sdm = DataManager.dm()
        try:
            Max = int(self.lineEdit.text())
            sdm.Cover(Max)
        except :
            pass
    
    def ExportDupCSV(self): #6
        try:
            if self.ExportByProductPath != "":
                ExportPath = self.launchDialogGetPath()
                self.label_5.setText("Waiting...")
                self.label_5.setStyleSheet("color : red;")
                self.ExportByProductTable = DataManager.dm.dfSum(self.ExportByProductTable)
                DataManager.dm.ExportDupCSV(self,self.ExportByProductTable,ExportPath)
                self.label_5.setText("Compleate")
                self.label_5.setStyleSheet("color : green;")
        except :
            pass
        
    def CustomerProduct(self):#7
        sdm = DataManager.dm()
        if self.ExportByCustomerPath != "":
            self.label_6.setText("Waiting...")
            self.label_6.setStyleSheet("color : red;")
            sdm.Customer_product(self.ExportByCustomerTable)
            self.label_6.setText("Compleate")
            self.label_6.setStyleSheet("color : green;")
            
    def getPathExportByProduct(self):
        sdm = DataManager.dm()
        try:
            self.label_2.setText("No choose file")
            self.label_2.setStyleSheet("color : red")
            self.ExportByProductPath = self.launchDialog()
            sdm.setdf(self.ExportByProductPath)
            self.ExportByProductTable = sdm.sort()
            self.ExportByProductTable = self.ExportByProductTable[['Product ID', 'Product Name', 'Line Item Quantity', 'Product SKU', 'Product Categories']]
            self.label.setText(self.ExportByProductPath)
            model = PandasModel.PandasModel(self.ExportByProductTable)
            self.tableView.setModel(model)
            # self.label_2.setText("Count : "+str(len(self.ExportByProductTable)))
            self.label_2.setText("Compleate")
            self.label_2.setStyleSheet("color : green")
        except :
            pass
        
    def getParcelCover_3Copy(self): #5
        sdm = DataManager.dm()
        try:
            Max = int(self.lineEdit.text())
            sdm.Order_label(self.ExportByCustomerTable)
        except :
            pass
        
    def getPathExportByCustomer(self):
        sdm = DataManager.dm()
        try:
            self.label_3.setText("No choose file")
            self.label_3.setStyleSheet("color : red")
            
            self.ExportByCustomerPath = self.launchDialog()
            self.label_4.setText(self.ExportByCustomerPath)
            
            sdm.setdf(self.ExportByCustomerPath)
            
            self.ExportByCustomerTable = sdm.sort()
            model = PandasModel.PandasModel(self.ExportByCustomerTable)
            self.tableView_2.setModel(model)
            # self.label_3.setText("Count : "+str(len(self.ExportByCustomerTable)))
            self.label_3.setText("Compleate")
            self.label_3.setStyleSheet("color : green")
        except :
            pass
    
    def launchDialogGetPath(self):
        self.options = ('Get File Name', 'Get File Names', 'Get Folder Dir', 'Save File Name')
        option = self.options.index('Save File Name')
        # print(self.combo.currentText())
        response = ''
        print(option)
        if option == 0:
            response = self.getFileName()
        elif option == 1:
            response = self.getFileNames()
        elif option == 2:
            response = self.getDirectory()
        elif option == 3:
            response = self.getSaveFileName()
        else:
            print('Got Nothing')
        
        if response != '' :
            return response
        
    def launchDialog(self):
        self.options = ('Get File Name', 'Get File Names', 'Get Folder Dir', 'Save File Name')
        option = self.options.index(self.combo.currentText())
        # print(self.combo.currentText())
        response = ''
        if option == 0:
            response = self.getFileName()
        elif option == 1:
            response = self.getFileNames()
        elif option == 2:
            response = self.getDirectory()
        elif option == 3:
            response = self.getSaveFileName()
        else:
            print('Got Nothing')
        
        if response != '' :
            return response
    
    def getFileName(self):  #1 file
        # file_filter = 'Excel File (*.xlsx *.csv *.xls)'
        file_filter = 'Excel File (*.csv)'
        
        response = QFileDialog.getOpenFileName(
            parent=self,
            caption='Select a data file',
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter='Excel File (*.csv)' #defult filter
        )
        # print('\n#########################################\n')
        # print(response[0])
        # df = pd.read_csv(response[0], encoding='windows-1252')
        # print(df.columns)
        # print('\n#########################################\n')
        return response[0]

    def getFileNames(self): #>1 files
        file_filter = 'Data File (*.csv);; Excel File (*.csv)'
        response = QFileDialog.getOpenFileNames(
            parent=self,
            caption='Select a data file',
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter='Excel File (*.csv)'
        )
        return response[0]

    def getDirectory(self): #floder
        response = QFileDialog.getExistingDirectory(
            self,
            caption='Select a folder'
        )
        return response 
        
    def getSaveFileName(self):
        self.saveFileName = self.ExportByProductPath.replace(".csv",".pdf")
        file_filter = 'PDF (*.pdf);'
        response = QFileDialog.getSaveFileName(
            parent=self,
            caption='Select a data file',
            directory = os.path.basename(self.saveFileName),
            filter=file_filter,
            initialFilter='PDF (*.pdf);'
        )
        # print('response ',response)
        # print('response 0 ',response[0])
        return response[0]
    
        
app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()