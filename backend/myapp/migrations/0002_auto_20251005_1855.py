# your_app/migrations/0002_add_initial_statuses_and_categories.py

from django.db import migrations

STATUSES = [
    "актуально",
    "забронирован",
    "продан",
]

CATEGORIES = [
    "верх",
    "низ",
    "кроссовки",
]

class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),  # ← укажите правильную предыдущую миграцию
    ]

    operations = [
        # Добавление статусов
        migrations.RunSQL(
            sql=[
                f"INSERT INTO statuses (title) VALUES ('{status}');"
                for status in STATUSES
            ],
            reverse_sql=[
                f"DELETE FROM statuses WHERE title = '{status}';"
                for status in STATUSES
            ],
        ),
        # Добавление категорий
        migrations.RunSQL(
            sql=[
                f"INSERT INTO categories (title) VALUES ('{category}');"
                for category in CATEGORIES
            ],
            reverse_sql=[
                f"DELETE FROM categories WHERE title = '{category}';"
                for category in CATEGORIES
            ],
        ),
    ]