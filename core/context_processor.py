from product.models import TelegramUser, StatusShoppingCartOrder


def telegram_users(request):
    return {
        'telegram_users': TelegramUser.objects.all()
    }


def statuses(request):
    return {
        'statuses': StatusShoppingCartOrder.objects.all()
    }

