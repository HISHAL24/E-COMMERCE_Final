"""
Service layer for catalogue operations.
interacts with the database using sql queries.
"""

from dto.catalogue_dto import catalogue  # ensure this import exists
from util.db_connection import get_connection  # assuming this path is correct

class catalogueService:
    """Service class providing metode to manage catalogue"""

    def create_catalogue(self, catalogue: catalogue) -> int:
        """
        Insert a new catalogue into the database.

        :param catalogue: An instance of the catalogue DTO containing catalogue data.
        :return: Number of rows inserted (should be 1 if successful).
        """

        conn = get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO catalogue (catalogue_name, catalogue_description, effective_from, effective_to, status)
        VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(query, (catalogue.catalogue_name,catalogue.catalogue_description,catalogue.effective_from,catalogue.effective_to,catalogue.status))
        conn.commit()
        row_count = cursor.rowcount
        cursor.close()
        conn.close()
        return row_count

    
    def get_catalogue_by_id(self, catalogue_id: int) -> dict | None:
        """
        Fetch a single catalogue record by ID.

        :param catalogue_id: The ID of the catalogue to retrieve.
        :return: A dictionary representing the catalogue record, or None if not found.
        """


        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM catalogue WHERE catalogue_id = %s",(catalogue_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
    
    def get_all_catalogues(self) -> list[dict]:
        """
        Fetch all catalogue records from the database.

        :return: A list of dictionaries, each representing a catalogue record.
        """

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM catalogue")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    
    
    def delete_catalogue_by_id(self, catalogue_id: int) -> bool:
        """
        Delete a catalogue record by its ID.

        :param catalogue_id: The ID of the catalogue to delete.
        :return: True if the record was deleted, False otherwise.
        """

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM catalogue WHERE catalogue_id = %s",(catalogue_id,))
        conn.commit()
        rate = cursor.rowcount>0
        cursor.close()
        conn.close()
        return rate
    
    def update_catalogue_by_id(self, catalogue_id: int, catalogue: catalogue) -> int:
        """
        Update an existing catalogue by its ID.

        :param catalogue_id: The ID of the catalogue to update.
        :param catalogue: An instance of the catalogue DTO with updated data.
        :return: Number of rows updated (should be 1 if successful).
        """


        conn = get_connection()
        cursor = conn.cursor()

        query = """
        UPDATE catalogue SET catalogue_name = %s, catalogue_description = %s, effective_from = %s, effective_to = %s, status = %s WHERE catalogue_id = %s
        """

        cursor.execute(query, (
            catalogue.catalogue_name,
            catalogue.catalogue_description,
            catalogue.effective_from,
            catalogue.effective_to,
            catalogue.status,
            catalogue_id
        ))

        conn.commit()
        row_count = cursor.rowcount
        cursor.close()
        conn.close()
        return row_count
