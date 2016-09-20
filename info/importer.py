
from lxml import etree
from info.models import MasterPage, Page


def read(doc='data/sivurakenne.xml'):

    x = etree.parse(doc)

    pages = x.xpath('//page')

    for master_page in pages:
        MP = MasterPage(page_guid=master_page.attrib['guid'])
        MP.save()

        for page in master_page.xpath('activelanguages/language'):
            P = Page(master=MP, language=page.text)
            P.save()
