# -*- coding:utf-8 -*-
import arrow

# 获取当前日期 ： 2020-06-29 14:00:28.047000
curr_time = cur = arrow.now()

# 获取当前天 ： 2020-06-29
currentdate = curr_time.date()

# 获取当前日期的前一天的Array类型
arrayyesterday = curr_time.shift(days=-1)

# 获取当前时间的前一天： 2020-06-28
yesterday = arrayyesterday.format("YYYY-MM-DD")

# 获取当前年月：  202006
currentmonth = arrayyesterday.format("YYYYMM")
intcurrentmonthmin = int(currentmonth.encode("utf-8"))
intcurrentmonth = int(curr_time.format("YYYYMM").encode("utf-8"))

# 获取当前时间的前一个月： 202005
lastmonth = arrayyesterday.shift(months=-1).format("YYYYMM")
intlastmonthmin = int(lastmonth.encode("utf-8"))
intlastmonth = int(curr_time.shift(months=-1).format("YYYYMM").encode("utf-8"))