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
        res[str(ww)] = {'week': ww}

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


def output_text_table_from_dict(table):
    print('\\begin {table}[h!]')
    print('  \\begin {tabular} {l | c | r}')
    print('    \\textbf{Value 1} & \\textbf{Value 2} & \\textbf{Value 3}\\\\ ')
    print('    \\hline')

    print('1 & 1110.1 & a \\\\ ')
    print('1 & 1110.1 & a \\\\ ')
    print('1 & 1110.1 & a \\\\ ')

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
