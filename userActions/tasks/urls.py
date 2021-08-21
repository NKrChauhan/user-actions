from django.urls import path
from views import creationTaskAPI,assignTaskAPI,completeTaskAPI

urlpatterns = [
    path('create/',creationTaskAPI,name="create"),
    path('assign/<id>/',assignTaskAPI,name="assign"),
    path('complete/<id>/',completeTaskAPI,name="complete"),
]