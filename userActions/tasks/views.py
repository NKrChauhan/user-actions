from .models import Post, Like, Task
from .serializers import TaskSerializer
from rest_framework.decorators import api_view, authentication_classes, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.

# def homeview(request, *args, **kwargs):
#     return render(request, 'post/home.html', {})

# REST APIs


@api_view(['GET'])
@permission_classes([AllowAny])
def TaskList(request, *args, **kwargs):
    """
    REST API for fetching feeds at home page
    """
    tasks = Task.objects.all()
    serialized_data = TaskSerializer(tasks, many=True)
    return Response(serialized_data.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([JWTAuthentication, ])
@permission_classes([IsAuthenticated, ])
def creationTaskAPI(request, *args, **kwargs):
    """
    REST API for creating the task
    """
    serialized_obj = TaskSerializer(data=request.data)
    if request.user.is_client() or request.user.is_admin(): 
        if serialized_obj.is_valid(raise_exception=True):
            task = serialized_obj.save(user=request.user)
            task = TaskSerializer(task)
            return Response({"task_obj": task.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "the form data is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"message":"permission denied"},status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST', ])
@authentication_classes([JWTAuthentication, ])
@permission_classes([IsAuthenticated, ])
def assignTaskAPI(request, id, *args, **kwargs):
    """
    REST API for fetching feeds detail
    """
    try:
        obj = Post.objects.get(id=id)
        if obj.completed == False:
            if request.user.is_manager():
                serialized_data = TaskSerializer(obj)
                return Response(serialized_data.data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "YOU are not MANAGER"}, status=status.HTTP_428_PRECONDITION_REQUIRED)
        else :
            return Response({"message": "alrady completed task cannot be re-assigned"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"message": "NotFound"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST', ])
@authentication_classes([JWTAuthentication, ])
@permission_classes([IsAuthenticated, ])
def completeTaskAPI(request,id, *args, **kwargs):
    """
    REST API for operations on Post
    """
    if request.user.is_employee() or request.user.is_admin():
        try:
            obj = Task.objects.get(id=id)
            obj.completed = True
            obj.save()
            data = TaskSerializer(obj)
        except:
            return Response({"message": "POST NotFound"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "completed ! congrats", "task_obj": data.data}, status=status.HTTP_200_OK)
    else:
        return Response({"message":"YOU are not an EMPLOYEE"}, status=status.HTTP_400_BAD_REQUEST)