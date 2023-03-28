import django_filters
from. models import *

class ReportFilter(django_filters.FilterSet):
    class Meta:
        model = Report
        fields = ['report_id']

class CompanyFilter(django_filters.FilterSet):
    class Meta:
        model = CollectionCompany
        fields = ['company_id']

