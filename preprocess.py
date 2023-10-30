from lxml import etree
import json

def extract_book(book):
    name = book.find('head').text
    it = book.iterfind('*')
    next(it)
    for child in it:
        assert child.tag == 'milestone' and child.attrib['unit'] == 'chapter', etree.tostring(child)
    it = book.iterfind('*')
    next(it)
    return {
        'name': name,
        'chapters': [child.tail for child in it],
    }

def extract_work(doc):
    title = doc.find('.//title[@type="work"]').text
    author = doc.find('.//author').text
    books = doc.iterfind('.//div1[@type="book"]')
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
    etree.strip_tags(elem, 'p')
    etree.strip_tags(elem, 'l')
    etree.strip_tags(elem, 'foreign')
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
    return tree.getroot()

def main(args):
    input_path = args[0]
    output_path = args[1]
    root = parse(input_path)
    clean(root)
    data = [extract_work(root)]
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
