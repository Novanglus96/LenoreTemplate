import pytest
from options.models import Version
from django.core.exceptions import ValidationError


@pytest.mark.django_db
@pytest.mark.unit
def test_version_creation():
    version = Version.objects.create(version_number="1.0.0")

    assert version.id is not None
    assert version.version_number == "1.0.0"


@pytest.mark.django_db
@pytest.mark.unit
def test_version_string_representation():
    version = Version.objects.create(version_number="1.0.0")
    expected = "1.0.0"

    assert str(version) == expected


@pytest.mark.django_db
@pytest.mark.unit
def test_version_singleton_prevents_second_instance():
    Version.objects.create(version_number="1.0.0")

    with pytest.raises(ValidationError) as exc:
        Version.objects.create(version_number="2.0.0")

    assert "already one instance" in str(exc.value)


@pytest.mark.django_db
@pytest.mark.unit
def test_version_singleton_cannot_be_deleted():
    version = Version.objects.create(version_number="1.0.0")

    with pytest.raises(ValidationError):
        version.delete()
