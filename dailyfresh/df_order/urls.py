#cooding:utf8

from django.conf.urls import url
import views
urlpatterns=[
    # url(r'^register/$',views.register),
    url(r'^$',views.order),
    url(r'^handle/$',views.handle),
]