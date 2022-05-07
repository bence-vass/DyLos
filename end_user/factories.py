import factory
import factory.fuzzy
from . import models
import random
import datetime
import uuid


class PreferencesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Preference

    service_name = factory.fuzzy.FuzzyChoice(['earn_and_burn', 'tiered', 'gamified', 'perks'])
    reach_out_count = random.randint(0, 1500)
    metric = factory.fuzzy.FuzzyFloat(0.0, 1.0)
    # user_id = factory.SubFactory(UserFactory)
    # user_id = models.EndUser.objects.get(pk=1)


class HistoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.History

    discount_id = uuid.uuid4()
    service_type = factory.fuzzy.FuzzyChoice(['earn_and_burn', 'tiered', 'gamified', 'perks'])
    reach_out_at = factory.fuzzy.FuzzyDateTime(
        datetime.datetime(2008, 1, 1, tzinfo=datetime.timezone.utc),
        datetime.datetime(2023, 1, 1, tzinfo=datetime.timezone.utc),
        force_day=3, force_second=42)
    is_recognised = bool(random.getrandbits(1))
    recognised_at = factory.fuzzy.FuzzyDateTime(
        datetime.datetime(2008, 1, 1, tzinfo=datetime.timezone.utc),
        datetime.datetime(2023, 1, 1, tzinfo=datetime.timezone.utc),
        force_day=3, force_second=42) \
        if is_recognised else None
    is_redeemed = bool(random.getrandbits(1))
    redeemed_at = factory.fuzzy.FuzzyDateTime(
        datetime.datetime(2008, 1, 1, tzinfo=datetime.timezone.utc),
        datetime.datetime(2023, 1, 1, tzinfo=datetime.timezone.utc),
        force_day=3, force_second=42) \
        if is_redeemed else None


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.EndUser

    foreign_platform_id = uuid.uuid4()
    redeem_rate = factory.fuzzy.FuzzyFloat(0.0, 1.0)
    recognitions_rate = factory.fuzzy.FuzzyFloat(0.0, 1.0)
    name = factory.Faker('name')
    preferences = factory.RelatedFactoryList(
        PreferencesFactory,
        'user_id',
        size=lambda: random.randint(2, 4),
    )
    history = factory.RelatedFactoryList(
        HistoryFactory,
        'user_id',
        size=lambda: random.randint(3, 7)
    )
