import asyncio
import jsonpickle
from HttpService import HttpService
from LPLogger import LPLogger

class Animal(object):
    pass

class AnimalService:
    __static_instance__ = None;

    def __init__(self, httpService = None):
        self.logger = LPLogger()

        # Poormans IOC
        if httpService == None:
            self.httpService = HttpService()
        else:
            self.httpService = httpService

        self.animals = [];
        self.homeUrl = 'http://localhost:3123/animals/v1/home'
        self.animalUrl = 'http://localhost:3123/animals/v1/animals'

    def __createFetchUrlList(self, totalPages):
        result = []
        for p in range(2, totalPages):
            result.append(f'{self.animalUrl}?page={p}')

        return result;

    def __deserializePage(self, page):
        for item in page["items"]:
            animal = Animal()
            animal.name = item["name"];
            animal.id = item["id"];
            animal.born_at = item["born_at"]

            self.animals.append(animal);

    def __deserializePages(self, pages):
        for page in pages:
           self.__deserializePage(page);

    def __chunkAnimalList(self, animals):
        # this could probably be refactored to be more efficient, less code, intend to revisit
        CHUNK_SIZE = 100;
        result = [];
        sublist = [];

        for animal in animals:
            sublist.append(animal)
            if len(sublist) == CHUNK_SIZE:
                result.append(sublist)
                sublist = [];

        result.append(sublist)
        return result;


    def __deserializeAnimal(self, dict):
        animal = Animal()
        animal.name = dict["name"]
        animal.id = dict["id"]
        animal.born_at = dict["born_at"]
        animal.friends = dict["friends"]

        return animal;

    async def __postChuckedAnimals(self, chunkedAnimals):
        httpService = self.httpService;

        jsonAnimals = jsonpickle.encode(chunkedAnimals, unpicklable=False)

        result = await httpService.post(self.homeUrl, jsonAnimals);
        message = result["message"]
        self.logger.log(message)

    async def fetchAllAnimals(self):
        httpService = self.httpService;
        page1 = await httpService.get(self.animalUrl)
        totalPages = page1["total_pages"]

        self.__deserializePage(page1);

        urlList = self.__createFetchUrlList(totalPages);

        self.logger.log("About to gather {totalPages} pages of Animals Asynchronous, this will take a minute...".format(totalPages = totalPages))
        allPages = await httpService.gather(urlList);

        self.__deserializePages(allPages)

        totalAnimals = len(self.animals)
        self.logger.log("Done fetching animal SUMMARIES!  Retrieved LIST of {totalAnimals} Animal summaries".format(totalAnimals = totalAnimals))

        return self.animals;

    async def fetchAnimal(self, animalId):
        httpService = self.httpService;
        url = "{baseUrl}/{animalId}".format(baseUrl = self.animalUrl, animalId = animalId)

        result = await httpService.get(url)
        animal = self.__deserializeAnimal(result)

        return animal;

    async def saveAnimals(self, animals):
        chuckedList = self.__chunkAnimalList(animals);
        await asyncio.gather(*map(self.__postChuckedAnimals, chuckedList))
        self.logger.log("Helped a total of {total} find home".format(total=len(animals)), 2)


    async def fetchAnimalDetails(self, liteAnimalList):
        totalUrls = []
        results = []

        for liteAnimal in liteAnimalList:
            totalUrls.append("{baseUrl}/{id}".format(baseUrl = self.animalUrl, id = liteAnimal.id))

        totalDetailUrls = len(totalUrls);

        self.logger.log("About to fetch Animal DETAILS for a total of {TA} animals (10 at a time) - This will take even longer...".format(TA=totalDetailUrls), 2)

        httpGetResults = await self.httpService.gather(totalUrls);

        for httpAnimal in httpGetResults:
            animal = self.__deserializeAnimal(httpAnimal)
            results.append(animal)

        return results;

    @staticmethod
    def getInstance():
        if AnimalService.__static_instance__ == None:
            AnimalService.__static_instance__ = AnimalService()

        return AnimalService.__static_instance__


