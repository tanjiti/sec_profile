
# -*- coding: utf-8 -*-

"""
知识图谱
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

class AipKg(AipBase):

    """
    知识图谱
    """

    __createTaskUrl = 'https://aip.baidubce.com/rest/2.0/kg/v1/pie/task_create'

    __updateTaskUrl = 'https://aip.baidubce.com/rest/2.0/kg/v1/pie/task_update'

    __taskInfoUrl = 'https://aip.baidubce.com/rest/2.0/kg/v1/pie/task_info'

    __taskQueryUrl = 'https://aip.baidubce.com/rest/2.0/kg/v1/pie/task_query'

    __taskStartUrl = 'https://aip.baidubce.com/rest/2.0/kg/v1/pie/task_start'

    __taskStatusUrl = 'https://aip.baidubce.com/rest/2.0/kg/v1/pie/task_status'

    
    def createTask(self, name, template_content, input_mapping_file, output_file, url_pattern, options=None):
        """
            创建任务
        """
        options = options or {}

        data = {}
        data['name'] = name
        data['template_content'] = template_content
        data['input_mapping_file'] = input_mapping_file
        data['output_file'] = output_file
        data['url_pattern'] = url_pattern

        data.update(options)

        return self._request(self.__createTaskUrl, data)
    
    def updateTask(self, id, options=None):
        """
            更新任务
        """
        options = options or {}

        data = {}
        data['id'] = id

        data.update(options)

        return self._request(self.__updateTaskUrl, data)
    
    def getTaskInfo(self, id, options=None):
        """
            获取任务详情
        """
        options = options or {}

        data = {}
        data['id'] = id

        data.update(options)

        return self._request(self.__taskInfoUrl, data)
    
    def getUserTasks(self, options=None):
        """
            以分页的方式查询当前用户所有的任务信息
        """
        options = options or {}

        data = {}

        data.update(options)

        return self._request(self.__taskQueryUrl, data)
    
    def startTask(self, id, options=None):
        """
            启动任务
        """
        options = options or {}

        data = {}
        data['id'] = id

        data.update(options)

        return self._request(self.__taskStartUrl, data)
    
    def getTaskStatus(self, id, options=None):
        """
            查询任务状态
        """
        options = options or {}

        data = {}
        data['id'] = id

        data.update(options)

        return self._request(self.__taskStatusUrl, data)
    