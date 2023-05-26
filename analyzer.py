import pandas as pd
import statistics as stats
import math


def count_students(percentages):
    student_ranges = {
        '>60': 0,
        '(50, 60]': 0,
        '(40, 50]': 0,
        '(12, 40]': 0,
        'Fail/KT': 0
    }

    for percentage in percentages:
        if percentage >= 60:
            student_ranges['>60'] += 1
        elif 50 < percentage <= 60:
            student_ranges['(50, 60]'] += 1
        elif 40 < percentage <= 50:
            student_ranges['(40, 50]'] += 1
        elif 12 < percentage <= 40:
            student_ranges['(12, 40]'] += 1
        elif percentage <= 12:
            student_ranges['Fail/KT'] += 1

    return student_ranges


def get_avg_cgpa(cleared_result):
    CGPA = cleared_result['cgpa'].fillna(0).values.tolist()
    CGPA = [float(i) for i in CGPA]
    avg_cgpa = stats.mean(CGPA)
    return avg_cgpa, CGPA


def get_avg_percentage(CGPA):
    percentages = []
    for i in range(len(CGPA)):
        if CGPA[i] >= 7:
            percentages.append(round(7.4*CGPA[i] + 12, 4))
        elif CGPA[i] < 7:
            percentages.append(round(7.1*CGPA[i] + 12, 4))
        elif CGPA[i] == 0.0:
            percentages.append(0)
    # print("PERCENTAGE: ", percentages)
    avg_perc = stats.mean(percentages)
    return avg_perc, percentages


def find_toppers(cleared_result):

    copy_df = cleared_result.copy()
    copy_df['cgpa'] = pd.to_numeric(copy_df['cgpa'])
    # find the top 3 students by CGPA
    top3 = copy_df.nlargest(3, 'cgpa')

    # select only the 'rollno' and 'cgpa' columns
    top3 = top3.loc[:, ['roll_no', 'cgpa']]

    # convert the result to a dictionary
    toppers = top3.to_dict('records')

    return toppers


def find_sub_max(cleared_result, semester):
    subjects = pd.read_excel('subjects.xlsx')
    subs = subjects[semester].tolist()
    # print(subs)
    heads = cleared_result.columns
    columns = [i for i in range(len(heads)) if isinstance(
        heads[i], int) and heads[i] % 10 == 1]
    # print(columns)
    result = {}
    for col in columns:
        name = subs[col]
        # print(name)
        try:
            result[name] = cleared_result[heads[col]].dropna().apply(
                pd.to_numeric, errors='coerce').max()
        except ValueError:
            print(f"Column {col} cannot be converted to float.")
    return result


def find_kts(cleared_result):
    kts = 0
    for i in cleared_result['cgpa']:
        if i != i:
            kts += 1
    return kts


def find_sub_mark_ranges(cleared_result, semester):
    sub_ranges = {}
    subjects = pd.read_excel('subjects.xlsx')
    subs = subjects[semester].tolist()
    subs = [x for x in subs if x == x]
    # print(subs)
    heads = cleared_result.columns
    # print(heads)
    columns = [i for i in range(len(heads)) if isinstance(
        heads[i], int) and heads[i] % 10 == 1]
    # print(columns)

    for col in columns:
        name = subs[col]
        # print(name)
        # print(cleared_result[heads[col]])
        sub_marks = cleared_result[heads[col]]
        count = 0
        for x in sub_marks:
            # print(x, type(x))
            if x.isdigit() and int(x) >= 60:
                count += 1

        sub_ranges[name] = count
    return sub_ranges
