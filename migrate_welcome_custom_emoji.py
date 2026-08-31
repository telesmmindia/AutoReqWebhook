"""
Adds the `welcome_data` column to req_bots.

It holds a JSON snapshot of the bot's own /start welcome message -- the
text/caption as HTML (premium emoji included, as <tg-emoji emoji-id="..."> tags)
plus the file_id of any attachment. The bot composes the welcome from that
snapshot so animated/premium emoji survive; see core/greetings.py.

The per-channel join greeting uses cm_channel_data.greet_data, which the
Channel-Guru repo's migrate_greet_custom_emoji.py creates in this same
`channel_manager` database -- run that one too if it hasn't been.

NULL for every existing row, which keeps those welcomes on the old
copy_message path until their owner next edits them.

Safe to re-run: the ALTER checks information_schema first.

Run once from the project root:
    python migrate_welcome_custom_emoji.py
"""
from models.database import get_connection

DB_NAME = 'channel_manager'


def column_exists(cursor, table, column):
    cursor.execute(
        "SELECT COLUMN_NAME FROM information_schema.columns "
        "WHERE table_schema = %s AND table_name = %s AND COLUMN_NAME = %s",
        (DB_NAME, table, column),
    )
    return cursor.fetchone() is not None


def main():
    connection = get_connection()
    cursor = connection.cursor()

    if column_exists(cursor, 'req_bots', 'welcome_data'):
        print("req_bots.welcome_data already exists, skipping ALTER.")
    else:
        print("> ALTER TABLE req_bots ADD COLUMN welcome_data")
        cursor.execute("ALTER TABLE req_bots ADD COLUMN welcome_data TEXT DEFAULT NULL")
        connection.commit()

    if not column_exists(cursor, 'cm_channel_data', 'greet_data'):
        print("WARNING: cm_channel_data.greet_data is missing -- per-channel join "
              "greetings will keep using copy_message until you run "
              "migrate_greet_custom_emoji.py from the Channel-Guru repo.")

    connection.close()
    print("Migration complete.")


if __name__ == "__main__":
    main()
