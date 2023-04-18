from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Task
from .serializers import UserSerializer, TaskSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint': '/tasks/',
            'method': 'POST',
            'body': {'id': ''},
            'description': 'Returns an array of tasks'
        },
        {
            'Endpoint': '/tasks/id',
            'method': 'GET',
            'body': None,
            'description': 'Returns a single task object'
        },
        {
            'Endpoint': '/login/',
            'method': 'POST',
            'body': {'username': '', 'password': ''},
            'description': 'Login'
        },
        {
            'Endpoint': '/user-forgot-password/',
            'method': 'POST',
            'body': {'email': ""},
            'description': 'Email for password reset'
        },
        {
            'Endpoint': '/user-change-password/id',
            'method': 'POST',
            'body': {'password': ""},
            'description': 'Email for reset'
        },
    ]

    return Response(routes)


@api_view(['POST'])
def getTasks(request):
    tasks = Task.objects.all().order_by('-created_on')

    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getTask(request, pk):
    tasks = Task.objects.all()
    task = ''
    for i in tasks:
        date_field = i.created_on.strftime(format="%d-%m-%Y %H:%M:%S")
        if date_field == pk:
            task = i
    serializer = TaskSerializer(task, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def loginPage(request):
    data = request.data
    username = data['username']
    password = data['password']

    if data['username'] in [None, ''] or data['password'] in [None, '']:
        content = {'Error': 'Заполните все поля'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    else:
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data)
        else:
            content = {'Error': 'No such User'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def ResetPassword(request):
    data = request.data
    email = data['email']
    verify = User.objects.filter(email=email).first()
    if verify:
        link = f"http://localhost:3000/user-change-password/{verify.id}"
        send_mail(
            'NewWay | Подтвердите сообщение',
            'Пожалуйста, подтвердите сообщение ниже для сброса своего пароля',
            'gleb.batyan@gmail.com',
            [email],
            fail_silently=False,
            html_message=f'<p>Пожалуйста, перейдите по ссылке ниже для сброса вашего пароля </p><p>{link}</p>'
                         f'<br></br><p>С уважением, команда NewWay</p>'
        )

        return JsonResponse({'bool': True, 'msg': 'Пожалуйста, проверьте ваш email'},
                            json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({'bool': False, 'msg': 'Данный email не найден'}, json_dumps_params={'ensure_ascii': False})


@api_view(['POST'])
def ChangePassword(request, pk):
    data = request.data
    password = data['password']

    verify = User.objects.filter(id=pk).first()
    if verify:
        try:
            user = User.objects.get(id=pk)
            user.set_password(password)
            user.save()
            return JsonResponse({'bool': True, 'msg': 'Пароль был успешно изменен'})
        except User.DoesNotExist:
            return JsonResponse({'bool': False, 'msg': 'Упс... Произошла ошибка'})
    else:
        return JsonResponse({'bool': False, 'msg': 'Упс... Произошла ошибка'})
