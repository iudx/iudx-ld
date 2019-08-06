##############################################################################
#
# A simple example of merging cells with the XlsxWriter Python module.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter


# Create an new Excel file and add a worksheet.
workbook = xlsxwriter.Workbook('merge1.xlsx')
worksheet = workbook.add_worksheet()

# Increase the cell size of the merged cells to highlight the formatting.
#worksheet.set_column('B:D', 12)
#worksheet.set_row(3, 30)
#worksheet.set_row(6, 30)
#worksheet.set_row(7, 30)



worksheet.set_row(0,200)
worksheet.set_column(0,0,200)


workbook.close()
