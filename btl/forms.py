from django import forms
from .models import User, Role, ServiceCategory, Report, Notification, StorageLocation, InventoryItem, Combo, Transaction, ApprovalLog, Reward_Penalty

class InsertUserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['role_id']
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Mật khẩu'}),
        }
        labels = {
            'full_name': 'Họ và tên',
            'email': 'Email',
            'password': 'Mật khẩu',
        }

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Mật khẩu")

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'email']
        labels = {
            'full_name': 'Họ và tên',
            'email': 'Email',
        }

class Quan_ly_do_vat(forms.ModelForm):
    class Meta:
        model = ServiceCategory
        fields = ['category_name']
        labels = {'category_name': 'Tên đồ vật'}
        widgets = {
            'category_name': forms.TextInput(attrs={'placeholder': 'VD: Nhài khô, cốm thơm...'})
        }

class Noi_de_do(forms.ModelForm):
    class Meta:
        model = StorageLocation
        fields = ['location_name']
        labels = {'location_name': 'Tên nơi để đồ'}
        widgets = {
            'location_name': forms.TextInput(attrs={'placeholder': 'VD: gác xép, gầm giường, tầng 2,...'})
        }

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['title','content']
        labels = {
            'location_name': 'Tên nơi để đồ',
            'content':'Nội dung',
        }

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['item_name', 'category', 'location', 'quantity', 'unit']
        labels = {
            'item_name': 'Tên đồ vật',
            'category': 'Danh mục',
            'location': 'Vị trí lưu trữ',
            'quantity': 'Số lượng',
            'unit': 'Đơn vị tính',
        }

class RewardForm(forms.ModelForm):
    class Meta:
        model = Reward_Penalty
        fields = ['so_lan_di_muon','so_lan_bi_phan_anh','so_lan_tip','tien_thuong_phat']
        labels = {
            'so_lan_di_muon': 'Số lần đi muộn',
            'so_lan_bi_phan_anh':'Số lần bị phản ánh',
            'so_lan_tip':'Số lần được khách tip',
            'tien_thuong_phat':'Tiền thưởng/phạt',
        }