from django.db import models

class CarManager(models.Manager):
    def get_cars_by_user(self, user):
        return self.filter(
            user=user
        )
