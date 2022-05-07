from django.db import models


class EndUser(models.Model):
    foreign_platform_id: models.CharField(max_length=150)
    redeem_rate = models.FloatField()
    recognitions_rate = models.FloatField()

    def __str__(self):
        return "ID: " + str(self.id)


class Preference(models.Model):
    user_id = models.ForeignKey(EndUser, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=100)
    reach_out_count = models.IntegerField()
    metric = models.FloatField()


class History(models.Model):
    user_id = models.ForeignKey(EndUser, on_delete=models.CASCADE)
    discount_id = models.CharField(max_length=150, default='')
    service_type = models.CharField(max_length=100)
    reach_out_at = models.DateTimeField()
    is_recognised = models.BooleanField()
    recognised_at = models.DateTimeField()
    is_redeemed = models.BooleanField()
    redeemed_at = models.DateTimeField()
