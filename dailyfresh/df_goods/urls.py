from django.conf.urls import url
import views
urlpatterns = [
    url(r'^$',views.index),
    url(r'^list(\d+)-(\d+)-(\d+)/$',views.list),
    url(r'^(\d+)$',views.details),

]