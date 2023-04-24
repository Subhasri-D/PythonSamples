import numpy as np
import pandas as pd
import itertools
from statistics import mean
from random import randint
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table

#Exception Handling
try:
    w, h = A4

    #File Handling
    # Open a CSV File using pandas
    openFile = pd.read_csv("PropertyDetails.csv", index_col=0)

    openFile = openFile.reset_index()

    # group by AVG price of properties in each location

    avgprice = openFile.groupby((['Location', 'PropertyType'])).agg(
        AveragePrice=('Price', 'mean'),
    ).reset_index()

    newfiles = np.array(avgprice)

    # AVG of bedrooms & bathrooms for each property
    avgbb = openFile.groupby(['PropertyType']).agg(
        AverageBedroom=('No. of Bedrooms', 'mean'),
        AverageBathroom=('No. of Bathrooms', 'mean')

    ).reset_index()

    # Total Average
    totavg = openFile.groupby(['PropertyType', 'Location']).agg(
        AveragePrice=('Price', 'mean'),
        AverageBedroom=('No. of Bedrooms', 'mean'),
        AverageBathroom=('No. of Bathrooms', 'mean'),
        Avgsf=('SQFT', 'mean')
    ).reset_index()

    # numpy
    FinalResult = np.array(totavg)

    # reportlab
    c = canvas.Canvas("Purchase Details.pdf")
    c.setFillColor('gray')
    c.setFont("Times-Roman", 12)
    max_rows_per_page = 45
    # Margin.
    x_offset = 50
    y_offset = 50
    # Space between rows.
    padding = 15

    xlist = [x + x_offset for x in [0, 120, 200, 260, 360, 450, 500]]
    ylist = [h - y_offset - i * padding for i in range(max_rows_per_page + 1)]

    rowgap = 0.6
    yaxis = 9.9

    data = [("PROPERTY_TYPE", "LOCATION", "PRICE", "BEDROOMS", "BATHROOMS", "SQFT")]
    #Combining Data into one set & Writing  data to the PDF
    for x in FinalResult:
        y = 0
        ptype, locate, price, bathroom, bedroom, sqft = y[0], y[1], int(y[2]), round(y[3]), round(y[4]), round(y[5])
        data.append((ptype, locate, price, bathroom, bedroom, sqft))
    def Combine(iterable, z):
        args = [iter(iterable)] * z
        return itertools.zip_longest(*args)

#Creating Grid to display the final data
    for rows in Combine(data, max_rows_per_page):
        rows = tuple(filter(bool, rows))
        c.grid(xlist, ylist[:len(rows) + 1])
        for y, row in zip(ylist[:-1], rows):
            for x, cell in zip(xlist, row):
                c.drawString(x + 2, y - padding + 3, str(cell))

    c.save()
except Exception as Ex:
    print(Ex)
