from io import BytesIO

import subprocess
import pandas as pd

req_url = 'http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx?' \
        'name=fileDown' \
        '&filetype=xls' \
        '&url=MKD/04/0406/04060100/mkd04060100_01' \
        '&market_gubun=STK' \
        '&isu_cdnm=%EC%A0%84%EC%B2%B4' \
        '&sort_type=A' \
        '&lst_stk_vl=1' \
        '&isu_cdnm=%EC%A0%84%EC%B2%B4' \
        '&pagePath=%2Fcontents%2FMKD%2F04%2F0406%2F04060100%2FMKD04060100.jsp'

code = subprocess.check_output(["curl", req_url], universal_newlines=True)
req_url = 'http://file.krx.co.kr/download.jspx'
header = 'Referer: http://marketdata.krx.co.kr/mdi'

excel_file = subprocess.check_output(["curl", "-d", "code=" + code, "-H", header, "-X", "POST", req_url])

df = pd.read_excel(BytesIO(excel_file))

del df['번호']
df['종목코드'] = df['종목코드'].map(lambda x: f'{x:0>6}')
df['업종코드'] = df['업종코드'].map(lambda x: f'{x:0>6}')
df['상장주식수(주)'] = df['상장주식수(주)'].str.replace(",", "")
df['상장주식수(주)'] = pd.to_numeric(df['상장주식수(주)'])
df['자본금(원)'] = df['자본금(원)'].str.replace(",", "")
df['자본금(원)'] = pd.to_numeric(df['자본금(원)'])

print(df.head())
df.to_csv('company-info.csv', sep=',', na_rep='NaN')