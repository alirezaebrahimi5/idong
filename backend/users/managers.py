from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email=None, password=None, **extra_field):

        if not email:
            raise ValueError('Email is required')

        user = self.model(email=email, **extra_field)

        if extra_field.get("is_superuser"):
            user.set_password(password)
            user.is_active = True
            user.is_superuser = True
            user.is_staff = True
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_field):
        if password is None:
            raise ValueError('Please write the password')
        extra_field.setdefault('is_superuser', True)

        super_user = self.create_user(email=email, password=password, **extra_field)
        super_user.save()
        return super_user
