
from django.shortcuts import render, get_object_or_404

from .models import Page


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
