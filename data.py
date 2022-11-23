from datetime import datetime, timedelta
import os

#vandaag = datetime.now()
#stdvandaag = vandaag.strftime("%Y-%m-%d")

#wd = os.getcwd()


#def create_date_file():
    #with open ("today.txt", "w") as bestand:
     #       bestand.write(stdvandaag)

#create_date_file()


# pas het databestand aan 





#read_date_file()     

def advanced_time(aantaldagen):
    with open ("today.txt", "w") as bestand:
        data_aangp = datetime.now() + timedelta(days=aantaldagen)
        #print("a" + data_aangp.strftime("%Y-%m-%d"))
        bestand.write(str(data_aangp.strftime("%Y-%m-%d")))  

def read_date_file():
    with open ("today.txt", "r") as bestand:
        date_set = bestand.readlines()
        return date_set        