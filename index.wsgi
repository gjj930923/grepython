# -*- coding: utf-8 -*-  
import sae

import urllib2    
import urllib    
import re    
import thread    
import time 
import json   
import cookielib 
  

class Spider_Model:    
    

    def __init__(self):  
        self.family_name = None
        self.given_name = None  
        self.neeaID = None
        self.etsID = None
        self.balance = None  
        self.cities = ['BEIJING','TIANJIN','SHIJIAZHUANG','TAIYUAN','HEFEI','XIAMEN','FUZHOU','NANJING','SUZHOU','NANTONG','YANGZHOU','NANCHANG','JINAN','QINGDAO','WEIFANG','WEIHAI','SHANGHAI','HANGZHOU','NINGBO','GUANGZHOU','SHENZHEN','SHANTOU','NANNING','HAIKOU','LUOYANG','ZHENGZHOU','WUHAN','CHANGSHA','HAERBIN','CHANGCHUN','DALIAN','SHENYANG','LANZHOU','HUHEHAOTE','XIAN','WULUMUQI','CHONGQING','CHENGDU','KUNMING']
        self.cityViews = ['北京','天津','石家庄','太原','合肥','厦门','福州','南京','苏州','南通','扬州','南昌','济南','青岛','潍坊','威海','上海','杭州','宁波','广州','深圳','汕头','南宁','海口','洛阳','郑州','武汉','长沙','哈尔滨','长春','大连','沈阳','兰州','呼和浩特','西安','乌鲁木齐','重庆','成都','昆明']
        self.provinceViews = ['BEIJING','TIANJIN','HEBEI','SHANXI','ANHUI','FUJIAN','FUJIAN','JIANGSU','JIANGSU','JIANGSU','JIANGSU','JIANGXI','SHANDONG','SHANDONG','SHANDONG','SHANDONG','SHANGHAI','ZHEJIANG','ZHEJIANG','GUANGDONG','GUANGDONG','GUANGDONG','GUANGXI','HAINAN','HENAN','HENAN','HUBEI','HUNAN','HEILONGJIANG','JILIN','LIAONING','LIAONING','GANSU','NEIMENGGU','SHAANXI','XINJIANG','CHONGQING','SICHUAN','YUNNAN']

    # 网站首页
    def login(self):
        loginUrl = 'http://gre.etest.net.cn/login.do'   # 登录的url
        infoUrl = 'http://gre.etest.net.cn/personalInfo.do' # 个人信息的url  
        #需要POST的数据：neeaID账号和密码。切勿外传！  
        postdata=urllib.urlencode({    
            'neeaID':'71327470',    
            'pwd':'GREpython2015'    
        })  
        #自定义一个请求  
        req = urllib2.Request(    
            url = loginUrl,    
            data = postdata  
        )  
        #访问该链接  
        result = opener.open(req)  
        #浏览器头信息
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'   
        headers = { 'User-Agent' : user_agent }
        #获取请求  
        req = urllib2.Request(infoUrl, headers = headers)    
        result_2 = opener.open(req).read()   
        #检测请求返回结果是否含'alert'字符串（未登录时进行访问会弹出对话框警告）
        p1 = re.compile(r'alert')
        #notLogin指是否已登录，若已登录则为None
        notLogin = p1.search(result_2)   
        if not notLogin:
            #设定获取信息的正则表达式，以下分别获取姓、名、neeaID、etsID和账户余额
            p2 = re.compile(r'<div class="smalltext"><b>(.*?)<br/>.*?</b></div>')
            p3 = re.compile(r'<div class="smalltext"><b>.*?<br/>(.*?)</b></div>')
            p4 = re.compile(r'<p class="smalltext"> NEEA ID: <b>(.*?)</b> </p>')
            p5 = re.compile(r'<span id="pInfoEtsID">(.*?)</span>')
            p6 = re.compile(r'<span id="pInfoBalance">(.*?)</span>')
            self.family_name = p2.findall(result_2,re.S)
            self.given_name = p3.findall(result_2,re.S)    
            self.neeaID = p4.findall(result_2,re.S)
            self.etsID = p5.findall(result_2,re.S)
            self.balance = p6.findall(result_2,re.S)   
            
            cityInfo = r"城市列表：<br>"
            i = 0
            num = len(self.cities)
            #根据__init__中的城市信息，将所有城市按照HTML格式串联起来接在cityInfo对象后
            while i < num:
                cityInfo = cityInfo + str(i+1) + ':' + self.provinceViews[i] + '-' + self.cities[i] + self.cityViews[i] + r'<br>'
                #cityInfo.join(str(i+1)).join(":").join(self.provinceViews[i]).join("-").join(self.cityViews[i]).join(self.cities[i]).join(r'<br>')
                i = i + 1
            #获取当前时间的数组对象
            date = time.strptime(time.ctime(),'%a %b %d %H:%M:%S %Y')
            #根据当前年月设置下拉列表中的年月选项，一般为本月至当年12月。如果本月月数大于10（不含）则为次年12月。
            template = r'<option value="%d-%d">%d-%d</option>'
            year = date.tm_year
            month = date.tm_mon
            dateList = ""
            while month < 13:
                dateList = dateList + template%(year,month,year,month)
                month = month + 1
            #判断本月月数是否大于10
            if date.tm_mon > 10:
                year = year + 1
                month = 1
                while month < 13:
                    dateList = dateList + template%(year,month,year,month)
                    month = month + 1
            #前端首页的HTML代码，内有数处替换点（%s,%d...）
            html = "".join([
            r'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml">',
            r'<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><title>考场设置</title></head>',
            r'<body>',
            r'<form action="/../getSites" method="get"><table width="300" border="0">',
            r'<tr></tr>',
            r'<tr>',
            r'  <td>%s</td>',
            r'</tr>',
            r'<tr>',
            r'  <td>城市编号（空格分隔）    ',
            r'    <input type="text" name="cities" id="cities" /></td>',
            r'</tr>',
            r'<tr>',
            r'  <td><select name="ym" id="ym">',
            r'    %s',
            r'  </select>',
            r'    <select name="whichFirst" id="whichFirst">',
            r'      <option value="AS">考试时间优先</option>',
            r'      <option value="SA">考场优先</option>',
            r'    </select></td>',
            r'</tr>',
            r'<tr>',
            r'  <td><input type="submit" id="submit" value="提交" /></td>',
            r'</tr>',
            r'<tr>',
            r'  <td>&nbsp;</td>',
            r'</tr>',
            r'</table></form></body></html>'
            ])
            # 替换处分别为城市信息列表和年月选项
            html = html % (cityInfo,dateList)
            return html 
        return "null"

    # 考点信息页面
    def getSiteStatus(self,cityList,date,method):
        # 考点信息官方查询url
        url = 'http://gre.etest.net.cn/testSites.do'
        # 获取传入的城市代码信息（GET方式传入信息时，空格会被替换成'+'号）
        cityNums = cityList.split("+")
        cities = ''
        cityNameList = ''
        #根据城市代码获取对应城市的省份英文和城市中英文，构建url的GET参数
        for num in cityNums:
            cities = cities + str(self.provinceViews[int(num)-1]) + '_' + str(self.cities[int(num)-1]) + '%3B'
            cityNameList = cityNameList + self.cityViews[int(num)-1] + '%3B'
        #组建GET请求url，同时对中文部分以url格式（%XX%xx）进行编码
        url = url + '?p=testSites&isFilter=0&isSearch=1&ym=' + date + '&cities=' + cities + '&citiesNames=' + urllib.quote(cityNameList).replace('%','%25').replace('%25253B','%3B') + '&whichFirst=' + method
        #浏览器头
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'   
        headers = { 'User-Agent' : user_agent }   
        #获取请求结果
        req = urllib2.Request(url, headers = headers)    
        result = opener.open(req).read()  
        #以下分别代表考试费用、省份、考点代码、考点状态、考点名称、考试时间、考位数量
        fees = []
        provinces = []
        siteCodes = []
        isCloseds = []
        siteNames = []
        bjtimes = []
        realSeats = []
        #设定正则表达式的规则
        p1 = re.compile(r'"fee":(.*?),')
        p2 = re.compile(r'"province":"(.*?)"')
        p3 = re.compile(r'"siteCode":"(.*?)"')
        p4 = re.compile(r'"isClosed":(.*?),')
        p5 = re.compile(r'"siteName":"(.*?)"')
        p6 = re.compile(r'"bjtime":"(.*?)"')
        p7 = re.compile(r'"realSeats":(.*?),')
        #获取截取的结果
        f1 = p1.findall(result,re.S)
        f2 = p2.findall(result)
        f3 = p3.findall(result,re.S)
        f4 = p4.findall(result,re.S)
        f5 = p5.findall(result)
        f6 = p6.findall(result)
        f7 = p7.findall(result,re.S)
        i = 0
        #获取考点信息条数
        num = len(f1)
        content = ""
        #可报名的考点数
        accessible = 0
        while i < num:
            if(f7[i] == "1"):
                #统计可报名的考点数
                accessible = accessible + 1
            #将状态代码替换成对应中文
            f7[i] = f7[i].replace('0','暂满').replace('1','<font color=#FF0000>有</font>')
            #将以分为单位的价格换位以元为单位
            f1[i] = str(int(f1[i]) / 100)
            #以HTML格式添加到content对象
            content = content + '<tr>' + '<td>' + f7[i] + '</td>'+ '<td>' + f2[i] + '</td>' + '<td>' + f3[i] + '</td>' + '<td>' + f4[i] + '</td>' + '<td>' + f5[i] + '</td>' + '<td>' + f6[i] + '</td>' + '<td>' + f1[i] + '</td>' + '</tr>'
            i = i + 1
        #HTML前端代码，含数个替换点
        html = "".join([
            r'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml">',
            r'<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><meta http-equiv="refresh" content="60"><title>考位状态（%s，考位：%d）</title></head>',
            r'<body>',
            r'<table width="700" border="0">',
            r'  <tr>',
            r'    <td height="59"><a href="../">回到首页</a><a href="http://gre.etest.net.cn" target="_blank"><br>进入GRE报名网</a><br>目前有<font size=12 color=#FF0000>%d</font>个考场可报名。最近更新时间%s<br>每1分钟刷新一次，报名请自行前往GRE官网。如果无法正常显示请<a  href=''>手动刷新</a>本页或<a href="../">回到首页</a>重新设置</td>',
            r'  </tr>',
            r'</table>',
            r'<table width="700" border="0">',
            r'  <tr>',
            r'    <th width="50" scope="col">状态</th>',
            r'    <th width="50" scope="col">省份</th>',
            r'    <th width="60" scope="col">考场代码</th>',
            r'    <th width="100" scope="col">考位数量</th>',
            r'    <th width="50" scope="col">考场名称</th>',
            r'    <th width="100" scope="col">考试时间</th>',
            r'    <th width="50" scope="col">费用</th>',
            r'  </tr>%s',
            r'</table></body></html>'
            ]) 
            # 替换点分别为城市名称（中文，在head部分）、可报考点数（head部分）、可报考点数（body）、格式化的当前时间、考点详细信息（content对象）
        return html % (cityNameList.replace('%3B',''),accessible,accessible,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),content)

myModel = Spider_Model()  # 全局变量，指向Spider_Model类
cookieJar = cookielib.CookieJar()  # 全局变量，初始化一个CookieJar来处理Cookie的信息  
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))  # 全局变量，使用该cookieJar的opener

def app(environ, start_response):
    # HTTP头文件信息
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)
    # method=接收请求为GET或POST等，path=域名后的字符串
    method = environ['REQUEST_METHOD']
    path = environ['PATH_INFO']

    if method=='GET' and path=='/':
        return myModel.login()
    #if method=='POST' and path=='/login':
    #    return str(environ)
    if method=='GET' and path=='/getSites':
        #对GET参数进行处理，总共三个参数：cityList（要查询的城市编号）,date（欲查询的年月）,method（时间优先or考点优先），存放在数组item中
        query = environ['QUERY_STRING'].split('&')
        item = []
        for q in query:
            items = q.split("=")
            item.append(items[1])
        return myModel.getSiteStatus(item[0],item[1],item[2])
    return "null"

application = sae.create_wsgi_app(app)
