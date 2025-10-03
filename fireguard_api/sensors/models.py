# sensors/models.py
from django.db import models

class SensorData(models.Model):
    timestamp = models.DateTimeField()
    dht_t = models.FloatField()
    dht_h = models.FloatField()
    mq2_d = models.IntegerField()
    flame_d = models.IntegerField()
    vibra_d = models.IntegerField()
    current_v = models.FloatField()
    encoder_c = models.IntegerField()
    dist_cm = models.FloatField()
    current_420 = models.FloatField()
    ds_t = models.FloatField()
    mpu_ax = models.FloatField()
    mpu_ay = models.FloatField()
    mpu_az = models.FloatField()
    mpu_gx = models.FloatField()
    mpu_gy = models.FloatField()
    mpu_gz = models.FloatField()
    zmpt_vrms = models.FloatField()
