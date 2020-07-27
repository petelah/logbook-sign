from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime, timedelta
import os

start_date = datetime(2020, 6, 1)
end_date = datetime(2020, 12, 31)
current_date = start_date

time_now = datetime.now()

REP_BY = "Joe Smith"
LOCATION = "Somewhere Co."
SIGNATURE = "sample-signature.png"
P_DESC = "Nothing to report, CCTV checked."


def create_IR(date_thing):
	packet = io.BytesIO()
	# create a new PDF with Reportlab
	can = canvas.Canvas(packet, pagesize=A4, bottomup=1, pageCompression=1)
	can.drawString(150, 635, P_DESC)
	can.drawString(65, 765, time_now.strftime("%d/%m/%Y"))
	can.drawString(285, 765, LOCATION)
	can.drawString(450, 765, REP_BY)
	can.drawString(155, 765, time_now.strftime("%H:%M:%S"))
	can.drawString(492, 572, date_thing)
	can.drawImage(SIGNATURE, 375, 565, width=100, height=40, mask="auto")
	can.drawImage("tick.png", 100, 570, width=20, height=20, mask="auto")
	can.showPage()
	can.save()
	# move to the beginning of the StringIO buffer
	packet.seek(0)
	new_pdf = PdfFileReader(packet)
	# read your existing PDF
	existing_pdf = PdfFileReader(open("original.pdf", "rb"))
	output = PdfFileWriter()
	# add the "watermark" (which is the new pdf) on the existing page
	page = existing_pdf.getPage(0)
	page.mergePage(new_pdf.getPage(0))
	output.addPage(page)
	# finally, write "output" to a real file
	if not os.path.isdir("IR/" + current_date.strftime("%Y")):
		os.mkdir("IR/" + current_date.strftime("%Y"))
	if not os.path.isdir("IR/" + current_date.strftime("%Y") + "/" + current_date.strftime("%B")):
		os.mkdir("IR/" + current_date.strftime("%Y") + "/" + current_date.strftime("%B"))
	outputStream = open(
		"IR/" + current_date.strftime("%Y") + "/" + current_date.strftime("%B") + "/" + date_thing + ".pdf", "wb")
	output.write(outputStream)
	outputStream.close()


def batch_logbook(c_date, e_date):
	while c_date != e_date:
		create_IR(c_date.strftime("%d-%m-%Y"))
		c_date = current_date + timedelta(days=1)
