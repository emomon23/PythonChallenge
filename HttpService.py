import asyncio
from LPLogger import LPLogger;
import httpx
import jsonpickle

class HttpService:
    def __init__(self):
        self.logger = LPLogger()

    def __chunkUrlList__(self, bigListOfUrls):
        result = [];
        innerList = []
        for url in bigListOfUrls:
            innerList.append(url)
            if len(innerList) == 10:
                result.append(innerList)
                innerList = []

        if (len(innerList) > 0):
            result.append(innerList)

        return result;

    async def __httpGet__(self, url, iterator = 0):
        async with httpx.AsyncClient() as client:
            if iterator > 0:
                self.logger.log("Retry logic on httpGet for url: {url}".format(url=url))

            try:
                response = await client.get(url, timeout=1)
                if response.status_code != 200:
                    iterator+=1;
                    return await self.__httpGet__(url, iterator)

                return jsonpickle.decode(response.text)

            except BaseException as err:
                if (iterator == 4):
                    self.logger.logError(err)
                    raise err

                iterator+=1
                return await self.__httpGet__(url, iterator)

    async def __httpPost__(self, url, data, iterator = 0):
        async with httpx.AsyncClient() as client:
            if iterator > 0:
                self.logger.log("Retry logic on httpPost for url: {url}".format(url=url))

            try:
                response = await client.post(url, data=data, timeout=1.5)
                if response.status_code != 200:
                    iterator+=1;
                    return await self.__httpPost__(url, data, iterator)

                return jsonpickle.decode(response.text)

            except BaseException as err:
                if (iterator == 4):
                    self.logger.logError(err)
                    raise err

                iterator+=1
                return await self.__httpPost__(url, data, iterator)

    async def get(self, url):
        return await self.__httpGet__(url)

    async def post(self, url, data):
        return await self.__httpPost__(url, data)

    async def gather(self, urlList):
        chunkedUrlList = self.__chunkUrlList__(urlList);
        result = []
        for urlSubList in chunkedUrlList:
           subResults = await asyncio.gather(*map(self.get, urlSubList))
           result = result + subResults;

        return result;
