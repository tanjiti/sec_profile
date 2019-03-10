# -*- coding: utf-8 -*-

"""
    AipBase
"""
import hmac
import json
import hashlib
import datetime
import base64
import time
import sys
import requests
requests.packages.urllib3.disable_warnings()


if sys.version_info.major == 2:
    from urllib import urlencode
    from urllib import quote
    from urlparse import urlparse
else:
    from urllib.parse import urlencode
    from urllib.parse import quote
    from urllib.parse import urlparse

class AipBase(object):
    """
        AipBase
    """

    __accessTokenUrl = 'https://aip.baidubce.com/oauth/2.0/token'

    __reportUrl = 'https://aip.baidubce.com/rpc/2.0/feedback/v1/report'

    __scope = 'brain_all_scope'

    def __init__(self, appId, apiKey, secretKey):
        """
            AipBase(appId, apiKey, secretKey)
        """

        self._appId = appId.strip()
        self._apiKey = apiKey.strip()
        self._secretKey = secretKey.strip()
        self._authObj = {}
        self._isCloudUser = None
        self.__client = requests
        self.__connectTimeout = 60.0
        self.__socketTimeout = 60.0
        self._proxies = {}
        self.__version = '2_2_13'

    def getVersion(self):
        """
            version
        """
        return self.__version

    def setConnectionTimeoutInMillis(self, ms):
        """
            setConnectionTimeoutInMillis
        """

        self.__connectTimeout = ms / 1000.0

    def setSocketTimeoutInMillis(self, ms):
        """
            setSocketTimeoutInMillis
        """

        self.__socketTimeout = ms / 1000.0

    def setProxies(self, proxies):
        """
            proxies
        """

        self._proxies = proxies

    def _request(self, url, data, headers=None):
        """
            self._request('', {})
        """
        try:
            result = self._validate(url, data)
            if result != True:
                return result

            authObj = self._auth()
            params = self._getParams(authObj)

            data = self._proccessRequest(url, params, data, headers)
            headers = self._getAuthHeaders('POST', url, params, headers)
            response = self.__client.post(url, data=data, params=params,
                            headers=headers, verify=False, timeout=(
                                self.__connectTimeout,
                                self.__socketTimeout,
                            ), proxies=self._proxies
                        )
            obj = self._proccessResult(response.content)

            if not self._isCloudUser and obj.get('error_code', '') == 110:
                authObj = self._auth(True)
                params = self._getParams(authObj)
                response = self.__client.post(url, data=data, params=params,
                                headers=headers, verify=False, timeout=(
                                    self.__connectTimeout,
                                    self.__socketTimeout,
                                ), proxies=self._proxies
                            )
                obj = self._proccessResult(response.content)
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout) as e:
            return {
                'error_code': 'SDK108',
                'error_msg': 'connection or read data timeout',
            }

        return obj

    def _validate(self, url, data):
        """
            validate
        """

        return True

    def _proccessRequest(self, url, params, data, headers):
        """
            参数处理
        """

        params['aipSdk'] = 'python'
        params['aipVersion'] = self.__version

        return data

    def _proccessResult(self, content):
        """
            formate result
        """

        if sys.version_info.major == 2:
            return json.loads(content) or {}
        else:
            return json.loads(content.decode()) or {}

    def _auth(self, refresh=False):
        """
            api access auth
        """

        #未过期
        if not refresh:
            tm = self._authObj.get('time', 0) + int(self._authObj.get('expires_in', 0)) - 30
            if tm > int(time.time()):
                return self._authObj

        obj = self.__client.get(self.__accessTokenUrl, verify=False, params={
            'grant_type': 'client_credentials',
            'client_id': self._apiKey,
            'client_secret': self._secretKey,
        }, timeout=(
            self.__connectTimeout,
            self.__socketTimeout,
        ), proxies=self._proxies).json()

        self._isCloudUser = not self._isPermission(obj)
        obj['time'] = int(time.time())
        self._authObj = obj

        return obj

    def _isPermission(self, authObj):
        """
            check whether permission
        """

        scopes = authObj.get('scope', '')

        return self.__scope in scopes.split(' ')

    def _getParams(self, authObj):
        """
            api request http url params
        """

        params = {}

        if self._isCloudUser == False:
            params['access_token'] = authObj['access_token']

        return params

    def _getAuthHeaders(self, method, url, params=None, headers=None):
        """
            api request http headers
        """

        headers = headers or {}
        params = params or {}

        if self._isCloudUser == False:
            return headers

        urlResult = urlparse(url)
        for kv in urlResult.query.strip().split('&'):
            if kv:
                k, v = kv.split('=')
                params[k] = v

        # UTC timestamp
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        headers['Host'] = urlResult.hostname
        headers['x-bce-date'] = timestamp
        version, expire = '1', '1800'

        # 1 Generate SigningKey
        val = "bce-auth-v%s/%s/%s/%s" % (version, self._apiKey, timestamp, expire)
        signingKey = hmac.new(self._secretKey.encode('utf-8'), val.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        # 2 Generate CanonicalRequest
        # 2.1 Genrate CanonicalURI
        canonicalUri = quote(urlResult.path)
        # 2.2 Generate CanonicalURI: not used here
        # 2.3 Generate CanonicalHeaders: only include host here

        canonicalHeaders = []
        for header, val in headers.items():
            canonicalHeaders.append(
                '%s:%s' % (
                    quote(header.strip(), '').lower(),
                    quote(val.strip(), '')
                )
            )
        canonicalHeaders = '\n'.join(sorted(canonicalHeaders))

        # 2.4 Generate CanonicalRequest
        canonicalRequest = '%s\n%s\n%s\n%s' % (
            method.upper(),
            canonicalUri,
            '&'.join(sorted(urlencode(params).split('&'))),
            canonicalHeaders
        )

        # 3 Generate Final Signature
        signature = hmac.new(signingKey.encode('utf-8'), canonicalRequest.encode('utf-8'),
                        hashlib.sha256
                    ).hexdigest()

        headers['authorization'] = 'bce-auth-v%s/%s/%s/%s/%s/%s' % (
            version,
            self._apiKey,
            timestamp,
            expire,
            ';'.join(headers.keys()).lower(),
            signature
        )

        return headers

    def report(self, feedback):
        """
            数据反馈
        """

        data = {}
        data['feedback'] = feedback

        return self._request(self.__reportUrl, data)

    def post(self, url, data, headers=None):
        """
            self.post('', {})
        """

        return self._request(url, data, headers)
