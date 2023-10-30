from lxml import etree
import json
import re

EXTRA_SPACES = re.compile(r'\s+')

def format_text(text):
    text = text.strip()
    text = text.replace('\n', ' ')
    text = EXTRA_SPACES.sub(' ', text)
    return text

def extract_book(book):
    name = book.find('.//head')
    it = book.iterfind('*')
    next(it)
    for child in it:
        assert child.tag == 'milestone' and child.attrib['unit'] == 'chapter', etree.tostring(child)
    it = book.iterfind('*')
    next(it)
    return {
        'name': name.text if name is not None else '',
        'chapters': [format_text(child.tail) for child in it],
    }

def extract_work(doc):
    title = doc.find('.//title').text
    author = doc.find('.//author').text
    books = doc.iterfind('.//div1')
    return {
        'title': title,
        'author': author,
        'books': [extract_book(book) for book in books],
    }

def clean(elem):
    etree.strip_elements(elem, 'cit', with_tail=False)
    etree.strip_elements(elem, 'note', with_tail=False)
    etree.strip_elements(elem, 'pb', with_tail=False)
    etree.strip_elements(elem, 'pb', with_tail=False)
    etree.strip_elements(elem, 'argument', with_tail=False)
    etree.strip_tags(elem, 'p')
    etree.strip_tags(elem, 'gap')
    etree.strip_tags(elem, 'l')
    etree.strip_tags(elem, 'foreign')
    etree.strip_tags(elem, 'persName')
    etree.strip_tags(elem, 'placeName')
    etree.strip_tags(elem, 'surname')
    etree.strip_tags(elem, 'quote')
    etree.strip_tags(elem, 'hi')
    for section in elem.iterfind('.//milestone[@unit="alternatesection"]'):
        section.tag = 'section'
    for section in elem.iterfind('.//milestone[@unit="section"]'):
        section.tag = 'section'
    etree.strip_tags(elem, 'section')

def parse(filename):
    parser = etree.XMLParser(dtd_validation=True, no_network=False)
    tree = etree.parse(filename, parser=parser)
    root = tree.getroot()
    clean(root)
    return root

def main(args):
    output_path = args[0]
    input_paths = args[1:]
    print(f"preprocessing to {output_path}: {input_paths}")
    data = [extract_work(parse(path)) for path in input_paths]
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
