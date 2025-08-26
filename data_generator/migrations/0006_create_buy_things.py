# Generated migration for dynamic table: buy_things
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_generator', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE TABLE IF NOT EXISTS buy_things (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name VARCHAR(255) NOT NULL,
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """,
            reverse_sql="DROP TABLE IF EXISTS buy_things"
        ),
    ]
