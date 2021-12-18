from django.conf import settings
from django.core.management import call_command
from django.db import migrations, models
import django.db.models.deletion
from django.core.serializers import base, python


def load_fixture(apps, schema_editor):
    # Save the old _get_model() function
    old_get_model = python._get_model

    # Define new _get_model() function here, which utilizes the apps argument to
    # get the historical version of a model. This piece of code is directly stolen
    # from django.core.serializers.python._get_model, unchanged. However, here it
    # has a different context, specifically, the apps variable.
    def _get_model(model_identifier):
        try:
            return apps.get_model(model_identifier)
        except (LookupError, TypeError):
            raise base.DeserializationError("Invalid model identifier: '%s'" % model_identifier)

    # Replace the _get_model() function on the module, so loaddata can utilize it.
    python._get_model = _get_model

    try:
        pass
        # Call loaddata command
        # call_command('loaddata', 'tests/fixures/contenttypes.json')
        # call_command('loaddata', 'tests/fixures/gere_coworking_auth.json')
        # call_command('loaddata', 'tests/fixures/gere_coworking_cliente.json')
        
    finally:
        # Restore old _get_model() function
        python._get_model = old_get_model

def get_operations():
    operations = [
        migrations.AddField(
            model_name='ClienteModel',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='FuncionariosModel',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
    if settings.AUTOMATIC_TEST:
        operations.append(migrations.RunPython(load_fixture))
    return operations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gere_coworking', '0002_manual_migration'),
    ]

    operations = get_operations()