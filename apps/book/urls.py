from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^add_user$', views.add_user),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^wishlist$', views.wishlist),
    url(r'^add_item$', views.add_item),
    url(r'^add$', views.add),
    url(r'^add_to_wishlist$', views.add_to_wishlist),
    url(r'^remove_from_wishlist$', views.remove_from_wishlist),
    url(r'^delete_item$', views.delete_item),
    url(r'wish_items/(?P<item_id>\d+)$', views.display_item),
]
