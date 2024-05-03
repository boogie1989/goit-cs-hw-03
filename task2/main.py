from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure


def create_cat(col, name, age, features):
    """Insert a new cat document into the 'cats' collection."""
    try:
        cat_document = {
            "name": name,
            "age": age,
            "features": features
        }
        result = col.insert_one(cat_document)
        if result.inserted_id:
            print(f"New cat created with _id: {result.inserted_id}")
    except OperationFailure as e:
        print(f"Error inserting data: {e}")


def read_all_cats(col):
    """Reading: Output all records from the collection"""
    try:
        cats = col.find()
        for cat in cats:
            print(cat)
    except OperationFailure as e:
        print(f"Error reading data: {e}")


def read_cat_by_name(col, name):
    """Reading: Output data about a cat by name"""
    try:
        cat = col.find_one({"name": name})
        if cat:
            print(cat)
        else:
            print("No cat found with that name.")
    except OperationFailure as e:
        print(f"Error reading data: {e}")


def update_cat_age(col, name, new_age):
    """Updating: Change the age of a cat by name"""
    try:
        result = col.update_one({"name": name}, {"$set": {"age": new_age}})
        if result.modified_count > 0:
            print("Cat age updated successfully.")
        else:
            print("No updates made.")
    except OperationFailure as e:
        print(f"Error updating data: {e}")


def add_feature_to_cat(col, name, feature):
    """Updating: Adding a new feature to a cat"""
    try:
        result = col.update_one(
            {"name": name}, {"$addToSet": {"features": feature}})
        if result.modified_count > 0:
            print("Feature added successfully.")
        else:
            print("No feature added.")
    except OperationFailure as e:
        print(f"Error updating data: {e}")


def delete_cat_by_name(col, name):
    """Deletion: Deleting a cat by name"""
    try:
        result = col.delete_one({"name": name})
        if result.deleted_count > 0:
            print("Cat deleted successfully.")
        else:
            print("No cat found with that name.")
    except OperationFailure as e:
        print(f"Error deleting data: {e}")


def delete_all_cats(col):
    """Deletion: Deleting all records from the collection"""
    try:
        result = col.delete_many({})
        print(f"All cats deleted. Count: {result.deleted_count}")
    except OperationFailure as e:
        print(f"Error deleting data: {e}")


def main():
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['cat_database']
        col = db['cats']

        # Test functions
        print("Create barsik:")
        create_cat(col, "barsik", 3, ["curious", "cuddly"])

        print("Reading all cats:")
        read_all_cats(col)

        print("\nReading cat by name 'barsik':")
        read_cat_by_name(col, 'barsik')

        print("\nUpdating cat 'barsik' age to 5:")
        update_cat_age(col, 'barsik', 5)

        print("\nAdding feature 'sleepy' to 'barsik':")
        add_feature_to_cat(col, 'barsik', 'sleepy')

        print("\nDeleting cat by name 'barsik':")
        delete_cat_by_name(col, 'barsik')

        print("\nDeleting all cats:")
        delete_all_cats(col)

    except ConnectionFailure as e:
        print(f"MongoDB Connection Error: {e}")
    finally:
        client.close()
        print("MongoDB connection closed.")


if __name__ == "__main__":
    main()
