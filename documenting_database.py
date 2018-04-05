import psycopg2
import webbrowser
import time
from fpdf import FPDF
 
#db connection
try:
    conn = psycopg2.connect("dbname='iophub_internal' user='postgres' host='localhost' password='postgres'")
    print('Connected successfully \n\n')
except:
    print("Unable to connect to the database")
 
#find all table names
cur = conn.cursor()
cur.execute(""" SELECT DISTINCT table_name FROM information_schema.tables WHERE table_schema = 'iophub' """)
tables = cur.fetchall()
 
d = time.strftime("%Y-%m-%d_%H-%M-%S")
pre_file_name = 'db_'+str(d)
html_file = pre_file_name+'.html'
text_file = pre_file_name+'.txt'
pdf_file = pre_file_name+'.pdf'
 
pdfWriter = FPDF()
pdfWriter.add_page()
pdfWriter.set_xy(0, 0)
pdfWriter.set_font('arial', '', 12.0)
 
#write title
f = open(text_file, 'w')
f.write('IOPHUB TABLES WITH COLUMN NAMES AND DATA TYPES')
pdfWriter.multi_cell(w=300, h=5, txt=str('IOPHUB TABLES WITH COLUMN NAMES AND DATA TYPES'), border=0, align='L', fill=False)
 
#write PDF and TXT files with columns and data types
try:
    for table in tables:
        t = str(table[0])
        r = "SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE table_schema = 'iophub' and TABLE_NAME LIKE '%" + str(t) + "%'"
 
        cur.execute(r)
        rows = cur.fetchall()
        t_name = '\n\n'+ t.upper() +'\n'
        print(t_name)
        f.write(t_name)
        pdfWriter.multi_cell(w=300, h=5, txt=str(t_name), border=0, align='L', fill=False)
        i = 1
        for row in rows:
            data = str(i) + ". " + str(row[0]) + " - " + str(row[1])
            print(data)
            f.write(data+'\n')
            pdfWriter.multi_cell(w=300, h=5, txt=str(data), border=0, align='L', fill=False)
            i+=1
    pdfWriter.output(pdf_file, 'F')
    f.close()
 
except Exception as e:
    print(str(e))
 
#convert from TXT file to HTML
m = open(text_file,'r').read()
f = open(html_file,'w')
f.write("<html>\n<body>\n<pre>\n")
f.write(str(m))
f.write("</pre>\n</body>\n</html>\n")
f.close()
