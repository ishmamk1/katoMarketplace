from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from.forms import Login

app_name = 'item'

urlpatterns = [
    # Home Page
    path('', views.index, name='index'),

    # Contact Page (Filler)
    path('contact/', views.contact, name='contact'),

    # About Page
    path('about/', views.about, name='about'),

    # Privacy Page
    path('privacy/', views.privacy, name='privacy'),

    # Terms of Service Page
    path('terms/', views.terms, name='terms'),

    # View details of specific item
    path('<int:pk>/', views.detail, name='detail'),

    # Sign-up and login page
    path('signup/', views.signUp, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=Login), name='login'),

    # Create a new item
    path('new/', views.new, name='new'),

    # Dashboard of all your items
    path('dashboard/', views.dashboard, name='dashboard'),

    # Delete or edit item if you are the owner
    path('<int:pk>/delete/', views.delete, name="delete"),
    path('<int:pk>/edit/', views.edit, name="edit"),

    # Page where you can search for items
    path('search/', views.search, name='search'),

    # Start a new conversation
    path('conversation/<int:item_pk>/', views.newConversation, name='convo'),

    # View all inboxes
    path('inbox/', views.inbox, name='inbox'),

    # Individual message log with other person
    path('inbox/<int:pk>/', views.detailInfo, name='info'),

    path('/logout', views.logout, name='logout')
]
