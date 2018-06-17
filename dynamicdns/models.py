from django.db import models


# Create your models here.


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
    zone = models.ForeignKey(Zone, on_delete=models.PROTECT)
    relative_domain = models.CharField(max_length=50)
    ttl = models.PositiveIntegerField(null=True)
    ipv4 = models.GenericIPAddressField(protocol='IPv4', null=True)
    ipv6 = models.GenericIPAddressField(protocol='IPv6', null=True)

    def __str__(self):
        return "%s.%s" % (self.relative_domain, self.zone.domain)
        # return self.relative_domain

    class Meta:
        ordering = ['relative_domain']
        unique_together = ("zone", "relative_domain")
