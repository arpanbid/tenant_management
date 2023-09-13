def month_set(year):
    months_set = set()
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    for month_name in month_names:
        month_year = f"{month_name} {year}"
        months_set.add(month_year)
   
    
    
    return (months_set)




