import csv
from PyQt5 import QtWidgets, uic
import sys
import os
import DataManager
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QPushButton, QFileDialog, QVBoxLayout
import PandasModel
import  jpype     
import  asposecells
class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('MRINCE\GUI_Mrince.ui', self)
        self.CSV1 = ""
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.options = ('Get File Name', 'Get File Names', 'Get Folder Dir', 'Save File Name')

        self.combo = QComboBox()
        self.combo.addItems(self.options)
        layout.addWidget(self.combo)

        self.button = self.findChild(QtWidgets.QPushButton, 'pushButton') # Find the button
        self.button.clicked.connect(self.launchDialog)
        
        self.pushButton_9.clicked.connect(self.ExportDupCSV)
        
        self.show()
    
    def ExportDupCSV(self):
        try:
            # self.df2
            file_location = self.CSV1
            # print(file_location)
            file_name = os.path.basename(file_location)
            # print(file_name)
            newPath = file_location.replace(file_name, "Cleared_"+file_name)
            self.df2.to_csv(newPath)
            # print(newPath)
                 
            jpype.startJVM() 
            from asposecells.api import Workbook
            workbook = Workbook(newPath)
            pdfPath = newPath.replace(".csv",".pdf")
            workbook.Save(pdfPath)
            jpype.shutdownJVM()
            
        except :
            pass
        
    def launchDialog(self):
        self.options = ('Get File Name', 'Get File Names', 'Get Folder Dir', 'Save File Name')
        option = self.options.index(self.combo.currentText())
        response = "Got Nothing Start"
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
            self.CSV1 = response
            self.label.setText(self.CSV1)
            
            df = DataManager.dm(self.CSV1).sort()
            model = PandasModel.PandasModel(df)
            self.tableView.setModel(model)
            self.label_2.setText("Count : "+str(len(df)))
            
            self.df2 = DataManager.dm(self.CSV1).dfSum()
            model2 = PandasModel.PandasModel(self.df2)
            self.tableView_2.setModel(model2)
            self.label_3.setText("Count : "+str(len(self.df2)))
            
            # print("---------------------------",response)
        
    def getFileName(self):  #1 file
        # file_filter = 'Excel File (*.xlsx *.csv *.xls)'
        file_filter = 'Excel File (*.csv)'
        
        response = QFileDialog.getOpenFileName(
            parent=self,
            caption='Select a data file',
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter='Excel File (*.xlsx *.xls *.csv)' #defult filter
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