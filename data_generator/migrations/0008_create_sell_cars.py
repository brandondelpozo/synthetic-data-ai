# Generated migration for dynamic table: sell_cars
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_generator', '0007_merge_20250826_0238'),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE TABLE IF NOT EXISTS sell_cars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                car_name VARCHAR(255) NOT NULL,
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """,
            reverse_sql="DROP TABLE IF EXISTS sell_cars"
        ),
    ]
