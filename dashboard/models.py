from django.db import models
from django.contrib.auth.models import User
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
# Create your models here.
category=(
    ('stationary','stationary'),
    ('electronics','electronics'),
    ('non-technical','non-technical'),
)
class Product(models.Model):
    asset=models.CharField(max_length=30,null=True)
    sno=models.CharField(max_length=15,null=True)
    name=models.CharField(max_length=100,null=True)
    category=models.CharField(max_length=20,choices=category,null=True)
    quantity=models.PositiveIntegerField(null=True)
    model=models.CharField(max_length=300,null=True)
    #barcode=models.ImageField(upload_to='images/',null=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True) 
    price=models.CharField(max_length=20, default='Rs 0')
    class Meta:
        verbose_name_plural='Product'
    
    def __str__(self) -> str:
        return f'{self.name}-{self.quantity}'
    
    def save(self,*args,**kwargs):

        def save(self,args,*kwargs):
         details = f"Name: {self.name}\nPrice: {self.price}\nDescription: {self.model}"
         qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=3,
            border=2,
        )
         qr.add_data(details)
         qr.make(fit=True)

         img = qr.make_image(fill_color="black", back_color="white")
         buffer = BytesIO()
         img.save(buffer)
         self.qr_code.save(f"{self.name}.png", ImageFile(buffer), save=False)

         super().save(*args, **kwargs)
    


class Issued_Items(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    staff=models.ForeignKey(User,models.CASCADE,null=True)
    issueditem_quantity=models.PositiveIntegerField(null=True)
    date=models.DateTimeField(auto_now_add=True)
    location=models.CharField(max_length=50,null=True)
    STATUS_CHOICES=(('Pending','Pending'),
                    ('Accepted','Accepted'),
                    ('Rejected','Rejected'),)
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default='Pending')
    is_accepted=models.BooleanField(default='False')
    

    
    class Meta:
        verbose_name_plural='Issued_Items'

    def __str__(self) -> str:
        return f'{self.product} issued to {self.staff}'
    


