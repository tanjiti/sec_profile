
# -*- coding: utf-8 -*-

"""
图像识别
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

class AipImageClassify(AipBase):

    """
    图像识别
    """

    __advancedGeneralUrl = 'https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general'

    __dishDetectUrl = 'https://aip.baidubce.com/rest/2.0/image-classify/v2/dish'

    __carDetectUrl = 'https://aip.baidubce.com/rest/2.0/image-classify/v1/car'

    __logoSearchUrl = 'https://aip.baidubce.com/rest/2.0/image-classify/v2/logo'

    __logoAddUrl = 'https://aip.baidubce.com/rest/2.0/realtime_search/v1/logo/add'

    __logoDeleteUrl = 'https://aip.baidubce.com/rest/2.0/realtime_search/v1/logo/delete'

    __animalDetectUrl = 'https://aip.baidubce.com/rest/2.0/image-classify/v1/animal'

    __plantDetectUrl = 'https://aip.baidubce.com/rest/2.0/image-classify/v1/plant'

    __objectDetectUrl = 'https://aip.baidubce.com/rest/2.0/image-classify/v1/object_detect'

    __landmarkUrl = 'https://aip.baidubce.com/rest/2.0/image-classify/v1/landmark'

    
    def advancedGeneral(self, image, options=None):
        """
            通用物体识别
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__advancedGeneralUrl, data)
    
    def dishDetect(self, image, options=None):
        """
            菜品识别
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__dishDetectUrl, data)
    
    def carDetect(self, image, options=None):
        """
            车辆识别
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__carDetectUrl, data)
    
    def logoSearch(self, image, options=None):
        """
            logo商标识别
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__logoSearchUrl, data)
    
    def logoAdd(self, image, brief, options=None):
        """
            logo商标识别—添加
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()
        data['brief'] = brief

        data.update(options)

        return self._request(self.__logoAddUrl, data)
    
    def logoDeleteByImage(self, image, options=None):
        """
            logo商标识别—删除
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__logoDeleteUrl, data)
    
    def logoDeleteBySign(self, cont_sign, options=None):
        """
            logo商标识别—删除
        """
        options = options or {}

        data = {}
        data['cont_sign'] = cont_sign

        data.update(options)

        return self._request(self.__logoDeleteUrl, data)
    
    def animalDetect(self, image, options=None):
        """
            动物识别
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__animalDetectUrl, data)
    
    def plantDetect(self, image, options=None):
        """
            植物识别
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__plantDetectUrl, data)
    
    def objectDetect(self, image, options=None):
        """
            图像主体检测
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__objectDetectUrl, data)
    
    def landmark(self, image, options=None):
        """
            地标识别
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__landmarkUrl, data)
    