import factory
from end_user import models as end_user_model

class PreferenceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = end_user_model.Preference

    user_id = 123
    service_name = "adasd"
    reach_out_count = 121
    metric = 0.4

class EndUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = end_user_model.EndUser

    foreign_platform_id = '12121'
    redeem_rate = 0.4
    recognitions_rate = 0.6
    name = factory.Faker('first_name')



