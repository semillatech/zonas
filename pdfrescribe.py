import PyPDF2

pdf_file=open('requi1.pdf', 'rb')
pdf_reader=PyPDF2.PdfReader(pdf_file)
page= pdf_reader.rçeaderpages[0]

pdf_write = PyPDF2.PdfFileWriter()

pdf_write.addPage(page)

text= PyPDF2.pdf.TextStringObject()
text.set_text('REQUISITOS 1. NOTAS CERTIFICADAS')

TEXT_ANNOTATION = PyPDF2.pdf.Annotation(
    name='/Text',
    title='Title',
    contents='Contents',
    subtype='Text',
    x=100,
    y=100,
    width=200,
    height=50,
    color=PyPDF2.pdfColor(1,1,1),
    text=text

)

page.addAnnotation(TEXT_ANNOTATION)

pdf_output_file = open('requisitos1.pdf', 'wb')
pdf_write.write(pdf_output_file)
pdf_file.close()
pdf_output_file.close()


