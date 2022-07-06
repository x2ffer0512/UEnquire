from django.http import HttpResponse, JsonResponse
#reports import
import datetime
import xlwt
import xlsxwriter
from xlwt import *
from xlsxwriter.workbook import Workbook
import xlrd
import io

# ==================================================================================
	# EXPORT EXCEL FILES 
def excel_dl(table):
	# @login_required(login_url='Home')
	# def export_transaction_excel(request):
	output = io.BytesIO()
	workbook = xlsxwriter.Workbook(output, {'in_memory': True})
	worksheet = workbook.add_worksheet("Tweets")
	bold = workbook.add_format({'bold': True})

	# Some data we want to write to the worksheet.
	report = table.objects.all() #my model
	# Start from the first cell. Rows and columns are zero indexed.
	row = 1
	col = 0

	# Iterate over the data and write it out row by row.
	for val in report:
		worksheet.write(row, col, row)
		worksheet.write(row, col + 1, val.source)
		worksheet.write(row, col + 2, val.posts)
		worksheet.write(row, col + 3, val.likes)
		worksheet.write(row, col + 4, val.dates)
		worksheet.write(row, col + 5, val.time)
		worksheet.write(row, col + 6, val.tags)
		worksheet.write(row, col + 7, val.links)

		row += 1

	# HEADER TITLES 
	worksheet.write('A1', 'NUMBER', bold)
	worksheet.write('B1', 'SOURCE', bold)
	worksheet.write('C1', 'POSTS', bold)
	worksheet.write('D1', 'LIKES', bold)
	worksheet.write('E1', 'DATE CREATED', bold)
	worksheet.write('F1', 'TIME CREATED', bold)
	worksheet.write('G1', 'HASHTAGS', bold)
	worksheet.write('H1', 'LINKS', bold)

	workbook.close()

	output.seek(0)
	response = HttpResponse(output.read(), content_type="'application/vnd.ms-excel'")
	response['Content-Disposition']='attachment; filename=Tweets '+ \
	str(datetime.datetime.now())+'.xlsx'
	return response

	# EXPORT EXCEL FILES 
def excel_dl_intents(table):
	# @login_required(login_url='Home')
	# def export_transaction_excel(request):
	output = io.BytesIO()
	workbook = xlsxwriter.Workbook(output, {'in_memory': True})
	worksheet = workbook.add_worksheet("Tweets")
	bold = workbook.add_format({'bold': True})

	# Some data we want to write to the worksheet.
	report = table.objects.all() #my model
	# Start from the first cell. Rows and columns are zero indexed.
	row = 1
	col = 0

	# Iterate over the data and write it out row by row.
	for val in report:
		worksheet.write(row, col, row)
		worksheet.write(row, col + 1, val.source)
		worksheet.write(row, col + 2, val.posts)
		worksheet.write(row, col + 3, val.likes)
		worksheet.write(row, col + 4, val.dates)
		worksheet.write(row, col + 5, val.time)
		worksheet.write(row, col + 6, val.tags)
		worksheet.write(row, col + 7, val.links)

		row += 1

	# HEADER TITLES 
	worksheet.write('A1', 'NUMBER', bold)
	worksheet.write('B1', 'SOURCE', bold)
	worksheet.write('C1', 'POSTS', bold)
	worksheet.write('D1', 'LIKES', bold)
	worksheet.write('E1', 'DATE CREATED', bold)
	worksheet.write('F1', 'TIME CREATED', bold)
	worksheet.write('G1', 'HASHTAGS', bold)
	worksheet.write('H1', 'LINKS', bold)

	workbook.close()

	output.seek(0)
	response = HttpResponse(output.read(), content_type="'application/vnd.ms-excel'")
	response['Content-Disposition']='attachment; filename=Intents '+ \
	str(datetime.datetime.now())+'.xlsx'
	return response