# Delays_BeautifulSoup
The script was created as part of the master's thesis and was aimed at collecting data about train delays at a railway station from the passenger portal. Then the data was stored in the SQLite database.
## Features
- Retrieves data about train delay in minutes
- Retrieves train path data
- Retrieves data about the railway carrier and the name of the train
- Connection to SQLite database
## Installation
Beautiful Soup is a Python library for pulling data out of HTML and XML files.
```bash
pip install beautifulsoup4
```
## Usage
The requests module plays a primary role in the process of retrieving data from a website, as it is responsible for sending a query to it and requesting the data it has in the source of the page. The result of the correct execution of this process is the Response object, and the downloaded web page is saved in it as a string of a text variable.
```python
import requests
from bs4 import BeautifulSoup
import sqlite3
```
The created parse_page (number) method downloads from the website data about all delayed trains at the station in Katowice. Then, the collected data is assigned to the appropriate columns in the table and saved in the SQLite database.
```python
URL = 'https://portalpasazera.pl/Opoznienia?s=2&sid=BuyYisF6KXxTPVVt1T66eQY1aVrVbRVKmscc2BaECdhgbIUlHwmkYiK5TBVLX67kKQ5DotJ3scc2BU9KeAalfn8hMx3BwalOaUkgqi6hn9qscc2Bqmf30xDscc2BqTGIepaxFmWK9trJZt2p&p={}'.format(number)
response = requests.get(URL)
bs = BeautifulSoup(response.content, 'html.parser')
```
The for loop finds all the necessary classes in the source code of the web page.
```python
for delay in bs.find_all('div', class_='row delays-table__row abt-focusable'):

    # parse data about the railway carrier
    przewoznik = parse_przewoznik(delay.find('h3', class_='item-value').get_text(strip=True))
    # parse train path data
    relacja = parse_relacja(delay.find('div', class_='col-3 col-6--phone').get_text(strip=True))
    # parse data about train delay in minutes
    czas = parse_czas(delay.find('strong', class_='item-value color--alert txlc').get_text(strip=True))
    # parse data about the name of the train
    pociag = delay.find('strong', class_='item-value').get_text(strip=True)
    
    cursor.execute('INSERT INTO Katowice VALUES (?, ?, ?, ?)', (przewoznik, relacja, czas, pociag))
 db.commit()
```
Connection to SQLite database.
```python
db = sqlite3.connect('Katowice.db')
cursor = db.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS Katowice (przewoznik text, relacja text, czas real, pociag text)''')
```
### A fragment of the website's source code with the train delay time.
```html
<div class="col-2 col-6--phone">
   <span class="item-label visible--phone">Czas opóźnienia</span>
   <span class="visuallyhidden hidden--phone">Czas opóźnienia</span>
   <strong class="item-value color--alert txlc">56 Min</strong>
</div>
```
## Result
![database](https://user-images.githubusercontent.com/57764193/142311368-f5da269e-963b-4ef2-a3d7-34d4a5b04260.png)

