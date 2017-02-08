# coding: utf-8

import base64
import logging
import random
import pickle
import os
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware


class RotateUserAgentMiddleware(UserAgentMiddleware):

    def __init__(self, user_agent=''):
        UserAgentMiddleware.__init__(self, user_agent)

    def process_request(self, request, spider):
        ua = random.choice(self.user_agent_list)
        if ua:
            request.headers.setdefault('User-Agent', ua)

    # for more user agent strings,you can find it in
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'user_agent_list')
    user_agent_list = pickle.load(open(file_path, 'r'))


# class ProxyMiddleware(object):
#
#     def process_request(self, request, spider):
#
#         proxy = random.choice(self.proxy_list)
#         request.meta['proxy'] = proxy["ip_port"]
#         request.headers["Proxy-Authorization"] = "Basic " + base64.b64encode(proxy['user_pass']).strip()
#         logging.info(request.meta['proxy'])
