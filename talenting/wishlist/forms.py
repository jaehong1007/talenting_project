from django.forms import ModelForm

from wishlist.models import WishListItems


class WishListItemsForm(ModelForm):

    class Meta:
        model = WishListItems
        fields = [
            'wish_event'
        ]
