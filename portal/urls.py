from django.urls import path

from . import views

urlpatterns = [
    # path('', views.IndexView.as_view(), name='index'),
    path('', views.index, name='index'),
    path('upload/', views.upload.as_view(), name='upload'),
    path('analyze/', views.analyze_files, name='analyze'),
    path('Instrument QC/', views.iqc, name='IQC'),
    path('Cartridge QC/', views.cqc, name='CQC'),
    path('documents/', views.documents, name='documents'),
    path('about/', views.about, name='about')
]