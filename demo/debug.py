"""
Debug script for developing PDFDataExtractor
"""

from pprint import pprint
import re
from chemdataextractor.doc import Document, Paragraph, Heading, Title
from chemdataextractor.doc.meta import MetaData
from pdfdataextractor import Reader


ignored_sections = {"Supporting Information", "Acknowledgements"}

def pdf_from_path(path):
    """Read a PDF file using PDFDataExtractor reader"""
    reader = Reader()
    pdf = reader.read_file(path)
    return pdf

def create_metadata(paper):
    """return MetaData from PDF

    Args:
        paper : _description_

    Returns:
        chemdataextractor.doc.MetaData: _description_
    """
    metadata = {}
    for k, v in paper.journal().items():
        metadata['_'+k] = v
    metadata['_doi'] = paper.doi()
    return MetaData(metadata)


def create_document(path):
    """Function to create a ChemDataExtractor Document from a PDF file at $path.

    Args:
        path (string): path that points to the PDF file.

    Returns:
        chemdataextractor.doc.Document: a ChemDataExtractor Document Object
    """    

    paper = pdf_from_path(path)
    # print(paper.plaintext()[:100])
    # pprint(paper.section())
    elements = [Title(paper.title()), create_metadata(paper)]
    if len(' '.join(paper.abstract())) > 15:
        elements.append(Heading("Abstract"))
        elements.append(Paragraph(' '.join(paper.abstract())))
    for k, v in paper.section().items():

        if k in ignored_sections:
            # ignore sections
            continue

        elements.append(Heading(k))
        for e in v:
            if len(e) > 15:
                if re.match(r"^\d{1,2}\s?\.\d{1,2}\.?(\s\w[^\s]+){1,5}", e):
                    elements.append(Heading(e))
                else:
                    elements.append(Paragraph(e))

    return Document(*elements)


if __name__ == "__main__":

    path = r"F:/tadf_papers/wiley/10_1002_adom_201701147.pdf"
    d = create_document(path)
    pprint(d.serialize())
