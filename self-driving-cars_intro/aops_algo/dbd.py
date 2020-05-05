# days between dates

dom = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def leap_year(year):

    return year % 4 == 0

def days_between_dates(month1, day1, year1, month2, day2, year2):

    days = 0

    month1 -= 1
    month2 -= 1

    #days += (year2 - year1) * 365
    if (month2 - 1 % 12) != month1 or month1 != month2:
        month_diff = sum(dom[month1 + 1: month2 - 1])
        days += month_diff

    day_diff = (day2 - day1) if (month2 - month1) % 12 == 0 else dom[month1] - day1 + day2

    if year2 - year1 > 1:
        for y in range(year2 - year1):
            