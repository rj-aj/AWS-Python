from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login, name='do_the_login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^register$', views.register),
    url(r'^dashboard$', views.dashboard),
    url(r'^addItem$', views.addItem),#adds a new wish/item to my own wishlist.
    url(r'^item/(?P<id>\d+)$', views.item),
    url(r'^addWish/(?P<id>\d+)$', views.addWish),#adds another user's wish/item to my list
    url(r'^removeWish/(?P<id>\d+)$', views.removeWish),#removes another user's wish/item from my list
    url(r'^submitItem$', views.submitItem),
    url(r'^delete/(?P<id>\d+)$', views.delete),
]