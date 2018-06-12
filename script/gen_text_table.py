#!/bin/env python
import csv
import glob
import os

tex_header_file = "tex_header.tex"
tex_footer_file = "tex_footer.tex"

week_no_start = 4
week_no_end = 26

escape_table = {"-": r"\-", "]": r"\]", "\\": r"\\",
                "^": r"\^", "$": r"\$", "*": r"\*",
                "&": r"\&", "?": r"{?}"}


def output_tex_from_file(filename):
    with open(filename, 'r') as f:
        for line in f:
            print(line)


def gen_dict(weeklist):
    res = {}
    for ww in weeklist:
        res[str(ww)] = {'Week': ww}

    return res


def read_from_csv(filename):
    with open(filename, 'r') as f:
        res = []
        reader = csv.DictReader(f)
        for entry in reader:
            esc_content = entry['Content'].translate(str.maketrans(escape_table))
            res.append((entry['Week'], esc_content))

        return res


def merge_content(table, new_entries, col_name, week_list):
    for ww in week_list:
        table[str(ww)][col_name] = ""

    for week, content in new_entries:
        table[str(week)][col_name] = content

    return table


def get_headers(table):
    return table[list(table.keys())[0]].keys()


def get_tex_begin_longtable(headers, col_width='5cm'):
    string = '\\begin {longtable} {'
    string += ' p{{{}}}'.format('1.5cm')

    for h in headers:
        if h == 'Week':
            continue
        string += ' | p{{{}}}'.format(col_width)

    string += ' }'
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
    #    print('\\begin {longtable}')

    headers = get_headers(table)
    col_width = (29.7 - 2 * 2.0 - 2.0 - 2.0) / (len(headers) - 1)
    print(get_tex_begin_longtable(headers, '{:.1f}cm'.format(col_width)))
    print(' ', get_tex_headers(headers))

    print(' ', '\\hline')
    print(' ', '\\endhead')

    for week in range(week_no_start, week_no_end + 1):
        print(' ', get_tex_row(table[str(week)]))
        print(' ', '\\hline')

    print('\\end {longtable}')


def output_tex_table_from_csv(filelist, week_list):
    table_content = gen_dict(week_list)
    for filename in filelist:
        entries = read_from_csv(filename)
        col_name = '.'.join(os.path.basename(filename).split('.')[:-1])
        table_content = merge_content(table_content, entries, col_name, week_list)

    output_text_table_from_dict(table_content)


if __name__ == "__main__":
    output_tex_from_file(tex_header_file)

    csv_files = glob.glob('data/*.csv')
    output_tex_table_from_csv(csv_files, week_list=range(week_no_start, week_no_end + 1))

    output_tex_from_file(tex_footer_file)
