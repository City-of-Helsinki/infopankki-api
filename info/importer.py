
from lxml import etree
from info.models import MasterPage, Page, Embed
from collections import namedtuple, defaultdict
import os.path
from django.conf import settings
from django.db.models import Q
import operator
import functools
import json
from django.db import transaction

PageData = namedtuple('PageData', ['languages', 'documents', 'meta', 'guid', 'embeds'])
Document = namedtuple('Document', ['doc_id', 'path', 'language', 'title'])


def read(dump=settings.INFOPANKKI_DUMP):
    x = etree.parse(dump)
    return [page_to_data(page) for page in x.xpath('//page')]


def parse_meta(items, languages):
    """
    Creates dictionary from meta data where each key and its value
    is put under its language if active
    Meta items without language is put directly

    :param items:[item element]
    :return:{}
    """
    meta = defaultdict(dict)

    for item in items:
        data = item.attrib
        lang = data.get('language', False)
        if lang and lang in languages:
            meta[lang][data['name']] = item.text
        elif not lang:
            meta[data['name']] = item.text

    return meta


def parse_docs(docs):
    """
    Documents have page's content
    :param docs:document element
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


def parse_embeds(embeds):
    """
    Embeds are configuration elements that are attached to pages,
    but not its meta nor content

    Currently only iframe embeds are supported

    :param embeds:configuration element
    :return:{}
    """
    resp = defaultdict(list)

    for embed in embeds:
        for configuration in embed.getchildren():
            if configuration.tag in 'iframe':
                # Language is on the configuration's parent element Control
                lang = embed.getparent().attrib.get('language')
                resp[lang].append({'uri': configuration.attrib.get('uri')})

    return resp


def page_to_data(page):
    """
    Transform page elements into PageData object
    :param page:page element
    :return:PageData
    """
    languages = [elem.text for elem in page.xpath('activelanguages/language')]
    return PageData(
        guid=page.attrib['guid'],
        languages=languages,
        documents=parse_docs(page.xpath('controls/control/configuration/document')),
        embeds=parse_embeds(page.xpath('controls/control/configuration[not(document)]')),
        meta=parse_meta(page.xpath('meta/item'), languages)
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
        if pagedata.documents.get(lang):
            doc = pagedata.documents[lang]
            meta = pagedata.meta[lang]
            embeds = pagedata.embeds[lang]
            page = Page(master=master,
                        language=lang,
                        meta=meta,
                        doc_id=doc.doc_id,
                        doc_title=doc.title,
                        content=get_content(doc.path))
            page.save()
            for embed_data in embeds:
                # Embed is assumed to be valid dict for Embed class at this stage
                # TODO: Add some validation for embeds when Real Data arrives
                embed = Embed(page=page, **embed_data)
                embed.save()


@transaction.atomic
def do_import():
    with transaction.atomic():
        MasterPage.objects.all().delete()
        for page in read():
            pagedata_to_db(page)


def combine_paths_to_query(paths):
    ops = ['/{}/'.format(i) for i in paths]
    ops += ['/{}-'.format(i) for i in paths]
    ops += ['-{}-'.format(i) for i in paths]
    return functools.reduce(operator.or_, (Q(meta__url__contains=city_url) for city_url in ops))


def export(export_file_path, excludes):
    some_of_these_paths = combine_paths_to_query(excludes)
    remaining_pages = Page.objects.exclude(some_of_these_paths)
    remaining_masters = {r.master for r in remaining_pages}
    out = [
        [{'url': p.meta['url'], 'language': p.language, 'content': p.content}
         for p in r.pages.all()] for r in remaining_masters]
    json.dump(out, export_file_path, indent=2)
