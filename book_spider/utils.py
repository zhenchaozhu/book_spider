# coding: utf-8

chinese_num_2_digit ={u'零':0, u'一':1, u'二':2, u'三':3, u'四':4, u'五':5, u'六':6, u'七':7, u'八':8, u'九':9, u'十':10, u'百':100, u'千':1000, u'万':10000,
       u'０':0, u'１':1, u'２':2, u'３':3, u'４':4, u'５':5, u'６':6, u'７':7, u'８':8, u'９':9,
                u'壹':1, u'贰':2, u'叁':3, u'肆':4, u'伍':5, u'陆':6, u'柒':7, u'捌':8, u'玖':9, u'拾':10, u'佰':100, u'仟':1000, u'萬':10000,
       u'亿':100000000}

def get_digit(a, encoding="utf-8"):

    if isinstance(a, str):
        a = a.decode(encoding)

    count = 0
    result = 0
    tmp = 0
    Billion = 0
    while count < len(a):
        tmpChr = a[count]
        #print tmpChr
        tmpNum = chinese_num_2_digit.get(tmpChr, 0)
        #如果等于1亿
        if tmpNum == 100000000:
            result = result + tmp
            result = result * tmpNum
            #获得亿以上的数量，将其保存在中间变量Billion中并清空result
            Billion = Billion * 100000000 + result
            result = 0
            tmp = 0
        #如果等于1万
        elif tmpNum == 10000:
            result = result + tmp
            result = result * tmpNum
            tmp = 0
        #如果等于十或者百，千
        elif tmpNum >= 10:
            if tmp == 0:
                tmp = 1
            result = result + tmpNum * tmp
            tmp = 0
        #如果是个位数
        elif tmpNum is not None:
            tmp = tmp * 10 + tmpNum
        count += 1

    result = result + tmp
    result = result + Billion

    return result

category = {
    '_id': '',
    'name': ''
}

book = {
    '_id': '',
    'title': '',
    'category_id': ''
}

chapter = {
    '_id': '',
    'book_id': '',
    'name': '',
    'text_id': '',
}

text = {
    '_id': '',
    'text': ''
}