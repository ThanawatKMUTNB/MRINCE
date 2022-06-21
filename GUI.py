import csv
from email.policy import strict
from PyQt5 import QtWidgets, uic
import sys
import os
import DataManager
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QPushButton, QFileDialog, QVBoxLayout
import PandasModel

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('GUI_Mrince.ui', self)
        self.ExportByProductPath = ""
        self.ExportByCustomerPath = ""
        
        self.ExportByProductTable = ""
        self.ExportByCustomerTable = ""
        
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.options = ('Get File Name', 'Get File Names', 'Get Folder Dir', 'Save File Name')

        self.combo = QComboBox()
        self.combo.addItems(self.options)
        layout.addWidget(self.combo)

        self.ExportByProductButton = self.findChild(QtWidgets.QPushButton, 'pushButton')
        self.ExportByProductButton.clicked.connect(self.getPathExportByProduct)
        
        self.ExportByProductCustomer = self.findChild(QtWidgets.QPushButton, 'pushButton_2')
        self.ExportByProductCustomer.clicked.connect(self.getPathExportByCustomer)
        
        self.pushButton_3.clicked.connect(self.getBarcodeCopy) #1
        
        self.pushButton_4.clicked.connect(self.getProductType) #2
        
        #3
        
        self.pushButton_6.clicked.connect(self.getDurianCrate) #4
        
        self.pushButton_7.clicked.connect(self.getParcelCover) #5
        
        self.pushButton_9.clicked.connect(self.ExportDupCSV) #6
        
        self.pushButton_8.clicked.connect(self.CustomerProduct) #7
        
        
        self.CustomerProductBT = self.findChild(QtWidgets.QPushButton, 'pushButton_8') #7
        self.CustomerProductBT.clicked.connect(self.CustomerProduct)
        self.show()
    
    def getBarcodeCopy(self): #1
        sdm = DataManager.dm()
        if self.ExportByProductPath != "":
            sdm.Barcode_Copy(self.ExportByProductTable)
    
    def getProductType(self): #2
        sdm = DataManager.dm()
        if self.ExportByProductPath != "":
            sdm.Product_type(self.ExportByProductTable)
            
    #3
    
    def getDurianCrate(self): #4
        sdm = DataManager.dm()
        if self.ExportByProductPath != "":
            sdm.Durian_crate(self.ExportByProductTable)
    
    def getParcelCover(self): #5
        sdm = DataManager.dm()
        try:
            Max = int(self.lineEdit.text())
            # print(int(self.lineEdit.text()),self.lineEdit.text())
            sdm.Cover(Max)
        except :
            pass
    
    def ExportDupCSV(self): #6
        if self.ExportByProductPath != "":
            self.label_5.setText("Waiting...")
        self.ExportByProductTable = DataManager.dm.dfSum(self.ExportByProductTable)
        DataManager.dm.ExportDupCSV(self,self.ExportByProductTable,self.ExportByProductPath)
        if self.ExportByProductPath != "":
            self.label_5.setText("Compleate")
            
    def CustomerProduct(self):#7
        sdm = DataManager.dm()
        
        if self.ExportByCustomerPath != "":
            self.label_6.setText("Waiting...")
        # try:
        sdm.Customer_product(self.ExportByCustomerTable)
        # except :
        #     pass
        if self.ExportByCustomerPath != "":
            self.label_6.setText("Compleate")
            
    def getPathExportByProduct(self):
        sdm = DataManager.dm()
        try:
            self.ExportByProductPath = self.launchDialog()
            self.label.setText(self.ExportByProductPath)
            sdm.setdf(self.ExportByProductPath)
            
            self.ExportByProductTable = sdm.sort()
            model = PandasModel.PandasModel(self.ExportByProductTable)
            self.tableView.setModel(model)
            self.label_2.setText("Count : "+str(len(self.ExportByProductTable)))
        except :
            pass
        
    def getPathExportByCustomer(self):
        sdm = DataManager.dm()
        try:
            self.ExportByCustomerPath = self.launchDialog()
            self.label_4.setText(self.ExportByCustomerPath)
            
            sdm.setdf(self.ExportByCustomerPath)
            
            self.ExportByCustomerTable = sdm.sort()
            model = PandasModel.PandasModel(self.ExportByCustomerTable)
            self.tableView_2.setModel(model)
            self.label_3.setText("Count : "+str(len(self.ExportByCustomerTable)))
        except :
            pass
        
    def launchDialog(self):
        self.options = ('Get File Name', 'Get File Names', 'Get Folder Dir', 'Save File Name')
        option = self.options.index(self.combo.currentText())
        
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
        file_filter = 'Data File (*.xlsx *.csv *.dat);; Excel File (*.xlsx *.xls)'
        response = QFileDialog.getOpenFileNames(
            parent=self,
            caption='Select a data file',
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter='Excel File (*.xlsx *.xls)'
        )
        return response[0]

    def getDirectory(self): #floder
        response = QFileDialog.getExistingDirectory(
            self,
            caption='Select a folder'
        )
        return response 

    def getSaveFileName(self):
        file_filter = 'Data File (*.xlsx *.csv *.dat);; Excel File (*.xlsx *.xls)'
        response = QFileDialog.getSaveFileName(
            parent=self,
            caption='Select a data file',
            directory= 'Data File.dat',
            filter=file_filter,
            initialFilter='Excel File (*.xlsx *.xls)'
        )
        print(response)
        return response[0]
    
        
app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()