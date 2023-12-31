"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views.json_test import json_test
from .views.query import query, list_queries
from .views.plotly_graph import plotly_graph, list_graph_data
from .views.labels import list_labels, add_label

urlpatterns = [
    path('admin/', admin.site.urls),
    path('json_test/', json_test),
    path('query/', query),
    path('list_queries/', list_queries),
    path('plotly_graph/', plotly_graph),
    path('list_graphs/', list_graph_data),
    path('add_label/', add_label),
    path('list_labels/', list_labels),
]
