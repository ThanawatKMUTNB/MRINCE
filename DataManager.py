import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
# import barcode
from barcode import Code128
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
        '''
        From unutbu on [python PIL draw multiline text on image](https://stackoverflow.com/a/7698300/395857)
        '''
        draw = ImageDraw.Draw(image)
        image_width, image_height = image.size
        y_text = text_start_height
        lines = textwrap.wrap(text, width=40)
        for line in lines:
            line_width, line_height = font.getsize(line)
            draw.text(((image_width - line_width) / 2, y_text), 
                    line, font=font, fill=text_color)
            y_text += line_height
    
    def Barcode_Copy(self):     #1
        width = 500
        height = 500
        fonts = ImageFont.truetype(self.font, size=30)
        image_list = []
        for index, row in self.df.iterrows():
            product_name = row['Product Name']
            product_sku = row['Product SKU']
            img = Image.new('RGB', (width, height), color='white')
            imgDraw = ImageDraw.Draw(img)       
            text_color = (0,0,0)   #black
            text_start_height = 110
            self.draw_multiple_line_text(img, product_name, fonts, text_color, text_start_height)
            code = Code128(product_sku, writer=ImageWriter())
            code.save("barcode")
            code = Image.open("barcode.png")
            code = code.resize((int(width/4),int(height/4)))
            img.paste(code,(int(width/2),int(height/2.5)))
            subloop = int(row['Line Item Quantity'])
            for copy in range(subloop):
                image_list.append(img.convert('RGB'))

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
            imgDraw = ImageDraw.Draw(img)
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
    
    #3
    
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
        imgDraw = ImageDraw.Draw(img)
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