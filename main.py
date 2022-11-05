### Inspired by https://github.com/gerardrbentley/streamlit-random/blob/main/pdf_merge_and_split.py
from datetime import datetime
from pathlib import Path
import streamlit as st
import streamlit_pydantic as sp
from pydantic import BaseModel, Field
from typing import Optional, List
from streamlit_pydantic.types import FileContent
from PyPDF2 import PdfFileWriter, PdfFileReader

# Make folder for storing user uploads
destination_folder = Path('downloads')
destination_folder.mkdir(exist_ok=True, parents=True)

# Defines what options are in the form
class PDFMergeRequest(BaseModel):
    pdf_uploads: Optional[List[FileContent]] = Field(
        None,
        alias="PDF Files to merge",
        description="PDF files that need to be merged",
    )

st.title("PDF Merger")
st.markdown("### Upload at least 2 PDF files to merge")
# Get the data from the form, stop running if user hasn't submitted pdfs yet
data = sp.pydantic_form(key="pdf_merge_form", model=PDFMergeRequest)
if data is None or data.pdf_uploads is None or len(data.pdf_uploads) < 2:
    st.warning("Upload at least 2 PDFs and press Submit")
    st.stop()

# Save Uploaded PDFs
uploaded_paths = []
for pdf_data in data.pdf_uploads:
    input_pdf_path = destination_folder / f"input_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')}.pdf"
    input_pdf_path.write_bytes(pdf_data.as_bytes())
    uploaded_paths.append(input_pdf_path)

pdf_writer = PdfFileWriter()
for path in uploaded_paths:
    pdf_reader = PdfFileReader(str(path))
    for page in range(pdf_reader.getNumPages()):
        # Add each page to the writer object
        pdf_writer.addPage(pdf_reader.getPage(page))

# Write out the merged PDF
output_pdf_path = destination_folder / f"output_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')}.pdf"
with open(str(output_pdf_path), 'wb') as out:
    pdf_writer.write(out)
output_path = output_pdf_path
output_mime = 'application/pdf'
output_suffix = '.pdf'
st.download_button('Download Merged Document', output_path.read_bytes(), f"output_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')}{output_suffix}", mime=output_mime)
