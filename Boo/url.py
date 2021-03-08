from django.urls import path, include
from . import views


urlpatterns = [
    path("categories/", views.all_categories),
    path("category/", views.add_category),
    path("category_item/<uuid:category_id>/", views.all_category_items),
    path("category_item/", views.add_category_item),
    path("signup/", views.signup),
    path("login/", views.login),
    path("remove_category_item/", views.remove_category_item),
    path("remove_category/", views.remove_category),
    path("send_mail/", views.sendmail),
    path("confirm_code/", views.codeconfirm),
    path("reset_pass/", views.resetpass),
]
