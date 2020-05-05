# days between dates

dom = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def leap_year(year):

    return year % 4 == 0

def month_diff(month1, day1, month2, day2):
    
    days = dom[month1] - day1 + day2

    if (month1 + 1) % 12 == month2:
        return days

    else:

        days += sum(dom[month1 + 1: month2 - 1])

    return days

def days_between_dates(month1, day1, year1, month2, day2, year2):

    days = 0

    month1 -= 1
    month2 -= 1

    if year1 == year2:
        
        if month1 == month2:
            return day2 - day1

    else:
        num_leap_years = 0

        for year in range(year1 + 1, year2):
            if leap_year(year):
                num_leap_years += 1

        if leap_year(year1) and month1 <= 1:
            num_leap_years += 1

        if leap_year(year2) and month2 > 1:
            num_leap_years += 1

        days += num_leap_years

        if year2 - year1 > 1:
            days += (year2 - year1 - 1) * 365

    
    days += month_diff(month1, day1, month2, day2)


    # old

    #days += (year2 - year1) * 365
    if (month2 - 1 % 12) != month1 and month1 != month2:
        month_diff = sum(dom[month1 + 1 % 12: month2 - 1 % 12])
        days += month_diff

    day_diff = (day2 - day1) if (month2 - month1) % 12 == 0 else dom[month1] - day1 + day2
    days += day_diff

    if year2 - year1 > 1:

        num_leap_years = 0

        for y in range(1, year2 - year1):
            if leap_year(year1 + y):
                num_leap_years += 1

        year_diff = (year2 - year1 - 1) * 365 + num_leap_years
        days += year_diff

    else:
        days += sum(dom[month1 + 1 % 12: month2 - 1 % 12])
        days += (day2 - day1) if (month2 - month1) % 12 == 0 else dom[month1] - day1 + day2

    return days

if __name__ == "__main__":

    #print(days_between_dates(1, 1, 2020, 1, 2, 2020))
    #print(month_diff(0, 1, 1, 15))