#!/bin/env python
import csv
import glob
import os

tex_header_file = "tex_header.tex"
tex_footer_file = "tex_footer.tex"

week_no_start = 4
week_no_end = 24


def output_tex_from_file(filename):
    with open(filename, 'r') as f:
        for line in f:
            print(line)


def gen_dict(first_week, last_week):
    res = {}
    for ww in range(first_week, last_week + 1):
        res[str(ww)] = {'Week': ww}

    return res


def read_from_csv(filename):
    with open(filename, 'r') as f:
        res = []
        reader = csv.DictReader(f)
        for entry in reader:
            res.append((entry['Week'], entry['Content']))

        return res


def merge_content(table, new_entries, col_name):
    for week, content in new_entries:
        table[str(week)][col_name] = content

    return table


def get_headers(table):
    return table[table.keys()[0]].keys()


def get_tex_begin_tabular(headers, col_width = '5cm'):
    string = '\\begin {tabular} {c'

    for h in headers:
        if h == 'Week':
            continue
        string += ' | p{{{}}}'.format(col_width)

    string += '}'
    return string


def get_tex_headers(headers):
    string = '\\textbf {Week}'

    for h in headers:
        if h == 'Week':
            continue
        string += ' & \\textbf {{{}}}'.format(h)

    string += ' \\\\'
    return string


def get_tex_row(line):
    string = str(line['Week'])

    for key in line.keys():
        if key == 'Week':
            continue
        string += ' & {}'.format(line[key])

    string += ' \\\\'
    return string


def output_text_table_from_dict(table):
    print('\\begin {table}[h!]')

    headers = get_headers(table)
    print'  ', get_tex_begin_tabular(headers, '7cm')
    print'    ', get_tex_headers(headers)

    print'    ', '\\hline'

    for week in table:
        print'    ', get_tex_row(table[week])

    print('  \\end {tabular}')
    print('\\end {table}')


def output_tex_table_from_csv(filelist):
    table_content = gen_dict(week_no_start, week_no_end)
    for filename in filelist:
        entries = read_from_csv(filename)
        col_name = '.'.join(os.path.basename(filename).split('.')[:-1])
        table_content = merge_content(table_content, entries, col_name)

    output_text_table_from_dict(table_content)


if __name__ == "__main__":
    output_tex_from_file(tex_header_file)

    filelist = glob.glob('./*.csv')
    output_tex_table_from_csv(filelist)

    output_tex_from_file(tex_footer_file)
