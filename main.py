import requests
import json 
import argparse
import datetime
import matplotlib.pyplot as plt
import pandas as pd


def request_get(url: str):
    url_result = requests.get(url)
    rec_data = json.loads(url_result.text)
    return rec_data

def df_to_table_png(df: pd.DataFrame,name: str):
    # plt.rcParams["figure.figsize"] = [10, 10]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots(1, 1)
    data = df.values
    columns = df.columns
    ax.axis('tight')
    ax.axis('off')
    the_table = ax.table(cellText=data, colLabels=columns, loc='center')
    # the_table.auto_set_font_size(False)
    the_table.set_fontsize(20)
    # the_table.scale(2, 2)
    plt.savefig(name)

CITY_CODE = "311001"
MIN_AGE = 45
DATE = datetime.datetime.strftime(datetime.datetime.today(),"%d-%m-%Y")
COLUMNS = ['name', 'address', 'state_name', 'district_name',
       'block_name', 'from', 'to','date', 'available_capacity', 'fee', 'min_age_limit',
       'vaccine', 'slots']
api_url = (
    "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode="
    + CITY_CODE
    + "&date="
    + DATE
)

data = request_get(api_url)
list_of_avail_centers = data["sessions"]

if len(list_of_avail_centers) == 0:
    print("No Centers available today. SAD")
else:
    filtered = []
    for center_info in list_of_avail_centers:
        if center_info["min_age_limit"] <= MIN_AGE and center_info["available_capacity"] > 0:
            filtered.append(center_info)
    if len(filtered) == 0:
        print("No results for minimum age :",MIN_AGE)
    else:
        
        df = pd.DataFrame(filtered)
        df = df[COLUMNS]
        df_to_table_png(df,'mytable.png')