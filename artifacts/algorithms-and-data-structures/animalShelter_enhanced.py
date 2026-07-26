from pymongo import MongoClient


class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, username, password):
        """
        Initialize the MongoDB connection.

        Parameters:
            username (str): MongoDB username.
            password (str): MongoDB password.
        """
        try:
            self.client = MongoClient("mongodb://localhost:27017")
            self.database = self.client["AAC"]

        except Exception as e:
            raise ConnectionError (
                f"Failed to connect to the MongoDB database: {e}"
            )

# Complete this create method to implement the C in CRUD.
    def create(self, data):
        """
        Insert a new animal record into the databse.

        Parameters:
            data (dict): The animal information to insert.

        Returns:
            bool: True when the record is inserted successfully.

        Raises:
            ValueError: If data is missing or is not a dictionary.
            RuntimeError: If the databse operation fails.
        """

        if not isinstance(data, dict) or not data:
            raise ValueError(
                "A non-empty dictionary is required to create an animal record."
            )
        
        try:
            result = self.database.animals.insert_one(data)
            return result.acknowledged

        except Exception as error:
            raise RuntimeError(
                f"Unable to create the animal record: {error}"
            ) from error

# Create method to implement the R in CRUD.
    def read(self, criteria=None):
        """
        Retrieve animal records from the database.

        Parameters:
            criteria (dict, optional): MongoDB query used to filter records
                If no criteria is provided, all records are returned.

        Returns:
            list: A list of animal records without MongoDB object IDs.
        
        Raises:
            ValueError: If criteria is provided but is not a dictionary.
            RuntimeError: If the databse operation fails.
        """
        if criteria is not None and not isinstance(criteria, dict):
            raise ValueError("Search criteria must be provided as a dictionary.")

        try: 
            query = criteria if criteria is not None else {}

            records = self.database.animals.find(
                query,
                {"_id": False}
            )

            return list(records)

        except Exception as error:
            raise RuntimeError(
                f"Unable to retreive animal records: {error}"
            ) from error
    
# Create method to implement the U in CRUD.
    def update(self, criteria, changes):
        """
        Update animal records that match the provided criteria.

        Parameters:
            criteria (dict): MongoDB query used to identify records.
            changes (dict): Fields and values to update.

        Returns:
            dict: Information about how many records were matched and modified.

        Raises:
            ValueError: If criteria or changes is missing or invalid.
            RuntimeError: If the database operation fails.
        """
        if not isinstance(criteria, dict) or not criteria:
            raise ValueError(
                "A non-empty dictionary is required for the update criteria"
            )

        if not isinstance(changes, dict) or not changes:
            raise ValueError(
                "A non-empty dictionary is required for the update changes."
            )

        try:
            result = self.database.animals.update_many(
                criteria,
                {"$set": changes}
            )

            return {
                "matched_count": result.matched_count,
                "modified_count": result.modified_count
            }

        except Exception as error:
            raise RuntimeError(
                f"Unable to update animal records: {error}"
            ) from error

# Create method to implement the D in CRUD.
    def delete(self, criteria):
        """
        Delete animal records that match the provided criteria.

        Parameters:
            criteria (dict): MongoDB query used to identify records.

        Returns:
            dict: Information about how many records were deleted.

        Raises:
            ValueError: If criteria is missing or invalid.
            RuntimeError: If the database operation fails.
        """
        if not isinstance(criteria, dict) or not criteria:
            raise ValueError(
                "A non-empty dictionary is required for the delete criteria"
            )

        try:
            result = self.database.animals.delete_many(criteria)

            return {
                "deleted_count": result.deleted_count
            }
        except Exception as error:
            raise RuntimeError(
                f"Unable to delete animal records: {error}"
            ) from error