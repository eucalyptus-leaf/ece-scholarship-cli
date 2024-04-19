# hashtab.py

# maintab = new(Hashtab)
# ...
# student = new(Student)
# maintab.insert(student.student_id, student)
# ... do this recusively for all students

class Hashtab:
    def __init__(self):
        """ Description: Initialize new hash table with empty dictionary.
            Args: None
            Returns: None
            Error State: None
        """
        self.table = {}

    def insert(self, key, value):
        """ Description: Insert pair into hash table.
            Args: key: The key to look up in the hash table
                  value: The value associated with the key
            Returns: Returns true if after sucessfully inserting
            Error State: None
        """
        self.table[key] = value
        return True

    def add(self, key, value):
        """ Description: Adds or updates a key-value pair in the hash table.
            Args: key: The key to look up in the hash table.
                  value: The value associated with the key
            Returns: None
            Error State: if key is None, raise ValueError
        """
        self.table[key] = value

    def get(self, key):
        """ Description: Retrieves the value for a given key from the hash table, or a default value None if the key is not found.
            Args: key: The key to look up in the hash table.
            Returns: The value for the key if the key is found, otherwise None.
            Error State: if key is None, raise ValueError
        """
        return self.table.get(key)

    def remove(self, key):
        """ Description: Removes a key from the hash table if it exists and returns its value.
            Args: key: The key to look up in the hash table.
            Returns: Returns value associated with removed key, otherwise None
            Error State: None
        """
        return self.table.pop(key, None)

    def contains(self, key):
        """ Description: Checks if the hash table contains a specific key.
            Args: key: The key to look up in the hash table.
            Returns: True if key exists, otherwise False
            Error State: None
        """
        return key in self.table
    
    def search(self, key):
        """ Description: Searches for a key in the table.
            Args: key: The key to look up in the hash table.
            Returns: True if the key is found in the hash table, otherwise False.
            Error State: None
        """
        return key in self.table

    def __getitem__(self, key):
        """ Description: Allows for bracket notation access, safely returning None if key not found.
            Args: key: The key to look up in the hash table.
            Returns: The value associated with the key if the key is found in the hash table, otherwise None.
            Error State: None
        """
        return self.get(key)

    def __setitem__(self, key, value):
        """ Description: Allows for bracket notation setting (e.g., hashtable[key] = value).
            Args: key: The key to look up in the hash table.
                  value: The value associated with the key
            Returns: None
            Error State: None
        """
        self.add(key, value)

    def __delitem__(self, key):
        """ Description: Allows for bracket notation deletion (e.g., del hashtable[key]).
            Args: key: The key to look up in the hash table.
            Returns: None
            Error State: Raises KeyError is key is not found
        """
        if key in self.table:
            del self.table[key]
        else:
            raise KeyError(f"Key {key} not found")

    def __len__(self):
        """ Description: Returns the number of items in the hash table.
            Args: None
            Returns: Number of key value pairs
            Error State: None
        """
        return len(self.table)
    
    def keys(self):
        """ Description: Returns a list of keys in the hash table.
            Args: None
            Returns: List of keys in hash table
            Error State: None
        """
        return list(self.table.keys())

    def __iter__(self):
        """ Description: Returns an iterator over the keys in the hash table.
            Args: None
            Returns: Iterator over keys in hash table
            Error State: None
        """
        return iter(self.table.values())

    def __contains__(self, key):
        """ Description: Implements membership testing using 'in'.
            Args: key: The key to look up in the hash table.
            Returns: True if key exists in hash table, otherwise False
            Error State: None
        """
        return key in self.table

    def __str__(self):
        """ Description: Returns a string representation of the hash table.
            Args: None
            Returns: String representation of the hash table
            Error State: None
        """
        return str(self.table)
