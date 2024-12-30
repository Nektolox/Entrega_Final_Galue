from django.contrib import admin
from DIDs.models import DID, Tarifa, Compania


# Register your models here.
admin.site.register(DID)
admin.site.register(Tarifa)
admin.site.register(Compania)
