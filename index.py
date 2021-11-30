import requests
import time

# 易班打卡
def main(checkinfo):
    global date
    date = time.strftime("%Y-%m-%d", time.localtime())
    i = 0
    L = list(checkinfo.keys())
    L.sort()
    while i < len(checkinfo):
        post(checkinfo["%s" % L[i]][0], checkinfo["%s" % L[i]][1])
        i = i+1


def post(loginToken, address):
    global yb_result
    session = requests.Session()
    url_1 = "http://f.yiban.cn/iapp378946/i/%s" % loginToken
    a = session.get(url=url_1, headers=UA, allow_redirects=False)
    url_2 = a.headers['Location']
    header_loginToken = {"loginToken": "%s" % loginToken}
    b = session.get(url=url_2, headers=header_loginToken,
                    allow_redirects=False)
    url_get = b.headers["Location"]
    c = session.get(url=url_get, headers=UA, allow_redirects=False)
    studentID = c.headers['Location'].split('studentID=')[1]
    url_bind = "https://ygj.gduf.edu.cn/Handler/device.ashx?flag=checkBindDevice"
    bind = session.get(url=url_bind, headers=UA)
    url_save = "https://ygj.gduf.edu.cn/Handler/health.ashx?"
    data_yb_save = {
        "flag": "save",
        "studentID": "%s" % studentID,
        "date": "%s" % date,
        "health": "体温37.3℃以下（正常）",
        "address": "广东省广州市天河区迎福路78号靠近龙圣学校",
        "isTouch": "否",
        "isPatient": "不是"
    }
    if not address:
        yb_result = session.post(
            url=url_save, headers=UA, data=data_yb_save).json()
        return yb_result
    else:
        data_yb_save["address"] = address
        yb_result = session.post(
            url=url_save, headers=UA, data=data_yb_save).json()
        return yb_result


if __name__ == "__main__":
    USERS = {'张洵': ['cf8224510e7450226cb39601a4679079', '广东省广州市天河区华夏路92号靠近高德置地广场·夏']}
    UA = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 yiban_iOS/4.9.10"
    }

    main(USERS)
