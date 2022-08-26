import os,sqlite3,base64,cv2
import numpy as np
def selectpircture():
    '''
    搜索可以后面加东西 目前只写了全部存储和全部读出
    比如可以特意搜索某一张
    :return:
    '''
    conn=sqlite3.connect('picture.db') #同上
    c=conn.cursor()
    sql=f"SELECT image_bytes FROM pictureTable"
    c.execute(sql, ('3',))
    for picture in c.fetchall():
        if '/9j' in str(picture[0]):
            img=base64.b64decode(picture[0])
            nparr=np.fromstring(img,np.uint8)
            img_decode=cv2.imdecode(nparr,cv2.IMREAD_COLOR)
            cv2.imshow("img",img_decode)
            cv2.waitKey(0)
    conn.commit()

selectpircture()
