import time

def Showtime(key="$ + year/mon/f_mon/week/day/f_day/hour/min/sec/time/apm/b_time"):
    """   time.strftime  """
    key=key.replace("$f_week",r"%A")\
    .replace("$f_mon",r"%B")\
    .replace("$day",r"%d")\
    .replace("$hour",r"%H")\
    .replace("$f_day","%j")\
    .replace("$mon",r"%m")\
    .replace("$min",r"%M")\
    .replace("$apm",r"%p")\
    .replace("$week",r"%w")\
    .replace("$sec",r"%S")\
    .replace("$time",r"%X")\
    .replace("$year",r"%Y")\
    .replace("$b_time",r"%Y-%m-%d %X")
    return time.strftime(key)
    
def Timelog(func):
    name=func.__name__
    print("function name:",name," --time:",time.strftime(r"%Y-%m-%d %X"),"\n"+"-"*50)
    t=time.time()
    func()
    t2=time.time()
    print("\n"+"-"*50+"\nfunction name:",name," --time:",time.strftime(r"%Y-%m-%d %X"),"\nCost time:",t2-t)

def Simple_timelog(func):
    t=time.time()
    func()
    return print(time.time()-t)
