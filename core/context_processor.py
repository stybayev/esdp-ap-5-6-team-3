from product.models import TelegramUser


def telegram_users(request):
    return {
        'telegram_users': TelegramUser.objects.all()
    }


