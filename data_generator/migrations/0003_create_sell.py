# Generated migration for dynamic table: sell
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_generator', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE TABLE IF NOT EXISTS sell (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name VARCHAR(255) NOT NULL,
                city_sold VARCHAR(255) NOT NULL,
                seller_name VARCHAR(255) NOT NULL,
                product_description TEXT NOT NULL,
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """,
            reverse_sql="DROP TABLE IF EXISTS sell"
        ),
    ]
