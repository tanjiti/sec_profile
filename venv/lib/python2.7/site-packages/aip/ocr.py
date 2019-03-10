
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

class AipOcr(AipBase):

    """
    图像识别
    """

    __generalBasicUrl = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic'

    __accurateBasicUrl = 'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic'

    __generalUrl = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general'

    __accurateUrl = 'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate'

    __generalEnhancedUrl = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_enhanced'

    __webImageUrl = 'https://aip.baidubce.com/rest/2.0/ocr/v1/webimage'

    __idcardUrl = 'https://aip.baidubce.com/rest/2.0/ocr/v1/idcard'

    __bankcardUrl = 'https://aip.baidubce.com/rest/2.0/ocr/v1/bankcard'

    __drivingLicenseUrl = 'https://aip.baidubce.com/rest/2.0/ocr/v1/driving_license'

    __vehicleLicenseUrl = 'https://aip.baidubce.com/rest/2.0/ocr/v1/vehicle_license'

    __licensePlateUrl = 'https://aip.baidubce.com/rest/2.0/ocr/v1/license_plate'

    __businessLicenseUrl = 'https://aip.baidubce.com/rest/2.0/ocr/v1/business_license'

    __receiptUrl = 'https://aip.baidubce.com/rest/2.0/ocr/v1/receipt'

    __trainTicketUrl = 'https://aip.baidubce.com/rest/2.0/ocr/v1/train_ticket'

    __taxiReceiptUrl = 'https://aip.baidubce.com/rest/2.0/ocr/v1/taxi_receipt'

    __formUrl = 'https://aip.baidubce.com/rest/2.0/ocr/v1/form'

    __tableRecognizeUrl = 'https://aip.baidubce.com/rest/2.0/solution/v1/form_ocr/request'

    __tableResultGetUrl = 'https://aip.baidubce.com/rest/2.0/solution/v1/form_ocr/get_request_result'

    __vatInvoiceUrl = 'https://aip.baidubce.com/rest/2.0/ocr/v1/vat_invoice'

    __qrcodeUrl = 'https://aip.baidubce.com/rest/2.0/ocr/v1/qrcode'

    __numbersUrl = 'https://aip.baidubce.com/rest/2.0/ocr/v1/numbers'

    __lotteryUrl = 'https://aip.baidubce.com/rest/2.0/ocr/v1/lottery'

    __passportUrl = 'https://aip.baidubce.com/rest/2.0/ocr/v1/passport'

    __businessCardUrl = 'https://aip.baidubce.com/rest/2.0/ocr/v1/business_card'

    __handwritingUrl = 'https://aip.baidubce.com/rest/2.0/ocr/v1/handwriting'

    __customUrl = 'https://aip.baidubce.com/rest/2.0/solution/v1/iocr/recognise'

    
    def basicGeneral(self, image, options=None):
        """
            通用文字识别
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__generalBasicUrl, data)
    
    def basicGeneralUrl(self, url, options=None):
        """
            通用文字识别
        """
        options = options or {}

        data = {}
        data['url'] = url

        data.update(options)

        return self._request(self.__generalBasicUrl, data)
    
    def basicAccurate(self, image, options=None):
        """
            通用文字识别（高精度版）
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__accurateBasicUrl, data)
    
    def general(self, image, options=None):
        """
            通用文字识别（含位置信息版）
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__generalUrl, data)
    
    def generalUrl(self, url, options=None):
        """
            通用文字识别（含位置信息版）
        """
        options = options or {}

        data = {}
        data['url'] = url

        data.update(options)

        return self._request(self.__generalUrl, data)
    
    def accurate(self, image, options=None):
        """
            通用文字识别（含位置高精度版）
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__accurateUrl, data)
    
    def enhancedGeneral(self, image, options=None):
        """
            通用文字识别（含生僻字版）
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__generalEnhancedUrl, data)
    
    def enhancedGeneralUrl(self, url, options=None):
        """
            通用文字识别（含生僻字版）
        """
        options = options or {}

        data = {}
        data['url'] = url

        data.update(options)

        return self._request(self.__generalEnhancedUrl, data)
    
    def webImage(self, image, options=None):
        """
            网络图片文字识别
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__webImageUrl, data)
    
    def webImageUrl(self, url, options=None):
        """
            网络图片文字识别
        """
        options = options or {}

        data = {}
        data['url'] = url

        data.update(options)

        return self._request(self.__webImageUrl, data)
    
    def idcard(self, image, id_card_side, options=None):
        """
            身份证识别
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()
        data['id_card_side'] = id_card_side

        data.update(options)

        return self._request(self.__idcardUrl, data)
    
    def bankcard(self, image, options=None):
        """
            银行卡识别
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__bankcardUrl, data)
    
    def drivingLicense(self, image, options=None):
        """
            驾驶证识别
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__drivingLicenseUrl, data)
    
    def vehicleLicense(self, image, options=None):
        """
            行驶证识别
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__vehicleLicenseUrl, data)
    
    def licensePlate(self, image, options=None):
        """
            车牌识别
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__licensePlateUrl, data)
    
    def businessLicense(self, image, options=None):
        """
            营业执照识别
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__businessLicenseUrl, data)
    
    def receipt(self, image, options=None):
        """
            通用票据识别
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__receiptUrl, data)
    
    def trainTicket(self, image, options=None):
        """
            火车票识别
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__trainTicketUrl, data)
    
    def taxiReceipt(self, image, options=None):
        """
            出租车票识别
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__taxiReceiptUrl, data)
    
    def form(self, image, options=None):
        """
            表格文字识别同步接口
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__formUrl, data)
    
    def tableRecognitionAsync(self, image, options=None):
        """
            表格文字识别
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__tableRecognizeUrl, data)
    
    def getTableRecognitionResult(self, request_id, options=None):
        """
            表格识别结果
        """
        options = options or {}

        data = {}
        data['request_id'] = request_id

        data.update(options)

        return self._request(self.__tableResultGetUrl, data)
    
    def vatInvoice(self, image, options=None):
        """
            增值税发票识别
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__vatInvoiceUrl, data)
    
    def qrcode(self, image, options=None):
        """
            二维码识别
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__qrcodeUrl, data)
    
    def numbers(self, image, options=None):
        """
            数字识别
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__numbersUrl, data)
    
    def lottery(self, image, options=None):
        """
            彩票识别
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__lotteryUrl, data)
    
    def passport(self, image, options=None):
        """
            护照识别
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__passportUrl, data)
    
    def businessCard(self, image, options=None):
        """
            名片识别
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__businessCardUrl, data)
    
    def handwriting(self, image, options=None):
        """
            手写文字识别
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__handwritingUrl, data)
    
    def custom(self, image, options=None):
        """
            自定义模板文字识别
        """
        options = options or {}

        data = {}
        data['image'] = base64.b64encode(image).decode()

        data.update(options)

        return self._request(self.__customUrl, data)
    
    def tableRecognition(self, image, options=None, timeout=10000):
        """
            tableRecognition
        """
        
        result = self.tableRecognitionAsync(image)

        if 'error_code' in result:
            return result
        
        requestId = result['result'][0]['request_id']
        for i in range(int(math.ceil(timeout / 1000.0))):
            result = self.getTableRecognitionResult(requestId, options)
            
            # 完成
            if int(result['result']['ret_code']) == 3: 
                break
            time.sleep(1)

        return result