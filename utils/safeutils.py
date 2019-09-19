__author__ = 'yuchen'
__date__ = '2018/8/31 02:13'

from urllib.parse import urlparse,urljoin
from flask import request

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    print('request.host',request.host)
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc