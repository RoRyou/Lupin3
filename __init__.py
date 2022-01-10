import pandas as pd
import datetime
import itertools

pip install psycopg2-binary 

import psycopg2

pip install mysql-connector

import mysql.connector
import random
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

from IPython.core.interactiveshell import InteractiveShell

InteractiveShell.ast_node_interactivity = "all"

import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)


def str2date(strword):
    return datetime.datetime.strptime(strword, '%Y-%m-%d')


def date2str(dateword):  # only save date
    return str(datetime.datetime.strftime(dateword, '%Y-%m-%d'))


def datestr(word):
    if type(word) == datetime.datetime:
        return datetime.datetime.strftime(word,'%Y-%m-%d')
    elif type(word) == str:
        return datetime.datetime.strptime(word, '%Y-%m-%d')



def dateminus(startdate, daynum):
    if type(startdate) == str:
        return date2str(str2date(startdate) - datetime.timedelta(days=daynum))
    elif type(startdate) == datetime.datetime:
        return date2str(startdate - datetime.timedelta(days=daynum))


def dateplus(startdate, daynum):
    if type(startdate) == str:
        return date2str(str2date(startdate) + datetime.timedelta(days=daynum))
    elif type(startdate) == datetime.datetime:
        return date2str(startdate + datetime.timedelta(days=daynum))


def showeveryday(startday, endday):  # input string of date
    startd = str2date(startday)
    endd = str2date(endday)
    if startd > endd:
        print('startday must more than endday')
    else:
        daynum = (endd - startd).days
    outputdays = []
    for dayn in range(daynum + 1):
        newdate = dateplus(startd, dayn)
        outputdays.append(newdate)
    return outputdays


def splitlist(listsample, size=1000):
    donelist = [listsample[i:i + size] for i in range(0, len(listsample), size)]
    return donelist


def cartesian(l1, l2):
    carte = []
    for i in itertools.product(l1, l2):
        carte.append(i)
    df = pd.DataFrame(carte)
    return df


def postgreSqlconnect(host, port, user, password, database, sql):
    conn_string = "host=" + host + " port=" + port + " dbname=" + database + " user=" + user + " password=" + password
    gpconn = psycopg2.connect(conn_string)

    curs = gpconn.cursor()

    curs.execute(sql)

    data = curs.fetchall()

    gpconn.commit()

    curs.close()
    gpconn.close()
    data = pd.DataFrame(data)

    return data


class MyConverter(mysql.connector.conversion.MySQLConverter):

    def row_to_python(self, row, fields):
        row = super(MyConverter, self).row_to_python(row, fields)

        def to_unicode(col):
            if type(col) == bytearray:
                return col.decode('utf-8')
            return col

        return [to_unicode(col) for col in row]


def mySqlconnect(host, port, user, password, database, sql, ret):
    mysqlcon = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        passwd=password,
        database=database, use_unicode=False, converter_class=MyConverter
    )
    mysqlcurs = mysqlcon.cursor(buffered=True)
    # mysql

    mysqlcurs.execute(sql)

    if ret is True:

        myresult = mysqlcurs.fetchall()  # fetchall() 获取所有记录
        return myresult
        mysqlcon.close()
        mysqlcurs.close()

    elif ret is False:

        mysqlcon.commit()
        mysqlcon.close()
        mysqlcurs.close()


def find_pd(word, pd):
    index_ = []
    for num_row in range(pd.shape[0]):  # 5
        for num_col in range(pd.shape[1]):  # 4
            if pd.iloc[num_row, num_col] == word:
                # print([num_row, num_col])
                index_.append([num_row, num_col])
            else:
                pass
    return index_


def chineseloto(N=1000):
    def rand_num():
        n_l, e_l = [], []
        while len(n_l) < 5:
            t = random.randint(1, 35)
            if t in n_l:
                pass
            else:
                n_l.append(t)
        n_l.sort()
        while len(e_l) < 2:
            t = random.randint(1, 12)
            if t in e_l:
                pass
            else:
                e_l.append(t)
        e_l.sort()
        l = n_l + e_l
        return l

    sum_ = []
    for n in range(N):
        sum_.append(str(rand_num()))

    dict_ = {}
    for key in sum_:
        dict_[key] = dict_.get(key, 0) + 1

    def top_n_scores(n, score_dict):
        lot = [(k, v) for k, v in dict_.items()]  # make list of tuple from scores dict
        nl = []
        while len(lot) > 0:
            nl.append(max(lot, key=lambda x: x[1]))
            lot.remove(nl[-1])
        return nl[0:n]

    return top_n_scores(4, dict_)


def Stackedbar(titlename, xlabel, label, botV, cenV, topV):
    plt.title(titlename)
    N = len(xlabel)
    ind = np.arange(N)  # [ 0  1  2  3  4  5  6  7  8 ]
    plt.xticks(ind, xlabel)

    # plt.ylabel('Scores')
    Bottom, Center, Top = botV, cenV, topV

    d = []
    for i in range(0, len(Bottom)):
        sum = Bottom[i] + Center[i]
        d.append(sum)

    colors = list(mcolors.TABLEAU_COLORS.keys())

    p1 = plt.bar(ind, Bottom, color=colors[0])
    p2 = plt.bar(ind, Center, bottom=Bottom, color=colors[1])
    p3 = plt.bar(ind, Top, bottom=d, color=colors[2])

    plt.legend((p1[0], p2[0], p3[0]), label, loc=2)

    plt.show()


def multiplebar(n=2, total_width=0.5, size=5):
    print('待修改')
    x = np.arange(size)
    a = np.random.random(size)
    b = np.random.random(size)
    c = np.random.random(size)

    # total_width, n = 0.8, 3
    width = total_width / n
    x = x - (total_width - width) / 2

    plt.bar(x, a, width=width, label='a')
    plt.bar(x + width, b, width=width, label='b')
    plt.bar(x + 2 * width, c, width=width, label='c')
    plt.legend()

    plt.plot(x, a)
    plt.plot(x + width, b)
    plt.plot(x + 2 * width, c)
    # plt.plot(x, y, "r", marker='*', ms=10, label="a")
    # plt.xticks(rotation=45)
    # plt.legend(loc="upper left")

    plt.show()

    
def proba_to_score(prob):
    pdo = -6
    rate = 2
    base_odds = 1/50
    base_score = 60

    factor = pdo / np.log(rate)
    offset = base_score + factor * np.log(base_odds)
    score = factor * (np.log(1 - prob) - np.log(prob)) + offset
    return score
