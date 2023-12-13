import os
import subprocess
import sys

from fpdf import FPDF

PAGE_WIDTH = 48
PAGE_HEIGHT = 105

MARGIN = 5
TEXT_WIDTH = PAGE_WIDTH - 2 * MARGIN
TOLERANCE = 0.1

OUTPUT_FILENAME = "output.pdf"


def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    elif sys.platform == "darwin":
        subprocess.call(["open", filename])
    else:
        subprocess.call(["xdg-open", filename])


def create_pdf(user_text, outfile=OUTPUT_FILENAME):
    # Create instance of FPDF class
    pdf = FPDF(unit="mm", format=(PAGE_WIDTH, PAGE_HEIGHT))

    # Add a page
    pdf.add_page()

    # User input for font and text
    font_size = PAGE_WIDTH

    # Set font
    pdf.add_font("CyberwayRiders", "", os.path.abspath("CyberwayRiders.ttf"), True)
    pdf.set_font("CyberwayRiders", size=font_size)
    while True:
        width = pdf.get_string_width(user_text)
        if 0 <= (TEXT_WIDTH - width) < TOLERANCE or width < TOLERANCE:
            break
        font_size = font_size / width * TEXT_WIDTH
        pdf.set_font_size(font_size)

    # Add the user input text
    pdf.set_xy(MARGIN + font_size / 50, MARGIN + font_size / 8 + font_size / 50)
    pdf.set_text_color(192)
    pdf.cell(0, 0, user_text)
    pdf.set_xy(MARGIN, MARGIN + font_size / 8)
    pdf.set_text_color(0)
    pdf.cell(0, 0, user_text)

    pdf.image("2077.png", 20, 7 + font_size / 8 + font_size / 8, 20)

    # Save the pdf with name .pdf
    pdf.output(outfile)


if __name__ == "__main__":
    user_text = input("Enter message: ")
    outfile = sys.argv[1] if len(sys.argv) > 1 else OUTPUT_FILENAME
    create_pdf(user_text, outfile)
    open_file(outfile)
