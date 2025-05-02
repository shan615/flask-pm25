from flask import Flask, render_template
from datetime import datetime
import pandas as pd
import pymysql
from pm25 import get_pm25_data_from_mysql, updata_db
import json

app = Flask(__name__)


@app.route("/filter")
def filter_data():
    county = request.args.get("county")
    columns, datas = get_pm25_data_from_mysql()
    df = pd.DataFrame(datas, columns=columns)

    df1 = df.groupby("county").get_group(county).groupby("site")["pm25"].mean()
    print(df1)
    return {"county": county}


@app.route("/updata-db")
def updata_pm25_db():
    count, message = updata_db
    nowtime = datetime.now().strftime("%Y-%m-%d")
    result = json.dumps(
        {"時間": nowtime, "更新筆數": count, "結果": message}, ensure_ascii=False
    )


@app.route("/")
def index():
    columns, datas = get_pm25_data_from_mysql()

    df = pd.DataFrame(datas, columns=columns)

    counties = sorted(df["county"].unique().tolist())

    county = request.arg.get("county", "ALL")
    if county != "ALL":
        df1 = df.groupby("county")["pm25"].mean().reset_index()
        x_data = df["county"].to_list()

    else:
        df = df.groupby("county").get_group(county)
        x_data = df["site"].to_list()

    y_data = df["pm25"].to_list()
    columns = df.columns.tolist()
    datas = df.values.tolist()

    return render_template(
        "index.html",
        columns=columns,
        data=datas,
        counties=counties,
        selected_county=selected_county,
        x_data=x_data,
        y_data=y_data,
    )


def get_pm25_data():
    api_url = "https://data.moenv.gov.tw/api/v2/aqx_p_02?api_key=540e2ca4-41e1-4186-8497-fdd67024ac44&limit=1000&sort=datacreationdate%20desc&format=CSV"
    df = pd.read_csv(api_url)
    df["datacreationdate"] = pd.to_datetime(df["datacreationdate"])
    df1 = df.dropna()
    return df1.values.tolist()


app.run(debug=True)
