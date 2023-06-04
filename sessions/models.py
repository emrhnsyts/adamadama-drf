from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.

cities = (('ISTANBUL', 'İstanbul')
          , ('TRABZON', 'Trabzon')
          , ('ANKARA', 'Ankara'))


class Session(models.Model):
    description = models.TextField(max_length=255)
    city = models.CharField(choices=cities, blank=False, null=False, max_length=30)
    district = models.CharField(max_length=30)
    facility_name = models.CharField(null=False, blank=False, max_length=30)
    event_date = models.DateTimeField(null=False, blank=False)
    owner = models.ForeignKey('auth.User', related_name='owned_sessions', on_delete=models.CASCADE, editable=False)
    users = models.ManyToManyField('auth.User', related_name='attended_sessions', editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    player_limit = models.IntegerField(null=False, blank=False,
                                       validators=[MinValueValidator(2), MaxValueValidator(22)])

    def __str__(self):
        return self.city + " " + self.facility_name + " " + self.owner.email
