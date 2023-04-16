import json

class Budget:
    def __init__(self):
        try:
            with open("budget.json", "r") as f:
                self.budget = json.load(f)
        except FileNotFoundError:
            self.budget = []

    def all(self):
        return self.budget

    def get(self, id):
        item = [item for item in self.all() if item['id'] == id]
        if item:
            return item[0]
        return []

    def create(self, data):
        self.budget.append(data)
        self.save_all()

    def save_all(self):
        with open("budget.json", "w") as f:
            json.dump(self.budget, f)

    def delete(self, id):
        item = self.get(id)
        if item:
            self.budget.remove(item)
            self.save_all()
            return True
        return False
    
    def update(self, id, data):
        item = self.get(id)
        if item:
            index = self.budget.index(item)
            self.budget[index] = data
            self.save_all()
            return True
        return False
        
budget = Budget()
