import os
import pandas as pd
import DataManager

dfProduct = pd.read_csv(os.path.join('Phase1','Order_Items_Export_-_2022-06-20.csv'))
dfCustomer = pd.read_csv(('orders-2022-06-20-00-16-07.csv'))

DataManager.dm.CIFinvoiceExel(DataManager.dm,dfProduct,dfCustomer)
print("CP")