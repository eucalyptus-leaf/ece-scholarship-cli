# hashtab.py

# maintab = new(Hashtab)
# ...
# student = new(Student)
# maintab.insert(student.student_id, student)
# ... do this recusively for all students

class Hashtab:
    def __init__(self):
        self.table = {}

    def insert(self, key, value):
        self.table[key] = value
        return True

    def add(self, key, value):
        """Adds or updates a key-value pair in the hash table."""
        self.table[key] = value

    def get(self, key):
        """Retrieves the value for a given key from the hash table, or a default value None if the key is not found.
            Args: key: The key to look up in the hash table.
            Returns: The value for the key if the key is found, otherwise None.
        """
        return self.table.get(key)

    def remove(self, key):
        """Removes a key from the hash table if it exists and returns its value, or None if the key is not found."""
        return self.table.pop(key, None)

    def contains(self, key):
        """Checks if the hash table contains a specific key."""
        return key in self.table
    
    def search(self, key):
        # Searches for a key in the table.
        return key in self.table

    def __getitem__(self, key):
        """Allows for bracket notation access, safely returning None if key not found."""
        return self.get(key)

    def __setitem__(self, key, value):
        """Allows for bracket notation setting (e.g., hashtable[key] = value)."""
        self.add(key, value)

    def __delitem__(self, key):
        """Allows for bracket notation deletion (e.g., del hashtable[key])."""
        if key in self.table:
            del self.table[key]
        else:
            raise KeyError(f"Key {key} not found")

    def __len__(self):
        """Returns the number of items in the hash table."""
        return len(self.table)

    def __iter__(self):
        """Returns an iterator over the keys in the hash table."""
        return iter(self.table.values())

    def __contains__(self, key):
        """Implements membership testing using 'in'."""
        return key in self.table

    def __str__(self):
        """Returns a string representation of the hash table."""
        return str(self.table)