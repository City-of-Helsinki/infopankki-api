import xlsxwriter
from xlsxwriter.workbook import Workbook

from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.apps import apps
from django.conf import settings
from django.utils.html import strip_tags


from .models import Page


def translate_view(request, page):

    """
    Returns Excel of translated strings in given models
    Accepts as arguments either *all* which exports models from
    settings.TRANSLATED_MODELS_EXPORT
    or *models* as comma separated model name list
    :param request:Django HttpRequest
    :param page:string
    :return:Django HttpResponse
    """

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = "attachment; filename=test.xlsx"

    page = get_object_or_404(Page, pk=page)
    fi_page = page.master.pages.get(language='fi')

    result = make_translation_excel(response, page, fi_page)

    if not result:
        return HttpResponseBadRequest("Problem with producing Excel")

    return response


def page_view(request, page):
    page = get_object_or_404(Page, pk=page)
    siblings = [p for p in page.master.pages.all() if p.language != 'fi']
    return render(request=request,
                  template_name='info/translations_page.html',
                  context={
                      "page": page,
                      "siblings": siblings
                  })


def master_view(request):

    pages = Page.objects.filter(language='fi')
    return render(request=request,
                  template_name='info/translations_master.html',
                  context={
                      "pages": pages
                  })


def make_translation_excel(output, page, fi_page):
    """
    Based on models.utils.generate_reservation_xlsx and this SO answer:
    http://stackoverflow.com/a/36836927
    Output is either BytesIO (for writing to a file) or StringIO (for Django HttpResponse)
    Data is a dict where key is the model's name and value is a list
    with first item the translated field names and second item list of instances
    (or a queryset returning such)
    Each model gets added to its own sheet (tab) in XLS file
    :param output:BytesIO|StringIO
    :return:XLS file as bytes
    """

    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet("Käännettävät sivut")
    header_format = workbook.add_format({'bold': True})
    worksheet.write(0, 0, "FI page", header_format)
    worksheet.write(0, 1, page.language.upper() + " page", header_format)
    worksheet.set_column(0, 0, 100)
    worksheet.set_column(0, 1, 100)

    for index, row in enumerate(strip_tags(fi_page.content).split("\n")):
        worksheet.write(index, 0, row.strip())

    for index, row in enumerate(strip_tags(page.content).split("\n")):
        worksheet.write(index, 1, row.strip())

    workbook.close()
    return True
