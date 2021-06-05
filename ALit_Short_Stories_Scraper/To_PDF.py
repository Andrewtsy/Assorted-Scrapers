import sqlite3
from fpdf import FPDF

# Connects to database
conn = sqlite3.connect('ALit_SS.sqlite')
cur = conn.cursor()
cur.execute('SELECT title, author, text from Pages')

# Set basic formatting
pdf = FPDF(format = 'A4')
pdf.add_page()
pdf.set_font('Times', size = 42)

pdf.cell(200, 32, txt = 'Assorted Short Stories to Tickle your Tummy', 
         ln = 1, align = 'C')

# Writes each page in
for i in cur.fetchall()[1:]:
    pdf.set_font('Times', size = 36)
    pdf.cell(200, 24, txt = i[0].encode('latin-1', 'replace').decode('latin-1'), ln = 1, align = 'C')
    pdf.set_font('Times', size = 24)
    pdf.cell(200, 18, txt = i[1].encode('latin-1', 'replace').decode('latin-1'), ln = 1, align = 'C')
    pdf.set_font('Times', size = 18)
    pdf.multi_cell(189, 13, txt = i[2].encode('latin-1', 'replace').decode('latin-1'))
    pdf.add_page()

pdf.output(dest = 'F', name = 'Short_Stories.pdf')