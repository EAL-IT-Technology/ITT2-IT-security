#!/bin/env python

tex_header_file = "tex_header.tex"
tex_footer_file = "tex_footer.tex"


def output_tex(filename):
    with open(filename, 'r') as f:
        for line in f:
            print(line)


if __name__ == "__main__":
    output_tex(tex_header_file)

    output_tex(tex_footer_file)
