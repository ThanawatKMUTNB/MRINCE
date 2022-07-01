##########################################################
import time
import pandas as pd
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter,A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.platypus import Image as ims
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

from datetime import date

from reportlab.platypus import Paragraph, SimpleDocTemplate, Table
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib import colors

import DataManager

today = date.today()
doc = SimpleDocTemplate("Invoic.pdf",pagesize=A4,
                        rightMargin=72,leftMargin=150,
                        topMargin=72,bottomMargin=18)
pdfmetrics.registerFont(TTFont('THSarabunNew', 'THSarabunNew.ttf'))

Story=[]
logo = "Phase1\src\logo-web.png"
paperHead = '<b>Invoic</b>'
noByDate = 'No '+str(today.strftime("%Y%m%d"))
DateToday = 'Date '+str(today.strftime("%d %B %Y"))
textExpH = 'Exporter...'
textImpH = 'Importer...'
textExp = ['1','2','3','4','5','6','7']
textImp = ['1','2','3','4','5','6','']

adressData = [[textExpH,textImpH]]
for i,s in zip(textExp,textImp):
    adressData.append(['    '+i,'   '+s])

t = Table(adressData,style = [  ('FONT', (0,0), (-1,-1),('THSarabunNew')),
                                ('FONTSIZE', (0,0), (-1,-1),12)
                                ],colWidths=[285,285])
df1 = pd.read_csv('Phase1\Order_Items_Export_-_2022-06-20.csv')
df2 = pd.read_csv('orders-2022-06-20-00-16-07.csv')
print(DataManager.dm.btn_Invoice(DataManager.dm,df2,df1))
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

doc.build(Story)
print('CP')
##########################################################
# from reportlab.lib import colors
# from reportlab.lib.pagesizes import LETTER, inch, portrait
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
# from reportlab.lib.styles import getSampleStyleSheet


# doc = SimpleDocTemplate("kkk.pdf", pagesize=LETTER, rightMargin=30,leftMargin=30, topMargin=30,bottomMargin=18)
# doc.pagesize = portrait(LETTER)
# elements = []


# data = [
#         ["Directory"],
#         ["AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA "],
#         ]


# style = TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
#                        ('TEXTCOLOR',(1,1),(-2,-2),colors.red),
#                        ('VALIGN',(0,0),(0,-1),'TOP'),
#                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
#                        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
#                        ])

# #Configure style and word wrap
# s = getSampleStyleSheet()
# s = s["BodyText"]
# s.wordWrap = 'CJK'
# data2 = [[Paragraph(cell, s) for cell in row] for row in data]
# t=Table(data2)
# # t.setStyle(style)


# #Send the data and build the file
# elements.append(t)
# doc.build(elements)
################################
# from pip.operations import freeze  

# modules = list(
#     map(lambda x: x.split('=='), freeze.freeze(local_only=True))
# )

###########################################3
# import os
# import pandas as pd
# import DataManager

# df = pd.read_csv('Phase1\Order_Items_Export_-_2022-06-20.csv')
# # DataManager.dm.splitPageByProduct(DataManager.dm,df)

# df = pd.read_csv('orders-2022-06-20-00-16-07.csv')
# # x = DataManager.dm.dfSum(df)
# # print(df.loc[df['Product Name']=='ปังสังขยา ตรา ชฎา (300 กรัม)'])
# # print(len(x)) ,'Desktop\kkk.csv'

# x = DataManager.dm.new_Durian_crate_PDF(DataManager.dm,df,'')
# # print(x)

# # fileName = os.path.basename('Phase1\Order_Items_Export_-_2022-06-20.csv')
# # fileNameF = fileName.split("_")[0]
# # print(fileNameF)
#######################3

# from reportlab.lib import colors
# from reportlab.lib.pagesizes import letter, inch
# from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Table
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.platypus import PageBreak
# from reportlab.lib.pagesizes import A4

# doc = SimpleDocTemplate("complex_cell_values.pdf", pagesize=A4)
# elements = []
# styleSheet = getSampleStyleSheet()
# I = Image('Phase1\src\logo-web.png')
# I.drawHeight = 1.25*inch*I.drawHeight / I.drawWidth
# I.drawWidth = 1.25*inch
# P0 = Paragraph('''
# A paragraph
# 1''',
# styleSheet["BodyText"])
# P = Paragraph(''' The ReportLab Left
# Logo
# Image''',
# styleSheet["BodyText"])
# data= [['A', 'B', 'C', "k", 'D'],
#         ['00', '01', '02', "k", '04'],
#         ['10', '11', '12', "k", '14'],
#         ['20', '21', '22', '23', '24'],
#         ['30', '31', '32', '33', '34']]

# # t=Table(data,style=[('GRID',(1,1),(-2,-2),1,colors.green),
# #             ('BOX',(0,0),(1,-1),2,colors.red),
# #             ('LINEABOVE',(1,2),(-2,2),1,colors.blue),
# #             ('LINEBEFORE',(2,1),(2,-2),1,colors.pink),
# #             ('BACKGROUND', (0, 0), (0, 1), colors.pink),
# #             ('BACKGROUND', (1, 1), (1, 2), colors.lavender),
# #             ('BACKGROUND', (2, 2), (2, 3), colors.orange),
# #             ('BOX',(0,0),(-1,-1),2,colors.black),
# #             ('GRID',(0,0),(-1,-1),0.5,colors.black),
# #             ('VALIGN',(3,0),(3,0),'BOTTOM'),
# #             ('BACKGROUND',(3,0),(3,0),colors.limegreen),
# #             ('BACKGROUND',(3,1),(3,1),colors.khaki),
# #             ('ALIGN',(3,1),(3,1),'CENTER'),
# #             ('BACKGROUND',(3,2),(3,2),colors.beige),
# #             ('ALIGN',(3,2),(3,2),'LEFT'),
# #         ])
# t=Table(data,style=[('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
#                     ('BOX', (0,0), (-1,-1), 0.25, colors.black),
#                     # ('SPAN', (0,0), (4,0))
#         ])
# # t=Table(data)
# t._argW[3]=1.5*inch
# elements.append(PageBreak())
# elements.append(t)
# elements.append(PageBreak())
# # write the document to disk
# doc.build(elements) 

############################################################################################

# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import A4

# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
# from reportlab.lib.units import inch

# # c = canvas.Canvas('myfile.pdf', pagesize=A4)

# doc = SimpleDocTemplate("form_letter.pdf",pagesize=A4,
#                         rightMargin=72,leftMargin=72,
#                         topMargin=72,bottomMargin=18)
# width, height = A4

# Story=[]

# logo = "Phase1\src\logo-web.png"

# im = Image(logo, 2.5*inch, 2*inch)
# Story.append(im)
# # c = canvas.Canvas("hello.pdf")
# doc.build(Story)
# # c.drawString(100,750,"Welcome to Reportlab!")
# # c.save()

#######################################################################################

# import DataManager
# DataManager.dm.createBarcodeSKU('1232')

#######################################################################################
# import pdfkit
# pdfkit.from_string("kkk","str.pdf")
# import pandas as pd
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_pdf import PdfPages
# import matplotlib as mpl
# import os
# mpl.font_manager.fontManager.addfont( os.path.join('Phase1','thsarabunnew-webfont.ttf'))
# mpl.rc('font', family='TH Sarabun New')
# df = pd.read_csv('Phase1\Order_Items_Export_-_2022-06-20.csv')

# fig, ax = plt.subplots(figsize=(30,6))
# ax.axis('tight')
# ax.axis('off')
# the_table = ax.table(cellText=df.values,colLabels=df.columns,loc='center')
# the_table.set_fontsize(40)
# the_table.scale(1,4)
# #https://stackoverflow.com/questions/4042192/reduce-left-and-right-margins-in-matplotlib-plot
# pp = PdfPages("20.pdf")
# pp.savefig(fig, bbox_inches='tight')
# pp.close()