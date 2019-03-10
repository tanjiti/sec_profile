# -*- coding: utf-8 -*-

import re
import sys
from .base import AipBase
from .base import base64
from .base import json
from .base import urlencode
from .base import quote

class AipImageCensor(AipBase):
    """
        Aip ImageCensor
    """

    __antiPornUrl = 'https://aip.baidubce.com/rest/2.0/antiporn/v1/detect'

    __antiPornGifUrl = 'https://aip.baidubce.com/rest/2.0/antiporn/v1/detect_gif'

    __antiTerrorUrl = 'https://aip.baidubce.com/rest/2.0/antiterror/v1/detect'

    __faceAuditUrl = 'https://aip.baidubce.com/rest/2.0/solution/v1/face_audit'
    
    __imageCensorCombUrl = 'https://aip.baidubce.com/api/v1/solution/direct/img_censor'

    __imageCensorUserDefinedUrl = 'https://aip.baidubce.com/rest/2.0/solution/v1/img_censor/user_defined'

    __antiSpamUrl = 'https://aip.baidubce.com/rest/2.0/antispam/v2/spam'
    
    def antiPorn(self, image):
        """
            antiporn
        """

        data = {}
        data['image'] = base64.b64encode(image).decode()

        return self._request(self.__antiPornUrl, data)

    def antiPornGif(self, image):
        """
            antiporn gif
        """

        data = {}
        data['image'] = base64.b64encode(image).decode()

        return self._request(self.__antiPornGifUrl, data)

    def antiTerror(self, image):
        """
            antiterror
        """

        data = {}
        data['image'] = base64.b64encode(image).decode()

        return self._request(self.__antiTerrorUrl, data)

    def faceAudit(self, images, configId=''):
        """
            faceAudit
        """

        # 非数组则处理为数组
        if not isinstance(images, list):
            images = [images]

        data = {
            'configId': configId
        }

        isUrl = images[0][0:4] == 'http'
        if not isUrl:
            data['images'] = ','.join([
                base64.b64encode(image).decode() for image in images
            ])
        else:            
            data['imgUrls'] = ','.join([
                quote(url) for url in images
            ])

        return self._request(self.__faceAuditUrl, data)

    def imageCensorComb(self, image, scenes='antiporn', options=None):
        """
            imageCensorComb
        """

        options = options or {}

        if not isinstance(scenes, list):
            scenes = scenes.split(',')
        
        data = {
            'scenes': scenes,
        }

        isUrl = image.strip()[0:4] == 'http'
        if not isUrl:
            data['image'] = base64.b64encode(image).decode()
        else:
            data['imgUrl'] = image

        data.update(options)

        return self._request(self.__imageCensorCombUrl, json.dumps(data), {
            'Content-Type': 'application/json',
        })

    def imageCensorUserDefined(self, image):
        """
            imageCensorUserDefined
        """
        
        data = {}

        isUrl = image[0:4] == 'http'
        if not isUrl:
            data['image'] = base64.b64encode(image).decode()
        else:
            data['imgUrl'] = image

        return self._request(self.__imageCensorUserDefinedUrl, data)

    def antiSpam(self, content, options=None):
        """
            anti spam
        """

        data = {}
        data['content'] = content

        return self._request(self.__antiSpamUrl, data)
