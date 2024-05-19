import django_tables2 as tables
from .models import Paper

class PaperTable(tables.Table):
    class Meta:
        model = Paper
        template_name = "django_tables2/semantic.html"
        attrs = {"class": "mytable"}