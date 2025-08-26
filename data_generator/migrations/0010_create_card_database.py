# Generated migration for dynamic table: card_database
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_generator', '0009_auto_20250826_0250'),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE TABLE IF NOT EXISTS card_database (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                car_name VARCHAR(255) NOT NULL,
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """,
            reverse_sql="DROP TABLE IF EXISTS card_database"
        ),
    ]
