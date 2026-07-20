from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('me/', views.profile_view, name='profile'),
    path('me/edit/', views.edit_profile, name='edit_profile'),
    path('home/', views.user_home, name='user_home'),

    path('quan_ly/home/', views.admin_home, name='admin_home'),

    path('quan_ly/quan_ly_do_vat/', views.quan_ly_do_vat, name='quan_ly_do_vat'),
    path('quan_ly/quan_ly_do_vat/<int:id>/delete/', views.xoa_do_vat, name='xoa_do_vat'),
    path('quan_ly/quan_ly_do_vat/<int:id>/edit/', views.sua_do_vat, name='sua_do_vat'),

    path('quan_ly/noi_de_do/', views.noi_de_do, name='noi_de_do'),
    path('quan_ly/noi_de_do/<int:id>/delete/', views.xoa_noi_de_do, name='xoa_noi_de_do'),
    path('quan_ly/noi_de_do/<int:id>/edit/', views.sua_noi_de_do, name='sua_noi_de_do'),

    path('quan_ly/danh_sach_do_vat/', views.danh_sach_do_vat, name='danh_sach_do_vat'),
    path('quan_ly/danh_sach_do_vat/<int:id>/delete/', views.xoa_danh_sach_do_vat, name='xoa_danh_sach_do_vat'),
    path('quan_ly/danh_sach_do_vat/<int:id>/edit/', views.sua_danh_sach_do_vat, name='sua_danh_sach_do_vat'),

    path('quan_ly/notifications/', views.admin_notifications, name='admin_notifications'),
    path('quan_ly/notifications/send/', views.admin_send_notification, name='admin_send_notification'),
    path('quan_ly/notifications/edit/<int:id>/', views.admin_edit_notification, name='admin_edit_notification'),
    path('quan_ly/notifications/delete/<int:id>/', views.admin_delete_notification, name='admin_delete_notification'),
    path('user/notifications/', views.user_notifications, name='user_notifications'),

    path('user/kho_do/', views.kho_do, name='kho_do'),
    path('user/nhap_hang/', views.user_yeu_cau_nhap_kho, name='user_yeu_cau_nhap_kho'),
    path('quan_ly/duyet-nhap-kho/', views.admin_quan_ly_nhap_kho, name='admin_quan_ly_nhap_kho'),
    path('quan_ly/duyet-nhap-kho/<int:transaction_id>/<str:action>/', views.admin_set_transaction_status, name='admin_set_transaction_status'),

    path('user/xuat_hang/', views.user_yeu_cau_xuat_kho, name='user_yeu_cau_xuat_kho'),
    path('quan_ly/duyet-xuat-kho/', views.admin_quan_ly_xuat_kho, name='admin_quan_ly_xuat_kho'),
    path('quan_ly/duyet-xuat-kho/<int:transaction_id>/<str:action>/', views.admin_set_transaction_status_xuat, name='admin_set_transaction_status_xuat'),

    path('quan_ly/danh_sach_thuong_phat/', views.thuong_phat, name='danh_sach_thuong_phat'),
    path('quan_ly/danh_sach_thuong_phat/<int:id>/delete/', views.xoa_thuong_phat, name='xoa_danh_sach_thuong_phat'),
    path('quan_ly/danh_sach_thuong_phat/<int:id>/edit/', views.sua_thuong_phat, name='sua_danh_sach_thuong_phat'),
    path('user/danh_sach_thuong_phat/', views.user_thuong_phat, name='user_thuong_phat'),
]
