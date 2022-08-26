import socket
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
urls = ['https://www.shuishi.com']
print (urls[0])
print (type(urls[0]))
URL_IP(urls)
