import csv
from csv import writer
from csv import reader
from csv import DictReader
import os
import pandas as pd
from datetime import datetime
from datetime import timedelta
from datetime import date
from rich import print  as print_table
from rich_tools import df_to_table
import data
import math


# de datum uit today.txt wordt uitgelezen en als varibale stdvandaag aangemaakt die gebruikt wordt in de functies die hiermee moeten werken
vandaag = data.read_date_file()
stdvandaag = str(vandaag[0])

def vandaag():
    print(stdvandaag)

def create_bought():
    if os.path.exists("bought.csv") is not True:
        with open ("bought.csv", "w", newline='') as csvfile:
            id = '1'
            fieldnames = ('Id','artikel', 'prijs', 'date_exp', 'date_add', 'status', 'verk_prijs', 'mutatie_date')
            nieuwfile = csv.writer(csvfile)
            nieuwfile.writerow(fieldnames)
    else:
        return print("Bought.csv already exists")

def buy_product(artnm, artpr, expdate):
    if os.path.exists("bought.csv") is not True:
       create_bought()
       with open ('bought.csv', 'a', newline='') as csvfile:
            id = 1 + len(pd.read_csv("bought.csv"))
            item_data = id , artnm, artpr, expdate, stdvandaag, 'voorraad'
            nieuwfile = writer(csvfile)
            nieuwfile.writerow(item_data)
            print("Artikel: " + artnm + ' is toegevoegd aan de voorraad. De toevoegdatum (date_add) is: ' + stdvandaag)
    else:
        with open ('bought.csv', 'a', newline='') as csvfile:
            id = 1 + len(pd.read_csv("bought.csv"))
            item_data = id , artnm, artpr, expdate, stdvandaag, 'voorraad'
            nieuwfile = writer(csvfile)
            nieuwfile.writerow(item_data)
            df = pd.read_csv("bought.csv")
            df.sort_values(by=['date_exp'], inplace=True)
            df.to_csv('bought.csv', index=False)
            print("Artikel: " + artnm + ' is toegevoegd aan de voorraad. De toevoegdatum (date_add) is: ' + stdvandaag)

def show_inventory(x):
    df = pd.read_csv("bought.csv")
    inventory = df.loc[(df['status']=='voorraad') & (df['date_exp'] >= stdvandaag)] 
    if x == 'alles':
        table = df_to_table(inventory)
        print_table(table)
    elif x == 'aantal':   
        aantal = inventory.groupby('artikel')['prijs'].agg(['sum', 'count'])
        aantal2 = aantal.rename(columns={"sum":"Inkoopwaarde", "count":"Aantal"})
        print("Aantal beschikbare items per artikel:")
        print(aantal2)

def compleet():
    df = pd.read_csv("bought.csv")
    table = df_to_table(df)
    print_table(table)

def show_expired():
    df = pd.read_csv("bought.csv")
    expired = df.loc[df['status']=='expired'] 
    table = df_to_table(expired)
    print("Onderstaande producten zijn expired")
    print_table(table)

def expired():
    df = pd.read_csv("bought.csv")  
    df.loc[(df['date_exp'] <= stdvandaag) & (df['status'] == 'voorraad'), ['status', 'mutatie_date']]  = ['expired', stdvandaag]
    aantal_expired = df['status'].value_counts().expired
    df.to_csv('bought.csv', index=False)
    print(str(aantal_expired)+" product(en) hebben de status expired")


def sell_product(naam, prijs):
    df = pd.read_csv("bought.csv")
    if naam in df['artikel'].values:
        selectie = df.loc[(df['artikel'] == naam) & (df['status'] == 'voorraad')] 
        if len(selectie) == 0:
            print(naam + " is niet beschikbaar voor aankoop, niet op voorraad of expired")
        else:
            verkoop_id = (selectie['Id'].loc[selectie.index[0]])
            df.loc[df['Id'] == verkoop_id, ['status', 'verk_prijs', 'mutatie_date']] = ['verkocht', prijs, stdvandaag]
            df.to_csv('bought.csv', index=False)
            verkoop = df.loc[df['Id'] == verkoop_id]
            print("Onderstaande artikel is verkocht")
            print(verkoop)
    else:
        print(naam +" artikel zit niet in het assortiment")

def correct(id, kolom, waarde):
    df = pd.read_csv("bought.csv")
    print("De volgende regel:")
    selectie = df.loc[df['Id'] == id]
    print(selectie)
    df.loc[df['Id'] == id, kolom] = waarde
    print("Is aangepast naar:")
    selectie = df.loc[df['Id'] == id]
    print(selectie)
    df.to_csv('bought.csv', index=False)
    

def omzet(date_input):
    if date_input == 'vandaag':
        datum = stdvandaag
        df = pd.read_csv("bought.csv")
        selectie = df.loc[(df['status'] == 'verkocht') & (df['mutatie_date'] == datum)]
        omzet = (selectie['verk_prijs']).sum()
        print("Vandaag is de omzet: " + str(omzet))
    elif date_input == 'gisteren':
        datum = datetime.strptime(stdvandaag, '%Y-%m-%d') + timedelta(days=-1)
        stddatum = datum.strftime("%Y-%m-%d") 
        df = pd.read_csv("bought.csv")
        selectie = df.loc[(df['status'] == 'verkocht') & (df['mutatie_date'] == stddatum)]
        omzet = (selectie['verk_prijs']).sum()
        print("Gisteren was de omzet: " + str(omzet)) 
    else:
        df = pd.read_csv("bought.csv")
        selectie = df.loc[(df['status'] == 'verkocht') & (df['mutatie_date'].str.startswith(date_input))]
        omzet = (selectie['verk_prijs']).sum()
        print("De omzet voor deze datum / periode " + str(date_input) + ' is ' + str(omzet)) 

def opbrengst(date_input):
    if date_input == 'vandaag':
        datum = stdvandaag
        df = pd.read_csv("bought.csv")
        selectie = df.loc[(df['status'] == 'verkocht') & (df['mutatie_date'] == datum)]
        opbrengst = (selectie['verk_prijs'] - selectie['prijs']).sum()
        print("Vandaag is de opbrengst " + str(opbrengst))
    elif date_input == 'gisteren':
        datum = datetime.strptime(stdvandaag, '%Y-%m-%d') + timedelta(days=-1)
        stddatum = datum.strftime("%Y-%m-%d")
        df = pd.read_csv("bought.csv")
        selectie = df.loc[(df['status'] == 'verkocht') & (df['mutatie_date'] == stddatum)]
        opbrengst = (selectie['verk_prijs'] - selectie['prijs']).sum()
        print("Gisteren was de opbrengst " + str(opbrengst))
    else:
        df = pd.read_csv("bought.csv")
        selectie = df.loc[(df['status'] == 'verkocht') & (df['mutatie_date'].str.startswith(date_input))]
        opbrengst = (selectie['verk_prijs'] - selectie['prijs']).sum()
        print("De opbrengst voor deze datum / periode " + str(date_input) + ' is ' + str(opbrengst))

def korting(percentage):
    df = pd.read_csv("bought.csv")
    morgen = data.read_date_file()
    morgen_to_date = datetime.strptime(morgen[0], '%Y-%m-%d')
    morgen = morgen_to_date + timedelta(days=1)
    stdmorgen = morgen.strftime("%Y-%m-%d")
    if stdmorgen in df['date_exp'].values:   
        df.loc[(df['date_exp'] == stdmorgen) & (df['status'] == 'voorraad'), 'prijs'] = round((df['prijs'] * (1-(percentage / 100))), 2)
        selectie = df.loc[(df['date_exp'] == stdmorgen) & (df['status'] == 'voorraad')]
        print(selectie)
        df.to_csv('bought.csv', index=False)
    else:
        print("Er komen geen artikelen in aanmerking voor korting")    