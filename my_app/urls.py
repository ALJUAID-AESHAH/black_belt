from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register',views.register),
    path('wishes',views.dashboard),
    path('login',views.login),
    path('logout',views.logout),
    path('wishes/new',views.new_wish),
    path('create',views.create_wish),
    path('delete/<int:wish_id>',views.delete_wish),
    path('wishes/edit/<int:wish_id>',views.edit_wish),
    path('edit/<int:wish_id>',views.update),
    path('granted/<int:wish_id>',views.mark_wish_as_granted),
    path('cancel',views.cancel),
    path('like/<int:wish_id>',views.mark_wish_as_favorite),
    path('state_page',views.state)
]
