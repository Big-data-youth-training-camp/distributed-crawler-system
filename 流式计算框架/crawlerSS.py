from ensurepip import bootstrap
import requests, re, os
from bs4 import BeautifulSoup
from kafka import Kafkaproducer


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


# 解析得到标题与项目地址的列表
def parse_html(url):
    """
    拆分出：每个项目的信息，方便后续解析

    :param:url:需要解析的网址

    :return:ResultSet，项目列表的soup

    """
    html = download_page(url)
    soup = BeautifulSoup(html, features='lxml')
    project_list_soup = soup.find_all('div', {'class': {'work-item grid-item', 'work-item grid-item first'}})
    return project_list_soup



def get_project_title(project_list_soup):
    """
    在项目信息中提取项目的名称，得到一个列表

    :param:project_list_soup:ResultSet，项目列表的soup

    :returns:list[str],项目的名称列表
    """
    project_title = []
    for link in project_list_soup:
        name = link.find('h3', {'class': 'work-item__title fz-20'})
        project_title.append(name.string)
    return project_title


def get_project_link(project_list_soup):
    """
    从项目列表的soup中，解析出每个项目的地址，得到一个列表

    :param:project_list_soup:ResultSet，项目列表的soup

    :return:list[str]，记录每个项目页面的地址

    """
    project_link = []
    for link in project_list_soup:
        links = link.find('a')['href']
        # 因为网页地址是一个相对地址，所以需要一个网站的前缀拼接成绝对地址
        links = str(r"https://www.shuishi.com/" + links)
        project_link.append(links)
    return project_link


def parse_sub_html(project_link):
    """
    解析项目子项页面，得到图片地址的列表

    :param:project_link:需要解析的项目地址

    :return:list[str],每张图片的地址的列表
    """
    html = download_page(project_link)
    project_soup = BeautifulSoup(html, features='lxml')
    project_img_links = project_soup.find_all('div', {'class': {'wbanner-item'}})
    # print(project_img_links)
    # print(type(project_img_links))
    project_img_links2 = []
    for l in project_img_links:
        lk = l.find('img')['src']
        lkr = str(r"https://www.shuishi.com/") + lk
        # print(lkr)
        project_img_links2.append(lkr)
    print("此项目大图数量 = " + str(len(project_img_links2)))
    return project_img_links2


def save_img(links, name):
    """
    根据图片地址的列表，设定命名规则，保存图片

    :param links:list，单个项目所需要保存的图片网址列表

    :param name:str，项目的名称，最终存储的文件会加后缀
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    os.makedirs('./SS project img/', exist_ok=True)
    t = 1
    for link in links:
        filename = str('./SS project img/' + str(name) + '%s.jpg' % (repr(t)))
        print("Downloading----", str(filename))
        with open(filename, "wb") as img:
            img.write(requests.get(link, headers=headers).content)
            t += 1


def main():
    # 输入大师的网址，这里的r是转义符
    typeNo = 1
    project_url = r'https://www.shuishi.com/works?type=' + str(typeNo) + r'&pagenum=1'
    name = []
    link = []
    page = 1
    producer = Kafkaproducer(bootstrap_servers=['localhost:9092','localhost:9093','localhost:9094'])

    for i in range(page, 10):
        project_url = project_url[0:-1] + str(i)
        print(project_url)
        soup = parse_html(project_url)
        # 得到项目名称以及项目地址
        namei = get_project_title(soup)
        linki = get_project_link(soup)

        producer.send("Name Sub List %d is :" % (i))
        producer.send(namei)
        producer.send("Link Sub List %d is :" % (i))
        producer.send(linki)
        name += namei
        link += linki
    producer.send("共有项目： " + str(len(link)))
    # 进入项目子项地址下载图片
    # 引入项目代号t可以从第t个项目开始下载，以防网络错误
    t = 0
    while t < len(name):
        # 考虑空项目地址引起download函数报错
        if link[t] == "":
            producer.send("Skip it,Because it is null,Hurry coding,,Fix it later")
            t += 1
        else:
            img_list = parse_sub_html(link[t])
            producer.send('Project Name is :', name[t])
            save_name = str("t" + repr(typeNo) + "-" + repr(t + 1) + "-" + name[t])
            save_img(img_list, save_name)
            producer.send('No %s is ok' % repr(t + 1))
            t += 1
    producer.flush()


if __name__ == '__main__':
    main()
