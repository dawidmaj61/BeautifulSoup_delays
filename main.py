import requests
from bs4 import BeautifulSoup
import sqlite3

def parse_przewoznik(przewoznik):
    return przewoznik.replace('Przewoźnik', '')
def parse_relacja(relacja):
    return relacja.replace('Relacja', '')
def parse_czas(czas):
    return float(czas.replace(' ', '').replace('Min', ''))

def parse_page(number):
    print('Pobieram dane ze strony numer', number)
    URL = 'https://portalpasazera.pl/Opoznienia?s=2&sid=BuyYisF6KXxTPVVt1T66eQY1aVrVbRVKmscc2BaECdhgbIUlHwmkYiK5TBVLX67kKQ5DotJ3scc2BU9KeAalfn8hMx3BwalOaUkgqi6hn9qscc2Bqmf30xDscc2BqTGIepaxFmWK9trJZt2p&p={}'.format(number)
    response = requests.get(URL)
    bs = BeautifulSoup(response.content, 'html.parser')

    for delay in bs.find_all('div', class_='row delays-table__row abt-focusable'):
        przewoznik = parse_przewoznik(delay.find('h3', class_='item-value').get_text(strip=True))
        relacja = parse_relacja(delay.find('div', class_='col-3 col-6--phone').get_text(strip=True))
        czas = parse_czas(delay.find('strong', class_='item-value color--alert txlc').get_text(strip=True))
        pociag = delay.find('strong', class_='item-value').get_text(strip=True)

        cursor.execute('INSERT INTO Katowice VALUES (?, ?, ?, ?)', (przewoznik, relacja, czas, pociag))
    db.commit()

db = sqlite3.connect('Katowice.db')
cursor = db.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS Katowice (przewoznik text, relacja text, czas real, pociag text)''')

for number in range(1,3):
    parse_page(number)


db.close()

