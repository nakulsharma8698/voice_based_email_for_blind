from django.conf.urls import url
from django.urls import path
from .views import home_view, signup_view, login_view, logout_view, first, auth_view, compose_view, inbox_view, \
    read_view, sent_view,read_sent_view, trash_view, read_trash_view, search_view,read_search_view

app_name = 'myapp'


urlpatterns = [
    path('', first, name='first'),
    path('home/', home_view, name='home'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('auth-code/', auth_view, name='auth'),
    path('logout/', logout_view, name='logout'),
    path('compose/', compose_view, name='compose'),
    path('inbox/', inbox_view, name='inbox'),
    path('sent/', sent_view, name='sent'),
    path('trash/', trash_view, name='trash'),
    # url(r'read/(?P<id>[0-9]+)$',read_view, name='read'),
    path('read/<id>',read_view, name='read'),
    path('read_sent/<id>',read_sent_view, name='read_sent'),
    path('read_trash/<id>', read_trash_view, name='read_trash'),
    path('read_search/<key>/<id>', read_search_view, name='read_search'),
    path('search/<key>', search_view, name='search'),

]
