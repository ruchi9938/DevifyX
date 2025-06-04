from django.db import migrations, models
import django.db.models.deletion
from django.utils import timezone
from django.contrib.auth.models import User

def create_default_category_and_admin(apps, schema_editor):
    Category = apps.get_model('Quiz', 'Category')
    QuesModel = apps.get_model('Quiz', 'QuesModel')
    
    # Create default admin user if it doesn't exist
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin')
        admin_user.save()
    
    # Create default category
    default_category = Category.objects.create(
        name="General",
        description="General knowledge questions"
    )
    
    # Assign default category and admin to all existing questions
    QuesModel.objects.filter(category__isnull=True).update(
        category=default_category,
        created_by=admin_user
    )

class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.AddField(
            model_name='quesmodel',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='Quiz.category'),
        ),
        migrations.AddField(
            model_name='quesmodel',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quesmodel',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='quesmodel',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
        ),
        migrations.RunPython(create_default_category_and_admin),
        migrations.AlterField(
            model_name='quesmodel',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='Quiz.category'),
        ),
        migrations.AlterField(
            model_name='quesmodel',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
        ),
    ] 