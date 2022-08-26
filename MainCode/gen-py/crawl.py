from ensurepip import bootstrap
import requests, re, os, sqlite3, base64, cv2
from bs4 import BeautifulSoup
from kafka import KafkaProducer
import socket
import sys
import json
import threading
import datetime
import urllib.robotparser

def download_page(url):
    """
    访问网站的模块，以后需要访问网站的时候都会用到这个函数

    :param:url:str,需要读取的网页地址

    :return:str,下载下来的网页信息
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
        }
    data = requests.get(url, headers=headers).content.decode('utf-8')
    # print(data)
    return data

def download_imgs(imgs, project_title):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
        }
    current_working_dir = os.getcwd()  # 获取程序的本地路径
    global filename
    conn=sqlite3.connect('picture.db') #本地有的就可以直接连接 本地没有的就直接创建 格式是---.db
    c=conn.cursor() #获取游标
    symbol='pictureTable'
    symbol1 = 'textTable'
    c.execute('create table IF NOT EXISTS %s(id INTEGER PRIMARY KEY, title TEXT)' % symbol1)
    for item in project_title:
        c.execute('BEGIN TRANSACTION')
        sql = f"INSERT INTO textTable (id, title) VALUES (?, ?);"
        c.execute(sql, (None, item))
        c.execute('COMMIT')
    os.makedirs('./imgs/', exist_ok=True)
    t = 1
    for item in imgs:
        img_src = 'https://www.shuishi.com' + item.get('src')
        filename = str('./imgs/' + '%s.jpg' % (str(datetime.datetime.now())))
        print ('Downloading----', str(filename))
        with open(filename, 'wb') as img:
            img.write(requests.get(img_src, headers=headers).content)
            t += 1
    dirs=current_working_dir+'/imgs'
    files=os.listdir(dirs)
    c.execute('create table IF NOT EXISTS %s(id INTEGER PRIMARY KEY,image_bytes BLOB)' % symbol)
    c.execute('create index IF NOT EXISTS id_index on pictureTable(id)')
    conn.commit()
    for file in files:
        filename=dirs+'/'+file
        with open(filename, 'rb') as f:
            Pic_byte = f.read()
            tent = base64.b64encode(Pic_byte)
            c.execute('BEGIN TRANSACTION')
            sql = f"INSERT INTO pictureTable (id,image_bytes) VALUES (?,?);"
            c.execute(sql, (None, tent))
            c.execute('COMMIT')
    conn.commit()
    conn.close()

def URL_IP(project_link):
    for oneurl in project_link:
        if(str(oneurl.strip())[:8]=="https://"):
            url = str(oneurl.strip())[8:]
            print(url)
            try:
                ip = socket.gethostbyname(url)
                print(ip)
                #iplist.writelines(str(ip) + "\n")
            except:
                print("this URL 2 IP ERROR")
        else:
          url = str(oneurl.strip())[7:]
          print(url)
          try:
            ip = socket.gethostbyname(url)
            print(ip)
            #iplist.writelines(str(ip) + "\n")
          except:
            print("this URL 2 IP ERROR")

def parse_html(url):
    """
    拆分出：每个项目的信息，方便后续解析

    :param:url:需要解析的网址

    :return:ResultSet，项目列表的soup

    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
        }
    html = download_page(url)
    soup = BeautifulSoup(html, features='lxml')
    # project_list_soup = soup.find_all('div', {'class': {'work-item grid-item', 'work-item grid-item first'}})
    project_list_soup = soup.find_all('a')
    links = set()
    for item in project_list_soup:
    	item_href = item.get('href')
    	if filter_link(item_href):
    	    links.add(item_href)
    imgs = soup.find_all('img')
    project_list_soup = soup.find_all('div', {'class': {'work-item grid-item', 'work-item grid-item first'}})
    project_title = []
    for link in project_list_soup:
        name = link.find('h3', {'class': 'work-item__title fz-20'})
        project_title.append(name.string)
    t1 = threading.Thread(target=download_imgs, args=(imgs, project_title,))
    t1.start()
    # robot_txt(links)
    return links

def robot_txt(project_link):
    """
           利用robotparser分析知乎 Robots 协议
           """
    n = 0
    for oneurl in project_link:

        rp = urllib.robotparser.RobotFileParser()

        # 设置 robots.txt 文件 URL
        rp.set_url('https://www.shuishi.com/robots.txt')

        # 读取操作必须有, 不然后面解析不到
        rp.read()

        # 判断网址是否运行爬取
        if(rp.can_fetch('*', oneurl) == False):
            del project_link[n]
            n+1

def get_project_link(project_list_soup):
    """
    从项目列表的soup中，解析出每个项目的地址，得到一个列表

    :param:project_list_soup:ResultSet，项目列表的soup

    :return:list[str]，记录每个项目页面的地址

    """
    project_link = []
    for link in project_list_soup:
        # 因为网页地址是一个相对地址，所以需要一个网站的前缀拼接成绝对地址
        links = str(r"https://www.shuishi.com" + link)
        project_link.append(links)
    return project_link

def filter_link(link):
    reg = re.compile(r'(\/[\s\S\d\D\w\W]+)+')
    if link == None:
        return False
    elif reg.match(link):
        return True
    else:
        return False

def main(project_url):
    # 输入大师的网址，这里的r是转义符
    typeNo = 1
    # project_url = r'https://www.shuishi.com'
    if project_url == 'https://www.shuishi.com':
        urls = [project_url]
        URL_IP(urls)
    links = parse_html(project_url)
    links = get_project_link(links)
    producer = KafkaProducer(bootstrap_servers=['localhost:9093'])

    for item in links:
        producer.send('flink-stream-in-topic', bytes(item, encoding='UTF-8'))
        producer.flush()

if __name__ == '__main__':
    main(sys.argv[1])
