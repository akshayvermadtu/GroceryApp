from django.contrib import admin
from .models import User
from .models import Item
from .models import Order
from .models import Offer
from .models import Structure


admin.site.register(User)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(Offer)
admin.site.register(Structure)



