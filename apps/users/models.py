from django.db import models
from django.contrib.auth.models import User


class Address(models.Model):
    country = models.CharField(
        verbose_name='Pais',
        blank=True,
        null=True,
        default='MX',
        max_length=3
    )
    region = models.CharField(
        verbose_name='Estado o Region',
        blank=False,
        null=False,
        max_length=100
    )
    town = models.CharField(
        verbose_name='Municipio o delegacion',
        blank=False,
        null=False,
        max_length=100
    )
    neighborhood = models.CharField(
        verbose_name='Colonia',
        blank=False,
        null=False,
        max_length=100,
    )
    zip_code = models.CharField(
        verbose_name='Código Postal',
        blank=False,
        null=False,
        max_length=6
    )
    street = models.CharField(
        verbose_name='Calle',
        blank=False,
        null=False,
        max_length=100
    )
    street_number = models.CharField(
        verbose_name='Número exterior',
        blank=False,
        null=False,
        max_length=10
    )
    suite_number = models.CharField(
        verbose_name='Numero interior',
        blank=True,
        null=True,
        max_length=100
    )

    @property
    def address_name(self):
        return "{} {}, {}".format(
            self.street,
            self.street_number,
            self.suite_number
        )

    @classmethod
    def create(cls, region, town, neighborhood, zip_code, street, street_number, suite_number, country):  # NOQA
        address = cls(
            region=region,
            town=town,
            neighborhood=neighborhood,
            zip_code=zip_code,
            street=street,
            street_number=street_number,
            suite_number=suite_number if suite_number is not None else ' ',
            country=country if country is not None else 'MX'
        )
        address.save()
        return address

    def __str__(self):
        return "{} {} {} {}".format(
            self.street,
            self.street_number,
            self.neighborhood,
            self.town
        )

    class Meta:
        verbose_name = "Direccion"
        verbose_name_plural = "Direcciones"


class Client(models.Model):
    user = models.OneToOneField(
        User,
        verbose_name='Usuario',
        null=False,
        blank=True,
        on_delete=models.CASCADE
    )
    addresses = models.ManyToManyField(Address, blank=True)
    phone = models.CharField(
        verbose_name='Telefono',
        max_length=13,
        blank=True,
        null=True
    )

    @property
    def full_name(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)

    @classmethod
    def create(cls, username, first_name, last_name, email, phone, password):
        user = User.objects.create(
            email=email,
            username=username
        )
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        user.set_password(password)
        _user = cls(user=user)
        if phone is not None:
            _user.phone = phone
        user.save()
        _user.save()
        return _user

    def __str__(self):
        return '{}'.format(self.user.username)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'


class Social(models.Model):
    user = models.ForeignKey(
        Client,
        verbose_name='Usuario',
        null=False,
        blank=True,
        on_delete=models.CASCADE
    )
    provider = models.CharField(
        verbose_name='Proveedor', null=False, blank=True, max_length=50
    )
    uid = models.CharField(null=False, blank=True, max_length=100)
    extra_data = models.CharField(null=True, blank=True, max_length=100)

    def __str__(self):
        return '{} {}'.format(self.provider, self.user.full_name)

    class Meta:
        verbose_name = 'Users Social Auth'
        verbose_name_plural = 'User Social Auth'
