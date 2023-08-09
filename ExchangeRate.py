import requests

url = "https://currency-converter5.p.rapidapi.com/currency/convert"

querystring = {"format":"json","from":"USD","to":"INR","amount":"1"}

headers = {
	"X-RapidAPI-Key": "Your Api Key from Rapid Api",
	"X-RapidAPI-Host": "currency-converter5.p.rapidapi.com"
}

def get_exchange_rate():
    """Retruns Dictionary with Exchange rate of one USD to INR as key 'Rate' and 'Date' on which exchange rate was last updated."""
    response = requests.get(url, headers=headers, params=querystring)

    theJson=response.json()

    Rate=theJson['rates']['INR']['rate']
    Date=theJson['updated_date']

    return {"Date":Date,"Rate":Rate}

