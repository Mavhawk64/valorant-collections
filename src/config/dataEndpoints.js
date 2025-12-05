const SPREADSHEET_ID = "1TIAECa8lDoAmQUTgX89DQgf5PfSHK_LLeXvUyw6OHfk";
const BASE_URL = `https://docs.google.com/spreadsheets/d/${SPREADSHEET_ID}/gviz/tq?tqx=out:csv`;
export const ENDPOINTS = {
    SKINS: `${BASE_URL}&gid=0`,
    BANNERS: `${BASE_URL}&gid=749609107`,
    SPRAYS: `${BASE_URL}&gid=48422085`,
    FLEXES: `${BASE_URL}&gid=612041987`,
};
