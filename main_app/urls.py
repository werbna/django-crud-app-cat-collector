from django.urls import path # type: ignore
from . import views

urlpatterns = [
  path('', views.Home.as_view(), name='home'),
  path('about/', views.about, name='about'),
  path('cats/', views.cats_index, name='cats_index'),
  path('cats/<int:cat_id>/', views.cats_detail, name='cat_detail'),
  path('cats/create/', views.CatCreate.as_view(), name='cat_create'),
  path('cats/<int:pk>/update/', views.CatUpdate.as_view(), name='cat_update'),
  path('cats/<int:pk>/delete/', views.CatDelete.as_view(), name='cat_delete'),
  path(
        'cats/<int:cat_id>/add-feeding/', 
        views.add_feeding, 
        name='add-feeding'
    ),
  path('toys/create/', views.ToyCreate.as_view(), name='toy_create'),
  path('toys/<int:pk>/', views.ToyDetail.as_view(), name='toy_detail'),
  path('toys/', views.ToyList.as_view(), name='toy_index'),
  path('toys/<int:pk>/update/', views.ToyUpdate.as_view(), name='toy_update'),
  path('toys/<int:pk>/delete/', views.ToyDelete.as_view(), name='toy_delete'),
  path('cats/<int:cat_id>/assoc_toy/<int:toy_id>/', views.assoc_toy, name='assoc_toy'),
  path('cats/<int:cat_id>/unassoc_toy/<int:toy_id>/', views.unassoc_toy, name='unassoc_toy'),
  path('accounts/signup/', views.signup, name='signup'),
]

# cats/:catId
