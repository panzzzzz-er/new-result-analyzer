import pandas as pd
import add_header as ah

def remove_rows_columns(result):
    result = result.iloc[10:]
    cheads = [x for x in range(len(result.columns))]
    result.columns = cheads

    result = result.drop(2, axis=1)
    result = result.drop(3, axis=1)

    if len(result.columns) == 31:
        result = result.drop(32, axis=1)
    elif len(result.columns) == 33:
        result = result.drop(34, axis=1)
    elif len(result.columns) == 35:
        result = result.drop(36, axis=1)
    elif len(result.columns) == 36:
        result = result.drop(37, axis=1)

    return result


def correct_rows_columns(result):

    # print(len(result.columns))
    sorted_columns = sorted(result.columns)
    result = result[sorted_columns]

    result = result.reset_index(drop=True)
    result.index = [x for x in range(0, len(result))]

    return result


def find_junk_indices(result):
    pos = []
    for i in range(len(result[1])):
        if result[1][i] == '/ : FEMALE, # : 0.229, @ : 0.5042, * : 0.5045, ADC : ADMISSION CANCELLED, RR : RESERVED, -- : Fails in Theory or Practical, RPV : PROVISIONAL, RCC : 0.5050, AA : ABSENT, F : FAILS, P : PASSES, NULL : NULL & VOID':
            pos.append(i)
    return pos


def cleared_result(result_cleared, result):

    pos = find_junk_indices(result)
    n = len(pos)
    result_cleared = result.iloc[0:pos[0]]

    for i in range(1, n):
        test = pd.DataFrame()
        test = result.iloc[(pos[i-1]+18):pos[i]]
        result_cleared = pd.concat([result_cleared, test], axis=0)

    return result_cleared


def extract_rollnumbers(result):

    rno = [x for x in result[0]]
    roll_nos = [x for x in rno if x == x]  # removes NaN
    roll_nos = [x for x in roll_nos if len(x) < 4]  # removes longer string
    roll_nos = [x for x in roll_nos if x != 'No.']  # removes 'No.'
    roll_nos = [int(x) for x in roll_nos]  # convert string to number

    return roll_nos


def remove_empty_rows(result_cleared):

    index_names1 = result_cleared[result_cleared[1].isnull()].index
    result_cleared.drop(index_names1, inplace=True)

    index_names2 = result_cleared[result_cleared[4].isnull()].index
    result_cleared.drop(index_names2, inplace=True)

    return result_cleared


def reassign_rollnos(roll_numbers, result_cleared):
    result_cleared[0] = roll_numbers
    return result_cleared


def clear_result_data(result, semester):

    result = remove_rows_columns(result)
    result = correct_rows_columns(result)
    result_cleared = pd.DataFrame()
    result_cleared = cleared_result(result_cleared, result)
    roll_numbers = extract_rollnumbers(result)
    remove_empty_rows(result_cleared)
    reassign_rollnos(roll_numbers, result_cleared)
    result_cleared = ah.add_header(result_cleared, semester)
    return (result_cleared)
