from django.urls import path
from poll.views import *

urlpatterns = [
    path('add/', PollView.as_view(), name='polls_add'),
    path('<int:id>/edit/', PollView.as_view(), name='polls_edit'),
    path('<int:id>/delete/', poll_delete, name='polls_delete'),

    path('list/', index, name='polls_list'),
    path('<int:id>/details/', details, name='polls_details'),
    path('<int:id>/', poll, name='polls_vote'),

]
