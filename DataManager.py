import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from barcode import EAN13
from barcode.writer import ImageWriter
import textwrap
import re
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QPushButton, QFileDialog, QVBoxLayout

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
        
    def dfSum(self):
        try:
            # print("------///")
            # cols = list(self.df.columns.values)
            # print(cols)
            self.df1 = self.df.sort_values(by=['Product ID'])
            self.df1 = self.df1.drop(['Line Item Quantity'], axis=1)
            self.df1 = self.df1.drop_duplicates()
            # print(len(self.df1))
            self.df2 = self.df.groupby(['Product ID'], as_index=False)['Line Item Quantity'].sum()
            # print(len(self.df2))
            
            # print("------///")
            self.dfsum = pd.merge(self.df1,self.df2) 
            self.dfsum = self.dfsum[['Product ID', 'Product Name', 'Line Item Quantity', 'Product SKU', 'Product Categories']]
            
            return self.dfsum
        except :
            return self.df
    
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
    
    def createbarcode(self,sku):
        num_list = []
        for c in re.findall('[a-zA-Z]+',sku)[0]: num_list.append(str(ord(c)))
        str_to_num = "".join(num_list) + "".join(re.findall('[0-9]+',sku))
        i=0
        while len(str_to_num) <13:
            str_to_num = f"{str_to_num}{i}"
            i+=1
        code = EAN13(str_to_num,writer=ImageWriter())
        code.save('Barcode_Copy')
        img = Image.open('Barcode_Copy.png')
        return img
    
    def readbarcode(self,num):
        num = num[:-1]
        while num[-1] != "0": num = num[:-1]
        num = num[:-1]      #detect trash digits
        chr_list = []
        alpha = textwrap.wrap(num[:-4],2)       #split digit for character
        for c in alpha: chr_list.append(str(chr(int(c))))   
        return str("".join(chr_list)+num[-4:])
    
    def Barcode_Copy(self):     #1
        width = 400
        height = 250
        fonts = ImageFont.truetype(self.font, size=20)
        image_list = []
        for index, row in self.df.iterrows():
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
    
    def Product_type(self):     #2
        logo = Image.open("/Phase1/src/logo-web.png")
        width = 1240
        height = 1754
        head_font = ImageFont.truetype(self.font, size=160)
        content_1_font = ImageFont.truetype(self.font, size=100)
        content_2_font = ImageFont.truetype(self.font, size=60)
        image_list = []
        for index, row in self.df.iterrows():
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
    
    def Durian_crate(self):     #4
        Durian_ID = [7576,7562,7564,8140,8216]    #กล่อง ,ลังเล็ก, ลังใหญ่, ก้านยาวกล่องเดี่ยว, ภูเขาไฟกล่องเดียว
        boxshare = [24,12]          #ลังใหญ่ ,ลังเล็ก
        durianDF = self.df.loc[self.df['Product ID'].isin(Durian_ID)]
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