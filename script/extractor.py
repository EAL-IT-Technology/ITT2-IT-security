import frontmatter
import io
from os.path import basename, splitext
import glob

# Where are the files to modify
path = "../weekly_plans/*.md"

# Loop through all files
for fname in glob.glob(path):
    with io.open(fname, 'r') as f:
 	print "file:", fname
	# Parse file's front matter
        post = frontmatter.load(f)
	for p in post.keys():
		print u'- {}: {}'.format(p, post[p])
	#print post
#        if post.get('author') == None:
#            post['author'] = "alex"
#            # Save the modified file
#            newfile = io.open(fname, 'w', encoding='utf8')
#            frontmatter.dump(post, newfile)
#            newfile.close()

