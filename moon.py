import datetime


date_list = str(datetime.date.today()).split('-')
day = int(date_list[2])
month = int(date_list[1])
year = int(date_list[0])
MoonCh = 7


def getPhaze(da, mo, ch):
    get_v = da + mo + ch
    if get_v > 30:
        get_v -= 30
    if get_v <= 1.84566:
        return 'новая'
    elif get_v > 1.84566 and get_v <= 5.53699:
        return 'растущая серповидность'
    elif get_v > 5.53699 and get_v <= 9.22831:
        return 'первая четверть'
    elif get_v > 9.22831 and get_v <= 12.91963:
        return 'нарастающая выпуклость'
    elif get_v > 12.91963 and get_v <= 16.61096:
        return 'полная'
    elif get_v > 16.61096 and get_v <= 20.30228:
        return 'убывающая выпуклость'
    elif get_v > 20.30228 and get_v <= 23.99361:
        return 'убывающая четверть'
    elif get_v > 23.99361 and get_v <= 27.68493:
        return 'убывающая серповидность'
    else:
        return "новая"


def Img(phaz):
    if phaz == 'новая':
        return 'img/1.jpg'
    if phaz == 'растущая серповидность':
        return 'img/2.jpg'
    if phaz == 'первая четверть':
        return 'img/3.jpg'
    if phaz == 'нарастающая выпуклость':
        return 'img/4.jpg'
    if phaz == 'полная':
        return 'img/5.jpg'
    if phaz == 'убывающая выпуклость':
        return 'img/6.jpg'
    if phaz == 'убывающая четверть':
        return 'img/7.jpg'
    if phaz == 'убывающая серповидность':
        return 'img/8.jpg'


def CreateHTML(ph, img):
    return f'<div style="aligin-items: center">Фаза: {ph}</div>\n <div><img src={img} alt="moon"</div>'
