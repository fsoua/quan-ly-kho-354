from django.db import models

class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=6, unique=True)

    def __str__(self):
        return self.role_name

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    role_id = models.ForeignKey(Role,db_column='role_id',on_delete=models.CASCADE)
    full_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name
    
class ServiceCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.category_name
    
class StorageLocation(models.Model):
    location_id = models.AutoField(primary_key=True)
    location_name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.location_name

class InventoryItem(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=255)
    category = models.ForeignKey(ServiceCategory, on_delete=models.RESTRICT)
    location = models.ForeignKey(StorageLocation, on_delete=models.RESTRICT)
    quantity = models.IntegerField(default=0)
    unit = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.item_name} ({self.quantity} {self.unit})"
    
class Combo(models.Model):
    combo_id = models.AutoField(primary_key=True)
    combo_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.combo_name

class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    TYPE_CHOICES = [('IMPORT', 'Nhập kho'), ('EXPORT', 'Xuất kho')]
    transaction_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    
    quantity = models.IntegerField()
    note = models.TextField(blank=True)
    
    STATUS_CHOICES = [('PENDING', 'Chờ duyệt'), ('APPROVED', 'Đã duyệt'), ('REJECTED', 'Từ chối')]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.item.item_name}"
    
class ApprovalLog(models.Model):
    log_id = models.AutoField(primary_key=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=[('APPROVED', 'Duyệt'), ('REJECTED', 'Từ chối')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log #{self.log_id} - {self.get_action_display()}"
    
class Report(models.Model):
    report_id = models.AutoField(primary_key=True)

    item = models.ForeignKey(InventoryItem,on_delete=models.CASCADE)
    reporter_id = models.ForeignKey(User,on_delete=models.CASCADE)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report #{self.report_id} - {self.item.item_name}"
    
class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, db_column='user_id')
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.user.full_name}"

class Reward_Penalty(models.Model):
    reward_penalty_id = models.AutoField(primary_key=True)
    so_lan_di_muon = models.IntegerField()
    so_lan_bi_phan_anh = models.IntegerField()
    so_lan_tip = models.IntegerField()
    tien_thuong_phat = models.CharField(max_length=50)

    def __str__(self):
        return self.tien_thuong
    