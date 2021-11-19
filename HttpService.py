import asyncio
import jsonpickle

class HttpService:

    def __httpGet__(self, url, iterator = 0):
        return ""

    def __httpPost__(self, url, jsonString, iterator = 0):
        return "";

    def get(self, url):
        return await __httpGet(url)

    def post(self, url, data):
        return await __httpPost__(self, url, data);
