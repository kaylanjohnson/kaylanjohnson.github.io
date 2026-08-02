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

    def get_top_breeds(self, limit=5):
        """
        Return the most common animal breeds using a MongoDB
        aggregation pipeline.

        Parameters:
            limit (int): Maximum number of breeds to return.

        Returns:
            list: Breed names and their record counts.

        Raises:
            ValueError: If limit is not a positive integer.
            RuntimeError: If the aggregation operation fails.
        """
        if not isinstance(limit, int) or limit <= 0:
            raise ValueError(
                "The breed report limit must be a positive integer."
            )

        pipeline = [
            {
                "$match": {
                    "breed": {"$nin": [None, ""]}
                }
            },
            {
                "$group": {
                    "_id": "$breed",
                    "count": {"$sum": 1}
                }
            },
            {
                "$sort": {
                    "count": -1,
                    "_id": 1
                }
            },
            {
                "$limit": limit
            },
            {
                "$project": {
                    "_id": False,
                    "breed": "$_id",
                    "count": True
                }
            }
        ]

        try:
            return list(
                self.database.animals.aggregate(pipeline)
            )

        except Exception as error:
            raise RuntimeError(
                f"Unable to generate the breed report: {error}"
            ) from error

    def get_database_summary(self):
        """
        Return basic animal totals from MongoDB.

        Returns:
            dict: Total animals, dogs, and cats.

        Raises:
            RuntimeError: If the database operation fails.
        """
        try:
            total_animals = self.database.animals.count_documents({})

            pipeline = [
                {
                    "$match": {
                        "animal_type": {"$in": ["Dog", "Cat"]}
                    }
                },
                {
                    "$group": {
                        "_id": "$animal_type",
                        "count": {"$sum": 1}
                    }
                }
            ]

            results = list(
                self.database.animals.aggregate(pipeline)
            )

            animal_counts = {
                result["_id"]: result["count"]
                for result in results
            }

            return {
                "total_animals": total_animals,
                "dogs": animal_counts.get("Dog", 0),
                "cats": animal_counts.get("Cat", 0)
            }

        except Exception as error:
            raise RuntimeError(
                f"Unable to generate the database summary: {error}"
            ) from error

    def get_outcome_summary(self, limit=5):
        """
        Return the most common animal outcome types using a MongoDB
        aggregation pipeline.

        Parameters:
            limit (int): Maximum number of outcome types to return.

        Returns:
            list: Outcome types and their record counts.

        Raises:
            ValueError: If limit is not a positive integer.
            RuntimeError: If the aggregation operation fails.
        """
        if not isinstance(limit, int) or limit <= 0:
            raise ValueError(
                "The outcome report limit must be a positive integer."
            )

        pipeline = [
            {
                "$match": {
                    "outcome_type": {"$nin": [None, ""]}
                }
            },
            {
                "$group": {
                    "_id": "$outcome_type",
                    "count": {"$sum": 1}
                }
            },
            {
                "$sort": {
                    "count": -1,
                    "_id": 1
                }
            },
            {
                "$limit": limit
            },
            {
                "$project": {
                    "_id": False,
                    "outcome_type": "$_id",
                    "count": True
                }
            }
        ]

        try:
            return list(
                self.database.animals.aggregate(pipeline)
            )

        except Exception as error:
            raise RuntimeError(
                f"Unable to generate the outcome report: {error}"
            ) from error
        
    def create_database_indexes(self):
        """
        Create indexes for fields frequently used in dashboard
        searches, filters, sorting, and database reports.

        Returns:
            list: Names of the indexes created.

        Raises:
            RuntimeError: If index creation fails.
        """
        try:
            collection = self.database.animals

            index_names = [
                collection.create_index("animal_type"),
                collection.create_index("breed"),
                collection.create_index("outcome_type"),
                collection.create_index("sex_upon_outcome"),
                collection.create_index("age_upon_outcome_in_weeks")
            ]

            return index_names

        except Exception as error:
            raise RuntimeError(
                f"Unable to create database indexes: {error}"
            ) from error