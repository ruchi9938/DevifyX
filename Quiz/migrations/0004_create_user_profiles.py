from django.db import migrations

def create_user_profiles(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    UserProfile = apps.get_model('Quiz', 'UserProfile')
    
    # Create UserProfile for all existing users
    for user in User.objects.all():
        UserProfile.objects.get_or_create(user=user)

class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0003_quesmodel_points_quesmodel_time_limit_userprofile_and_more'),
    ]

    operations = [
        migrations.RunPython(create_user_profiles),
    ] 