
from lxml import etree
from info.models import MasterPage, Page
from collections import namedtuple, defaultdict
import os.path
from django.conf import settings

PageData = namedtuple('PageData', ['languages', 'documents', 'meta', 'guid'])
Document = namedtuple('Document', ['doc_id', 'path', 'content', 'language'])


def read(doc=settings.INFOPANKKI_DUMP):
    x = etree.parse(doc)
    return [page_to_data(page) for page in x.xpath('//page')]


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


def parse_docs(docs):
    """
    Documents have page's content
    :param doc:document element
    :return:{}
    """
    resp = {}

    for doc in docs:
        lang = doc.xpath('../../@language')[0]
        resp[lang] = Document(
            doc_id=doc.attrib['id'],
            title=doc.attrib['title'],
            path=settings.INFOPANKKI_DATA_PATH + doc.attrib['id'],
            language=lang
        )

    return resp


def page_to_data(page):
    """
    Transform page elements into PageData object
    :param page:page element
    :return:PageData
    """

    return PageData(
        guid=page.attrib['guid'],
        languages=[elem.text for elem in page.xpath('activelanguages/language')],
        documents=parse_docs(page.xpath('controls/control/configuration/document')),
        meta=parse_meta(page.xpath('meta/item'))
    )


def get_content(path):
    if not os.path.exists(path):
        return False
    else:
        return open(path, 'r').read()


def pagedata_to_db(pagedata):

    master = MasterPage(page_guid=pagedata.guid,
                        meta={key: val
                              for key, val in pagedata.meta.items()
                              if key not in pagedata.languages})
    master.save()

    for lang in pagedata.languages:
        doc = pagedata.documents[lang]
        meta = pagedata.meta[lang]

        page = Page(master=master,
                    language=lang,
                    meta=meta,
                    doc_id=doc.doc_id,
                    content=get_content(doc.path),
                    title=doc.title)

        page.save()
