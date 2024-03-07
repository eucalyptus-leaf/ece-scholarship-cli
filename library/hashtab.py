# hashtab.py

# maintab = new(Hashtab)
# ...
# student = new(Student)
# maintab.insert(student.student_id, student)
# ... do this recusively for all students

class Hashtab:
    # A hash table data structure made up of a list of dictorionaries. Include a hash function to hash the keys.
    def __init__(self, size=100):
        self.table = [dict() for _ in range(100)]
        self.size = size
        self.count = 0
        self.load_factor = 0.70

    def hash(self, key):
        # A hash function that takes a key and returns the hash value.
        return key % self.size
    
    def resize(self, new_size):
        # Resizes the hash table to a new size.
        new_table = [dict() for _ in range(new_size)]
        for i in range(self.size):
            for key in self.table[i]:
                index = self.hash(key)
                new_table[index][key] = self.table[i][key]
        self.table = new_table
        self.size = new_size
        return True
    
    def insert(self, key, value):
        # Inserts a key-value pair into the hash table and resizes if the load factor is exceeded.
        index = self.hash(key)
        if key in self.table[index]:
            return False
        self.table[index][key] = value
        self.count += 1
        if self.count / self.size > self.load_factor:
            self.resize(self.size * 2)
        return True
    
    
    def remove(self, key):
        # Removes a key-value pair from the hash table and rezises if structure has become too sparse.
        index = self.hash(key)
        if key not in self.table[index]:
            return False
        self.table[index].pop(key)
        self.count -= 1
        if self.count / self.size < 0.10:
            self.resize(self.size // 2)
        return True
    
    
    def search(self, key):
        # Searches for a key in the hash table.
        index = self.hash(key)
        return key in self.table[index]
    
    def get(self, key):
        # Returns the value associated with a key in the hash table if it exists. Otherwise, returns None.
        index = self.hash(key)
        if key in self.table[index]:
            return self.table[index][key]
        return None
    
    def __str__(self):
        # Returns a string representation of the hash table.
        return str(self.table)
    
    def __len__(self):
        # Returns the number of key-value pairs in the hash table.
        return self.count
    
    def __contains__(self, key):
        # Returns True if a key is in the hash table, False otherwise.
        return self.search(key)
    
    def __getitem__(self, key):
        # Returns the value associated with a key in the hash table.
        return self.get(key)
    
    def __setitem__(self, key, value):
        # Inserts a key-value pair into the hash table.
        self.insert(key, value)

    def __iter__(self):
        # Iterate over each bucket (which is a dictionary) in the hash table
        for bucket in self.table:
            # Iterate over each key-value pair in the bucket
            for key, value in bucket.items():
                yield value