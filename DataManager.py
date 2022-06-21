import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from barcode import EAN13
from barcode.writer import ImageWriter
import textwrap
import re
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QPushButton, QFileDialog, QVBoxLayout
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib as mpl
class dm():
    def __init__(self):
        self.font = "Phase1/src/Kanit-Light.ttf"
        
    def setdf(self,path):
        self.df = pd.read_csv(path)
        
    def sort(self):
        try:
            self.df = self.df.sort_values(by=['Product ID'])
            return self.df
        except :
            return self.df
        
    def dfSum(df):
        try:
            # print("------///")
            # cols = list(self.df.columns.values)
            # print(cols)
            df1 = df.sort_values(by=['Product ID'])
            df1 = df1.drop(['Line Item Quantity'], axis=1)
            df1 = df1.drop_duplicates()
            # print(len(self.df1))
            df2 = df.groupby(['Product ID'], as_index=False)['Line Item Quantity'].sum()
            # print(len(self.df2))
            
            # print("------///")
            dfsum = pd.merge(df1,df2) 
            dfsum = dfsum[['Product ID', 'Product Name', 'Line Item Quantity', 'Product SKU', 'Product Categories']]
            
            return dfsum
        except :
            return df
    
    def draw_multiple_line_text(self,image, text, font, text_color, text_start_height):
        draw = ImageDraw.Draw(image)
        image_width, image_height = image.size
        y_text = text_start_height
        lines = textwrap.wrap(text, width=40)
        for line in lines:
            line_width, line_height = font.getsize(line)
            draw.text(((image_width - line_width) / 2, y_text), 
                    line, font=font, fill=text_color)
            y_text += line_height
    
    def createBarcodeSKU(sku):
        str_to_num = str(sku)
        while len(str_to_num) <13:
            str_to_num = f"{str_to_num}0"
        code = EAN13(str_to_num,writer=ImageWriter())
        code.save('CustomerID')
        img = Image.open('Phase1\src\CustomerID.png')
        return img
    
    def createbarcode(self,sku):
        num_list = []
        for c in re.findall('[a-zA-Z]+',sku)[0]: num_list.append(str(ord(c)))
        str_to_num = "".join(num_list) + "".join(re.findall('[0-9]+',sku))
        while len(str_to_num) <13:
            str_to_num = f"{str_to_num}0"
        code = EAN13(str_to_num,writer=ImageWriter())
        code.save('Barcode_Copy')
        img = Image.open('Barcode_Copy.png')
        return img
    
    def Barcode_Copy(self,df):     #1
        width = 400
        height = 250
        fonts = ImageFont.truetype(self.font, size=20)
        image_list = []
        for index, row in df.iterrows():
            product = row['Product Name']
            product_name = product.split()[0]
            product_weight = f"{re.findall('[0-9]+',product)[0]} กรัม"
            product_sku = row['Product SKU']
            img = Image.new('RGB', (width, height), color='white')
            ImageDraw.Draw(img)       
            text_color = (0,0,0)   #black
            self.draw_multiple_line_text(img, product_weight, fonts, text_color, height*(2/10))
            self.draw_multiple_line_text(img, product_name, fonts, text_color, height*(3/10))
            self.draw_multiple_line_text(img, product_sku, fonts, text_color, height*(4/10))
            code = self.createbarcode(product_sku)
            code = code.resize((int(width/3),int(height/4)))
            img.paste(code,(int(width*(1/3)),int(height*(1/2))))
            subloop = int(row['Line Item Quantity'])
            for copy in range(subloop): image_list.append(img.convert('RGB'))
        image_list[0].save('Quantity_pages.pdf', save_all=True, append_images=image_list[1:])
        print("Barcode Copy Complete")
    
    def Product_type(self,df):     #2
        logo = Image.open(os.path.join("Phase1","src","logo-web.png"))
        width = 1240
        height = 1754
        head_font = ImageFont.truetype(self.font, size=160)
        content_1_font = ImageFont.truetype(self.font, size=100)
        content_2_font = ImageFont.truetype(self.font, size=60)
        image_list = []
        for index, row in df.iterrows():
            img = Image.new('RGB', (width, height), color='white')
            ImageDraw.Draw(img)
            text_color = (0,0,0)
            self.draw_multiple_line_text(img, row['Product SKU'], head_font, text_color, 400)
            self.draw_multiple_line_text(img, f"{re.findall('[0-9]+',row['Product Name'])[0]}  กรัม/แพ็ค", content_1_font, text_color, 700)
            self.draw_multiple_line_text(img, f"{row['Product Name']}     {row['Product Categories']}", content_2_font, text_color, 1000)
            self.draw_multiple_line_text(img, str(row['Line Item Quantity']), head_font, text_color, 1200)
            self.draw_multiple_line_text(img, "แพ็ค", content_1_font, text_color, 1400)
            img.paste(logo,(int(width/2.4),200))
            image_list.append(img.convert('RGB'))

        image_list[0].save('Product_pages.pdf', save_all=True, append_images=image_list[1:])
        print("Product type Complete")
    
    def Product_label(self):    #3 filter veg and fruits
        filter_values = ['ผัก','ผลไม้']
        newdf = self.df.loc[~self.df['Product Categories'].isin(filter_values)]
        width = 400
        height = 250
        fonts = ImageFont.truetype(self.font, size=20)
        image_list = []
        for index, row in newdf.iterrows():
            product = row['Product Name']
            product_name = product.split()[0]
            product_weight = f"{re.findall('[0-9]+',product)[0]} กรัม"
            product_sku = row['Product SKU']
            img = Image.new('RGB', (width, height), color='white')
            ImageDraw.Draw(img)       
            text_color = (0,0,0)   #black
            self.draw_multiple_line_text(img, product_weight, fonts, text_color, height*(2/10))
            self.draw_multiple_line_text(img, product_name, fonts, text_color, height*(3/10))
            self.draw_multiple_line_text(img, product_sku, fonts, text_color, height*(4/10))
            code = self.createbarcode(product_sku)
            code = code.resize((int(width/3),int(height/4)))
            img.paste(code,(int(width*(1/3)),int(height*(1/2))))
            subloop = int(row['Line Item Quantity'])
            for copy in range(subloop): image_list.append(img.convert('RGB'))
    
    def Durian_crate(self,df):     #4
        Durian_ID = [7576,7562,7564,8140,8216]    #กล่อง ,ลังเล็ก, ลังใหญ่, ก้านยาวกล่องเดี่ยว, ภูเขาไฟกล่องเดียว
        boxshare = [24,12]          #ลังใหญ่ ,ลังเล็ก
        durianDF = df.loc[df['Product ID'].isin(Durian_ID)]
        sumbox = 0
        width = 1240
        height = 1754
        font = ImageFont.truetype(self.font, size=90)
        for index, row in durianDF.iterrows():
            if row['Product ID'] == Durian_ID[2]: sumbox += 24
            elif row['Product ID'] == Durian_ID[1]: sumbox += 12
            else: sumbox += 1
        box = { 'big':int(sumbox/boxshare[0]),
                'small':int((sumbox%boxshare[0])/boxshare[1]),
                'single':int((sumbox%boxshare[0])%boxshare[1])}
        img = Image.new('RGB', (width, height), color='white')
        ImageDraw.Draw(img)
        text_color = (0,0,0)
        text_start_height = height/5
        text = [f"กล่องเดี่ยวทั้งหมด  {sumbox}  กล่อง",
                f"ลังใหญ่  {box['big']}  ลัง",
                f"ลังเล็ก  {box['small']}  ลัง",
                f"กล่องเดี่ยว  {box['single']}  ลัง"]
        for t in text:
            self.draw_multiple_line_text(img, t, font, text_color, text_start_height)
            text_start_height += int(height/6)
        img.save('Durian.pdf', save_all=True)
        print("Calculate Durians Complete")
    
    def Cover(self,Max):        #5
        width = 378
        height = 284
        image_list = []
        font = ImageFont.truetype("Phase1/src/Kanit-Medium.ttf", size=90)
        logo = Image.open("/Phase1/src/LogoBW.png")

        for i in range(Max):
            num = str(i+1)
            while len(num)<3:
                num = f"0{num}"
            img = Image.new('RGB', (width, height), color='white')
            imgDraw = ImageDraw.Draw(img)
            textWidth, textHeight = imgDraw.textsize(num, font=font)
            xText = (width - textWidth) / 2
            yText = (height - textHeight) / 2
            imgDraw.text((xText, yText), num, font=font, fill=(0, 0, 0))
            img.paste(logo,(int(width/2.7),50))
            image_list.append(img.convert('RGB'))
        image_list[0].save('Amount_pages.pdf', save_all=True, append_images=image_list[1:])
        print("Amount Complete")
    
    def ExportDupCSV(self,df,dfPath):
        try:
            self.ExportByProductTable = df
            self.ExportByProductPath = dfPath
            cols = list(self.ExportByProductTable.columns.values)
            if cols == ['Product ID', 'Product Name', 'Line Item Quantity', 'Product SKU', 'Product Categories']:
                # self.ExportByCustomerTable
                file_location = self.ExportByProductPath
                # print(file_location)
                file_name = os.path.basename(file_location)
                # print(file_name)
                newPath = file_location.replace(file_name, "Cleared_"+file_name)
                # self.label_5.setText(newPath)
                # self.ExportByProductTable.to_csv(newPath, index=False)
                # print(newPath)
                
                pdfPath = newPath.replace(".csv",".pdf")
                htmlPath = newPath.replace(".csv",".html")
                mpl.font_manager.fontManager.addfont( os.path.join('Phase1','src','thsarabunnew-webfont.ttf'))
                mpl.rc('font', family='TH Sarabun New')

                fig, ax = plt.subplots(figsize=(30,6))
                ax.axis('tight')
                ax.axis('off')
                the_table = ax.table(cellText=self.ExportByProductTable.values,colLabels=self.ExportByProductTable.columns,loc='center')
                the_table.set_fontsize(40)
                the_table.scale(1,4)
                pp = PdfPages(pdfPath)
                pp.savefig(fig, bbox_inches='tight')
                pp.close()
        except :
            pass
        