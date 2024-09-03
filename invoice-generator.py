import requests
from datetime import date, timedelta
import pyperclip
from dotenv import dotenv_values

today = date.today()

def get_dollar_exchange_rate(salary_value):
    base_url = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao='"
    
    data = {'value': []}

    days=0
    while not data['value']:
        days += 1
        yesterday_date = get_last_exchange_date(days)[0]
        url = f"{base_url}{yesterday_date}'&$top=100&$skip=0&$format=json&$select=cotacaoVenda"
        response = requests.get(url)
        data = response.json()

    dolar = data['value'][0]['cotacaoVenda']
    real = round(1 / dolar, 6)
    converted_value = salary_value * dolar
    
    return [dolar, real, converted_value, days]

def get_last_exchange_date(days=1):
    yesterday = today - timedelta(days=days)
    yesterday_date_us = yesterday.strftime("%m-%d-%Y")
    yesterday_date_br = yesterday.strftime("%d/%m/%Y")
    return [yesterday_date_us, yesterday_date_br]

salary_value = int(dotenv_values(".env")['SALARY'])

exchange_rate = get_dollar_exchange_rate(salary_value)

day = int(today.strftime("%d"))
month = int(today.strftime("%m"))
month_name = today.strftime("%B")
year = int(today.strftime("%Y"))

period_of_month = [1, 15] if day < 16 else [16, day]

invoice_name = f"DOCUMENT INV-{year}-{month*2-1 if day < 16 else month*2}" 


invoice = f"""
{invoice_name}
ISSUE DATE {month_name} {period_of_month[1]-5}, {year}

Perform the duties of customizing, building data connectors, and specialized apps for working with our Odoo ERP implementation. 
Will also work as a full stack developer building software for our customers, manufactures, and our own internal operations.

Invoice for work between {month_name} {period_of_month[0]}, {year} to {month_name} {period_of_month[1]}, {year}

Valor em: USD ${format(salary_value, ",.2f")}
Resultado da conversão: {exchange_rate[2]}

Data cotação utilizada: {get_last_exchange_date(exchange_rate[3])[1]}
Taxa:
1 Dólar dos Estados Unidos/USD (220) = {exchange_rate[0]} Real/BRL (790)
1 Real/BRL (790) = {exchange_rate[1]} Dólar dos Estados Unidos/USD (220)

"""

print(invoice)

pyperclip.copy(invoice)
