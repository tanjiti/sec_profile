# -*- coding: utf-8 -*-

"""
    EasyDL
"""

from .base import AipBase
from .base import base64
from .base import hashlib
from .base import json

class EasyDL(AipBase):
    """
        EasyDL
    """

    def _isPermission(self, authObj):
        """
            check whether permission
        """

        return True

    def predictImage(self, url, image, options=None):
        """
            图像
        """

        data = {}

        data['image'] = base64.b64encode(image).decode()

        data.update(options or {})

        return self._request(url, json.dumps(data, ensure_ascii=False), {
            'Content-Type': 'application/json',
        })

    def predictSound(self, url, sound, options=None):
        """
            声音
        """

        data = {}

        data['sound'] = base64.b64encode(sound).decode()

        data.update(options or {})

        return self._request(url, json.dumps(data, ensure_ascii=False), {
            'Content-Type': 'application/json',
        })
