from django.urls import path

from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path('', views.home, name='adv_home'),

    #advisement session urls
    path('add_session/<int:advisee>/', views.add_advisement, name="add_advisement"),

    #checksheet template urls
    path('checksheets/', views.checksheet_listing, name="list_checksheets"),
    path('view_template/<int:template>', views.view_template, name="list_checksheets"),
    path('add_checksheet/', views.add_checksheet, name="add_checksheet"),
    path('delete_checksheet/', views.delete_checksheet, name="delete_checksheet"),

    # manage student urls
    path('add_students/', views.add_students, name="add_students"),
    path('advisee_list/', views.advisee_list, name="advisee_list"),
    path('edit_advisee/<int:advisee>', views.edit_advisee, name="edit_advisee"),

    # manage faculty urls
    path('faculty_list', views.faculty_list, name="faculty_list"),
    path('edit_faculty/<int:faculty>', views.edit_faculty, name="edit_faculty"),

    #testing urls
    path('new_edit_session/<int:advisement>', views.new_edit_advisement, name="new_edit"),
    path('new_view_session/<int:advisement>', views.new_view_advisement, name="new_view"),
]


