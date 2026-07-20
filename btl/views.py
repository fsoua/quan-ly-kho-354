from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import User, Role, ServiceCategory, Report, Notification, StorageLocation, InventoryItem, Combo, Transaction, ApprovalLog, Reward_Penalty
from .forms import InsertUserForm, UpdateUserForm, Quan_ly_do_vat, Noi_de_do, InventoryItemForm, NotificationForm, RewardForm
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

def register(request):
    if request.method == 'POST':
        form = InsertUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role_id = Role.objects.get(role_id=2)
            user.save()
            request.session['uid'] = str(user.user_id)
            return render(request, 'success.html', {'user': user})
    else:
        form = InsertUserForm()

    return render(request, 'register.html', {'form': form})

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        user = User.objects.filter(email=email, password=password).first()
        if user:
            request.session['uid'] = str(user.user_id)
            return redirect('profile')
        else:
            return render(request, 'login.html', {'error': 'Sai email hoặc mật khẩu'})
    return render(request, 'login.html')


def logout_view(request):
    if 'uid' in request.session:
        del request.session['uid']
    return redirect('login')

@csrf_exempt
def profile_view(request):
    uid = request.session.get('uid')
    if not uid:
        return redirect('login')
    user = User.objects.filter(user_id=uid).first()
    if not user:
        return redirect('login')
    return render(request, 'profile.html', {'user': user})

def edit_profile(request):
    uid = request.session.get('uid')
    if not uid:
        return redirect('login')
    user = User.objects.filter(user_id=uid).first()
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UpdateUserForm(instance=user)
    return render(request, 'edit_profile.html', {'form': form, 'user': user})

def get_current_user(request):
    uid = request.session.get('uid')
    return User.objects.filter(user_id=uid).first()

def admin_home(request):
    user = get_current_user(request)
    if not user or user.role_id.role_name.upper() != 'ADMIN':
        return redirect('login')
    return render(request, 'quan_ly/home.html', {'user': user})

def user_home(request):
    user = get_current_user(request)
    if not user:
        return redirect('login')
    return render(request, 'user/home.html', {'user': user,})

def quan_ly_do_vat(request):
    if request.method == 'POST':
        form = Quan_ly_do_vat(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quan_ly_do_vat')
    else:
        form = Quan_ly_do_vat()

    do_vat = ServiceCategory.objects.all().order_by('category_name')
    return render(request, 'quan_ly/quan_ly_do_vat.html', {
        'form': form,
        'do_vat': do_vat
    })    

def xoa_do_vat(request, id):
    loc = get_object_or_404(ServiceCategory, pk=id)
    loc.delete()
    return redirect('quan_ly_do_vat')

def sua_do_vat(request, id):
    loc = get_object_or_404(ServiceCategory, pk=id)
    if request.method == 'POST':
        form = Quan_ly_do_vat(request.POST, instance=loc)
        if form.is_valid():
            form.save()
            return redirect('quan_ly_do_vat')
    else:
        form = Quan_ly_do_vat(instance=loc)
    return render(request, 'quan_ly/sua_do_vat.html', {'form': form})

def noi_de_do(request):
    if request.method == 'POST':
        form = Noi_de_do(request.POST)
        if form.is_valid():
            form.save()
            return redirect('noi_de_do')
    else:
        form = Noi_de_do()

    noi_de_dos = StorageLocation.objects.all().order_by('location_name')
    return render(request, 'quan_ly/noi_de_do.html', {
        'form': form,
        'noi_de_dos': noi_de_dos
    })  

def xoa_noi_de_do(request, id):
    loc = get_object_or_404(StorageLocation, pk=id)
    loc.delete()
    return redirect('noi_de_do')

def sua_noi_de_do(request, id):
    loc = get_object_or_404(StorageLocation, pk=id)
    if request.method == 'POST':
        form = Noi_de_do(request.POST, instance=loc)
        if form.is_valid():
            form.save()
            return redirect('noi_de_do')
    else:
        form = Noi_de_do(instance=loc)
    return render(request, 'quan_ly/sua_noi_de_do.html', {'form': form})  

def danh_sach_do_vat(request):
    if request.method == 'POST':
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('danh_sach_do_vat')
    else:
        form = InventoryItemForm()

    do_vat = InventoryItem.objects.select_related('category', 'location').order_by('item_name')
    
    return render(request, 'quan_ly/danh_sach_do_vat.html', {
        'form': form,
        'do_vat': do_vat
    })

def xoa_danh_sach_do_vat(request, id):
    loc = get_object_or_404(InventoryItem, pk=id)
    loc.delete()
    return redirect('danh_sach_do_vat')

def sua_danh_sach_do_vat(request, id):
    loc = get_object_or_404(InventoryItem, pk=id)
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, instance=loc)
        if form.is_valid():
            form.save()
            return redirect('danh_sach_do_vat')
    else:
        form = InventoryItemForm(instance=loc)
    return render(request, 'quan_ly/sua_danh_sach_do_vat.html', {'form': form})

def admin_notifications(request):
    notifications = Notification.objects.select_related('user').all().order_by('notification_id')
    users = User.objects.filter(role_id=2)
    return render(request, 'quan_ly/notifications.html', {
        'notifications': notifications,
        'users': users
    })

def admin_send_notification(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        title = request.POST.get("title")
        content = request.POST.get("content")

        Notification.objects.create(
            user_id=user_id,
            title=title,
            content=content,
        )
    return redirect('admin_notifications')

def admin_delete_notification(request, id):
    n = get_object_or_404(Notification, pk=id)
    n.delete()
    return redirect('admin_notifications')

def admin_edit_notification(request, id):
    loc = get_object_or_404(Notification, pk=id)
    if request.method == 'POST':
        form = NotificationForm(request.POST, instance=loc)
        if form.is_valid():
            form.save()
            return redirect('admin_notifications')
    else:
        form = NotificationForm(instance=loc)
    return render(request, 'quan_ly/sua_thong_bao.html', {'form': form})

def user_notifications(request):
    user = get_current_user(request)
    if not user:
        return redirect('login')
    notifications = Notification.objects.filter(user=user).order_by('notification_id')
    return render(request, 'user/notifications.html', {
        'notifications': notifications,
        'user': user
    })

def kho_do(request):
    user = get_current_user(request)
    if not user:
        return redirect('login')
    do_vat = InventoryItem.objects.select_related('category', 'location').order_by('item_name')
    return render(request, 'user/kho_do.html', {
        'user': user,
        'do_vat': do_vat
    })

def user_yeu_cau_nhap_kho(request):
    user = get_current_user(request)
    if not user:
        return redirect('login')
    
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity', 0))
        note = request.POST.get('note', '')
        item = get_object_or_404(InventoryItem, pk=item_id)
        Transaction.objects.create(
            item=item,
            user=user,
            transaction_type='IMPORT',
            quantity=quantity,
            note=note,
            status='PENDING'
        )
        messages.success(request, "Yêu cầu nhập hàng của bạn đã được gửi và đang chờ Admin duyệt!")
        return redirect('user_yeu_cau_nhap_kho')
        
    items = InventoryItem.objects.all()
    return render(request, 'user/nhap_hang.html', {'items': items})

def admin_quan_ly_nhap_kho(request):
    user = get_current_user(request)
    if not user or user.role_id.role_name.upper() != 'ADMIN':
        return redirect('login')
    
    pending_transactions = Transaction.objects.filter(status='PENDING', transaction_type='IMPORT')
    logs = ApprovalLog.objects.select_related('transaction', 'admin').order_by('-created_at')[:20]
    return render(request, 'admin/duyet_nhap_kho.html', {
        'transactions': pending_transactions,
        'logs': logs
    })

def admin_set_transaction_status(request, transaction_id, action):
    user = get_current_user(request)
    if not user or user.role_id.role_name.upper() != 'ADMIN':
        return redirect('login')

    t = get_object_or_404(Transaction, pk=transaction_id)

    if action == 'approve':
        with transaction.atomic():
            t.status = 'APPROVED'
            t.save()
            item = t.item
            item.quantity += t.quantity
            item.save()           
            ApprovalLog.objects.create(transaction=t, admin=user, action='APPROVED')
            Notification.objects.create(
                user=t.user,
                title="Duyệt nhập kho",
                content=f"Yêu cầu nhập {item.item_name} số lượng {t.quantity} đã được duyệt."
            )
            
    elif action == 'reject':
        t.status = 'REJECTED'
        t.save()
        ApprovalLog.objects.create(transaction=t, admin=user, action='REJECTED')
        
    return redirect('admin_quan_ly_nhap_kho')

def user_yeu_cau_xuat_kho(request):
    user = get_current_user(request)
    if not user:
        return redirect('login')
    
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity', 0))
        
        item = get_object_or_404(InventoryItem, pk=item_id)
        
        if quantity > item.quantity:
            messages.error(request, f"Không đủ hàng! Chỉ còn {item.quantity} trong kho.")
            return redirect('user_yeu_cau_xuat_kho')

        Transaction.objects.create(
            item=item, user=user, transaction_type='EXPORT',
            quantity=quantity, status='PENDING'
        )
        messages.success(request, "Đã gửi yêu cầu xuất kho, vui lòng chờ Admin duyệt.")
        return redirect('user_yeu_cau_xuat_kho')
        
    items = InventoryItem.objects.all()
    return render(request, 'user/xuat_hang.html', {'items': items})

def admin_quan_ly_xuat_kho(request):
    user = get_current_user(request)
    if not user or user.role_id.role_name.upper() != 'ADMIN':
        return redirect('login')
    
    pending_transactions = Transaction.objects.filter(status='PENDING', transaction_type='EXPORT')
    logs = ApprovalLog.objects.select_related('transaction', 'admin').filter(transaction__transaction_type='EXPORT').order_by('-created_at')[:20]
    
    return render(request, 'admin/duyet_xuat_kho.html', {
        'transactions': pending_transactions,
        'logs': logs
    })

def admin_set_transaction_status_xuat(request, transaction_id, action):
    user = get_current_user(request)
    if not user or user.role_id.role_name.upper() != 'ADMIN':
        return redirect('login')

    t = get_object_or_404(Transaction, pk=transaction_id)

    if action == 'approve':
        with transaction.atomic():
            t.status = 'APPROVED'
            t.save()
            
            # XUẤT KHO thì TRỪ số lượng
            item = t.item
            item.quantity -= t.quantity
            item.save()
            
            ApprovalLog.objects.create(transaction=t, admin=user, action='APPROVED')
            
            Notification.objects.create(
                user=t.user,
                title="Duyệt xuất kho",
                content=f"Yêu cầu xuất {item.item_name} số lượng {t.quantity} đã được duyệt."
            )
            
    elif action == 'reject':
        t.status = 'REJECTED'
        t.save()
        ApprovalLog.objects.create(transaction=t, admin=user, action='REJECTED')
        
    return redirect('admin_quan_ly_xuat_kho')

def thuong_phat(request):
    if request.method == 'POST':
        form = RewardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('danh_sach_thuong_phat')
    else:
        form = RewardForm()

    thuong_phats = Reward_Penalty.objects.all().order_by('tien_thuong_phat')
    
    return render(request, 'admin/danh_sach_thuong_phat.html', {
        'form': form,
        'thuong_phats': thuong_phats
    })

def xoa_thuong_phat(request, id):
    loc = get_object_or_404(Reward_Penalty, pk=id)
    loc.delete()
    return redirect('danh_sach_thuong_phat')

def sua_thuong_phat(request, id):
    loc = get_object_or_404(Reward_Penalty, pk=id)
    if request.method == 'POST':
        form = RewardForm(request.POST, instance=loc)
        if form.is_valid():
            form.save()
            return redirect('danh_sach_thuong_phat')
    else:
        form = RewardForm(instance=loc)
    return render(request, 'admin/sua_danh_sach_thuong_phat.html', {'form': form})

def user_thuong_phat(request):
    thuong_phats = Reward_Penalty.objects.all().order_by('tien_thuong_phat') 
    return render(request, 'user/danh_sach_thuong_phat.html', {
        'thuong_phats': thuong_phats
    })