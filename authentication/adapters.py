from allauth.account.adapter import AccountAdapter

class CustomAccountAdapter(AccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)
        user.is_active = False
        if commit:
            user.save()
        return user
