from django.urls import path
from . import views

app_name = 'ideas'

urlpatterns = [
    # 아이디어 관련 URL
    path('', views.ideas_list, name='ideas_list'),
    path('ideas/create/', views.ideas_create, name='ideas_create'),
    path('ideas/<int:pk>/', views.ideas_detail, name='ideas_detail'),
    path('ideas/<int:pk>/update/', views.ideas_update, name='ideas_update'),
    path('ideas/<int:pk>/delete/', views.ideas_delete, name='ideas_delete'),
    
    # 찜하기 관련 URL (AJAX)
    path('ideas/<int:pk>/star/', views.ideas_star_toggle, name='ideas_star_toggle'),
    
    # 관심도 조절 URL (AJAX)
    path('ideas/<int:pk>/interest/increase/', views.ideas_interest_increase, name='ideas_interest_increase'),
    path('ideas/<int:pk>/interest/decrease/', views.ideas_interest_decrease, name='ideas_interest_decrease'),
    
    # 개발툴 관련 URL
    path('devtools/', views.devtools_list, name='devtools_list'),
    path('devtools/create/', views.devtools_create, name='devtools_create'),
    path('devtools/<int:pk>/', views.devtools_detail, name='devtools_detail'),
    path('devtools/<int:pk>/update/', views.devtools_update, name='devtools_update'),
    path('devtools/<int:pk>/delete/', views.devtools_delete, name='devtools_delete'),
]