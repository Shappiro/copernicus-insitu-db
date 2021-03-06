import re
import json
import requests
from datetime import datetime
from django.urls import reverse_lazy
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone

from insitu.views.protected import (
    IsAuthenticated,
    IsSuperuser,
)
from insitu.views.protected.views import ProtectedTemplateView
from insitu.utils import PICKLISTS_DESCRIPTION
from picklists import models
from insitu.models import Product, Requirement, Data, DataProvider


class Manager(ProtectedTemplateView):
    template_name = 'manage.html'
    permission_classes = (IsSuperuser,)
    permission_denied_redirect = reverse_lazy('auth:login')


class HelpPage(ProtectedTemplateView):
    template_name = 'help.html'
    permission_classes = (IsAuthenticated, )
    permission_denied_redirect = reverse_lazy('auth:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['models'] = dict()

        PICKLISTS = [
            models.Barrier, models.ComplianceLevel, models.Area,
            models.Criticality, models.Country, models.DataFormat,
            models.DataPolicy, models.DataType, models.DefinitionLevel,
            models.Dissemination, models.EssentialVariable, models.InspireTheme,
            models.ProductGroup, models.ProductStatus, models.ProviderType,
            models.Relevance, models.RequirementGroup,
            models.QualityControlProcedure, models.Timeliness,
            models.UpdateFrequency,
        ]

        for model in PICKLISTS:
            data = {
                'nice_name': model._meta.verbose_name,
                'description': PICKLISTS_DESCRIPTION.get(model.__name__, None),
                'objects': model.objects.order_by('pk'),
                'fields': [field.name for field in model._meta.fields
                           if field.name not in ('id', 'sort_order')]
            }
            context['models'][model._meta.model_name] = data
            context['email'] = settings.SUPPORT_EMAIL
        return context


class AboutView(ProtectedTemplateView):
    template_name = 'about.html'
    permission_classes = (IsAuthenticated,)
    permission_denied_redirect = reverse_lazy('auth:login')

    @staticmethod
    def get_issues():
        base_url = settings.SENTRY_API_URL
        endpoint = '/issues/?query=&sort=date&statsPeriod=14d'

        url = ''.join((base_url, endpoint))
        r = requests.get(
            url,
            headers={
                "Authorization": f"Bearer {settings.SENTRY_AUTH_TOKEN}"
            }
        )

        issues = []

        if r.status_code == 200:
            response = json.loads(r.text)
            for message in response:
                parsed_date = re.sub('[A-Z]', '', message['lastSeen'])[0:18]
                try:
                    date = datetime.strptime(parsed_date, '%Y-%m-%d%H:%M:%S')
                except:
                    date = parsed_date
                issue = {
                    'name': message['title'],
                    'timestamp': date,
                    'resolved': (message['status'] == 'resolved')
                }
                issues.append(issue)

        return issues

    def statistics(self):
        return {
            'products': Product.objects.all().count(),
            'requirements': Requirement.objects.all().count(),
            'data': Data.objects.all().count(),
            'data_providers': DataProvider.objects.all().count(),
            'logged_users': Session.objects.filter(expire_date__gte=timezone.now()).count(),
            'registered_users': User.objects.all().count(),
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(**self.statistics())

        if settings.SENTRY_API_URL:
            context['issues'] = AboutView.get_issues()

        return context

