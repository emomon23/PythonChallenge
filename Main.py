import asyncio
from LPLogger import LPLogger
from AnimalService import AnimalService
from AnimalTransformer import AnimalTransformer

async def main():
    # Singleton for singletons sake (no good reason, just felt like doing it for this review)
    animalService = AnimalService.getInstance()
    animalTransformer = AnimalTransformer()
    logger = LPLogger(3)

    # ***************************************************************************************
    # Thought about doing a while loop with a animalService.fetchNextPageOfDetails() method,
    # that MIGHT have been more efficient or less strain on the server, but since
    # I'm hosting the server, that's not a concern I have for this client
    # **************************************************************************************
    liteAnimalList = await animalService.fetchAllAnimals();
    animalDetails = await animalService.fetchAnimalDetails(liteAnimalList);

    for originalAnimalDetail in animalDetails:
        animalTransformer.transformAnimal(originalAnimal=originalAnimalDetail)

    transformedCount = animalTransformer.transformedCount();
    logger.log("Transformed a total of {transformedCount} animals (born_at and friends).  About to SAVE them all!".format(transformedCount = transformedCount), 2)

    await animalService.saveAnimals(animalTransformer.transformedAnimals)
    logger.log("...Application Finished...", 1)


# Python 3.7+
asyncio.run(main())