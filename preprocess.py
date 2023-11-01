from lxml import etree
import json
import re

EXTRA_SPACES = re.compile(r'\s+')

class FormatError(Exception):
    pass

def format_text(text):
    text = text.strip()
    text = text.replace('\n', ' ')
    text = EXTRA_SPACES.sub(' ', text)
    return text

def extract_book(path, book):
    name = book.find('.//head')
    name_text = name.text if name is not None else ''
    clean(book)
    for child in book.iterfind('*'):
        if child.tag != 'milestone':
            raise FormatError(f'{path}:{child.sourceline}: {child.tag}')
    chapters = [format_text(child.tail) for child in book.iterfind('*')]
    return { 'name': name_text, 'chapters': chapters }

def extract_work(path, doc):
    title = doc.find('.//title').text
    author = doc.find('.//author').text
    if doc.find('.//div2') is not None:
        books = doc.iterfind('.//div2')
    elif doc.find('.//div1') is not None:
        books = doc.iterfind('.//div1')
    else:
        books = [body.getparent() for body in doc.iterfind('.//body')]
    extracted_books = [extract_book(path, book) for book in books]
    return {
        'title': title,
        'author': author,
        'books': [book for book in extracted_books if book['chapters']]
    }

def clean(elem):
    etree.strip_elements(elem, 'table', with_tail=False)
    etree.strip_elements(elem, 'cit', with_tail=False)
    etree.strip_elements(elem, 'note', with_tail=False)
    etree.strip_elements(elem, 'pb', with_tail=False)
    etree.strip_elements(elem, 'pb', with_tail=False)
    etree.strip_elements(elem, 'argument', with_tail=False)
    etree.strip_elements(elem, 'front', with_tail=False)
    etree.strip_elements(elem, 'head', with_tail=False)
    etree.strip_elements(elem, 'epigraph', with_tail=False)
    etree.strip_elements(elem, 'opener', with_tail=False)
    etree.strip_elements(elem, 'figure', with_tail=False)
    etree.strip_tags(elem, 'p')
    etree.strip_tags(elem, 'corr')
    etree.strip_tags(elem, 'salute')
    etree.strip_tags(elem, 'text')
    etree.strip_tags(elem, 'div2')
    etree.strip_tags(elem, 'date')
    etree.strip_tags(elem, 'dateline')
    etree.strip_tags(elem, 'dateRange')
    etree.strip_tags(elem, 'title')
    etree.strip_tags(elem, 'group')
    etree.strip_tags(elem, 'body')
    etree.strip_tags(elem, 'q')
    etree.strip_tags(elem, 'gap')
    etree.strip_tags(elem, 'l')
    etree.strip_tags(elem, 'bibl')
    etree.strip_tags(elem, 'foreign')
    etree.strip_tags(elem, 'persName')
    etree.strip_tags(elem, 'placeName')
    etree.strip_tags(elem, 'surname')
    etree.strip_tags(elem, 'name')
    etree.strip_tags(elem, 'quote')
    etree.strip_tags(elem, 'hi')
    etree.strip_tags(elem, 'emph')
    for section in elem.iterfind('.//milestone[@unit="alternatesection"]'):
        section.tag = 'REMOVE'
    for section in elem.iterfind('.//milestone[@unit="chapter"]'):
        section.tag = 'REMOVE'
    for section in elem.iterfind('.//milestone[@unit="line"]'):
        section.tag = 'REMOVE'
    etree.strip_tags(elem, 'REMOVE')

def parse(filename):
    parser = etree.XMLParser(dtd_validation=False, no_network=False)
    tree = etree.parse(filename, parser=parser)
    return tree.getroot()

def main(args):
    output_path = args[0]
    input_paths = args[1:]
    print(f"preprocessing to {output_path}: {input_paths}")
    data = [extract_work(path, parse(path)) for path in input_paths]
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
