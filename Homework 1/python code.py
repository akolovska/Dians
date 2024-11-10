import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
from datetime import datetime

BASE_URL = "https://www.mse.mk/en/stats/symbolhistory/SYMBOL?year=YEAR"
company_symbols = [
    "TEL", "KMB", "STB", "ALK", "ALKB", "AMEH", "APTK", "ATPP", "AUMK", "BANA",
    "BGOR", "BIKF", "BIM", "BLTU", "CBNG", "CDHV", "CEVI", "CKB", "CKBKO",
    "DEBA", "DIMI", "EDST", "ELMA", "ELNC", "ENER", "ENSA", "EUHA", "EUMK",
    "EVRO", "FAKM", "FERS", "FKTL", "FOMK", "GLO", "GRKI", "GNB", "GRC",
    "HAPA", "HOYA", "HUM", "ILEX", "INVI", "IRAC", "ITSP", "KAP", "KAKV",
    "KAX", "KEIN", "KGL", "KOL", "KONT", "KRIN", "KTP", "LIR", "LUX",
    "MKD", "MGM", "MTB", "MZK", "NEUK", "NEZN", "NGK", "NLB", "NLBK",
    "NLG", "NPT", "OHR", "OHRP", "OKEG", "OPT", "ORCE", "OZ", "PBP",
    "PEST", "PLPT", "PRIN", "PNT", "RBA", "RAK", "RBKR", "RUB", "SBU",
    "SHNK", "SKOP", "SMAG", "SMK", "SNK", "SNT", "SNP", "SOF", "SRB",
    "STUB", "TAN", "TKO", "TLM", "VAP", "VIK", "VIT", "VLB", "ZST",
    "ZSE", "М101039", "М190927", "М190939", "M010428", "M010428D", "M010931D",
    "M011133D", "M011231D", "M011237", "M020126", "M020127", "M021132D",
    "M030337", "M030338", "M031131D", "M031230D", "M031235D", "M040336",
    "M040532D", "M040630D", "M040837", "M040837D", "M040838", "M041224",
    "M050325", "M050836", "M050939", "M051032D", "M051125", "M051234D",
    "M060432D", "M060629", "M060639", "M060732D", "M060825D", "M060830D",
    "M060850D", "M070329", "M070339", "M070426D", "M070530D", "M070633",
    "M070932D", "M070938", "M070938D", "M071134", "M071232D", "M080229",
    "M080239", "M080333D", "M080632D", "M080731D", "M080834D", "M080839",
    "M081030D", "M090238", "M090332D", "M090631D", "M090725", "M090725D",
    "M090730D", "M090833D", "M090937", "M090937D", "M100526", "M100539",
    "M100832D", "M110128", "M110133D", "M110139", "M110226", "M110226D",
    "M110231D", "M110538", "M110739", "M120132D", "M120138", "M120230D",
    "M120325", "M120330D", "M120439", "M120439D", "M120537", "M130137",
    "M130235", "M130738", "M131037", "M140126D", "M140131D", "M140136",
    "M140431D", "M140437D", "M140526", "M141031D", "M141036", "M141226",
    "M141238", "M150233D", "M150436", "M150436D", "M150638", "M150638D",
    "M151030", "M151030D", "M160225", "M160232D", "M160430D", "M160534",
    "M160637", "M160637D", "M160936", "M161138", "M161224", "M170331D",
    "M170636", "M170636D", "M170832D", "M170930D", "M171137", "M171225D",
    "M180449D", "M180635", "M180749D", "M180826", "M180826D", "M180831D",
    "M180837D", "M181048D", "M181136D", "M190748D", "M190934", "M191032D",
    "M191125D", "M191130D", "M200732D", "M200738", "M200825", "M200830D",
    "M200933", "M200933D", "M210525D", "M210633D", "M210932D", "M210938",
    "M220131D", "M220632D", "M220931D", "M221133D", "M221231D", "M230332D",
    "M230631D", "M230725D", "M230730D", "M231132D", "M240326", "M240925D",
    "M240930D", "M241225D", "M250133", "M250133D", "M250625", "M250625D",
    "M250630D", "M251027", "M260132D", "M260230D", "M260325", "M260330D",
    "M260448D", "M260538D", "M270125", "M270825", "M270825D", "M270830D",
    "M280131D", "M280234", "M280731D", "M281238D", "M290125", "M290125D",
    "M290632D", "M290638D", "M290931D", "M291030D", "M291035", "M291237",
    "M291237D", "M300150D", "M300332D", "M300338", "M300338D", "M300450D",
    "M300637", "M300730D", "M301132D", "M310149D", "M310331D", "M311049D"
]

output_dir = "MSE_data"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

current_year = datetime.now().year
years_to_retrieve = 10

start_time = time.time()

for symbol in company_symbols:
    for year in range(current_year - years_to_retrieve, current_year):
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

                output_path = os.path.join(output_dir, f"{symbol}_{year}.csv")
                df.to_csv(output_path, index=False)

            else:
                break
        else:
            print(f"Failed to retrieve data for {symbol} in {year}, status code: {response.status_code}")

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Total time taken to scrape all data: {elapsed_time / 60:.2f} minutes")