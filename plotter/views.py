import sys
import os
from os.path import join, isfile

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist

import xlrd

from util import process_import_file, ModelImportInfo
from forms import UploadImportFileForm
#from forms import ImportOptionsForm
#from batchimport_settings import *

def import_start(request, extra_context=None):
        if request.method == 'POST':
                form = UploadImportFileForm(request.POST, request.FILES)
                if form.is_valid():
                        save_file_name = process_import_file(form.cleaned_data['import_file'], request.session)
                        selected_model = form.cleaned_data['model_for_import']
                        request.session['save_file_name'] = save_file_name
                        request.session['model_for_import'] = selected_model
                        return HttpResponseRedirect(reverse('batchimport_import_options'))
        else:
                form = UploadImportFileForm()
        if extra_context is None:
                extra_context = {}

        context = RequestContext(request)
        for key, value in extra_context.items():
                context[key] = callable(value) and value() or value

        return render_to_response('import_start.html',
                                                          {'form': form},
                              context_instance=context)

def import_options(request, extra_context={}):
  	try:
                save_file_name = request.session['save_file_name']
                model_for_import = request.session['model_for_import']
        except KeyError:
                # Either we don't have a file or we don't know what we're importing.
                # So restart the process with a blank form (which will show the
                # model list).
                form = UploadImportFileForm()
                context = RequestContext(request)
                for key, value in extra_context.items():
                        context[key] = callable(value) and value() or value
                return render_to_response(BATCH_IMPORT_START_TEMPLATE,
                                                                  {'form': form},
                                          context_instance=context)

        # Process the request.
        if request.method == 'POST':
                # Add the various options to the session for use during execution.
                form = ImportOptionsForm(model_for_import, save_file_name, request.POST, request.FILES)
                if form.is_valid():
                        # Put the list of models and the various user-specified options in the session
                        # for use during execution.
                        request.session['process_options'] = {}
                        for option in form.get_process_options_dict().keys():
                                request.session['process_options'][option] = form.cleaned_data[option]
                        model_field_value_dict = {}
                        for field_name in form.model_field_names:
                                model_field_value_dict[field_name] = form.cleaned_data[field_name]
                        model_import_info = ModelImportInfo(model_for_import, model_field_value_dict, form.relation_info_dict)
                        request.session['model_import_info'] = model_import_info
                else:
                        context = RequestContext(request)
                        for key, value in extra_context.items():
                                context[key] = callable(value) and value() or value
                        return render_to_response(BATCH_IMPORT_OPTIONS_TEMPLATE, {'form': form, 'model_for_import':model_for_import},
                                          context_instance=context)

                # Redirect to the Processing template which displays a "processing,
                # please wait" notice and immediately fires off execution of the import.
                context = RequestContext(request)
		for key, value in extra_context.items():
                        context[key] = callable(value) and value() or value
                return render_to_response(BATCH_IMPORT_EXECUTE_TEMPLATE, {}, context_instance=context)
        else:
                form = ImportOptionsForm(model_for_import, save_file_name)
                context = RequestContext(request)
                for key, value in extra_context.items():
                        context[key] = callable(value) and value() or value
                return render_to_response(BATCH_IMPORT_OPTIONS_TEMPLATE, {'form': form, 'model_for_import':model_for_import},
                                  context_instance=context)

