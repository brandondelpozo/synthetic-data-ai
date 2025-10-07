# Generated migration for dynamic table: testcars
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_generator', '0012_auto_20251007_0105'),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE TABLE IF NOT EXISTS testcars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                car_name VARCHAR(255) NOT NULL,
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """,
            reverse_sql="DROP TABLE IF EXISTS testcars"
        ),
    ]
