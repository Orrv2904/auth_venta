# Generated by Django 4.2.2 on 2023-07-03 20:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_publicacion_comentario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publicacion',
            name='Image',
        ),
        migrations.CreateModel(
            name='Imagen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='images/muapp/')),
                ('publicacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagenes', to='accounts.publicacion')),
            ],
        ),
    ]
