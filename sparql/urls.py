from django.urls import path

from .views import *

urlpatterns = [
    # path('', test, name='rdf'),
    path('query',query,name='query')
    # path('blazegraph',blazegraph,name='blazegraph')
]
