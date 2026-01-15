from .models import Notification

def unread_notifications(request):
    if request.user.is_authenticated:
        return {
            'unread_notifications': Notification.objects.filter(
                to_user=request.user,
                is_read=False
            ).count()
        }
    return {}
