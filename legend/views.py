from django.shortcuts import render

# Create your views here.
from WebsiteGuide.basic import CustomResponse, CustomPagination
from websiteapp import models
from websiteapp.serializers.websites_serializer import \
    AllWebsiteDataSerializers, UpdateWebsiteDataSerializers, GetWebsiteDataSerializers
from websiteapp.serializers.group_serializer import WebsiteGroupSerializers
from websiteapp.serializers.user_serializer import UserInfoSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

import os
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views import View

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserAuthView(APIView):
    '''
    Получение токена аутентификации пользователя
    '''

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            payload = jwt_payload_handler(user)
            payload['is_superuser'] = user.is_superuser
            return CustomResponse({'token': jwt_encode_handler(payload)}, status=status.HTTP_200_OK)
        else:
            return CustomResponse('Неверное имя пользователя или пароль!', status=status.HTTP_400_BAD_REQUEST)


class AllWebsiteDataViewSet(ReadOnlyModelViewSet):
    '''
    Группировка вложенных URL-адресов домашней страницы: Запрос/api/alldata/
    '''

    queryset = models.WebSiteGroup.objects.all()
    serializer_class = AllWebsiteDataSerializers
    # authentication_classes = (JSONWebTokenAuthentication,)
    # permission_classes = [IsAuthenticated]
    filter_backends = (SearchFilter,)
    search_fields = ('websites__title','websites__description')
    '''Параметр по умолчанию pk изменен на id'''
    lookup_field = 'pk'
    lookup_url_kwarg = 'id'


class WebsiteDataViewSet(ModelViewSet):
    queryset = models.WebSite.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ('title', 'path', 'description')
    pagination_class = CustomPagination
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
    lookup_url_kwarg = 'id'

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method in ('POST', 'PUT', 'PATCH', 'DELETE'):
            serializer_class = UpdateWebsiteDataSerializers
        if self.request.method == 'GET':
            serializer_class = GetWebsiteDataSerializers
        return serializer_class

    def create(self, request, *args, **kwargs):

        for data in request.data:
            serializer = self.get_serializer(data=data)
            if not serializer.is_valid():
                return CustomResponse(
                    status=status.HTTP_400_BAD_REQUEST,
                    msg='проверка формы не прошла',
                    data={'data': serializer.data, 'error': serializer.errors}
                )

        for data in request.data:
            serializer = self.get_serializer(data=data)
            serializer.is_valid()
            self.perform_create(serializer)

        return CustomResponse(
            status=status.HTTP_201_CREATED,
            msg='Добавлено успешно'
        )

    @action(methods=['delete'], detail=False, permission_classes=[IsAuthenticated], url_path='delete')
    def multiple_delete(self, request, *args, **kwargs):
        selectids = request.query_params.get('selectId', None)
        if not selectids:
            return CustomResponse(status=status.HTTP_404_NOT_FOUND)
        selectid = selectids.split(',')
        selectid = [int(x) for x in selectid if x.split()]
        models.WebSite.objects.filter(id__in=selectid).delete()
        return CustomResponse(status=status.HTTP_204_NO_CONTENT)


class WebsiteGroupViewSet(ModelViewSet):
    queryset = models.WebSiteGroup.objects.all()
    serializer_class = WebsiteGroupSerializers
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    pagination_class = CustomPagination
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = (IsAuthenticated,)

    lookup_field = 'pk'
    lookup_url_kwarg = 'id'


class UserInfoViewSet(ModelViewSet):
    queryset = models.UserInfo.objects.all()
    serializer_class = UserInfoSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('username', 'alias', 'is_active',)
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticated,)
    authentication_classes = [JSONWebTokenAuthentication, ]
    lookup_field = 'pk'
    lookup_url_kwarg = 'id'

    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated],
            url_path='change-passwd', url_name='change-passwd')
    def change_password(self, request, *args, **kwargs):
        id = kwargs.get('id')
        password1 = request.data['password1']
        password2 = request.data['password2']
        user = models.UserInfo.objects.get(id=id)
        if password1 == password2:
            user.set_password(password2)
            user.save()
            return CustomResponse(msg="Пароль был успешно изменен", status=status.HTTP_200_OK)
        else:
            return CustomResponse(msg="Пароль вводится дважды с ошибками!", status=status.HTTP_400_BAD_REQUEST)



class IconViewSet(View):
    def get(self, request, *args, **kwargs):
        content_type_map = {
            "png": "image/png",
            "svg": "image/svg+xml"
        }
        id = request.GET.get('id')
        ins = models.WebSite.objects.filter(id=id).first()
        icon_path = os.path.join(settings.MEDIA_ROOT, 'icon', str(ins.icon))
        icon_type = str(ins.icon).split('.')[-1]
        try:
            content_type = content_type_map[icon_type]
        except KeyError:
            content_type = "image/png"
        with open(icon_path, 'rb') as f:
            return HttpResponse(f, content_type=content_type)

    def post(self, request):
        id = request.POST.get('id')
        name = request.POST.get('name')
        if str(name) == "default.png":
            return JsonResponse({"code": 500, "msg": '图片名称不能为default.png，请修改'})
        file = request.FILES.get('file')
        save_path = os.path.join(settings.MEDIA_ROOT, 'icon', name)
        ins = models.WebSite.objects.filter(id=id).first()
        if ins:
            ins.icon = name
            ins.save()
            try:
                with open(save_path, 'wb') as f:
                    for chunk in file.chunks():
                        f.write(chunk)
                return JsonResponse({"code": 200, "msg": "Замена прошла успешно", "detail": ''})
            except Exception as e:
                return JsonResponse({"code": 500, "msg": "Замена не удалась", "detail": e})
        else:
            return JsonResponse({"code": 404})
