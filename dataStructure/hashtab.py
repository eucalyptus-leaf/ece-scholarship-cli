# hashtab.py

# maintab = new(Hashtab)
# ...
# student = new(Student)
# maintab.insert(student.student_id, student)
# ... do this recusively for all students


class Hashtab:
    def __init__(self, size=100):
        self.size = size
        self.table = [[] for _ in range(size)]
        self.count = 0
        self.load_factor = 0.7

    def _hash(self, key):
        return hash(key) % self.size

    def _resize(self, new_size):
        old_table = self.table
        self.size = new_size
        self.table = [[] for _ in range(new_size)]
        for bucket in old_table:
            for key, value in bucket:
                self.insert(key, value)

    def insert(self, key, value):
        if self.count / self.size >= self.load_factor:
            self._resize(self.size * 2)
        index = self._hash(key)
        bucket = self.table[index]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self.count += 1

    def search(self, key):
        index = self._hash(key)
        bucket = self.table[index]
        for k, v in bucket:
            if k == key:
                return v
        return None

    def delete(self, key):
        index = self._hash(key)
        bucket = self.table[index]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.count -= 1
                if self.count / self.size <= self.load_factor / 4:
                    new_size = max(self.size // 2, 10)
                    self._resize(new_size)
                return

    
class ScholarshipSystem():
    department_budget = -1
    def __init__(self, capacity=100):
        working_budget = -1
        student_table = Hashtab(capacity)
        scholarship_table = Hashtab(capacity)

