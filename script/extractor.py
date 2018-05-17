import frontmatter
import io
# from os.path import basename, splitext
import glob
import csv

source_dir = "../weekly_plans"


def read_md(filename):
    with io.open(fname, 'r') as f:
        return frontmatter.load(f)


# https://gist.github.com/kgaughan/2491663
from itertools import chain


def parse_range(rng):
    parts = rng.split('-')
    if 1 > len(parts) > 2:
        raise ValueError("Bad range: '%s'" % (rng,))
    parts = [int(i) for i in parts]
    start = parts[0]
    end = start if len(parts) == 1 else parts[1]
    if start > end:
        end, start = start, end
    return range(start, end + 1)


def parse_range_list(rngs):
    return sorted(set(chain(*[parse_range(rng) for rng in rngs.split(',')])))


def write_multi_row(writer, weeks, content):
    try:
        w = int(weeks)
        writer.writerow([w, content])
    except ValueError:
        ws = parse_range(weeks)
        writer.writerow([ws[0], content])
        for w in ws[1:]:
            writer.writerow([w, content+" (cont.)"])


# Loop through all files
fieldnames = ['Week', 'Content']
with open('names.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(fieldnames)

    for fname in sorted(glob.glob(source_dir + '/*.md')):
        try:
            post = read_md(fname)
            print fname
            write_multi_row(writer, post['Week'], post['Content'])
        except KeyError:
            print "- file {} missing key. (one of '{}')".format(fname, fieldnames)
            pass
        except ValueError:
            print "- Non-numeric week (was: {})".format(post['Week'])
            pass
