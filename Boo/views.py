from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from .models import Category, CategoryItem, User
from django.core.mail import send_mail
from django.shortcuts import render
from random import randint
import datetime
import hashlib
import json
import jwt

secret_key = "imbs-=%lmlu7p804nfc%3=dms*i&o)!5ythu(wpciz#uko2y5-"


@csrf_exempt
def sendmail(request):

    if request.method == "POST":

        email = json.loads(request.body.decode("utf-8"))

        global forget_mail
        forget_mail = email["email"]

        if len(list(User.objects.filter(email=forget_mail))) == 0:
            context = {"message": "account not exist"}

        else:
            global confirm_code
            confirm_code = str(randint(100000, 999999))

            send_mail(
                "Boo Confirm Code",
                "Hello from Boo support... your confirm code is: {}".format(
                    confirm_code
                ),
                "boo.support@gmail.com",
                [forget_mail],
                fail_silently=False,
            )

            context = {"message": "ok"}

    return JsonResponse(context, safe=False)


@csrf_exempt
def codeconfirm(request):

    if request.method == "POST":
        code = json.loads(request.body.decode("utf-8"))
        code = code["code"]

        if code != confirm_code:
            context = {"message": "wrong code"}

        else:
            context = {"message": "ok"}

        return JsonResponse(context, safe=False)


@csrf_exempt
def resetpass(request):

    if request.method == "POST":

        password = json.loads(request.body.decode("utf-8"))
        password = password["password"]

        hash_object = hashlib.md5(password.encode())
        hash_password = hash_object.hexdigest()

        data = User.objects.filter(email=forget_mail)

        if bool(data.update(password=hash_password)) == True:

            _data = data.first()

            payload = {
                "id": str(_data.id),
                "iat": datetime.datetime.now().timestamp(),
            }
            access_token = jwt.encode(payload, secret_key)

            context = {
                "data": access_token,
                "name": str(_data.name),
            }

        else:
            context = {"data": "somethig get wrong", "name": ""}

        return JsonResponse(context, safe=False)


@csrf_exempt
def signup(request):
    if request.method == "POST":

        new_user = json.loads(request.body.decode("utf-8"))
        name = new_user["name"]
        email = new_user["email"]
        password = new_user["password"]

        hash_object = hashlib.md5(password.encode())
        hash_password = hash_object.hexdigest()

        if len(list(User.objects.filter(email=email))) == 0:
            data = User(name=name, email=email, password=hash_password)
            data.save()

            payload = {
                "id": str(data.id),
                "iat": datetime.datetime.now().timestamp(),
            }
            access_token = jwt.encode(payload, secret_key)

            context = {"data": access_token, "name": str(data.name)}

        else:
            context = {"data": "this email exist", "name": ""}

        return JsonResponse(context, safe=False)


@csrf_exempt
def login(request):
    if request.method == "POST":

        user_info = json.loads(request.body.decode("utf-8"))
        email = user_info["email"]
        password = user_info["password"]

        hash_object = hashlib.md5(password.encode())
        hash_password = hash_object.hexdigest()

        user = User.objects.filter(email=email).first()

        if user is None:
            context = {"data": "account not exist", "name": ""}

        elif user.password != hash_password:
            context = {"data": "password not correct", "name": ""}

        else:
            payload = {
                "id": str(user.id),
                "iat": datetime.datetime.now().timestamp(),
            }
            access_token = jwt.encode(payload, secret_key)

            context = {
                "data": access_token,
                "name": str(user.name),
            }

        return JsonResponse(context, safe=False)


def all_categories(request):
    access_token = request.headers["authorization"]

    user_id = jwt.decode(access_token, secret_key, algorithms="HS256")["id"]

    data = Category.objects.filter(user__id=user_id).all()
    list_data = []

    for i in range(len(data)):
        context = {
            "id": str(data[i].id),
            "category_name": str(data[i].category_name),
        }
        list_data.append(context)

    return JsonResponse(list_data, safe=False)


@csrf_exempt
def add_category(request):
    if request.method == "POST":

        new_category = json.loads(request.body.decode("utf-8"))
        category_name = new_category["name"]
        token = new_category["token"]

        user_id = jwt.decode(token, secret_key, algorithms="HS256")["id"]

        data = Category(category_name=category_name, user_id=user_id)
        data.save()

        return HttpResponse("ok")


@csrf_exempt
def remove_category(request):
    if request.method == "POST":

        new_category = json.loads(request.body.decode("utf-8"))
        category_id = new_category["id"]

        Category.objects.filter(id=category_id).delete()

        return HttpResponse("ok")


def all_category_items(request, category_id):
    data = CategoryItem.objects.filter(category__id=category_id).all()
    list_data = []

    for i in range(len(data)):
        context = {"id": str(data[i].id), "name": str(data[i].item)}
        list_data.append(context)

    return JsonResponse(list_data, safe=False)


@csrf_exempt
def add_category_item(request):
    if request.method == "POST":

        new_category = json.loads(request.body.decode("utf-8"))
        item = new_category["item"]
        category_id = new_category["id"]

        data = CategoryItem(item=item, category_id=category_id)
        data.save()

        items = CategoryItem.objects.filter(category_id=category_id)

        list_data = []

        for i in range(len(items)):
            context = {"id": str(items[i].id), "name": str(items[i].item)}
            list_data.append(context)

        return JsonResponse(list_data, safe=False)


@csrf_exempt
def remove_category_item(request):
    if request.method == "POST":

        item = json.loads(request.body.decode("utf-8"))
        item_id = item["id"]

        item = CategoryItem.objects.filter(id=item_id).first()
        item.delete()

        items = CategoryItem.objects.filter(category=item.category)

        list_data = []

        for i in range(len(items)):
            context = {"id": str(items[i].id), "name": str(items[i].item)}
            list_data.append(context)

        return JsonResponse(list_data, safe=False)

        # return HttpResponse("ok")