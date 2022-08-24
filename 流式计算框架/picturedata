import os,sqlite3,base64,cv2
import numpy as np
'''
    和爬图片的代码放在同一个函数里
    current_working_dir = os.getcwd()  # 获取程序的本地路径
    global filename
    conn=sqlite3.connect('') #本地有的就可以直接连接 本地没有的就直接创建 格式是---.db
    c=conn.cursor() #获取游标
    symbol='pictureTable'
    爬图片的代码
    for item in project_list_soup:
    	item_href = item.get('href')
    	if filter_link(item_href):
    	    links.add(item_href)
    imgs = soup.find_all('img')
    os.makedirs('./imgs/', exist_ok=True)
    t = 1
    for item in imgs:
       img_src = 'https://www.shuishi.com' + item.get('src')
       filename = str('./imgs/' + '%s.jpg' % (repr(t)))
       print ('Downloading----', str(filename))
       with open(filename, 'wb') as img:
           img.write(requests.get(img_src, headers=headers).content)
           t += 1
   dirs=current_working_dir+'/imgs'
   files=os.listdir(dirs)
   c.execute('create table IF NOT EXISTS %s(id TEXT,image_bytes BLOB)' % symbol)
   c.execute('create index id_index on pictureTable(id)')
   conn.commit()
   i=1
   for file in files:
        filename=dirs+'\\'+file
        with open(filename, 'rb') as f:
            Pic_byte = f.read()
            tent = base64.b64encode(Pic_byte)
            sql = f"INSERT INTO pictureTable (id,image_bytes) VALUES (?,?);"
            c.execute(sql, (i, tent))
            i += 1
    conn.commit()
    conn.close()
'''
def selectpircture():
    '''
    搜索可以后面加东西 目前只写了全部存储和全部读出
    比如可以特意搜索某一张
    :return:
    '''
    conn=sqlite3.connect('') #同上
    c=conn.cursor()
    sql=f"SELECT image_bytes FROM pictureTable WHERE id=?"
    c.execute(sql)
    for picture in c.fetchall():
        img=base64.b64decode(picture[0])
        nparr=np.fromstring(img,np.uint8)
        img_decode=cv2.imdecode(nparr,cv2.IMREAD_COLOR)
        cv2.imshow("img",img_decode)
        cv2.waitKey(0)
    conn.commit()




