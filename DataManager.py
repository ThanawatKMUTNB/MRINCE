import pandas as pd


class dm():
    def __init__(self,direc):
        self.df = pd.read_csv(direc)
    def sort(self):
        try:
            self.df = self.df.sort_values(by=['Product ID'])
            return self.df
        except :
            return self.df
    def dfSum(self):
        try:
            # print("------///")
            cols = list(self.df.columns.values)
            print(cols)
            self.df1 = self.df.sort_values(by=['Product ID'])
            self.df1 = self.df1.drop(['Line Item Quantity'], axis=1)
            self.df1 = self.df1.drop_duplicates()
            print(len(self.df1))
            self.df2 = self.df.groupby(['Product ID'], as_index=False)['Line Item Quantity'].sum()
            print(len(self.df2))
            
            # print("------///")
            self.dfsum = pd.merge(self.df1,self.df2) 
            self.dfsum = self.dfsum[['Product ID', 'Product Name', 'Line Item Quantity', 'Product SKU', 'Product Categories']]
            
            return self.dfsum
        except :
            return self.df