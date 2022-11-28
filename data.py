from datetime import datetime, timedelta, date
import os

 

def advanced_time(aantaldagen):
    with open ("today.txt", "w") as bestand:
        data_aangp = datetime.now() + timedelta(days=aantaldagen)
        bestand.write(str(data_aangp.strftime("%Y-%m-%d")))
        print("Ingstelde datum is: "+str(data_aangp.strftime("%Y-%m-%d")))  



def read_date_file():
    with open ("today.txt", "r") as bestand:
        date_set = bestand.readlines()
        return date_set
        #print(date_set[0])        