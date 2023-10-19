# sholarship.py

class Scholarship:
    def __init__(self, name, budget, numAwards, priority):
        self.name = name
        self.budget = budget
        self.numAwards = numAwards
        self.priority = priority
        self.requirements = set()

    def search_requirements(self, requirement):
        for n in self.requirements:
            if n in requirement:
                return True
        return False
    
    def add_requirement(self, requirement):
        self.requirements.append(requirement)
        return
    
    def delete_requirement(self, requirement):
        if requirement in self.requirements:
            self.requirements.discard(requirement)
            return True
        else: return False