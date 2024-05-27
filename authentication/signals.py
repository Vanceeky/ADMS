from django.dispatch import receiver


from allauth.account.signals import user_signed_up

@receiver(user_signed_up)
def set_user_inactive(sender, request, user, **kwargs):
    print("Signal received!")
    print(f"User signed up: {user.username}")  # Add this line
    user.is_active = False
    user.save()
    print(f"User is_active after setting: {user.is_active}")  # Add this line