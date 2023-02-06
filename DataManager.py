from datetime import date
from ntpath import join
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
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, PageBreak, PageTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus.frames import Frame
from reportlab.platypus import Image as ims
from functools import partial
from reportlab.platypus import Spacer
import xlsxwriter
class dm():
    def __init__(self):
        self.font = "src/Kanit-Light.ttf"
        
    def setdf(self,path):
        self.df = pd.read_csv(path)
        
    def sort(self):
        try:
            self.df = self.df.sort_values(by=['Product ID'])
            return self.df
        except :
            return self.df
        
    def dfSum(df):
        # try:
            # print("------///")
            cols = list(df.columns.values)
            # print(cols)
            df = df[['Product ID', 'Product Name', 'Line Item Quantity', 'Product SKU', 'Product Categories']]
            
            df1 = df.sort_values(by=['Product Name','Product ID'])
            # df1 = df.sort_values(by=['Product Name'])
            # print(len(df1))
            # print(df1)
            df1 = df1.drop(['Line Item Quantity'], axis=1)
            # print(len(df1))
            df1 = df1.drop_duplicates()
            # print(len(df1))
            # print(df1['Product ID'])
            df2 = df.groupby(['Product ID'], as_index=False)['Line Item Quantity'].sum()
            # print(len(df2))
            # print(df2)
            # print("------///")
            dfsum = pd.merge(df1,df2) 
            dfsum = dfsum[['Product ID', 'Product Name', 'Line Item Quantity', 'Product SKU', 'Product Categories']]
            # cols = list(dfsum.columns.values)
            # print(cols)
            return dfsum
        # except :
        #     return df
    
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
    
    def draw_multiple_line_text2(self,image, text, font, text_color, text_start_height,start_width):
        draw = ImageDraw.Draw(image)
        image_width, image_height = image.size
        y_text = text_start_height
        lines = textwrap.wrap(text, width=32)
        for line in lines:
            line_width, line_height = font.getsize(line)
            draw.text((start_width, y_text), 
                    line, font=font, fill=text_color)
            y_text += line_height
    
    def draw_multiple_line_text_barcode(self,image, text, font, text_color, text_start_height):
        draw = ImageDraw.Draw(image)
        image_width, image_height = image.size
        y_text = text_start_height
        lines = textwrap.wrap(text, width=40)
        for line in lines:
            line_width, line_height = font.getsize(line)
            draw.text(((image_width - line_width) / 1.3, y_text), 
                    line, font=font, fill=text_color)
            y_text += line_height

    def createBarcodeSKU(sku):
        str_to_num = str(sku)
        while len(str_to_num) <13:
            str_to_num = f"{str_to_num}0"
        code = EAN13(str_to_num,writer=ImageWriter())
        code.save('CustomerID')
        img =  Image.open('src\CustomerID.png')
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
        if num[:-1] == "697970012345":return "EOF"  #End of file
        num = num[:-1]
        while num[-1] != "0": num = num[:-1]
        num = num[:-1]      #detect trash digits
        chr_list = []
        alpha = textwrap.wrap(num[:-4],2)       #split digit for character
        for c in alpha: chr_list.append(str(chr(int(c))))   
        return str("".join(chr_list)+num[-4:])
    
        # def Barcode_Copy(self,df):     #1
            # width = 400
            # height = 600
            # fonts = ImageFont.truetype(self.font, size=25)
            # sku_font = ImageFont.truetype(self.font, size=40)
            # logo =  Image.open(os.path.join("src","logoB.png"))
            # image_list = []
            # df.sort_values(by=['Product Name'],inplace=True)
            # for index, row in df.iterrows():
            #     if not (row['Product SKU'][:2] == 'VB' or row['Product SKU'][:2] == 'FT'): continue
            #     product = row['Product Name']
            #     product_name = row['Product Name'].split('(')
            #     product_engname = product_name[-1].split(')')[-1]
            #     if len(product_name) > 2:
            #         product_name.pop()
            #         product_name = "".join(product_name)[:-2]
            #     else: product_name = product_name[0][:-1]
            #     product_weight = f"{re.findall('[0-9]+',product)[0]} กรัม"
            #     product_sku = row['Product SKU']
            #     img = PIL.Image.new('RGB', (width, height), color='white')
            #     ImageDraw.Draw(img)       
            #     text_color = (0,0,0)   #black
            #     btm_text = " ".join([product_weight,product_sku])
            #     product_name = product_name[:25] if len(product_name) > 25 else product_name
            #     code = self.createbarcode(product_sku)
            #     code = code.resize((int(width*1.2),int(height*(1/1.45))))
            #     logo = logo.resize((int(width/2),int(height*(1/8))))
            #     img.paste(logo,(int(width/4),1))
            #     img.paste(code,(-40,int(height*(1/5.5))))
            #     self.draw_multiple_line_text2(img, "www.mrince.com", fonts, text_color, height*(1/10),width/4)
            #     self.draw_multiple_line_text2(img, "PRODUCT OF THAILAND", fonts, text_color, height*(1.5/10),width/6)
            #     self.draw_multiple_line_text2(img, product_name, fonts, text_color, height*(8/10),width*0.05)
            #     self.draw_multiple_line_text2(img, product_engname, fonts, text_color, height*(8.5/10),width*0.05)
            #     self.draw_multiple_line_text2(img, btm_text, sku_font, text_color, height*(9/10),width*0.05)
            #     subloop = int(row['Line Item Quantity'])
            #     for copy in range(subloop): image_list.append(img.convert('RGB'))
            # image_list[0].save('Quantity_pages.pdf', save_all=True, append_images=image_list[1:])
            # print("Barcode Copy Complete")

    def Barcode_Copy(self,df):     #1
        width = 400
        height = 600
        fonts = ImageFont.truetype(self.font, size=25)
        bg = Image.open(os.path.join("src","Ince_bg.png"))
        image_list = []
        df.sort_values(by=['Product Name'],inplace=True)
        for index, row in df.iterrows():
            if not (row['Product SKU'][:2] == 'VB' or row['Product SKU'][:2] == 'FT'): continue
            product = row['Product Name']
            product_name = row['Product Name'].split('(')
            product_engname = product_name[-1].split(')')[-1]
            if len(product_name) > 2:
                product_name.pop()
                product_name = "".join(product_name)[:-2]
            else: product_name = product_name[0][:-1]
            product_weight = f"{re.findall('[0-9]+',product)[0]} g"
            product_sku = row['Product SKU']
            img = PIL.Image.new('RGB', (width, height), color='white')
            ImageDraw.Draw(img)       
            text_color = (0,0,0)   #black
            product_name = product_name[:25] if len(product_name) > 25 else product_name
            product_name = " ".join([product_name,product_weight])
            product_engname = product_engname[:25] if len(product_engname) > 25 else product_engname
            product_engname = " ".join([product_engname,product_sku])
            code = self.createbarcode(product_sku)
            code = code.resize((int(width*1.3),int(height*(2.3/6))))
            bg = bg.resize((int(width),int(height)))
            img.paste(code,(-60,int(height*(1/2.5))))
            img.paste(bg,(0,0),bg)
            self.draw_multiple_line_text2(img, product_name, fonts, text_color, height*(2.7/10),width*0.05)
            self.draw_multiple_line_text2(img, product_engname, fonts, text_color, height*(3.2/10),width*0.05)
            subloop = int(row['Line Item Quantity'])
            for copy in range(subloop): image_list.append(img.convert('RGB'))
        image_list[0].save('Quantity_pages.pdf', save_all=True, append_images=image_list[1:])
        print("Barcode Copy Complete")
    
    def Product_type(self,df):     #2
        logo =  Image.open(os.path.join("src","logo-web.png"))
        width = int(1240/2)
        height = int(1754/2)
        head_font = ImageFont.truetype(self.font, size=80)
        content_1_font = ImageFont.truetype(self.font, size=50)
        content_2_font = ImageFont.truetype(self.font, size=30)
        image_list = []
        for index, row in df.iterrows():
            img = PIL.Image.new('RGB', (width, height), color='white')
            ImageDraw.Draw(img)
            text_color = (0,0,0)
            self.draw_multiple_line_text(img, row['Product SKU'], head_font, text_color, 200)
            self.draw_multiple_line_text(img, f"{re.findall('[0-9]+',row['Product Name'])[0]}  กรัม/แพ็ค", content_1_font, text_color, 350)
            self.draw_multiple_line_text(img, f"{row['Product Name']}     {row['Product Categories']}", content_2_font, text_color, 500)
            self.draw_multiple_line_text(img, str(row['Line Item Quantity']), head_font, text_color, 600)
            self.draw_multiple_line_text(img, "แพ็ค", content_1_font, text_color, 700)
            img.paste(logo,(int(width/3.3),20))
            image_list.append(img.convert('RGB'))

        image_list[0].save('Product_pages.pdf', save_all=True, append_images=image_list[1:])
        print("Product type Complete")

        # def Product_label(self,df):    #3 filter veg and fruits
            # width = 400
            # height = 600
            # fonts = ImageFont.truetype(self.font, size=25)
            # sku_font = ImageFont.truetype(self.font, size=40)
            # logo =  Image.open(os.path.join("src","logoB.png"))
            # image_list = []
            # df.sort_values(by=['Product Name'],inplace=True)
            # for index, row in df.iterrows():
            #     if (row['Product SKU'][:2] == 'VB' or row['Product SKU'][:2] == 'FT'): continue
            #     product = row['Product Name']
            #     product_name = row['Product Name'].split('(')
            #     product_engname = product_name[-1].split(')')[-1]
            #     if len(product_name) > 2:
            #         product_name.pop()
            #         product_name = "".join(product_name)[:-2]
            #     else: product_name = product_name[0][:-1]
            #     product_weight = f"{re.findall('[0-9]+',product)[0]} กรัม"
            #     product_sku = row['Product SKU']
            #     img = PIL.Image.new('RGB', (width, height), color='white')
            #     ImageDraw.Draw(img)       
            #     text_color = (0,0,0)   #black
            #     btm_text = " ".join([product_weight,product_sku])
            #     product_name = product_name[:25] if len(product_name) > 25 else product_name
            #     code = self.createbarcode(product_sku)
            #     code = code.resize((int(width*1.2),int(height*(1/1.45))))
            #     logo = logo.resize((int(width/2),int(height*(1/8))))
            #     img.paste(logo,(int(width/4),1))
            #     img.paste(code,(-40,int(height*(1/5.5))))
            #     self.draw_multiple_line_text2(img, "www.mrince.com", fonts, text_color, height*(1/10),width/4)
            #     self.draw_multiple_line_text2(img, "PRODUCT OF THAILAND", fonts, text_color, height*(1.5/10),width/6)
            #     self.draw_multiple_line_text2(img, product_name, fonts, text_color, height*(8/10),width*0.05)
            #     self.draw_multiple_line_text2(img, product_engname, fonts, text_color, height*(8.5/10),width*0.05)
            #     self.draw_multiple_line_text2(img, btm_text, sku_font, text_color, height*(9/10),width*0.05)
            #     subloop = int(row['Line Item Quantity'])
            #     for copy in range(subloop): image_list.append(img.convert('RGB'))
            # image_list[0].save('FoodBarcode_pages.pdf', save_all=True, append_images=image_list[1:])
            # print("Food Barcode Complete")
    
    def Product_label(self,df):    #3 filter veg and fruits
        width = 400
        height = 600
        fonts = ImageFont.truetype(self.font, size=25)
        bg = Image.open(os.path.join("src","Ince_bg.png"))
        image_list = []
        df.sort_values(by=['Product Name'],inplace=True)
        for index, row in df.iterrows():
            if (row['Product SKU'][:2] == 'VB' or row['Product SKU'][:2] == 'FT'): continue
            product = row['Product Name']
            product_name = row['Product Name'].split('(')
            product_engname = product_name[-1].split(')')[-1]
            if len(product_name) > 2:
                product_name.pop()
                product_name = "".join(product_name)[:-2]
            else: product_name = product_name[0][:-1]
            product_weight = f"{re.findall('[0-9]+',product)[0]} g"
            product_sku = row['Product SKU']
            img = PIL.Image.new('RGB', (width, height), color='white')
            ImageDraw.Draw(img)       
            text_color = (0,0,0)   #black
            product_name = product_name[:25] if len(product_name) > 25 else product_name
            product_name = " ".join([product_name,product_weight])
            product_engname = product_engname[:25] if len(product_engname) > 25 else product_engname
            product_engname = " ".join([product_engname,product_sku])
            code = self.createbarcode(product_sku)
            code = code.resize((int(width*1.3),int(height*(2.3/6))))
            bg = bg.resize((int(width),int(height)))
            img.paste(code,(-60,int(height*(1/2.5))))
            img.paste(bg,(0,0),bg)
            self.draw_multiple_line_text2(img, product_name, fonts, text_color, height*(2.7/10),width*0.05)
            self.draw_multiple_line_text2(img, product_engname, fonts, text_color, height*(3.2/10),width*0.05)
            subloop = int(row['Line Item Quantity'])
            for copy in range(subloop): image_list.append(img.convert('RGB'))
        image_list[0].save('FoodBarcode_pages.pdf', save_all=True, append_images=image_list[1:])
        print("Food Barcode Complete")
    
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
    
    def new_Durian_crate(self,newdf):
        Customer_df = newdf
        Durian_SKU = ['FT0011','FT0012','FT0015','FT0035','FT0480']   #ลังใหญ่, ลังเล็ก, กล่อง, ภูเขาไฟกล่องเดียว, ก้านยาวกล่องเดี่ยว
        
        print(Customer_df)
        
        Customer_durian_df = Customer_df.loc[Customer_df['Item Code'].isin(Durian_SKU)][['No.','Customer Name','Item Code','Item Name','Item Qty']]
        for index, row in Customer_durian_df.iterrows():
            if row['Item Code'] == 'FT0012': Customer_durian_df.loc[index,'total'] = str(24*int(row['Item Qty']))
            elif row['Item Code'] == 'FT0011': Customer_durian_df.loc[index,'total'] = str(12*int(row['Item Qty']))
            else: Customer_durian_df.loc[index,'total'] = str(int(row['Item Qty']))
        # print(Customer_durian_df)
        Customer_durian_df = Customer_durian_df.sort_values(by=['Item Code'])
        # print(Customer_durian_df)
        # print(type(Customer_durian_df))
        
        # Customer_durian_df = Customer_durian_df.sort_values(by=['Item Code'])

        # df_list = []
        # for item_code in Durian_SKU:
        #     df_list.append(Customer_durian_df.loc[Customer_durian_df['Item Code'].isin([item_code])])

        # col_one_list = list(set(Customer_durian_df['Item Code'].tolist())) 
        # print(col_one_list,Durian_SKU)
        return Customer_durian_df
    
    def new_Durian_crate_PDF(self,df,dfPath):
        # try:
            dfFT = self.new_Durian_crate(df)
            # self.ExportByProductPath = dfPath
            fileName = os.path.basename(dfPath)
            fileNameF = fileName.split("_")[0]
            # ['FT0011','FT0012','FT0015','FT0025','FT0035','FT0480'] 
                
            file_location = dfPath
            # print(file_location)
            file_name = os.path.basename(file_location)
            
            pdfPath = file_name.replace(".csv",".pdf")
            
            # col_one_list = list(set(dfFT['Item Code'].tolist()))
            # print(col_one_list)
            # col_one_list = col_one_list.sort()1
            
            doc = SimpleDocTemplate('Durian Order_'+pdfPath,pagesize=A4,
                    rightMargin=20,leftMargin=20,
                    topMargin=20,bottomMargin=20)
            
            elements = []
            
            ptext = [['รายการทุเรียน L...']]
            
            # s = getSampleStyleSheet()
            # s = s["BodyText"]
            # s.wordWrap = 'CJK'
            pdfmetrics.registerFont(TTFont('THSarabunNew', os.path.join('src','THSarabunNew.ttf')))
            style = ParagraphStyle(
                                    name='Normal_CENTER',
                                    fontName='THSarabunNew',
                                    alignment=TA_CENTER,
                                    fontSize=30,
                                    # spaceAfter = 15,
                                    leading = 40,
                                    )
            data2 = [[Paragraph(cell, style) for cell in row] for row in ptext]
            t=Table(data2)
            elements.append(t)
            
            Durian_SKU = ['FT0011','FT0012','FT0015','FT0035','FT0480']
            cr = ['#FF458F','#FF8352','#DEE500','#00E1DF','#00C3AF']
            pn = ['ทุเรียนแกะหมอนทอง (ลังเล็ก) (6000 กรัม)',
                  'ทุเรียนแกะหมอนทอง (ลังใหญ่) (12000 กรัม)',
                  'ทุเรียนกล่อง (เดี่ยว) (500 กรัม)',
                  'ทุเรียนภูเขาไฟ (500 กรัม)',
                  'ทุเรียนหมอนทองลูก (10000 กรัม)']
            strC = 65
            for i in range(5):
                rslt_df = dfFT.loc[dfFT['Item Code'] == Durian_SKU[i]]
                rslt_df = rslt_df.sort_values(by=['No.'])
                # print(list(rslt_df['No.']))
                # ItemName =rslt_df.loc[dfFT['Item Code'] == Durian_SKU[i], 'Item Name'].iloc[0]
                # print(df2)
                # ListOfList = [list(rslt_df.columns)] + rslt_df.values.tolist()
                ListOfList = rslt_df.values.tolist()
                style = getSampleStyleSheet()['Normal']

                data = [[chr(strC),
                         'Order no.',
                         str(pn[i])+'\n\n'+'รหัสสินค้า : '+str(Durian_SKU[i]),
                         'จำนวน']] 
                ListofNo = list(rslt_df['No.'])
                num = 1
                totalN = 0
                for j in ListofNo:
                    CuN =rslt_df.loc[dfFT['No.'] == j, 'Customer Name'].iloc[0]
                    ItQ =rslt_df.loc[dfFT['No.'] == j, 'Item Qty'].iloc[0]
                    totalN += ItQ
                    try:
                        if i == 0:
                            lineN = [num,j,CuN,str(ItQ)+'x12']
                        elif i == 1:
                            lineN = [num,j,CuN,str(ItQ)+'x24']
                        elif i == 4:
                            lineN = [num,j,CuN,str(ItQ)+'x10']
                        else:
                            lineN = [num,j,CuN,str(ItQ)]
                        num += 1
                        data.append(lineN)
                    except :
                        pass
                if i == 0:
                    lastSum = totalN*12
                    data.append(['','','Total = '+str(totalN)+'x12'+' กล่อง',lastSum])
                elif i == 1:
                    lastSum = totalN*24
                    data.append(['','','Total = '+str(totalN)+'x24'+' กล่อง',lastSum])
                elif i == 4:
                    lastSum = totalN*24
                    data.append(['','','Total = '+str(totalN)+'x24'+' กล่อง',lastSum])
                else:
                    lastSum = totalN
                    data.append(['','','Total = '+str(totalN)+' กล่อง',lastSum])
                #+ ListOfList
                strC += 1
                
                # print(ListOfList)
                pdfmetrics.registerFont(TTFont('THSarabunNew', 'THSarabunNew.ttf'))
                t=Table(data,style = [  ('BACKGROUND', (2, 0), (-1,0), str(cr[i])),
                                        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                        ('FONT', (0,0), (-1,-1),('THSarabunNew')),
                                        ('FONTSIZE', (0,0), (-1,-1),20),
                                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                                        ("ALIGN", (0, 0), (0, 0), "CENTER"),
                                        ('FONTSIZE', (0, 0), (0, 0), 30)
                                        ],colWidths=[1*inch,1*inch,4*inch,1*inch], 
                                        rowHeights=[1*inch]+[0.5*inch]*(len(ListofNo)+1))
                elements.append(t)
            doc.build(elements) 
        # except :
        #     pass
        
    def Cover(self,Max):        #5
        width = 4*100
        height = 4*75
        image_list = []
        font = ImageFont.truetype(os.path.join("src","Kanit-Medium.ttf"), size=90)
        logo = Image.open(os.path.join("src","LogoBW.png"))
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
    
    def Cover_3Copy(self,Max):
        # width = 4*100
        # height = 4*75
        # image_list = []
        # font = ImageFont.truetype(os.path.join("src","Kanit-Medium.ttf"), size=90)
        # logo = Image.open(os.path.join("src","LogoBW.png"))
        # for i in range(int(Max)):
        #     num = str(i+1)
        #     while len(num)<3:
        #         num = f"0{num}"
        #     img = PIL.Image.new('RGB', (width, height), color='white')
        #     imgDraw = ImageDraw.Draw(img)
        #     textWidth, textHeight = imgDraw.textsize(num, font=font)
        #     xText = (width - textWidth) / 2
        #     yText = (height - textHeight) / 2
        #     for i in range(3):
        #         imgDraw.text((xText, yText), num, font=font, fill=(0, 0, 0))
        #         img.paste(logo,(int(width/2.7),50))
        #         image_list.append(img.convert('RGB'))
        # image_list[0].save('Amount3Copy_pages.pdf', save_all=True, append_images=image_list[1:])
        print("Amount Complete")
    
    def Order_label(self,customer_df):
        width = 5*90
        height = 5*60
        image_list = []
        no_fonts = ImageFont.truetype(os.path.join("src","Kanit-Medium.ttf"), size=80)
        name_fonts = ImageFont.truetype(os.path.join("src","Kanit-Medium.ttf"), size=40)
        #address_fonts = ImageFont.truetype(os.path.join("src","Kanit-Medium.ttf"), size=10)
        logo = Image.open(os.path.join("src","LogoBW.png"))
        #Max = int(input("Enter max number: "))
        order_id = {}
        for index, row in customer_df.iterrows():
            if not row['No.'] in order_id: order_id[row['No.']] = row['Customer Name']

        for no in order_id:
            customer_name = order_id[no]
            text_color = (0,0,0)
            barcode = self.createbarcode(str(no)).resize((int(width/2),int(height/4)))
            img = Image.new('RGB', (width, height), color='white')
            ImageDraw.Draw(img)
            self.draw_multiple_line_text(img, str(no), no_fonts, text_color, height*(1.1/10))
            self.draw_multiple_line_text(img, customer_name, name_fonts, text_color, height*(4.5/10))
            # self.draw_multiple_line_text2(img, "Exporter : Ince TH Trade Co.,Ltd 37/346 M.7 Klong2 KlongLoung Pathum Thani 12120", address_fonts, text_color, height*(6/10),width/8)
            # self.draw_multiple_line_text2(img, "Importer : Ince UK limited 7 Blackstock Road London N4 2JF", address_fonts, text_color, height*(6/10),width/1.8)
            #img.paste(logo,(int(width/2.7),7))
            img.paste(barcode,(int(width/4),int(height/1.5)))    
            for copy in range(3): image_list.append(img.convert('RGB'))
        image_list[0].save('OrderLabel_pages.pdf', save_all=True, append_images=image_list[1:])
        print("OrderLabel Complete")
    
    def ExportDupCSV(self,df,dfPath):   #6
        cols = list(df.columns.values)
        if cols == ['Product ID', 'Product Name', 'Line Item Quantity', 'Product SKU', 'Product Categories']:
            pdfPath = dfPath
            col_one_list = list(set(df['Product Categories'].tolist()))
            elements = []
            for i in col_one_list:
                rslt_df = df.loc[df['Product Categories'] == i]
                rslt_df = rslt_df.sort_values(by=['Product ID'])
                ListOfList = [list(rslt_df.columns)] + rslt_df.values.tolist()
                doc = SimpleDocTemplate(pdfPath,pagesize=A4,
                    rightMargin=18,leftMargin=18,
                    topMargin=18,bottomMargin=18)
                # styleSheet = getSampleStyleSheet()
                data = ListOfList
                pdfmetrics.registerFont(TTFont('THSarabunNew', os.path.join('src','THSarabunNew.ttf')))
                t=Table(data,style = [('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                    ('FONT', (0,0), (-1,-1),('THSarabunNew')),
                                    ('FONTSIZE', (0,0), (-1,-1),14)
                                    ])
                elements.append(t)
                elements.append(PageBreak())
            doc.build(elements)
    
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
    
    # def unitPrice(self,customer_df):
    #     product_price = {}
    #     for index,row in customer_df[['Item Code','Item Price']].drop_duplicates(keep='first').iterrows(): 
    #         product_price[row['Item Code']] = row['Item Price']
    #     return product_price
    
    def btn_Invoice(self,product_df,customer_df):      #total USD
        use_df = product_df[['Product SKU','Product Name','Line Item Quantity','Product Categories']]
        # product_price = self.unitPrice(customer_df)
        product_price = {}
        for index,row in customer_df[['Item Code','Item Price']].drop_duplicates(keep='first').iterrows(): 
            product_price[row['Item Code']] = row['Item Price']
            
        for index, row in use_df.iterrows():    #calculate weight
            net_weight = str((int(re.findall('[0-9]+',row['Product Name'])[0])/1000)*int(row['Line Item Quantity']))  #Kg
            if len(net_weight.split('.')[-1]) >1:
                #net_weight = "".join(net_weight.split('.')[0]+'.'+net_weight.split('.')[-1][0])
                net_weight = format(float(net_weight),'.2f')
            price = product_price[row['Product SKU']] 
            product_name = row['Product Name']#.split('(')
            # if len(product_name) > 2:
            #     product_name.pop()
            #     product_name = "".join(product_name)[:-2]
            # else: product_name = product_name[0][:-1]
            use_df.loc[index,'Product Name'] = str(product_name)
            #use_df.loc[index,'Product Name'] = str(row['Product Name'].split('(')[0])
            use_df.loc[index,'N.W. (kg)'] = float(net_weight)
            use_df.loc[index,'Unit Price (USD)'] = round(price - 0.3 * price, 2)
            # use_df.loc[index,'Total (USD)'] = format(float(net_weight)*price,'.2f')
            use_df.loc[index,'Total (USD)'] = format(float(net_weight)*(price-(0.3*price)),'.2f')
        
        use_df[['Total (USD)']] = use_df[['Total (USD)']].astype(float)
        use_df = use_df.groupby(['Product SKU','Product Name','Product Categories',"Unit Price (USD)"]).sum().reset_index()

        categories = list(set(use_df['Product Categories'].values.tolist()))
        df_dict = {}
        for product in categories:
            new_df = use_df.loc[use_df['Product Categories']==product][['Product SKU','Product Name','N.W. (kg)','Unit Price (USD)','Total (USD)']].sort_values('Product SKU')
            new_df.rename(columns={'Product SKU':'Code'},inplace=True)
            numlist = []
            for n in range(len(new_df.index)): numlist.append(n+1)
            new_df.insert(0,'No',numlist)
            df_dict[product] = new_df.values.tolist()
        return df_dict
    
    def btn_fob_Invoice(self,product_df,customer_df):      #total USD
        use_df = product_df[['Product SKU','Product Name','Line Item Quantity','Product Categories']]
        # product_price = self.unitPrice(customer_df)
        product_price = {}
        for index,row in customer_df[['Item Code','Item Price']].drop_duplicates(keep='first').iterrows(): 
            product_price[row['Item Code']] = row['Item Price']
            
        for index, row in use_df.iterrows():    #calculate weight
            net_weight = str((int(re.findall('[0-9]+',row['Product Name'])[0])/1000)*int(row['Line Item Quantity']))  #Kg
            if len(net_weight.split('.')[-1]) >1:
                #net_weight = "".join(net_weight.split('.')[0]+'.'+net_weight.split('.')[-1][0])
                net_weight = format(float(net_weight),'.2f')
            price = product_price[row['Product SKU']] 
            product_name = row['Product Name']#.split('(')
            # if len(product_name) > 2:
            #     product_name.pop()
            #     product_name = "".join(product_name)[:-2]
            # else: product_name = product_name[0][:-1]
            use_df.loc[index,'Product Name'] = str(product_name)
            #use_df.loc[index,'Product Name'] = str(row['Product Name'].split('(')[0])
            use_df.loc[index,'N.W. (kg)'] = float(net_weight)
            use_df.loc[index,'Unit Price (USD)'] = round(price, 2)
            # use_df.loc[index,'Total (USD)'] = format(float(net_weight)*price,'.2f')
            use_df.loc[index,'Total (USD)'] = format(float(net_weight)*(price),'.2f')
        # print(use_df.sort_values(by=['Product SKU']))
        # ddf = use_df[use_df.duplicated(["Product SKU","Product Name","Product Categories","Unit Price (USD)"])]
        # print(ddf.sort_values(by=['Product SKU']))
        # print(use_df)
        # print(use_df.dtypes)
        use_df[['Total (USD)']] = use_df[['Total (USD)']].astype(float)
        # print(use_df.dtypes)
        # use_df = use_df.groupby(['Product SKU','Product Name','Product Categories',"Unit Price (USD)"])["Line Item Quantity","N.W. (kg)",'Total (USD)'].transform('sum')
        use_df = use_df.groupby(['Product SKU','Product Name','Product Categories',"Unit Price (USD)"]).sum().reset_index()
        # print(use_df)
        
        categories = list(set(use_df['Product Categories'].values.tolist()))
        # print(use_df)
        df_dict = {}
        for product in categories:
            new_df = use_df.loc[use_df['Product Categories']==product][['Product SKU','Product Name','N.W. (kg)','Unit Price (USD)','Total (USD)']].sort_values('Product SKU')
            new_df.rename(columns={'Product SKU':'Code'},inplace=True)
            numlist = []
            for n in range(len(new_df.index)): numlist.append(n+1)
            new_df.insert(0,'No',numlist)
            df_dict[product] = new_df.values.tolist()
        return df_dict
        # print(len(use_df) , len(new_df))
        # print(new_df)
        # return use_df
    
    def FOBinvoiceExel(self,dfProduct,dfCustumer):
        today = date.today()
        workbook = xlsxwriter.Workbook('FOB_Invoice_'+str(today.strftime("%Y%m%d"))+'.xlsx')
        worksheet = workbook.add_worksheet()
        noByDate = 'No '+str(today.strftime("%Y%m%d"))
        DateToday = 'Date '+str(today.strftime("%d %B %Y"))
        textExpH = 'Exporter'
        textImpH = 'Importer'
        textExp = ['Ince TH Trade Co.,Ltd.',
                   '37/346 M.7 Klong2 KlongLoung',
                   'Pathum Thani 12120',
                   'Thailand',
                   'Tel. +66874940303',
                   'Email. Lyn@mrince.com',
                   'Tax Id. 013556214814']
        textImp = ['Ince UK limited',
                   '7 Blackstock Road London N4 2JF',
                   'United Kingdom',
                   'Tel. +447427267206',
                   'Email. Kemal@mrince.com',
                   'Tax Id. 08760604','']
        # s = "-"
        # s = s.join(list1)
        worksheet.write('D1', 'Invoice')
        worksheet.write('F2', noByDate)
        worksheet.write('F3', DateToday)
        worksheet.write('A4', textExpH)
        worksheet.write('F4', textImpH)
        worksheet.write('A5', "\n".join(textExp))
        worksheet.write('F5', "\n".join(textImp))
        dataDict = self.btn_fob_Invoice(dfProduct,dfCustumer)
        key_list = list(dataDict.keys())
        # print(sorted(key_list))
        Lstart = 7
        tableData = [['No','Code','Product Name','N.W. (kg)','Unit Price (USD)','Total (USD)']]
        worksheet.add_table('A'+str(Lstart)+':F'+str(Lstart), {'data': tableData, 'style': None,'header_row': False})
        Lstart += 1
        ttunSum = 0
        ttnwSum = 0
        for i in sorted(key_list):
            worksheet.merge_range('A'+str(Lstart)+':F'+str(Lstart), str(i))
            nwSum = 0
            unSum = 0
            for j in dataDict[i]:
                nwSum += float(j[-3])
                unSum += float(j[-1])
            ttnwSum += round(nwSum, 2)
            ttunSum += round(unSum, 2)
            dataWithSum = dataDict[i] + [[str(i)+" Total","","",str(round(nwSum, 2)),"",str(round(unSum, 2))]]
            for data in dataWithSum:
                worksheet.write_row(Lstart, 0, data) 
                Lstart += 1   
            worksheet.merge_range('A'+str(Lstart)+':C'+str(Lstart),str(i))
            Lstart += 1
        worksheet.merge_range('A'+str(Lstart)+':C'+str(Lstart), "Grand Total")
        worksheet.write('D'+str(Lstart), str(round(ttnwSum, 2)))
        worksheet.write('F'+str(Lstart), str(round(ttunSum, 2)))
        workbook.close()
        
    def CIFinvoiceExel(self,dfProduct,dfCustumer):
        today = date.today()
        workbook = xlsxwriter.Workbook('CIF_Invoice_'+str(today.strftime("%Y%m%d"))+'.xlsx')
 
        # The workbook object is then used to add new
        # worksheet via the add_worksheet() method.
        worksheet = workbook.add_worksheet()
        noByDate = 'No '+str(today.strftime("%Y%m%d"))
        DateToday = 'Date '+str(today.strftime("%d %B %Y"))
        textExpH = 'Exporter'
        textImpH = 'Importer'
        textExp = ['Ince TH Trade Co.,Ltd.',
                   '37/346 M.7 Klong2 KlongLoung',
                   'Pathum Thani 12120',
                   'Thailand',
                   'Tel. +66874940303',
                   'Email. Lyn@mrince.com',
                   'Tax Id. 013556214814']
        textImp = ['Ince UK limited',
                   '7 Blackstock Road London N4 2JF',
                   'United Kingdom',
                   'Tel. +447427267206',
                   'Email. Kemal@mrince.com',
                   'Tax Id. 08760604','']
        # s = "-"
        # s = s.join(list1)
        worksheet.write('D1', 'Invoice')
        worksheet.write('F2', noByDate)
        worksheet.write('F3', DateToday)
        worksheet.write('A4', textExpH)
        worksheet.write('F4', textImpH)
        worksheet.write('A5', "\n".join(textExp))
        worksheet.write('F5', "\n".join(textImp))
        dataDict = self.btn_Invoice(dfProduct,dfCustumer)
        key_list = list(dataDict.keys())
        # print(sorted(key_list))
        Lstart = 7
        tableData = [['No','Code','Product Name','N.W. (kg)','Unit Price (USD)','Total (USD)']]
        worksheet.add_table('A'+str(Lstart)+':F'+str(Lstart), {'data': tableData, 'style': None,'header_row': False})
        Lstart += 1
        ttunSum = 0
        ttnwSum = 0
        for i in sorted(key_list):
            worksheet.merge_range('A'+str(Lstart)+':F'+str(Lstart), str(i))
            nwSum = 0
            unSum = 0
            for j in dataDict[i]:
                nwSum += float(j[-3])
                unSum += float(j[-1])
            ttnwSum += round(nwSum, 2)
            ttunSum += round(unSum, 2)
            dataWithSum = dataDict[i] + [[str(i)+" Total","","",str(round(nwSum, 2)),"",str(round(unSum, 2))]]
            for data in dataWithSum:
                worksheet.write_row(Lstart, 0, data) 
                Lstart += 1   
            worksheet.merge_range('A'+str(Lstart)+':C'+str(Lstart),str(i))
            Lstart += 1
        worksheet.merge_range('A'+str(Lstart)+':C'+str(Lstart), "Grand Total")
        worksheet.write('D'+str(Lstart), str(round(ttnwSum, 2)))
        worksheet.write('F'+str(Lstart), str(round(ttunSum, 2)))
        workbook.close()
    
    def invoicePDF(self,dfProduct,dfCustumer):
        df1 = dfProduct
        df2 = dfCustumer
        today = date.today()
        doc = SimpleDocTemplate("Invoic_"+str(today.strftime("%Y%m%d"))+".pdf",pagesize=A4,
                                rightMargin=100,leftMargin=100,
                                topMargin=20,bottomMargin=20)
        pdfmetrics.registerFont(TTFont('THSarabunNew', 'THSarabunNew.ttf'))

        Story=[]
        logo = "src\logo-web.png"
        paperHead = '<b>Invoic</b>'
        noByDate = 'No '+str(today.strftime("%Y%m%d"))
        DateToday = 'Date '+str(today.strftime("%d %B %Y"))
        textExpH = 'Exporter'
        textImpH = 'Importer'
        textExp = ['Ince TH Trade Co.,Ltd.',
                   '37/346 M.7 Klong2 KlongLoung',
                   'Pathum Thani 12120',
                   'Thailand',
                   'Tel. +66874940303',
                   'Email. Lyn@mrince.com',
                   'Tax Id. 013556214814']
        textImp = ['Ince UK limited',
                   '7 Blackstock Road London N4 2JF',
                   'United Kingdom',
                   'Tel. +447427267206',
                   'Email. Kemal@mrince.com',
                   'Tax Id. 08760604','']

        adressData = [[textExpH,textImpH]]
        for i,s in zip(textExp,textImp):
            adressData.append(['    '+i,'   '+s])

        t = Table(adressData,style = [  ('FONT', (0,0), (-1,-1),('THSarabunNew')),
                                        ('FONTSIZE', (0,0), (-1,-1),12)
                                        ],colWidths=[250,250])
        im = ims(logo, 1*inch, 0.5*inch)
        Story.append(im)
        styles=getSampleStyleSheet()
        # styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
        styles.add(ParagraphStyle(name='Normal_CENTER',
                                parent=styles['Normal'],
                                fontName='THSarabunNew',
                                alignment=TA_CENTER,
                                fontSize=20,
                                leading=13,
                                textColor=colors.black,
                                borderPadding=0,
                                leftIndent=0,
                                rightIndent=0,
                                spaceAfter=0,
                                spaceBefore=0,
                                splitLongWords=True,
                                spaceShrinkage=0.05,
                                ))
        styles.add(ParagraphStyle(name='Normal_Right',
                                parent=styles['Normal'],
                                fontName='THSarabunNew',
                                alignment=TA_RIGHT,
                                fontSize=20,
                                leading=13,
                                textColor=colors.black,
                                borderPadding=0,
                                leftIndent=0,
                                rightIndent=0,
                                spaceAfter=0,
                                spaceBefore=0,
                                splitLongWords=True,
                                spaceShrinkage=0.05,
                                ))
        Story.append(Paragraph(paperHead, styles["Normal_CENTER"]))
        Story.append(Spacer(1, 12))

        Story.append(Paragraph(noByDate, styles["Normal_Right"]))
        Story.append(Spacer(1, 12))

        Story.append(Paragraph(DateToday, styles["Normal_Right"]))
        Story.append(Spacer(1, 12))

        Story.append(t)
        Story.append(Spacer(1, 12))

        dataDict = self.btn_Invoice(df1,df2)
        key_list = list(dataDict.keys())
        tableData = [['No','Code','Product Name','N.W. (kg)','Unit Price (USD)','Total (USD)']]
        td = Table(tableData,style = [  ('BACKGROUND', (0, 0), (-1,-1), '#D2D2D2'),
                                        ('FONT', (0,0), (-1,-1),('THSarabunNew')),
                                        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                        ('FONTSIZE', (0,0), (-1,-1),15),
                                        ("ALIGN", (0, 0), (0, 0), "CENTER"),
                                        ],colWidths=[0.5*inch,0.7*inch,2.5*inch,0.7*inch,1.2*inch,1.2*inch],
                                            rowHeights=0.4*inch)
        Story.append(td)
        for i in key_list:
            tableData = [[str(i),'','','','']]
            # tableData = tableData +[[str(i)]]
            tableData = tableData + dataDict[i]
            nwSum = 0
            totalSum = 0
            for j in dataDict[i]:
                nwSum += float(j[-3])
                totalSum += float(j[-1])
            # print(round(nwSum, 2),round(totalSum, 2))
            tableData = tableData + [[str(i)+' Total','','',round(nwSum, 2),'',round(totalSum, 2)]]
            td = Table(tableData,style = [  ('SPAN', (0,0), (-1,0)),
                                            ('SPAN', (0,-1), (2,-1)),
                                            ('BACKGROUND', (0,-1), (2,-1), '#D2D2D2'),
                                            ('BACKGROUND', (4,-1), (4,-1), '#D2D2D2'),
                                            ('FONT', (0,0), (-1,-1),('THSarabunNew')),
                                            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                            # ("ALIGN", (0, 0), (0, 0), "CENTER"),
                                            ('FONTSIZE', (0,0), (-1,-1),16)
                                            ],colWidths=[0.5*inch,0.7*inch,2.5*inch,0.7*inch,1.2*inch,1.2*inch],
                                            rowHeights=0.4*inch)
            Story.append(td)
        # Story.append(td)
        Story.append(Spacer(1, 12))

        doc.build(Story)
    
    def footer(self,canvas, doc, content):
        canvas.saveState()
        w, h = content.wrap(doc.width, doc.bottomMargin)
        # print(doc.bottomMargin)
        # print(type(doc.bottomMargin))
        
        content.drawOn(canvas, doc.leftMargin, h+20)
        canvas.restoreState()

    def header_and_footer(self,canvas, doc, footer_content):
        self.footer(canvas, doc, footer_content)
    
    def  packingSumExcel(self,dfProduct):
        today = date.today()
        workbook = xlsxwriter.Workbook("Packing_Summary_"+str(today.strftime("%Y%m%d"))+'.xlsx')
        worksheet = workbook.add_worksheet()
        noByDate = 'Ref No : '+str(today.strftime("%Y%m%d"))
        textExpH = 'Exporter'
        textImpH = 'Importer'
        textExp = ['Ince TH Trade Co.,Ltd.',
                   '37/346 M.7 Klong2 KlongLoung',
                   'Pathum Thani 12120',
                   'Thailand',
                   'Tel. +66874940303',
                   'Email. Lyn@mrince.com',
                   'Tax Id. 013556214814']
        textImp = ['Ince UK limited',
                   '7 Blackstock Road London N4 2JF',
                   'United Kingdom',
                   'Tel. +447427267206',
                   'Email. Kemal@mrince.com',
                   'Tax Id. 08760604','']
        worksheet.write('D1', 'Packing Summary')
        worksheet.write('F2', noByDate)
        worksheet.write('A3', textExpH)
        worksheet.write('F3', textImpH)
        worksheet.write('A4', "\n".join(textExp))
        worksheet.write('F4', "\n".join(textImp))
        
        Lstart = 6
        tableData = [['No','Code','Product Name','Quantity','Unit','N.W. (kg)']]
        worksheet.add_table('A'+str(Lstart)+':F'+str(Lstart), {'data': tableData, 'style': None,'header_row': False})
        Lstart += 1
        dataDict = self.btn_PackingSummary(dfProduct)
        key_list = list(dataDict.keys())
        ttnwSum = 0
        for i in sorted(key_list):
            worksheet.merge_range('A'+str(Lstart)+':F'+str(Lstart), str(i))
            nwSum = 0
            for j in dataDict[i]:
                nwSum += float(j[-1])
            dataWithSum = dataDict[i] + [[str(i)+" Weigh","","","","",str(round(nwSum, 2))]]
            for data in dataWithSum:
                worksheet.write_row(Lstart, 0, data) 
                Lstart += 1
            ttnwSum += round(nwSum, 2)
            worksheet.merge_range('A'+str(Lstart)+':E'+str(Lstart),str(i))
            Lstart += 1
        # worksheet.merge_range('A'+str(Lstart)+':E'+str(Lstart), "Grand Weigh")
        worksheet.write('E'+str(Lstart), "Product Weight (Kg)")
        worksheet.write('F'+str(Lstart), str(round(ttnwSum, 2)))
        worksheet.write('E'+str(Lstart+1), "Carton Weight (Kg)")
        worksheet.write('E'+str(Lstart+2), "Total Weight (Kg)")
        worksheet.write('E'+str(Lstart+3), "Vegetable")
        worksheet.write('E'+str(Lstart+4), "Fruit")
        worksheet.write('E'+str(Lstart+5), "Seasoning")
        worksheet.write('E'+str(Lstart+6), "Flower")
        worksheet.write('E'+str(Lstart+7), "Dried Food")
        worksheet.write('E'+str(Lstart+8), "Dessert")
        workbook.close()
    
    def  packingSumPDF(self,dfProduct):
        df1 = dfProduct
        
        today = date.today()
        doc = SimpleDocTemplate("Packing_Summary_"+str(today.strftime("%Y%m%d"))+".pdf",pagesize=A4,
                                rightMargin=100,leftMargin=100,
                                topMargin=20,bottomMargin=30)
        pdfmetrics.registerFont(TTFont('THSarabunNew', 'THSarabunNew.ttf'))

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Normal_LEFT',
                                parent=styles['Normal'],
                                fontName='THSarabunNew',
                                alignment=TA_LEFT,
                                fontSize=20,
                                leading=13,
                                textColor=colors.black,
                                borderPadding=0,
                                leftIndent=0,
                                rightIndent=0,
                                spaceAfter=0,
                                spaceBefore=0,
                                splitLongWords=True,
                                spaceShrinkage=0.05,
                                ))
        # footer_content = Paragraph("This is a footer. It goes on every page.  ", styles['Normal_LEFT'])
        # frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
        # template = PageTemplate(id='test', frames=frame, onPage=partial(self.header_and_footer, footer_content=footer_content))
        # doc.addPageTemplates([template])

        Story=[]
        logo = "src\logo-web.png"
        paperHead = '<b>Packing Summary</b>'
        noByDate = 'Ref No : '+str(today.strftime("%Y%m%d"))
        textExpH = 'Exporter'
        textImpH = 'Importer'
        textExp = ['Ince TH Trade Co.,Ltd.',
                   '37/346 M.7 Klong2 KlongLoung',
                   'Pathum Thani 12120',
                   'Thailand',
                   'Tel. +66874940303',
                   'Email. Lyn@mrince.com',
                   'Tax Id. 013556214814']
        textImp = ['Ince UK limited',
                   '7 Blackstock Road London N4 2JF',
                   'United Kingdom',
                   'Tel. +447427267206',
                   'Email. Kemal@mrince.com',
                   'Tax Id. 08760604','']

        adressData = [[textExpH,textImpH]]
        for i,s in zip(textExp,textImp):
            adressData.append(['    '+i,'   '+s])

        t = Table(adressData,style = [  ('FONT', (0,0), (-1,-1),('THSarabunNew')),
                                        ('FONTSIZE', (0,0), (-1,-1),12)
                                        ],colWidths=[250,250])
        im = ims(logo, 1*inch, 0.5*inch)
        Story.append(im)
        styles=getSampleStyleSheet()
        # styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
        styles.add(ParagraphStyle(name='Normal_CENTER',
                                parent=styles['Normal'],
                                fontName='THSarabunNew',
                                alignment=TA_CENTER,
                                fontSize=20,
                                leading=13,
                                textColor=colors.black,
                                borderPadding=0,
                                leftIndent=0,
                                rightIndent=0,
                                spaceAfter=0,
                                spaceBefore=0,
                                splitLongWords=True,
                                spaceShrinkage=0.05,
                                ))
        styles.add(ParagraphStyle(name='Normal_Right',
                                parent=styles['Normal'],
                                fontName='THSarabunNew',
                                alignment=TA_RIGHT,
                                fontSize=20,
                                leading=13,
                                textColor=colors.black,
                                borderPadding=0,
                                leftIndent=0,
                                rightIndent=0,
                                spaceAfter=0,
                                spaceBefore=0,
                                splitLongWords=True,
                                spaceShrinkage=0.05,
                                ))
        Story.append(Paragraph(paperHead, styles["Normal_CENTER"]))
        Story.append(Spacer(1, 12))

        Story.append(Paragraph(noByDate, styles["Normal_Right"]))
        Story.append(Spacer(1, 12))

        Story.append(t)
        Story.append(Spacer(1, 12))
        # print(df1)
        dataDict = self.btn_PackingSummary(df1)
        # print(dataDict)
        key_list = list(dataDict.keys())
        tableData = [['No','Code','Product Name','Quantity','Unit','N.W. (kg)']]
        td = Table(tableData,style = [  ('BACKGROUND', (0, 0), (-1,-1), '#D2D2D2'),
                                        ('FONT', (0,0), (-1,-1),('THSarabunNew')),
                                        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                        ('FONTSIZE', (0,0), (-1,-1),15),
                                        ("ALIGN", (0, 0), (0, 0), "CENTER"),
                                        ],colWidths=[0.5*inch,0.7*inch,2.5*inch,0.7*inch,1.2*inch,1.2*inch],
                                            rowHeights=0.4*inch)
        Story.append(td)
        for i in key_list:
            tableData = [[str(i),'','','','']]
            # tableData = tableData +[[str(i)]]
            tableData = tableData + dataDict[i]
            nwSum = 0
            for j in dataDict[i]:
                nwSum += float(j[-1])
            # print(round(nwSum, 2),round(totalSum, 2))
            tableData = tableData + [[str(i)+' Weigh','','','','',round(nwSum, 2)]]
            td = Table(tableData,style = [  ('SPAN', (0,0), (-1,0)),
                                            ('SPAN', (0,-1), (4,-1)),
                                            ('BACKGROUND', (0,-1), (4,-1), '#D2D2D2'),
                                            ('FONT', (0,0), (-1,-1),('THSarabunNew')),
                                            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                            # ("ALIGN", (0, 0), (0, 0), "CENTER"),
                                            ('FONTSIZE', (0,0), (-1,-1),16)
                                            ],colWidths=[0.5*inch,0.7*inch,2.5*inch,0.7*inch,1.2*inch,1.2*inch],
                                            rowHeights=0.4*inch)
            Story.append(td)
        # Story.append(td)
        Story.append(Spacer(1, 12))

        doc.build(Story)
    
    # def btn_PackingList(self,df):      #Packing
    #     use_df = df[['Product SKU','Product Name','Line Item Quantity','Product Categories']]
    #     for index, row in use_df.iterrows():    #calculate weight
    #         net_weight = str((int(re.findall('[0-9]+',row['Product Name'])[0])/1000)*int(row['Line Item Quantity']))  #Kg
    #         if len(net_weight.split('.')[-1]) >1:
    #             net_weight = "".join(net_weight.split('.')[0]+'.'+net_weight.split('.')[-1][0])
    #         use_df.loc[index,'Item'] = f"{row['Product SKU']} {row['Product Name'].split('(')[0]}"
    #         use_df.loc[index,'Packing'] = 'xxx'
    #         use_df.loc[index,'Net WT (Kg)'] = float(net_weight)
    #         use_df.loc[index,'Gross WT (Kg)'] = 1
    #         use_df.loc[index,'Volume (x1000 cc.)'] = float(net_weight)*2

    #     categories = list(set(use_df['Product Categories'].values.tolist()))
    #     df_dict = {}
    #     for product in categories:
    #         new_df = use_df.loc[use_df['Product Categories']==product].sort_values('Product SKU')
    #         new_df.rename(columns={'Line Item Quantity':'Cts'},inplace=True)
    #         numlist = []
    #         for n in range(len(new_df.index)): numlist.append(n+1)
    #         new_df.insert(0,'No',numlist)
    #         new_df.drop(['Product SKU','Product Name','Product Categories'],axis=1,inplace=True)
    #         cst_column = new_df.pop('Cts')
    #         new_df.insert(3,'Cts',cst_column)
    #         df_dict[product] = new_df.values.tolist()
    #     return df_dict

    def btn_PackingSummary(self,df):    #Unit
        use_df = df[['Product SKU','Product Name','Line Item Quantity','Product Categories']]
        product_unit = {'FT0011':'12Box','FT0012':'24Box','VB':'Pack','DFT':'Piece','FT':'Kg','Else':'Pack'}
        for index, row in use_df.iterrows():    #calculate weight
            net_weight = str((int(re.findall('[0-9]+',row['Product Name'])[0])/1000)*int(row['Line Item Quantity']))  #Kg
            if len(net_weight.split('.')[-1]) >1:
                #net_weight = "".join(net_weight.split('.')[0]+'.'+net_weight.split('.')[-1][0])
                net_weight = format(float(net_weight),'.2f')
            product_name = row['Product Name']#.split('(')
            # if len(product_name) > 2:
            #     product_name.pop()
            #     product_name = "".join(product_name)[:-2]
            # else: product_name = product_name[0][:-1]
            use_df.loc[index,'Product Name'] = str(product_name)
            #use_df.loc[index,'Product Name'] = str(row['Product Name'].split('(')[0])
            if row['Product SKU'] in product_unit:
                use_df.loc[index,'Unit'] = product_unit[row['Product SKU']]
            elif re.findall('[a-zA-Z]+',row['Product SKU'])[0] in product_unit:
                use_df.loc[index,'Unit'] = product_unit[re.findall('[a-zA-Z]+',row['Product SKU'])[0]]
            else:
                use_df.loc[index,'Unit'] = product_unit['Else']
            use_df.loc[index,'N.W. (kg)'] = float(net_weight)
        
        # print(len(use_df))
        use_df = use_df.groupby(['Product SKU','Product Name',"Product Categories","Unit"]).sum().reset_index()
        # print(use_df)
        categories = list(set(use_df['Product Categories'].values.tolist()))
        df_dict = {}
        for product in categories:
            new_df = use_df.loc[use_df['Product Categories']==product][['Product SKU','Product Name','Line Item Quantity','Unit','N.W. (kg)']].sort_values('Product SKU')
            new_df.rename(columns={'Product SKU':'Code','Line Item Quantity':'Quantity'},inplace=True)
            numlist = []
            for n in range(len(new_df.index)): numlist.append(n+1)
            new_df.insert(0,'No',numlist)
            df_dict[product] = new_df.values.tolist()
        
        # ddf = use_df[use_df.duplicated(["Product SKU","Product Name"])]
        # # print(len(use_df))
        # ddf = ddf.sort_values(by=['Product SKU'])
        # print(ddf)
        return df_dict
    