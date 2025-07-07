"""
Service layer for catalogue operations.
Interacts with the database using SQL queries.
"""

import logging
from dto.catalogue_dto import catalogue  # ensure this import exists
from util.db_connection import get_connection  # assuming this path is correct

logger = logging.getLogger(__name__)

class catalogueService:
    """Service class providing methods to manage catalogue"""

    def create_catalogue(self, catalogue: catalogue) -> int:
        """
        Insert a new catalogue into the database.
        """
        logger.debug(f"Attempting to create catalogue: {catalogue}")
        try:
            conn = get_connection()
            cursor = conn.cursor()

            query = """
            INSERT INTO catalogue (catalogue_name, catalogue_description, effective_from, effective_to, status)
            VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(query, (
                catalogue.catalogue_name,
                catalogue.catalogue_description,
                catalogue.effective_from,
                catalogue.effective_to,
                catalogue.status
            ))
            conn.commit()
            row_count = cursor.rowcount
            logger.info(f"Catalogue created successfully. Rows inserted: {row_count}")
            return row_count
        except Exception as e:
            logger.exception("Failed to create catalogue")
            raise
        finally:
            cursor.close()
            conn.close()

    def get_catalogue_by_id(self, catalogue_id: int) -> dict | None:
        """
        Fetch a single catalogue record by ID.
        """
        logger.debug(f"Fetching catalogue by ID: {catalogue_id}")
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM catalogue WHERE catalogue_id = %s", (catalogue_id,))
            result = cursor.fetchone()
            if result:
                logger.info(f"Catalogue found: {result}")
            else:
                logger.warning(f"No catalogue found with ID: {catalogue_id}")
            return result
        except Exception as e:
            logger.exception(f"Error fetching catalogue with ID {catalogue_id}")
            raise
        finally:
            cursor.close()
            conn.close()

    def get_all_catalogues(self) -> list[dict]:
        """
        Fetch all catalogue records from the database.
        """
        logger.debug("Fetching all catalogues")
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM catalogue")
            result = cursor.fetchall()
            logger.info(f"Total catalogues fetched: {len(result)}")
            return result
        except Exception as e:
            logger.exception("Error fetching all catalogues")
            raise
        finally:
            cursor.close()
            conn.close()

    def delete_catalogue_by_id(self, catalogue_id: int) -> bool:
        """
        Delete a catalogue record by its ID.
        """
        logger.debug(f"Deleting catalogue with ID: {catalogue_id}")
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM catalogue WHERE catalogue_id = %s", (catalogue_id,))
            conn.commit()
            success = cursor.rowcount > 0
            if success:
                logger.info(f"Catalogue with ID {catalogue_id} deleted successfully")
            else:
                logger.warning(f"No catalogue found to delete with ID: {catalogue_id}")
            return success
        except Exception as e:
            logger.exception(f"Error deleting catalogue with ID {catalogue_id}")
            raise
        finally:
            cursor.close()
            conn.close()

    def update_catalogue_by_id(self, catalogue_id: int, catalogue: catalogue) -> int:
        """
        Update an existing catalogue by its ID.
        """
        logger.debug(f"Updating catalogue ID {catalogue_id} with data: {catalogue}")
        try:
            conn = get_connection()
            cursor = conn.cursor()

            query = """
            UPDATE catalogue
            SET catalogue_name = %s,
                catalogue_description = %s,
                effective_from = %s,
                effective_to = %s,
                status = %s
            WHERE catalogue_id = %s
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
            logger.info(f"Catalogue ID {catalogue_id} updated. Rows affected: {row_count}")
            return row_count
        except Exception as e:
            logger.exception(f"Error updating catalogue with ID {catalogue_id}")
            raise
        finally:
            cursor.close()
            conn.close()
