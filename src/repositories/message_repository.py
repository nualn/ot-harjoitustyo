from database.db_connection import get_db_conn


class MessageRepository:
    """Class for accessing messages in the database."""

    def __init__(self, conn):
        """Initialize the repository with a database connection.

        Args:
            conn: A database connection.
        """

        self._conn = conn

    def get_all_subjects(self):
        """Returns a list of all messages in the database

        Returns: A list of dicts with properties "id" and "subject"
        """

        cursor = self._conn.cursor()
        cursor.execute("SELECT id, subject FROM messages;")
        messages = cursor.fetchall()
        return list(map(lambda x: {"id": x[0], "subject": x[1]}, messages))

    def get_by_id(self, msg_id):
        """Loads a message from the database by its id

        Args:
            msg_id (int): The id of the message to load
        Returns:
            A dictionary with properties "to", "subject", and "body"
        """

        cursor = self._conn.cursor()
        cursor.execute(
            "SELECT recipient, subject, body FROM messages WHERE id = ?;",
            (msg_id,)
        )
        message = cursor.fetchone()
        return {"to": message[0], "subject": message[1], "body": message[2]}

    def create(self, recipient, subject, body):
        """Saves a message to the database

        Args:
            recipient (string): Contents of the "to" field
            subject (string): The subject of the message
            body (string): The message body
        """

        cursor = self._conn.cursor()
        cursor.execute(
            "INSERT INTO messages (recipient, subject, body) values (?,?,?);",
            (recipient, subject, body)
        )
        self._conn.commit()

    def edit(self, msg_id, recipient, subject, body):
        """Edits a message in the database

        Args:
            msg_id (int): The id of the message to edit
            recipient (string): Contents of the "to" field
            subject (string): The subject of the message
            body (string): The message body
        """

        cursor = self._conn.cursor()
        cursor.execute("""UPDATE messages SET
            recipient = ?, 
            subject = ?,
            body = ?
            WHERE id = ?;""",
                       (recipient, subject, body, msg_id)
                       )
        self._conn.commit()

    def delete(self, msg_id):
        """Deletes a message from the database by its id

        Args:
            msg_id (int): The id of the message to delete
        """

        cursor = self._conn.cursor()
        cursor.execute(
            "DELETE FROM messages WHERE id = ?;",
            (msg_id,)
        )
        self._conn.commit()


message_repository = MessageRepository(get_db_conn())
