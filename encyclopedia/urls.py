from django.urls import path

from . import views
app_name="encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.entryPage, name="entryPage"),
    path("newpage",views.newpage,name="newpage"),
    path("search",views.search,name = "search"),
    path("randompage", views.randompage, name="randompage"),
    path("edit/<str:name>",views.edit,name = "edit"),

]
