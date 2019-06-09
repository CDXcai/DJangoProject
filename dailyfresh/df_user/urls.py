from django.conf.urls import url
import views
urlpatterns=[
    url(r'^register/$',views.register),
    url(r'^registerHandle/$', views.registerHandle),
    url(r'^login/$', views.login),
    url(r'^register_exits/$', views.register_exits),
    url(r'^loginhandle/$',views.loginhandle),
    url(r'^loginhandlepwd/$',views.loginhandlepwd),
    url(r'^loginSubmission/$',views.loginSubmission),
    url(r'^info/$',views.info),
    url(r'^site/$',views.site),
    url(r'^sitehandle/$',views.sitehandle),
    url(r'^order/(\d*)$',views.order),
    url(r'^logout/$',views.logout),
    url(r'^car_len/$',views.car_len),
    url(r'^isplay/$',views.isplay),
]