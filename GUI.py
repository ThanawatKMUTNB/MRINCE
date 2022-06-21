import csv
from PyQt5 import QtWidgets, uic
import sys
import os
import DataManager
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QPushButton, QFileDialog, QVBoxLayout
import PandasModel
# import weasyprint
import pdfkit
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
        # self.ExportByProductButton.clicked.connect(self.launchDialog)
        self.ExportByProductButton.clicked.connect(self.getPathExportByProduct)
        
        self.ExportByProductCustomer = self.findChild(QtWidgets.QPushButton, 'pushButton_2')
        # self.ExportByProductButton.clicked.connect(self.launchDialog)
        self.ExportByProductCustomer.clicked.connect(self.getPathExportByCustomer)
        
        self.pushButton_9.clicked.connect(self.ExportDupCSV)
        
        self.show()
    
    def getPathExportByProduct(self):
        sdm = DataManager.dm()
        
        self.ExportByProductPath = self.launchDialog()
        self.label.setText(self.ExportByProductPath)
        
        sdm.setdf(self.ExportByProductPath)
        
        self.ExportByProductTable = sdm.sort()
        model = PandasModel.PandasModel(self.ExportByProductTable)
        self.tableView.setModel(model)
        self.label_2.setText("Count : "+str(len(self.ExportByProductTable)))
        print(type(self.ExportByProductTable))
        
    def getPathExportByCustomer(self):
        sdm = DataManager.dm()
        
        self.ExportByCustomerPath = self.launchDialog()
        self.label_4.setText(self.ExportByCustomerPath)
        
        sdm.setdf(self.ExportByCustomerPath)
        
        self.ExportByCustomerTable = sdm.sort()
        model = PandasModel.PandasModel(self.ExportByCustomerTable)
        self.tableView_2.setModel(model)
        self.label_3.setText("Count : "+str(len(self.ExportByCustomerTable)))
    
    def ExportDupCSV(self):
        # try:
            cols = list(self.ExportByProductTable.columns.values)
            if cols == ['Product ID', 'Product Name', 'Line Item Quantity', 'Product SKU', 'Product Categories']:
                # self.ExportByCustomerTable
                file_location = self.ExportByProductPath
                # print(file_location)
                file_name = os.path.basename(file_location)
                # print(file_name)
                newPath = file_location.replace(file_name, "Cleared_"+file_name)
                self.label_5.setText(newPath)
                self.ExportByProductTable.to_csv(newPath, index=False)
                # print(newPath)
                
                pdfPath = newPath.replace(".csv",".pdf")
                htmlPath = newPath.replace(".csv",".html")
                
                self.ExportByProductTable.to_html(htmlPath)
                # config = pdfkit.configuration(wkhtmltopdf='C:\Program Files (x86)\wkhtmltopdf')
                # pdfkit.from_file(newPath,pdfPath,configuration=config)
                
        #     else:
        #         pass
        # except :
        #     pass
        
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