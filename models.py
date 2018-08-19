from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


# Create your models here.

class WhizzDivaUserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager"
    """

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True)
    is_staff = models.BooleanField(
        "staff status",
        default=False,
        help_text="Designates whether the user can log into this site.",
    )
    is_superuser = models.BooleanField(
        "superuser status",
        default=False,
        help_text="Designates whether the user has superuser privileges.",
    )
    is_active = models.BooleanField(
        "active",
        default=True,
        help_text="Designates whether this user should be treated as active."
                  "Unselect this instead of deleting accounts.",
    )

    USERNAME_FIELD = 'email'
    objects = WhizzDivaUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


class AbstractModel(models.Model):
    name = models.CharField(max_length=200)
    create_date = models.DateTimeField('date created', auto_now_add=True, editable=False)
    modify_date = models.DateTimeField('date last modified', auto_now=True, editable=False)

    class Meta:
        abstract = True


class DnsKey(AbstractModel):
    DNSKEY_ALGORITHMS = (
        ("HMAC-MD5", "HMAC-MD5"),
        ("HMAC-SHA1", "HMAC-SHA1"),
        ("HMAC-SHA224", "HMAC-SHA224"),
        ("HMAC-SHA256", "HMAC-SHA256"),
        ("HMAC-SHA384", "HMAC-SHA384"),
        ("HMAC-SHA512", "HMAC-SHA512"),
    )
    usable = models.BooleanField(default=True)
    algorithm = models.CharField(max_length=32, choices=DNSKEY_ALGORITHMS)
    secret = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Zone(AbstractModel):
    domain = models.CharField(max_length=200, unique=True)
    default_ttl = models.PositiveIntegerField(default=60)
    keys = models.ManyToManyField(DnsKey)
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.domain

    class Meta:
        ordering = ['domain']


class DynamicDomain(AbstractModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    zone = models.ForeignKey(Zone, on_delete=models.PROTECT)
    relative_domain = models.CharField(max_length=50)
    ttl = models.PositiveIntegerField(null=True)
    ipv4 = models.GenericIPAddressField(protocol='IPv4', blank=True, null=True)
    ipv6 = models.GenericIPAddressField(protocol='IPv6', blank=True, null=True)

    def __str__(self):
        return "%s.%s" % (self.relative_domain, self.zone.domain)
        # return self.relative_domain

    class Meta:
        ordering = ['zone__domain', 'relative_domain']
        unique_together = ("zone", "relative_domain")
