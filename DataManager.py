import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import PIL.Image
from barcode import EAN13
from barcode.writer import ImageWriter
import textwrap
import re
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QPushButton, QFileDialog, QVBoxLayout
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib as mpl
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import PageBreak
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
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
    
    def draw_multiple_line_text_barcode(self,image, text, font, text_color, text_start_height):
        draw = ImageDraw.Draw(image)
        image_width, image_height = image.size
        y_text = text_start_height
        lines = textwrap.wrap(text, width=40)
        for line in lines:
            line_width, line_height = font.getsize(line)
            draw.text(((image_width - line_width) / 5, y_text), 
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
        try:
            for c in re.findall('[a-zA-Z]+',sku)[0]: num_list.append(str(ord(c)))
        except:pass
        str_to_num = "".join(num_list) + "".join(re.findall('[0-9]+',sku))
        i=0
        while len(str_to_num) <13:
            str_to_num = f"{str_to_num}{i}"
            i+=1
        code = EAN13(str_to_num,writer=ImageWriter())
        code.save('Barcode_Copy')
        img = PIL.Image.open('Barcode_Copy.png')
        return img
    
    def readbarcode(self,num):
        if num == "6979700123456":return "EOF"  #End of file
        num = num[:-1]
        while num[-1] != "0": num = num[:-1]
        num = num[:-1]      #detect trash digits
        chr_list = []
        alpha = textwrap.wrap(num[:-4],2)       #split digit for character
        for c in alpha: chr_list.append(str(chr(int(c))))   
        return str("".join(chr_list)+num[-4:])
    
    def Barcode_Copy(self,df):     #1
        width = 400
        height = 300
        fonts = ImageFont.truetype(self.font, size=20)
        fonts_weight = ImageFont.truetype(self.font, size=15)
        fonts_sku = ImageFont.truetype(self.font, size=20)
        image_list = []
        df.sort_values(by=['Product Name'],inplace=True)
        for index, row in df.iterrows():
            product = row['Product Name']
            product_name = product.split('(')[0]
            product_weight = f"{re.findall('[0-9]+',product)[0]} กรัม"
            product_sku = row['Product SKU']
            img = PIL.Image.new('RGB', (width, height), color='white')
            ImageDraw.Draw(img)       
            text_color = (0,0,0)   #black
            self.draw_multiple_line_text_barcode(img, product_weight, fonts, text_color, height*(5/10))
            self.draw_multiple_line_text_barcode(img, product_name, fonts, text_color, height*(6/10))
            self.draw_multiple_line_text_barcode(img, product_sku, fonts, text_color, height*(1/20))
            code = self.createbarcode(product_sku)
            code = code.resize((int(width/2),int(height/4)))
            img.paste(code,(int(width*(1/50)),int(height*(2/10))))
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
            img = PIL.Image.new('RGB', (width, height), color='white')
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
        # width = 400
        # height = 250
        # fonts = ImageFont.truetype(self.font, size=20)
        # image_list = []
        # for index, row in newdf.iterrows():
        #     product = row['Product Name']
        #     product_name = product.split('(')[0]
        #     product_weight = f"{re.findall('[0-9]+',product)[0]} กรัม"
        #     product_sku = row['Product SKU']
        #     img = PIL.Image.new('RGB', (width, height), color='white')
        #     ImageDraw.Draw(img)       
        #     text_color = (0,0,0)   #black
        #     self.draw_multiple_line_text(img, product_weight, fonts, text_color, height*(2/10))
        #     self.draw_multiple_line_text(img, product_name, fonts, text_color, height*(3/10))
        #     self.draw_multiple_line_text(img, product_sku, fonts, text_color, height*(4/10))
        #     code = self.createbarcode(product_sku)
        #     code = code.resize((int(width/3),int(height/4)))
        #     img.paste(code,(int(width*(1/3)),int(height*(1/2))))
        #     subloop = int(row['Line Item Quantity'])
        #     for copy in range(subloop): image_list.append(img.convert('RGB'))
    
    def Durian_crate(self,df):     #4
        Durian_ID = [7576,7562,7564,8140,8216]    #กล่อง ,ลังเล็ก, ลังใหญ่, ก้านยาวกล่องเดี่ยว, ภูเขาไฟกล่องเดียว
        boxshare = [24,12]          #ลังใหญ่ ,ลังเล็ก
        durianDF = df.loc[df['Product ID'].isin(Durian_ID)]
        sumbox = 0
        width = 1240
        height = 1754
        font = ImageFont.truetype(self.font, size=90)
        for index, row in durianDF.iterrows():
            if row['Product ID'] == Durian_ID[2]: sumbox += 24*int(row['Line Item Quantity'])
            elif row['Product ID'] == Durian_ID[1]: sumbox += 12*int(row['Line Item Quantity'])
            else: sumbox += 1*int(row['Line Item Quantity'])
        box = { 'big':int(sumbox/boxshare[0]),
                'small':int((sumbox%boxshare[0])/boxshare[1]),
                'single':int((sumbox%boxshare[0])%boxshare[1])}
        img = PIL.Image.new('RGB', (width, height), color='white')
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
        width = 4*100
        height = 4*75
        image_list = []
        font = ImageFont.truetype(os.path.join("Phase1","src","Kanit-Medium.ttf"), size=90)
        logo = Image.open(os.path.join("Phase1","src","LogoBW.png"))
        for i in range(int(Max)):
            num = str(i+1)
            while len(num)<3:
                num = f"0{num}"
            img = PIL.Image.new('RGB', (width, height), color='white')
            imgDraw = ImageDraw.Draw(img)
            textWidth, textHeight = imgDraw.textsize(num, font=font)
            xText = (width - textWidth) / 2
            yText = (height - textHeight) / 2
            imgDraw.text((xText, yText), num, font=font, fill=(0, 0, 0))
            img.paste(logo,(int(width/2.7),50))
            image_list.append(img.convert('RGB'))
        image_list[0].save('Amount_pages.pdf', save_all=True, append_images=image_list[1:])
        print("Amount Complete")
    
    def ExportDupCSV(self,df,dfPath):   #6
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
                col_one_list = list(set(df['Product Categories'].tolist()))
                # print(col_one_list)
                # col_one_list = col_one_list.sort()1
                elements = []
                # print(col_one_list)
                for i in col_one_list:
                    print(i)
                    rslt_df = df.loc[df['Product Categories'] == i]
                    rslt_df = rslt_df.sort_values(by=['Product ID'])
                    ListOfList = [list(rslt_df.columns)] + rslt_df.values.tolist()
                    # doc = SimpleDocTemplate(pdfPath, pagesize=A4)
                    doc = SimpleDocTemplate(pdfPath,pagesize=A4,
                        rightMargin=18,leftMargin=18,
                        topMargin=18,bottomMargin=18)
                    # styleSheet = getSampleStyleSheet()
                    data = ListOfList
                    pdfmetrics.registerFont(TTFont('THSarabunNew', 'THSarabunNew.ttf'))
                    t=Table(data,style = [('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                        ('FONT', (0,0), (-1,-1),('THSarabunNew')),
                                        ('FONTSIZE', (0,0), (-1,-1),14)
                                        ])
                    
                    elements.append(t)
                    elements.append(PageBreak())
                doc.build(elements) 
        except :
            pass
    
    def Customer_product(self,newdf):     #7
        # newdf = self.ExportByCustomerTable
        order_id = set(newdf['No.'].tolist())
        fonts = ImageFont.truetype(self.font, size=120)
        image_list = []
        text_color = (0,0,0)   #black
        width = 1240 
        height = 1754 
        for order in order_id:
            barcode_order = self.createbarcode(str(order)).resize((int(width/1.5),int(height/7)))
            barcode_EOF = self.createbarcode("EOF").resize((int(width/3),int(height/9)))
            barcode_zero = self.createbarcode("0").resize((int(width/3),int(height/9)))
            customer_name = set(newdf.loc[newdf['No.']==order]['Customer Name'].tolist()).pop()
            img = PIL.Image.new('RGB', (width, height), color='white')
            ImageDraw.Draw(img)       
            self.draw_multiple_line_text(img, f"No.  {str(order)}", fonts, text_color, height*(4/10))
            self.draw_multiple_line_text(img, customer_name, fonts, text_color, height*(5.5/10))
            img.paste(barcode_order,(int(width*(1/6)),int(height*(2/10))))
            img.paste(barcode_EOF,(int(width*(1/6)),int(height*(8/10))))
            img.paste(barcode_zero,(int(width*(3/6)),int(height*(8/10))))
            image_list.append(img.convert('RGB'))
        image_list[0].save('Customer_pages.pdf', save_all=True, append_images=image_list[1:])
        print('Customer page complete')