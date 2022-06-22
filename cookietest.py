# from pip.operations import freeze  

# modules = list(
#     map(lambda x: x.split('=='), freeze.freeze(local_only=True))
# )

###########################################3
import pandas as pd
import DataManager

# df = pd.read_csv('Phase1\Order_Items_Export_-_2022-06-20.csv')
# DataManager.dm.splitPageByProduct(DataManager.dm,df)

df = pd.read_csv('L70_export_by_product.csv')
# x = DataManager.dm.dfSum(df)
print(df.loc[df['Product Name']=='ปังสังขยา ตรา ชฎา (300 กรัม)'])
# print(len(x))
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