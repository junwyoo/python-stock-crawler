from io import BytesIO
import subprocess
import pandas as pd

from util import make_isin


def get_quote_daily(company_code, fromdate, todate, silent=False):
        stderr_dest = None
        if silent:
                stderr_dest = subprocess.DEVNULL

        isin_code = make_isin(company_code)
        req_url = 'http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx?' \
                'name=fileDown' \
                '&filetype=xls' \
                '&url=MKD/04/0402/04020100/mkd04020100t3_02' \
                '&market_gubun=STK' \
                '&isu_cdnm=A' + company_code + '%2F%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90' \
                '&isu_cd=' + isin_code + '&isu_nm=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90' \
                '&isu_srt_cd=A' + company_code + \
                '&fromdate=' + fromdate + \
                '&todate=' + todate + \
                '&pagePath=%2Fcontents%2FMKD%2F04%2F0402%2F04020100%2FMKD04020100T3T2.jsp'
        shell_command = ["curl", req_url]
        code = subprocess.check_output(shell_command, universal_newlines=True, stderr=stderr_dest)

        req_url = 'http://file.krx.co.kr/download.jspx'
        header = 'Referer: http://marketdata.krx.co.kr/mdi'
        shell_command = ["curl", "-d", "code=" + code, "-H", header, "-X", "POST", req_url]
        excel_file = subprocess.check_output(shell_command, stderr=stderr_dest)

        return pd.read_excel(BytesIO(excel_file))


if __name__ == "__main__":
        company_code = '005930'
        fromdate = '20200706'
        todate = '20200813'

        df = get_quote_daily(company_code, fromdate, todate, True)
        df.to_csv('quote-' + company_code + '.csv', sep=',', na_rep='NaN')