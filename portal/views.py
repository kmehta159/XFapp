from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import FormView
from django.core.files.storage import FileSystemStorage
from django.contrib.messages.views import SuccessMessageMixin
from base.settings import MEDIA_ROOT
from . import forms
from XF_tools import dataframe_generator, analyze
from django.http import HttpResponse
from .models import xftool
from math import ceil

def index(request):
    alltools=[]
    depxftools = xftool.objects.values('department', 'id')
    deps = {item['department'] for item in depxftools}
    for dep in deps:
        tool = xftool.objects.filter(department = dep)
        n = len(tool)
        nslides = n // 4 + ceil((n / 4) - (n // 4))
        alltools.append([tool,range(1, nslides), nslides])

    params = {'alltools': alltools}
    return render(request, 'index.html', params)

class upload(SuccessMessageMixin, FormView):
    extra_context = {
        'title': 'Data Upload Portal'
    }
    form_class = forms.FileUploadForm
    template_name = 'upload.html'
    success_url = reverse_lazy('upload')
    success_message = None

    def post(self, request, *args, **kwargs):
        self.files = request.FILES.getlist("data_file")
        fs = FileSystemStorage()
        for _file in self.files:
            fs.save(_file.name, _file)
        try:
            dataframe_generator.process_asyr_file(MEDIA_ROOT)
        except Exception as e:
            self.success_message = str(e)
        dataframe_generator.delete_folder_contents(MEDIA_ROOT)
        return super().post(request, *args, **kwargs)

    def get_success_message(self, cleaned_data):
        if not self.success_message:
            file_list = ', '.join(map(lambda x: x.name, self.files))
            return "The files {} were uploaded successfully".format(file_list)
        else :
            return self.success_message



def analyze_files(request):
    if request.method == "POST":
        dataframe_generator.delete_folder_contents(MEDIA_ROOT)

        files = request.FILES.getlist("data_file")
        fs = FileSystemStorage()
        for _file in files:
            fs.save(_file.name, _file)
        df_rate, df_raw, df_cal = analyze.convert_asyr_file(MEDIA_ROOT)
        values = analyze.IQC_auto_analyze(df_rate, df_raw, df_cal)
        values = analyze.IQC_evaluate_result(values)
        dataframe_generator.delete_folder_contents(MEDIA_ROOT)
        if values['inst_type'] == 'XFp':
            return render(request, 'analysis_results_xfp.html', values)
        if values['inst_type'] == 'XFe24':
            return render(request, 'analysis_results_xfe24.html', values)
        if values['inst_type'] == 'XFe96':
            return render(request, 'analysis_results_xfe96.html', values)
        if values['inst_type'] == 'HSmini':
            return render(request, 'analysis_results_hsmini.html', values)
        else:
            return render(request, 'analysis_results.html', values)
        # form = forms.FileUploadForm()
    else:
        form = forms.FileUploadForm()
    return render(request, 'analyze.html', {'form': form})

def iqc(request):
    return HttpResponse("we are at IQC")

def cqc(request):
    return HttpResponse("we are at CQC")

def documents(request):
    return render(request, 'analysis_results_hsmini_ECO.html')

def about(request):
    return render(request, 'about.html')