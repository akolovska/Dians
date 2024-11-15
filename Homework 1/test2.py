import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "https://www.mse.mk/en/stats/symbolhistory/SYMBOL?year=YEAR"
output_dir = "MSE_data"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

current_year = datetime.now().year
years_to_retrieve = 10


def filter_1_get_issuers():
    url = "https://www.mse.mk/en/stats/symbolhistory/TEL"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    issuers = [option['value'] for option in soup.select('select[name="Code"] option') if
               option['value'] and not any(char.isdigit() for char in option['value'])]
    return issuers


def filter_2_check_last_date(symbol):
    output_path = os.path.join(output_dir, f"{symbol}_data.csv")
    if os.path.exists(output_path):
        df = pd.read_csv(output_path)
        last_date = df['Date'].max()
        last_year = datetime.strptime(last_date, "%m/%d/%Y").year
        return last_year + 1
    return current_year - years_to_retrieve


def filter_3_fetch_data(symbol, year, session):
    url = BASE_URL.replace("SYMBOL", symbol).replace("YEAR", str(year))
    response = session.get(url)
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


def process_symbol(symbol):
    start_year = current_year - years_to_retrieve
    end_year = current_year
    all_data = pd.DataFrame()
    with requests.Session() as session:
        with ThreadPoolExecutor(max_workers=12) as executor:
            futures = [executor.submit(filter_3_fetch_data, symbol, year, session) for year in
                       range(start_year, end_year + 1)]
            for future in as_completed(futures):
                yearly_data = future.result()
                all_data = pd.concat([all_data, yearly_data])
                time.sleep(0.1)
    filter_4_save_data(symbol, all_data)


def main():
    start_time = time.time()
    company_symbols = filter_1_get_issuers()
    with ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(process_symbol, company_symbols)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"{elapsed_time:.2f}")


if __name__ == "__main__":
    main()
