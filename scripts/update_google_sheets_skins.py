import json
import os
import os.path

import gspread
import pandas as pd
from gspread_dataframe import set_with_dataframe

SPREADSHEET_ID = "1TIAECa8lDoAmQUTgX89DQgf5PfSHK_LLeXvUyw6OHfk"
BASE_URL = (
    f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv"
)

GID = {
    "SKINS": 0,
    "BANNERS": 749609107,
    "SPRAYS": 48422085,
    "FLEXES": 612041987,
}

ENDPOINTS = {
    "SKINS": f"{BASE_URL}&gid={GID['SKINS']}",
    "BANNERS": f"{BASE_URL}&gid={GID['BANNERS']}",
    "SPRAYS": f"{BASE_URL}&gid={GID['SPRAYS']}",
    "FLEXES": f"{BASE_URL}&gid={GID['FLEXES']}",
}


def get_current_google_sheets_as_df():
    # Open up the spreadsheets and read the collections across all sheets
    SKINS = pd.read_csv(ENDPOINTS["SKINS"], index_col="id")
    BANNERS = pd.read_csv(ENDPOINTS["BANNERS"], index_col="id")
    SPRAYS = pd.read_csv(ENDPOINTS["SPRAYS"], index_col="id")
    FLEXES = pd.read_csv(ENDPOINTS["FLEXES"], index_col="id")
    return SKINS, BANNERS, SPRAYS, FLEXES


def update_skins_tags_in_sheet(
    SKINS: pd.DataFrame, skins_data: list[dict], save_output: bool = False
):
    skins_df = pd.DataFrame(skins_data)
    combined = pd.concat([SKINS, skins_df], ignore_index=True)
    final_skins = combined.drop_duplicates(
        subset=["skin_name", "skin_type"], keep="first"
    )
    if save_output:
        final_skins.to_csv(
            os.path.join(os.path.dirname(__file__), "../data/final_skins.csv"),
            index=True,
            index_label="id",
        )

    # Upload to Google Sheets
    try:
        gc = gspread.service_account(
            filename=os.path.join(os.path.dirname(__file__), "../credentials.json")
        )
        sh = gc.open_by_key(SPREADSHEET_ID)
        worksheet = sh.get_worksheet_by_id(GID["SKINS"])
        worksheet.clear()
        final_skins.reset_index(inplace=True, names=["id"])
        final_skins.index_name = "id"
        set_with_dataframe(worksheet, final_skins)
        print("Google Sheets updated successfully.")
    except Exception as e:
        print(f"Error updating Google Sheets: {e}")


with open(os.path.join(os.path.dirname(__file__), "../data/skins_with_tags.json")) as f:
    skins_data = json.load(f)
    # 1. Load and clean SKINS (Google Sheets data)
    SKINS, BANNERS, SPRAYS, FLEXES = get_current_google_sheets_as_df()
    # Remove any "Unnamed" ghost columns from the Google Sheet
    SKINS = SKINS.loc[:, ~SKINS.columns.str.contains("^Unnamed")]
    update_skins_tags_in_sheet(SKINS, skins_data)
