from django.contrib import admin

# Register your models here.
from .models import UserNotification, Otp, UserCategory, BulkMessageIssuer, TokenIssuer

admin.site.register(UserNotification)
admin.site.register(Otp)
admin.site.register(UserCategory)
admin.site.register(BulkMessageIssuer)
admin.site.register(TokenIssuer)
