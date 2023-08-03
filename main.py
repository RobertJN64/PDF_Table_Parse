import pandas as pd
import tabula
import json

def parse_table_simple(table, p_list):
    for _, row in table.iterrows():
        param = row[0]
        if isinstance(param, float):
            continue
        p_list.append(param)

def parse_table_4col(table, p_list):
    for _, row in table.iterrows():
        param = row[0]
        if isinstance(param, float):
            pass
        elif param == 'Reserved':
            p_list.append('_Reserved')
        elif row[2] == 'YYYYMMDDHHMMSS':
            p_list.append('*TIME ' + param)
        elif param == 'Tail Character':
            pass
        else:
            p_list.append(param)

def parse_table_5col(table, p_list):
    for _, row in table.iterrows():
        param = row[1]
        if isinstance(param, float):
            pass
        elif param == 'Reserved':
            p_list.append('_Reserved')
        elif param == 'Tail Character':
            pass
        else:
            p_list.append(param)

def main():
    pdf_path = "HYN001 protocol.pdf"

    dfs: list[pd.DataFrame] = tabula.read_pdf(pdf_path, stream=True, pages='5-46', pandas_options={'header': None})
    # read_pdf returns list of DataFrames
    last_valid_p_list = []
    j = {}
    for counter, table in enumerate(dfs):
        table: pd.DataFrame = table
        p_list = []
        if table[0][0] == 'SN':
            parse_table_5col(table[1:], p_list)
            j['GTXX' + str(counter)] = p_list
            last_valid_p_list = p_list
        else:
            print(table[0][0])
            if len(table.columns) == 5:
                parse_table_5col(table, last_valid_p_list)
        #
        # if len(table.columns) != 4:
        #     print(len(table.columns))
        #     parse_table_v2(table, p_list)
        #     j['GTXX' + str(counter)] = p_list

    with open('tables_out.json', 'w+') as f:
        json.dump(j, f, indent=4)

main()

