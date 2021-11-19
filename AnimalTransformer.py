import copy
from datetime import datetime, timezone

class AnimalTransformer:
    def __init__(self):
        self.transformedAnimals = [];

    def transformAnimal(self, originalAnimal):
        if (originalAnimal == None):
            return;

        animalWasTransformed = False
        animal = copy.copy(originalAnimal)

        if isinstance(animal.friends, str):
            animal.friends = animal.friends.split(',')
            animalWasTransformed = True

        if isinstance(animal.born_at, int):
            animal.born_at = datetime.fromtimestamp(animal.born_at / 1000, timezone.utc).isoformat()
            animalWasTransformed = True

        if animalWasTransformed == True:
            self.transformedAnimals.append(animal)


    def transformedCount(self):
        return len(self.transformedAnimals)


