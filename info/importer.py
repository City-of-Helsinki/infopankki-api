
from lxml import etree
from info.models import MasterPage, Page
from collections import namedtuple, defaultdict

PageData = namedtuple('PageData', ['languages', 'documents', 'meta', 'guid'])


def read(doc='data/sivurakenne.xml'):
    x = etree.parse(doc)
    return [transform(page )for page in x.xpath('//page')]


def parse_meta(items):
    """
    Creates dictionary from meta data where each key and its value
    is put under its language

    :param items:[item element]
    :return:{{}}
    """
    meta = defaultdict(dict)

    for item in items:
        data = item.attrib
        lang = data.get('language', False)
        if lang:
            meta[lang][data['name']] = item.text
        else:
            meta[data['name']] = item.text

    return meta


def transform(page):
    """
    Transform page elements into PageData object
    :param page:page element
    :return:PageData
    """

    return PageData(
        guid=page.attrib['guid'],
        languages=[elem.text for elem in page.xpath('activelanguages/language')],
        documents=[{'id': doc.attrib['id'], 'title': doc.attrib['title']}
                   for doc in page.xpath('controls/control/configuration/document')],
        meta=parse_meta(page.xpath('meta/item'))
    )
