from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('book_detail/<int:book_id>',views.book_detail, name='book_detail'),
    path('book_delete/<int:book_id>', views.book_delete, name='book_delete'),
    path('postbook', views.postbook, name='postbook'),
    path('displaybooks', views.displaybooks, name='displaybooks'),
    path('mybooks', views.mybooks, name='mybooks'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('searchbook', views.searchbook, name='searchbook'),
    path('display_fav_list', views.display_fav_list, name='display_fav_list'),
    path('book/<int:book_id>/add-to-favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('book/<int:book_id>/remove-from-favorites/', views.remove_from_favorites, name='remove_from_favorites'),
]
