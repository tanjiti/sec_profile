# -*- coding: utf-8 -*-

"""
    Speech
"""

from .base import AipBase
from .base import base64
from .base import hashlib
from .base import json

class AipSpeech(AipBase):
    """
        Aip Speech
    """

    __asrUrl = 'http://vop.baidu.com/server_api'

    __ttsUrl = 'http://tsn.baidu.com/text2audio'

    def _isPermission(self, authObj):
        """
            check whether permission
        """

        return True    

    def _proccessRequest(self, url, params, data, headers):
        """
            参数处理
        """

        token = params.get('access_token', '')

        if not data.get('cuid', ''):
            data['cuid'] = hashlib.md5(token.encode()).hexdigest()

        if url == self.__asrUrl:
            data['token'] = token
            data = json.dumps(data)
        else:
            data['tok'] = token

        if 'access_token' in params:
            del params['access_token']

        return data

    def _proccessResult(self, content):
        """
            formate result
        """

        try:
            return super(AipSpeech, self)._proccessResult(content)
        except Exception as e:
            return {
                '__json_decode_error': content,
            }

    def asr(self, speech=None, format='pcm', rate=16000, options=None):
        """
            语音识别
        """

        data = {}

        if speech:
            data['speech'] = base64.b64encode(speech).decode()
            data['len'] = len(speech)

        data['channel'] = 1
        data['format'] = format
        data['rate'] = rate

        data = dict(data, **(options or {}))

        return self._request(self.__asrUrl, data)

    def synthesis(self, text, lang='zh', ctp=1, options=None):
        """
            语音合成
        """
        data ={}

        data['tex'] = text
        data['lan'] = lang
        data['ctp'] = ctp

        data = dict(data, **(options or {}))

        result = self._request(self.__ttsUrl, data)

        if '__json_decode_error' in result:
            return result['__json_decode_error']

        return result



