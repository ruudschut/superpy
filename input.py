import argparse
import csvbeheer
import data


parser = argparse.ArgumentParser(description='SuperPy voorraadbeheer')

subparsers = parser.add_subparsers(dest='command')

start = subparsers.add_parser("start", help='check voor csv')

expired = subparsers.add_parser("expired", help='zet voorraad op expired')

korting = subparsers.add_parser("korting", help="Artikelen die morgen expired zijn worden in prijs verlaagd")
korting.add_argument("-kp", "--kortingspercentage", default=10, type=float, help="Geef aan hoeveel korting er gegeven moet worden")

vandaag = subparsers.add_parser("vandaag", help="Welke datum staat als 'vandaag' ingesteld")

advancedtime = subparsers.add_parser("advancedtime",  help="past de datum van vandaag aan, input is aantal dagen")
advancedtime.add_argument("-ad", "--aantaldagen", default=0, type=int, help="hoeveel dagen naar voren of naar achteren")

rapport = subparsers.add_parser("rapport", help='creeer een rapport voor inventory, expoired, omzet of opbrengst over een periode')
rapport.add_argument("soort", choices=['inventory', 'expired', 'omzet', 'opbrengst', 'compleet'], help='kies het type rapport')
rapport.add_argument("-v", "--versie", choices=['alles', 'aantal'],  required=False, help='Uitgebreide inventory, of aantal items')
rapport.add_argument("-d", "--datum", default=0, type=str, required=False, help='welke datum?')

buy = subparsers.add_parser("buy", help='koop een item')
buy.add_argument("-n", "--naam", type=str, required=True,help='naam van artikel')
buy.add_argument("-p", "--prijs", type=float, required=True,help='aankoop prijs formaat 2.00')
buy.add_argument("-e", "--expdate", required=True, help="Expiration date")

sell = subparsers.add_parser("sell", help='verkoop een item')
sell.add_argument("-n", "--naam", type=str, required=True,help='naam van artikel')
sell.add_argument("-p", "--prijs", type=str, required=True,help='verkoopprijs')

correct = subparsers.add_parser("correct", help='pas een waarde van een regel in het bestand aan op basis van ID')
correct.add_argument("--id", type=int, required=True,help="geef het ID op van de artikel regel")
correct.add_argument("-k", "--kolom", type=str, choices=['artikel', 'prijs', 'date_exp', 'date_add', 'status'], help="kies in welke kolom de waarde aangepast moet worden")
correct.add_argument("-w", "--waarde", type=str, help="geef de nieuwe waarde op")

args = parser.parse_args()

if args.command == 'start':
    csvbeheer.create_bought()

if args.command == 'expired':
    csvbeheer.expired()  

if args.command == 'vandaag':
    csvbeheer.vandaag()
    data.read_date_file()    

if args.command == 'rapport':
    if args.soort == 'inventory':
        csvbeheer.show_inventory(args.versie)
    if args.soort == 'expired':
        csvbeheer.show_expired()
    if args.soort == 'omzet':
        if args.datum == 'gisteren':
            csvbeheer.omzet(args.datum)
        elif args.datum == 'vandaag':
            csvbeheer.omzet(args.datum)  
        else:
            csvbeheer.omzet(args.datum)
    if args.soort == 'opbrengst':
        if args.datum == 'gisteren':
            csvbeheer.opbrengst(args.datum)
        elif args.datum == 'vandaag':
            csvbeheer.opbrengst(args.datum)  
        else:
            csvbeheer.opbrengst(args.datum)
    if args.soort == 'compleet':
        csvbeheer.compleet()

if args.command == 'advancedtime':
    data.advanced_time(args.aantaldagen)

if args.command == 'buy':
    csvbeheer.buy_product(args.naam, args.prijs, args.expdate)

if args.command == 'sell':
    csvbeheer.expired()
    csvbeheer.sell_product(args.naam, args.prijs)

if args.command == 'correct':
        csvbeheer.correct(args.id, args.kolom, args.waarde)    

if args.command == 'korting':
    csvbeheer.korting(args.kortingspercentage)