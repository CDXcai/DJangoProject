from django.conf.urls import url
import views
urlpatterns=[
    url(r'^$',views.cart),
    url(r'^add_cart_handle-(\d+)-(\d+)$', views.add_cart_handle),
    url(r'^remove(\d+)-(\d+)/$', views.remove_item),
    url(r'^update_item(\d+)-(\d+)-(\d+)/$', views.update_item),
]