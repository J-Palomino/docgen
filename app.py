import gradio as gr
import pypandoc
import os
from pdf2docx import Converter

os.system('sudo apt-get install texlive')

def ensure_pandoc_installed():
    try:
        # Periksa apakah pandoc sudah ada
        pypandoc.get_pandoc_version()
        print("Pandoc is already installed and accessible.")
    except OSError:
        # Unduh pandoc jika belum ada
        print("Pandoc not found, downloading...")
        pypandoc.download_pandoc()
        print("Pandoc downloaded successfully.")

# Pastikan Pandoc terpasang
ensure_pandoc_installed()

# Daftar format yang didukung
input_supported_formats = [data.upper() for data in sorted(list(pypandoc.get_pandoc_formats()[0]).append('PDF') or [
    'BIBLATEX', 'BIBTEX', 'BITS', 'COMMONMARK', 'COMMONMARK_X', 'CREOLE', 'CSLJSON', 'CSV',
    'DJOT', 'DOCBOOK', 'DOCX', 'DOKUWIKI', 'ENDNOTEXML', 'EPUB', 'FB2', 'GFM', 'HADDOCK',
    'HTML', 'IPYNB', 'JATS', 'JIRA', 'JSON', 'LATEX', 'MAN', 'MARKDOWN', 'MARKDOWN_GITHUB',
    'MARKDOWN_MMD', 'MARKDOWN_PHPEXTRA', 'MARKDOWN_STRICT', 'MDOC', 'MEDIAWIKI', 'MUSE',
    'NATIVE', 'ODT', 'OPML', 'ORG', 'PDF', 'POD', 'RIS', 'RST', 'RTF', 'T2T', 'TEXTILE',
    'TIKIWIKI', 'TSV', 'TWIKI', 'TYPST', 'VIMWIKI'
])]

output_supported_formats = [data.upper() for data in sorted([
    "ANSI", "ASCIIDOC", "ASCIIDOC_LEGACY", "ASCIIDOCTOR", "BEAMER", "BIBLATEX", "BIBTEX", "CHUNKEDHTML", 
    "COMMONMARK", "COMMONMARK_X", "CONTEXT", "CSLJSON", "DJOT", "DOCBOOK", "DOCBOOK4", "DOCBOOK5", 
    "DOCX", "DOKUWIKI", "DZSLIDES", "EPUB", "EPUB2", "EPUB3", "FB2", "GFM", "HADDOCK", "HTML", 
    "HTML4", "HTML5", "ICML", "IPYNB", "JATS", "JATS_ARCHIVING", "JATS_ARTICLEAUTHORING", 
    "JATS_PUBLISHING", "JIRA", "JSON", "LATEX", "MAN", "MARKDOWN", "MARKDOWN_GITHUB", 
    "MARKDOWN_MMD", "MARKDOWN_PHPEXTRA", "MARKDOWN_STRICT", "MARKUA", "MEDIAWIKI", "MS", 
    "MUSE", "NATIVE", "ODT", "OPENDOCUMENT", "OPML", "ORG", "PDF", "PLAIN", "PPTX", "REVEALJS", 
    "RST", "RTF", "S5", "SLIDEOUS", "SLIDY", "TEI", "TEXINFO", "TEXTILE", "TYPST", "XWIKI", "ZIMWIKI"
])]

def convert_pdf_to_docx(pdf_file):
    """Konversi PDF ke DOCX menggunakan pdf2docx"""
    output_docx = f"{os.path.splitext(pdf_file.name)[0]}.docx"
    cv = Converter(pdf_file.name)
    cv.convert(output_docx, start=0, end=None)
    return output_docx

def convert_document(doc_file, target_format):
    try:
        target_format = target_format.lower()
        
        # If the file is a PDF, convert it to DOCX first
        if isinstance(doc_file, str) and doc_file.lower().endswith('.pdf'):
            print("Converting PDF to DOCX...")
            doc_file = convert_pdf_to_docx(doc_file)  # Pass the file path directly
            print("PDF converted to DOCX.")
        elif hasattr(doc_file, 'name'):  # If it's a file-like object
            doc_file = doc_file.name  # Get the file path from the file-like object

        # Get the base name of the file (without extension)
        base_name = os.path.splitext(os.path.basename(doc_file))[0]

        # Output file name
        output_file = f"document_converter_{base_name}.{target_format.lower()}"

        # Use pypandoc to convert the file
        pypandoc.convert_file(
            doc_file, 
            target_format.lower(),  # Convert the format to lowercase
            outputfile=output_file,
            extra_args=['-V geometry:margin=1.5cm',
                        # '--pdf-engine=/usr/bin/xelatex',
                        '--metadata', 'title="Converted Document by Flowly AI"']
        )

        return output_file
    except Exception as e:
        return f"Error: {e}"

# Antarmuka Gradio dengan tema kustom
interface = gr.Interface(
    fn=convert_document,
    inputs=[
        gr.File(label=f"Upload Document", file_types=[f'.{ext.lower()}' for ext in input_supported_formats]),
        gr.Dropdown(label="Select Output Format", choices=output_supported_formats)
    ],
    outputs=gr.File(label="Converted Document"),
    title="Document Format Converter",
    description="Upload a document and select any target format for conversion.",
    css="footer {visibility: hidden}"
)

# Jalankan aplikasi
if __name__ == "__main__":
    interface.launch()
    