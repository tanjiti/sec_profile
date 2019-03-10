
# -*- coding: utf-8 -*-

"""
图像搜索
"""

import re
import sys
import math
import time
from .base import AipBase
from .base import base64
from .base import json
from .base import urlencode
from .base import quote

class AipImageSearch(AipBase):

    """
    图像搜索
    """

    __sameHqAddUrl = 'https://aip.baidubce.com/rest/2.0/realtime_search/same_hq/add'

    __sameHqSearchUrl = 'https://aip.baidubce.com/rest/2.0/realtime_search/same_hq/search'

    __sameHqUpdateUrl = 'https://aip.baidubce.com/rest/2.0/realtime_search/same_hq/update'

    __sameHqDeleteUrl = 'https://aip.baidubce.com/rest/2.0/realtime_search/same_hq/delete'

    __similarAddUrl = 'https://aip.baidubce.com/rest/2.0/image-classify/v1/realtime_search/similar/add'

    __similarSearchUrl = 'https://aip.baidubce.com/rest/2.0/image-classify/v1/realtime_search/similar/search'

    __similarUpdateUrl = 'https://aip.baidubce.com/rest/2.0/image-classify/v1/realtime_search/similar/update'

    __similarDeleteUrl = 'https://aip.baidubce.com/rest/2.0/image-classify/v1/realtime_search/similar/delete'

    __productAddUrl = 'https://aip.baidubce.com/rest/2.0/image-classify/v1/realtime_search/product/add'

    __productSearchUrl = 'https://aip.baidubce.com/rest/2.0/image-classify/v1/realtime_search/product/search'

    __productUpdateUrl = 'https://aip.baidubce.com/rest/2.0/image-classify/v1/realtime_search/product/update'

    __productDeleteUrl = 'https://aip.baidubce.com/rest/2.0/image-classify/v1/realtime_search/product/delete'

    
    def sameHqAdd(self, image, options=None):
        """
            相同图检索—入库
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__sameHqAddUrl, data)
    
    def sameHqAddUrl(self, url, options=None):
        """
            相同图检索—入库
        """
        options = options or {}

        data = {}
        data['url'] = url

        data.update(options)

        return self._request(self.__sameHqAddUrl, data)
    
    def sameHqSearch(self, image, options=None):
        """
            相同图检索—检索
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__sameHqSearchUrl, data)
    
    def sameHqSearchUrl(self, url, options=None):
        """
            相同图检索—检索
        """
        options = options or {}

        data = {}
        data['url'] = url

        data.update(options)

        return self._request(self.__sameHqSearchUrl, data)
    
    def sameHqUpdate(self, image, options=None):
        """
            相同图检索—更新
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__sameHqUpdateUrl, data)
    
    def sameHqUpdateUrl(self, url, options=None):
        """
            相同图检索—更新
        """
        options = options or {}

        data = {}
        data['url'] = url

        data.update(options)

        return self._request(self.__sameHqUpdateUrl, data)
    
    def sameHqUpdateContSign(self, cont_sign, options=None):
        """
            相同图检索—更新
        """
        options = options or {}

        data = {}
        data['cont_sign'] = cont_sign

        data.update(options)

        return self._request(self.__sameHqUpdateUrl, data)
    
    def sameHqDeleteByImage(self, image, options=None):
        """
            相同图检索—删除
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__sameHqDeleteUrl, data)
    
    def sameHqDeleteByUrl(self, url, options=None):
        """
            相同图检索—删除
        """
        options = options or {}

        data = {}
        data['url'] = url

        data.update(options)

        return self._request(self.__sameHqDeleteUrl, data)
    
    def sameHqDeleteBySign(self, cont_sign, options=None):
        """
            相同图检索—删除
        """
        options = options or {}

        data = {}
        data['cont_sign'] = cont_sign

        data.update(options)

        return self._request(self.__sameHqDeleteUrl, data)
    
    def similarAdd(self, image, options=None):
        """
            相似图检索—入库
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__similarAddUrl, data)
    
    def similarAddUrl(self, url, options=None):
        """
            相似图检索—入库
        """
        options = options or {}

        data = {}
        data['url'] = url

        data.update(options)

        return self._request(self.__similarAddUrl, data)
    
    def similarSearch(self, image, options=None):
        """
            相似图检索—检索
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__similarSearchUrl, data)
    
    def similarSearchUrl(self, url, options=None):
        """
            相似图检索—检索
        """
        options = options or {}

        data = {}
        data['url'] = url

        data.update(options)

        return self._request(self.__similarSearchUrl, data)
    
    def similarUpdate(self, image, options=None):
        """
            相似图检索—更新
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__similarUpdateUrl, data)
    
    def similarUpdateUrl(self, url, options=None):
        """
            相似图检索—更新
        """
        options = options or {}

        data = {}
        data['url'] = url

        data.update(options)

        return self._request(self.__similarUpdateUrl, data)
    
    def similarUpdateContSign(self, cont_sign, options=None):
        """
            相似图检索—更新
        """
        options = options or {}

        data = {}
        data['cont_sign'] = cont_sign

        data.update(options)

        return self._request(self.__similarUpdateUrl, data)
    
    def similarDeleteByImage(self, image, options=None):
        """
            相似图检索—删除
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__similarDeleteUrl, data)
    
    def similarDeleteByUrl(self, url, options=None):
        """
            相似图检索—删除
        """
        options = options or {}

        data = {}
        data['url'] = url

        data.update(options)

        return self._request(self.__similarDeleteUrl, data)
    
    def similarDeleteBySign(self, cont_sign, options=None):
        """
            相似图检索—删除
        """
        options = options or {}

        data = {}
        data['cont_sign'] = cont_sign

        data.update(options)

        return self._request(self.__similarDeleteUrl, data)
    
    def productAdd(self, image, options=None):
        """
            商品检索—入库
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__productAddUrl, data)
    
    def productAddUrl(self, url, options=None):
        """
            商品检索—入库
        """
        options = options or {}

        data = {}
        data['url'] = url

        data.update(options)

        return self._request(self.__productAddUrl, data)
    
    def productSearch(self, image, options=None):
        """
            商品检索—检索
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__productSearchUrl, data)
    
    def productSearchUrl(self, url, options=None):
        """
            商品检索—检索
        """
        options = options or {}

        data = {}
        data['url'] = url

        data.update(options)

        return self._request(self.__productSearchUrl, data)
    
    def productUpdate(self, image, options=None):
        """
            商品检索—更新
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__productUpdateUrl, data)
    
    def productUpdateUrl(self, url, options=None):
        """
            商品检索—更新
        """
        options = options or {}

        data = {}
        data['url'] = url

        data.update(options)

        return self._request(self.__productUpdateUrl, data)
    
    def productUpdateContSign(self, cont_sign, options=None):
        """
            商品检索—更新
        """
        options = options or {}

        data = {}
        data['cont_sign'] = cont_sign

        data.update(options)

        return self._request(self.__productUpdateUrl, data)
    
    def productDeleteByImage(self, image, options=None):
        """
            商品检索—删除
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__productDeleteUrl, data)
    
    def productDeleteByUrl(self, url, options=None):
        """
            商品检索—删除
        """
        options = options or {}

        data = {}
        data['url'] = url

        data.update(options)

        return self._request(self.__productDeleteUrl, data)
    
    def productDeleteBySign(self, cont_sign, options=None):
        """
            商品检索—删除
        """
        options = options or {}

        data = {}
        data['cont_sign'] = cont_sign

        data.update(options)

        return self._request(self.__productDeleteUrl, data)
    
