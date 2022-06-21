# import pdfkit
# pdfkit.from_string("kkk","str.pdf")
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib as mpl
import os
mpl.font_manager.fontManager.addfont( os.path.join('Phase1','thsarabunnew-webfont.ttf'))
mpl.rc('font', family='TH Sarabun New')
df = pd.read_csv('Phase1\Order_Items_Export_-_2022-06-20.csv')

fig, ax = plt.subplots(figsize=(30,6))
ax.axis('tight')
ax.axis('off')
the_table = ax.table(cellText=df.values,colLabels=df.columns,loc='center')
the_table.set_fontsize(40)
the_table.scale(1,4)
#https://stackoverflow.com/questions/4042192/reduce-left-and-right-margins-in-matplotlib-plot
pp = PdfPages("20.pdf")
pp.savefig(fig, bbox_inches='tight')
pp.close()