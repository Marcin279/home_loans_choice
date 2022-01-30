import pandas as pd
from typing import List
import numpy as np

crits_type = {'Marża [%]': 0, 'Prowizja [%]': 0, 'RRSO [%]': 0, 'Koszt miesięczny [PLN]': 0, 'Wkład własny [%]': 0,
              'Opinie[pkt. Max. 5]': 1}

columns_names_order = {'Marża [%]': 1, 'Prowizja [%]': 2, 'RRSO [%]': 3, 'Koszt miesięczny [PLN]': 4,
                       'Wkład własny [%]': 5, 'Opinie[pkt. Max. 5]': 6}


def find_max(df):
    columns = list(df.columns)
    max_vals = []
    for column in columns:
        col_vals = df[column]
        max_vals.append(col_vals.max())
    return max_vals


def find_min(df):
    columns = list(df.columns)
    min_vals = []
    for column in columns:
        col_vals = df[column]
        min_vals.append(col_vals.min())
    return min_vals


def find_ideal(mins, maxs, is_max, crits):
    result = []
    for i in range(len(mins)):
        if is_max[crits[i]]:
            result.append(maxs[i])
        else:
            result.append(mins[i])
    return result


def find_inideal(mins, maxs, is_max, crits):
    result = []
    for i in range(len(mins)):
        if is_max[crits[i]]:
            result.append(mins[i])
        else:
            result.append(maxs[i])
    return result


def find_use_funs(point_ideal, point_inideal, is_max, crits, num_of_divs=2):
    divs = []
    result = []
    no_of_crits = len(point_ideal)

    if type(num_of_divs) == int:
        for i in range(no_of_crits):
            divs.append(num_of_divs)
    elif type(num_of_divs) == List and len(num_of_divs) == no_of_crits:
        for i in range(no_of_crits):
            divs.append(num_of_divs[i])
    else:
        return None

    max_value = 1 / no_of_crits
    for i in range(no_of_crits):
        weigths = []
        functions = []
        args = np.sort(np.linspace(point_inideal[i], point_ideal[i], divs[i] + 1))
        no_of_args = len(args)

        if is_max[crits[i]]:
            for j in range(no_of_args):
                weigths = np.linspace(0, max_value, no_of_args)
        else:
            for j in range(no_of_args):
                weigths = np.linspace(max_value, 0, no_of_args)

        for k in range(divs[i]):
            a = (weigths[k + 1] - weigths[k]) / (args[k + 1] - args[k])
            b = weigths[k + 1] - args[k + 1] * a
            functions.append((a, b, args[k], args[k + 1]))

        result.append(functions)

    return result


def make_ranking(df, funs_and_parts, crits):
    no_of_crits = len(funs_and_parts)
    all_u_values = []
    for i in range(no_of_crits):
        u_values = []
        no_of_parts = len(funs_and_parts[i])
        for val in list(df[crits[i]]):
            checked = False
            for j in range(no_of_parts):
                a, b, x1, x2 = funs_and_parts[i][j]
                if x1 <= val <= x2 and not checked:
                    u = a * val + b
                    if u <= 0:
                        u = 0
                    u_values.append(u)
                    checked = True
        all_u_values.append(u_values)

    points = list(df.index)
    ranking = {}

    for i, point in enumerate(points):
        sum = 0
        for j in range(no_of_crits):
            sum += all_u_values[j][i]
        ranking[point] = sum

    return ranking


def run(active_crits, path='dane.xlsx', exel_data_sheet='Arkusz3'):
    crits = []
    no_of_crits = len(active_crits)
    crits_values = []

    while len(crits) < no_of_crits:
        min_order = 10
        for crit in active_crits:
            order = columns_names_order[crit]
            if order < min_order:
                min_order = order
                column = crit

        crits.append(active_crits.pop(active_crits.index(column)))

    crits.append('Punkt')
    df = pd.read_excel(io=path, sheet_name=exel_data_sheet, index_col=0, usecols=crits)
    maxs = find_max(df)
    mins = find_min(df)
    ideal_point = find_ideal(mins, maxs, crits_type, crits)
    inideal_point = find_inideal(mins, maxs, crits_type, crits)
    funs_and_parts = find_use_funs(ideal_point, inideal_point, crits_type, crits)
    ranking = make_ranking(df, funs_and_parts, crits)

    sorted_ranking = {}
    sorted_keys = sorted(ranking, key=ranking.get, reverse=True)
    for w in sorted_keys:
        crits_values = []
        for k in range(no_of_crits):
            crits_values.append(df[crits[k]].loc[w])
            sorted_ranking[w] = crits_values

    return sorted_ranking
