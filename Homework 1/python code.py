import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
from datetime import datetime

BASE_URL = "https://www.mse.mk/en/stats/symbolhistory/SYMBOL?year=YEAR"

output_dir = "MSE_data"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

current_year = datetime.now().year
years_to_retrieve = 10

start_time = time.time()


def filter_1_get_issuers():
    url = "https://www.mse.mk/en/stats/symbolhistory/TEL"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Extracting the options from the dropdown menu
    issuers = [option['value'] for option in soup.select('select[name="Code"] option') if option['value']]
    return issuers


def filter_2_check_last_date(symbol):
    output_path = os.path.join(output_dir, f"{symbol}_data.csv")
    if os.path.exists(output_path):
        df = pd.read_csv(output_path)
        last_date = df['Date'].max()
        last_year = datetime.strptime(last_date, "%m/%d/%Y").year
        return last_year + 1
    return current_year - years_to_retrieve


def filter_3_fetch_data(symbol, year):
    url = BASE_URL.replace("SYMBOL", symbol).replace("YEAR", str(year))
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table")

        if table:
            rows = table.find_all("tr")
            headers = [header.text.strip() for header in rows[0].find_all("th")]
            data = []
            for row in rows[1:]:
                columns = row.find_all("td")
                data.append([col.text.strip() for col in columns])

            df = pd.DataFrame(data, columns=headers)
            return df

    return pd.DataFrame()


def filter_4_save_data(symbol, all_data):
    output_path = os.path.join(output_dir, f"{symbol}_data.csv")
    if not all_data.empty:
        all_data.to_csv(output_path, index=False)


company_symbols = filter_1_get_issuers()

for symbol in company_symbols:
    start_year = filter_2_check_last_date(symbol)
    all_data = pd.DataFrame()

    for year in range(start_year, current_year + 1):
        yearly_data = filter_3_fetch_data(symbol, year)
        all_data = pd.concat([all_data, yearly_data])
        time.sleep(1)

    filter_4_save_data(symbol, all_data)

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Total time taken to scrape all data: {elapsed_time / 60:.2f} minutes")
