# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.files.storage import default_storage

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.fields.files import FieldFile
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.shortcuts import render #gio
from django.http import HttpResponseRedirect #gio

from .forms import ContactForm, FilesForm, ContactFormSet

import os
import logging

# http://yuji.wordpress.com/2013/01/30/django-form-field-in-initial-data-requires-a-fieldfile-instance/
class FakeField(object):
    storage = default_storage


fieldfile = FieldFile(None, FakeField, 'dummy.txt')



###
import requests
from bs4 import BeautifulSoup
import readcredentials

baseurl = r'https://svn.oss.deltares.nl/repos/openearthrawdata/trunk/rijkswaterstaat/coastline_graphs_beheerregister/processed'
graphtype = r'/KL_Plots'

cr = readcredentials.get_credentials()
f = requests.get(baseurl + graphtype, auth=requests.auth.HTTPBasicAuth(cr[0], cr[1]))
children = []
body = f.content
bs = BeautifulSoup(body)
for uls in bs.findAll('li'):
    lis = uls.findAll('a')
    for li in lis:
        children.append(li.text)
#[u'..', u'Ameland_3000100.png', u'Ameland_3000101.png', ...,]
f.close()
###

class HomePageView(TemplateView):
    template_name = 'demo/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        messages.info(self.request, 'This is a demo of a message.')
        return context


class DefaultFormsetView(FormView):
    template_name = 'demo/formset.html'
    form_class = ContactFormSet


class DefaultFormView(FormView):
    template_name = 'demo/form.html'
    form_class = ContactForm


class DefaultFormByFieldView(FormView):
    template_name = 'demo/form_by_field.html'
    form_class = ContactForm


class FormHorizontalView(FormView):
    template_name = 'demo/form_horizontal.html'
    form_class = ContactForm


class FormInlineView(FormView):
    template_name = 'demo/form_inline.html'
    form_class = ContactForm


class FormWithFilesView(FormView):
    template_name = 'demo/form_with_files.html'
    form_class = FilesForm

    def get_context_data(self, **kwargs):
        context = super(FormWithFilesView, self).get_context_data(**kwargs)
        context['layout'] = self.request.GET.get('layout', 'vertical')
        context = {'layout':'horizontal'}
        return context

    def get_initial(self):
        return {
            'file4': fieldfile,
        }

class UICoast(FormView):
    template_name = 'demo/ui_coast.html'
    form_class = FilesForm
    initial = {'key': 'value'}

    def get_context_data(self, **kwargs):
        context = super(UICoast, self).get_context_data(**kwargs)
        context['layout'] = self.request.GET.get('layout', 'vertical')
        context['baseurl'] = self.request.GET.get('baseurl', baseurl)
        context['list'] = self.request.GET.get('list', children[1:]) # don't take '..'
        #logging.info(context)
        selected_option = self.request.GET.get('graphtype')
        logging.info(selected_option)
        if selected_option:
            context['so'] = selected_option

        return context

    # def get(self,request):
    #     selected_option = request.GET.get('graphtype', None)  
    #     logging.info(selected_option)
    #     return render(request, self.template_name, {'form': form})

class PaginationView(TemplateView):
    template_name = 'demo/pagination.html'

    def get_context_data(self, **kwargs):
        context = super(PaginationView, self).get_context_data(**kwargs)
        lines = []
        for i in range(10000):
            lines.append('Line %s' % (i + 1))
        paginator = Paginator(lines, 10)
        page = self.request.GET.get('page')
        try:
            show_lines = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            show_lines = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            show_lines = paginator.page(paginator.num_pages)
        context['lines'] = show_lines
        return context


class MiscView(TemplateView):
    template_name = 'demo/misc.html'

