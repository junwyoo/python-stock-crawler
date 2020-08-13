def make_isin(company_code):
        result = 0
        for i in range(0, len(company_code)):
                temp = int(company_code[i]) * (1 + (i % 2))
                if temp>=10:
                        result += int(temp / 10)
                        result += int(temp % 10)
                else:
                        result += temp
        result += 20

        return "KR7" + company_code + "00" + str((10 - result % 10) % 10)