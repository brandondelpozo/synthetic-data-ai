# Generated migration for dynamic table: venta_autos
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_generator', '0010_create_card_database'),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE TABLE IF NOT EXISTS venta_autos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                modelo_auto VARCHAR(255) NOT NULL,
                precio_venta INTEGER NOT NULL,
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """,
            reverse_sql="DROP TABLE IF EXISTS venta_autos"
        ),
    ]
