import uuid

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from .storage import CustomS3Storage


class RoleChoices(models.TextChoices):
    ADMIN = 'Admin', 'Admin'
    CUSTOMER = 'Customer', 'Customer'
    EMPLOYEE = 'Employee', 'Employee'
# from django.db import models
# from django.contrib.auth import get_user_model
#
# User = get_user_model()




class TransactionTypeChoices(models.TextChoices):
    ACCRUAL = 'accrual', 'Accrual'
    DEDUCTION = 'deduction', 'Deduction'

class DiscountTypeChoices(models.TextChoices):
    PERCENT = 'percent', 'Percent'
    AMOUNT = 'amount', 'Amount'






class ChannelPosts(models.Model):
    post_id = models.AutoField(primary_key=True)  # ���������� ������������� �����
    content = models.TextField()
    posted_at = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"Post #{self.post_id} - {'Active' if self.status else 'Inactive'}"








class LoyaltyProgram(models.Model):
    loyalty_id = models.AutoField(primary_key=True)  # ������������� ID
    user_id = models.IntegerField()
    points_balance = models.IntegerField()
    transaction_type = models.CharField(
        max_length=10,
        choices=TransactionTypeChoices.choices
    )
    points_changed = models.IntegerField()
    transaction_date = models.DateTimeField(default=timezone.now)
    description = models.TextField()

    def __str__(self):
        return f"Loyalty #{self.loyalty_id} - User {self.user_id} - {self.transaction_type}"










class UserActivityLogs(models.Model):
    log_id = models.AutoField(primary_key=True)  # �������������� ID
    user_id = models.IntegerField()
    activity_type = models.CharField(max_length=255)
    activity_details = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Log #{self.log_id} for User {self.user_id} - {self.activity_type}"






class DeliveryMethods(models.Model):
    delivery_method_id = models.AutoField(primary_key=True)  # ���������� ID
    name = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {'Active' if self.status else 'Inactive'}"



class Promocodes(models.Model):
    promocode_id = models.AutoField(primary_key=True)  # ���������� ID
    code = models.CharField(max_length=100, unique=True)
    discount_type = models.CharField(
        max_length=10,
        choices=DiscountTypeChoices.choices
    )
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    usage_limit = models.IntegerField()
    valid_from = models.DateTimeField(default=timezone.now)
    valid_until = models.DateTimeField()
    status = models.BooleanField(default=True)

    def is_valid(self):
        now = timezone.now()
        if not self.status:
            return False
        if self.valid_from and now < self.valid_from:
            return False
        if self.valid_until and now > self.valid_until:
            return False
        if self.usage_limit <= self.orders.count():
            return False
        return True

    def __str__(self):
        return f"{self.code} ({self.discount_type})"







class Branches(models.Model):
    branch_id = models.AutoField(primary_key=True)  # ���������� �������������
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=555)
    phone = models.CharField(max_length=50)
    working_hours = models.CharField(max_length=255)
    description = models.TextField()
    geo_location = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.address}"





class PaymentMethods(models.Model):
    payment_method_id = models.AutoField(primary_key=True)  # ���������� �������������
    name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {'Active' if self.status else 'Inactive'}"





class BotConfiguration(models.Model):
    bot_id = models.AutoField(primary_key=True)  # ���������� ID ����
    bot_token = models.CharField(max_length=255)
    bot_name = models.CharField(max_length=255)
    settings = models.JSONField()  # ������ ��������� � ������� JSON
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.bot_name} - {'Active' if self.status else 'Inactive'}"





# class SMSCampaigns(models.Model):
#     campaign_id = models.AutoField(primary_key=True)  # ���������� ID ��������
#     name = models.CharField(max_length=255)
#     message = models.TextField()
#     scheduled_time = models.DateTimeField()
#     status = models.BooleanField(default=True)
#
#     def __str__(self):
#         return f"{self.name} - {'Scheduled' if self.status else 'Inactive'}"




class ExportHistory(models.Model):
    export_id = models.AutoField(primary_key=True)  # ���������� ID ��������
    file_name = models.CharField(max_length=255)
    export_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=50)
    details = models.TextField()

    def __str__(self):
        return f"{self.file_name} ({self.status})"



#�������� ������:

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)






class User(AbstractBaseUser, PermissionsMixin):
    telegram_id = models.BigIntegerField(null=True, blank=True, unique=True)
    user_name = models.CharField(max_length=250)
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=200, unique=True)
    phone_number = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(
        max_length=20,
        choices=RoleChoices.choices,
        default=RoleChoices.CUSTOMER
    )
    status = models.BooleanField(default=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)


    groups = models.ManyToManyField(
        'auth.Group',
        related_name='bestbuy_user_groups',  # Unique reverse accessor
        blank=True,
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='bestbuy_user_permissions',  # Unique reverse accessor
        blank=True,
        help_text='Specific permissions for this user.'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']  # Removed 'user_id' as it's auto-generated

    objects = CustomUserManager()

    def __str__(self):
        return self.user_name





class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(
        'Orders',
        on_delete=models.CASCADE,
        to_field='id',
        db_column='order_id',
        related_name='transactions'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='transactions'
    )
    payment_method = models.ForeignKey(
        'PaymentMethods',
        on_delete=models.SET_NULL,
        null=True,
        to_field='payment_method_id',
        db_column='payment_method_id',
        related_name='transactions'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Сумма транзакции'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Время создания транзакции'
    )
    external_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text='ID транзакции в платёжной системе (если есть)'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'

    def __str__(self):
        return f"Transaction #{self.transaction_id} — Order #{self.order.id} — {self.amount}"



class Market(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    working_hours_from = models.TimeField(null=True, blank=True)
    working_hours_to = models.TimeField(null=True, blank=True)
    is_daily = models.BooleanField(default=True)
    logo = models.ImageField(storage=CustomS3Storage(),upload_to='market_logos/', blank=True, null=True)
    user = models.OneToOneField('User', related_name='market', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='markets_owned', null=True)

    def __str__(self):
        return f"{self.name} ({self.user.user_name})"

class AdditionalMarket(models.Model):
    user = models.ForeignKey(User, related_name='additional_markets', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.user.user_name})"




class OrderStatus(models.TextChoices):
    PENDING = 'pending', 'Ожидает'
    PROCESSING = 'processing', 'В обработке'
    COMPLETED = 'completed', 'Завершён'
    CANCELED = 'canceled', 'Отменён'

class PaymentStatus(models.TextChoices):
    UNPAID = 'unpaid', 'Не оплачен'
    PAID = 'paid', 'Оплачен'
    REFUNDED = 'refunded', 'Возвращен'






class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')

    order_status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('shipped', 'Shipped'), ('delivered', 'Delivered')],
        default='pending'
    )

    payment_status = models.CharField(
        max_length=20,
        choices=[('unpaid', 'Unpaid'), ('paid', 'Paid')],
        default='unpaid'
    )

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    shipping_address = models.TextField(null=True, blank=True)

    delivery_method = models.ForeignKey(
        'DeliveryMethods',
        on_delete=models.SET_NULL,
        null=True,
        to_field='delivery_method_id',
        db_column='delivery_method_id',
        related_name='orders'
    )

    payment_method = models.ForeignKey(
        'PaymentMethods',
        on_delete=models.SET_NULL,
        null=True,
        to_field='payment_method_id',
        db_column='payment_method_id',
        related_name='orders'
    )

    branch = models.ForeignKey(
        'Branches',
        on_delete=models.SET_NULL,
        null=True,
        to_field='branch_id',
        db_column='branch_id',
        related_name='orders'
    )

    promocode = models.ForeignKey(
        Promocodes,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )

    def __str__(self):
        return f"Order #{self.id}"





# class Orders(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
#
#     order_status = models.CharField(
#         max_length=20,
#         choices=OrderStatus.choices,
#         default=OrderStatus.PENDING
#     )
#
#     payment_status = models.CharField(
#         max_length=20,
#         choices=PaymentStatus.choices,
#         default=PaymentStatus.UNPAID
#     )
#
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2)
#
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     shipping_address = models.TextField(null=True, blank=True)
#
#     delivery_method = models.ForeignKey(
#         'DeliveryMethods',
#         on_delete=models.SET_NULL,
#         null=True,
#         to_field='delivery_method_id',
#         db_column='delivery_method_id',
#         related_name='orders'
#     )
#
#     payment_method = models.ForeignKey(
#         'PaymentMethods',
#         on_delete=models.SET_NULL,
#         null=True,
#         to_field='payment_method_id',
#         db_column='payment_method_id',
#         related_name='orders'
#     )
#
#     branch = models.ForeignKey(
#         'Branches',
#         on_delete=models.SET_NULL,
#         null=True,
#         to_field='branch_id',
#         db_column='branch_id',
#         related_name='orders'
#     )
#
#     def __str__(self):
#         return f"Order #{self.id}"


# class Orders(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
#     # order_status = models.CharField(max_length=50)
#     order_status = models.CharField(
#         max_length=20,
#         choices=OrderStatus.choices,
#         default=OrderStatus.PENDING
#     )
#     # payment_status = models.CharField(max_length=50)
#     payment_status = models.CharField(
#         max_length=20,
#         choices=PaymentStatus.choices,
#         default=PaymentStatus.UNPAID)
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     shipping_address = models.TextField(null=True, blank=True)
#     delivery_method_id = models.IntegerField()
#     payment_method = models.CharField(max_length=100, default='card')
#     payment_method_id = models.IntegerField()
#     branch_id = models.IntegerField()
#
#     def __str__(self):
#         return f"Order #{self.id} by {self.user.username if self.user else 'Unknown'}"

    # def __str__(self):
    #     return f"Order #{self.id} by {self.user.user_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price_at_time = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.product.name} in Order #{self.order.id}"













def category_image_upload_path(instance, filename):
    return f'categories/{instance.name}/{filename}'

def product_media_upload_path(instance, filename):
    return f'products/{instance.name}/{filename}'


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(storage=CustomS3Storage(), upload_to=category_image_upload_path, blank=True, null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name




class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock_quantity = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', blank=True, null=True)
    brand = models.CharField(max_length=255, blank=True, null=True)
    media = models.ImageField(storage=CustomS3Storage(), upload_to=product_media_upload_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    product_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    image = models.ImageField(storage=CustomS3Storage(), upload_to='product_images/', null=True, blank=True)

    def __str__(self):
        return self.name

    def average_rating(self):
        reviews = self.reviews.all()
        ratings = []
        for review in reviews:
            try:
                ratings.append(int(review.rating))
            except ValueError:
                pass
        return round(sum(ratings) / len(ratings), 2) if ratings else None



# class Product(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField(blank=True, null=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     stock_quantity = models.IntegerField(default=0)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', blank=True, null=True)
#     brand = models.CharField(max_length=255, blank=True, null=True)
#     media = models.ImageField(storage=CustomS3Storage(), upload_to=product_media_upload_path, blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     product_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
#
#
#     image = models.ImageField(storage=CustomS3Storage(), upload_to='product_images/', null=True, blank=True)
#
#     def __str__(self):
#         return self.name


#это вариации например цвет
class Variations(models.Model):
    variation_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE, related_name='variations')
    option_name = models.CharField(max_length=255)
    option_value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.option_name}: {self.option_value} (Product: {self.product.product_id if self.product else 'No Product'})"




from django.core.validators import MinValueValidator, MaxValueValidator

class Reviews(models.Model):
    RATING_CHOICES = [
        ('1', '😡 Плохо'),
        ('2', '🙁 Не очень'),
        ('3', '😐 Нормально'),
        ('4', '🙂 Хорошо'),
        ('5', '😍 Отлично'),
    ]

    product = models.ForeignKey(
        'Product',
        to_field='product_id',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    rating = models.CharField(max_length=20, choices=RATING_CHOICES)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # один отзыв от одного юзера на один продукт

    def __str__(self):
        return f"Review {self.id} - Product {self.product.name} - User {self.user.user_name}"



# class Reviews(models.Model):
#     review_id = models.AutoField(primary_key=True)
#     product_id = models.IntegerField()
#     user_id = models.IntegerField()
#     rating = models.FloatField(
#         validators=[MinValueValidator(1.0), MaxValueValidator(5.0)]
#     )
#     comment = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"Review {self.review_id} - Product {self.product_id} - User {self.user_id}"



class SMSCampaign(models.Model):
    title = models.CharField(max_length=100)
    message = models.TextField()
    recipients = models.TextField(help_text="Phone numbers separated by commas")
    created_at = models.DateTimeField(auto_now_add=True)
    scheduled_time = models.DateTimeField(null=True, blank=True)
    is_sent = models.BooleanField(default=False)

    def __str__(self):
        return self.title



class BadPassword(models.Model):
    password = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.password




#Отдел доставки

class DeliveryDepartment(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
