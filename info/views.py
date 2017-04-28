
from django.shortcuts import render

from .models import MasterPage


def master_view(request):
    return render(request=request,
                  template_name='info/translations.html',
                  context={
                      "master_pages": MasterPage.objects.filter(pages__isnull=False)
                  })

