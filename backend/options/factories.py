import factory
from options.models import Version


class VersionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Version

    version_number = "0.0.0"
