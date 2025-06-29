from cart.models import Cart

def get_user_cart(request):
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user).select_related('product').order_by('id')

    if not request.session.session_key:
        request.session.create()

    return Cart.objects.filter(session_key=request.session.session_key).select_related('product').order_by('id')