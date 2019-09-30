### MODULES
import PyPDF2



# CONSTANTS
PT_TO_MM = 0.352778



### INTRO

separator = "\n" + "#"*20 + "\n"

print(separator)
print("Welcome to the Print PDF Aligner!")
print()
print("This app helps you correct the misalignent that occurs in recto-verso printing by slightly moving the PDF pages.")
print()
print("(To exit anytime, press CTRL+C)")
print(separator)
print("Important note:")
print("This software has some problems with PDF with complex filenames.\nPlease rename your PDF with only lowercase characters (a-z) before use.\nSorry for the inconvenience.")
print(separator)



### GETTING VARIABLES

pdf_i_path  = input("Insert the path of the PDF to be aligned and press ENTER \n(you can drag the file inside this window)\n: ")
print()

side = input("Insert the side to move and press ENTER [0: front, 1: back]\n: ")
print()

print("||  You're about to insert the offset values.")
print("||  Remember that:")
print("||  • a POSITIVE value moves the page RIGHT (X) or UP   (Y)")
print("||  • a NEGATIVE value moves the page LEFT  (X) or DOWN (Y)")
print()

dx = input("Insert the X offset [in millimeters] and press ENTER\n: ")
print()

dy = input("Insert the Y offset [in millimeters] and press ENTER\n: ")
print(separator)
print("Working...")



### CONVERTING VARIABLES
pdf_i_path = pdf_i_path.strip()
side = int(side)
dx = float(dx)
dy = float(dy)



### INSTRUCTIONS

# Converting dx and dy in DEFAULT USER SPACE UNITS (pt)
dx = dx / PT_TO_MM
dy = dy / PT_TO_MM

# Reading pdf input
pdf_i = PyPDF2.PdfFileReader(pdf_i_path)

# Getting page size
# Here assuming that all the pages have same size
page_box = pdf_i.getPage(0).cropBox
page_wdt = page_box.getWidth()
page_hgt = page_box.getHeight()


# Initializing writer
pdf_writer = PyPDF2.PdfFileWriter()

# Iterating over all pdf pages and translating
for i in range(pdf_i.getNumPages()):

    # Getting reference to the page
    page_i = pdf_i.getPage(i)

    # If the page matches the selected side, we translate it:
    if i%2==side:
        # To translate the page, we actually create an empty one with the same size
        page_new = PyPDF2.pdf.PageObject.createBlankPage(pdf=None, width=page_wdt, height=page_hgt)
        # And then we overlay the original one, translated
        page_new.mergeTranslatedPage(page2=page_i, tx=dx, ty=dy, expand=False)
        pdf_writer.addPage(page_new)

    # Otherwise we leave it as it is
    else:
        pdf_writer.addPage(page_i)

# Getting file path
pdf_o_path = pdf_i_path.split(".")[0] + "-ppa.pdf"

# Writing the pdf
with open(pdf_o_path, 'wb') as f:
        pdf_writer.write(f)

print(separator)
print("Done!")
print("The fixed PDF has been saved next to the original one:")
print(pdf_o_path)
print(separator)