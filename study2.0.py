import datetime as dt

studd = {'Иванов Иван': ['Java Basics', dt.datetime(2020, 6, 1, hour=10)],
         'Петров Петр': ['Java Advanced', dt.datetime(2020, 6, 15, hour=10)]}
progd = {'Java Basics': ['Java Fundamentals', 'OOP'], 'Java Advanced': ['Java IO', 'JDBC']}
corsd = {'Java Fundamentals': 14, 'OOP': 20, 'Java IO': 10, 'JDBC': 15}
time_now = dt.datetime(2020, 6, 5, hour=12, minute=3) #дата на момент запроса

def itogo(stud): #считает общее число академических часов обучения
    stud = studd[stud]
    a = 0
    for i in progd[stud[0]]:
        a += corsd[i]
    return a

def finally_day(stud): #выводит дату окончания обучения
    hours = itogo(stud)  #общее количество часов которое должен отучиться студент
    finally_time = studd[stud][1]  #время начала обучения
    while hours > 0:
        if finally_time.isoweekday() < 6 and 18 > finally_time.hour >= 10:
            hours -= 1
            finally_time += dt.timedelta(hours=1)
        else:
            finally_time += dt.timedelta(hours=1)
    return finally_time

def visual_akadem_time(hours):  #время в академических часах, если обучение не закончилось, в формате задания
    days = hours // 8
    hours = hours - days * 8
    if days:
        return "{} д. {} ч.".format(days, hours)
    else:
        return "{} ч.".format(hours)

def visual_cal_time(finday, time_now): #календарное время с окончания обучения, в формате заданя
    if time_now.minute:
        delta_hours = (time_now - finday) // dt.timedelta(hours=1) + 1 #округление к большему (по условию задачи)
    else:
        delta_hours = (time_now - finday) // dt.timedelta(hours=1)
    days = delta_hours // 24
    hours = delta_hours - days * 24
    if days:
        return "{} д. {} ч.".format(days, hours)
    else:
        return "{} ч.".format(hours)

def visual_fintime(fintime):  #выводит дату окончания обучения в формате задания
    s = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября',
         'декабря']
    month = s[fintime.month - 1]
    return "{} {} {} года, {}.".format(fintime.day, month, fintime.year, str(fintime.time())[:5])

class AkademHours: #считает общее количество акадеических часов с момента запроса до конца обучения
    def __init__(self): #накапливает количество академических часов
        self.date = 0

    def plus(self, time_out): #получает дату с разницей в 1 час и добавляет академ. час, если он рабочий
        self.time_out = time_out
        if time_out.isoweekday() < 6 and 18 >= time_out.hour >= 11:
            self.date += 1

    def reset(self): #метод сбрасывает счетчик академ. часов в классе
        self.date = 0

for stud in studd.keys(): #перебираем всех студентов
    if (time_now - finally_day(stud)).days >= 0:
        print("{} ({}, {} ч.) - Обучение закончено. После окончания прошло\n{} Дата окончания обучения - {}\n".format(
                        stud, studd[stud][0], itogo(stud), visual_cal_time(finally_day(stud), time_now),
                        visual_fintime(finally_day(stud))))
    else:
        time_out = time_now
        cal_days_all = finally_day(stud) - time_now
        if time_now.minute:          #округление (по условию)
            cal_hours = cal_days_all // dt.timedelta(hours=1) + 1
        else:
            cal_hours = cal_days_all // dt.timedelta(hours=1)
        x = AkademHours()
        x.reset()
        while cal_hours > 0:
            cal_hours -= 1
            time_out += dt.timedelta(hours=1)
            x.plus(time_out)
        print("{} ({}, {} ч.) - Обучение не закончено. До окончания осталось\n{} Дата окончания обучения - {}\n".format(
            stud, studd[stud][0], itogo(stud), visual_akadem_time(x.date), visual_fintime(finally_day(stud))))