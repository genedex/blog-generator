from flask import Flask, render_template, url_for, abort
from werkzeug import cached_property
import markdown
import os
import yaml
import time
POSTS_FILE_EXTENSIION = '.md'
#app = Flask(__name__)

app = Flask(__name__)
class Blog(object):
	def __init__(self, app, root_dir='',file_ext=POSTS_FILE_EXTENSIION):
		self.root_dir = root_dir
		self.file_ext = file_ext
		self._app = app
		self._cache = {}
		self._initialize_cache()


	@property
	def posts(self):
		return self._cache.values()

	def _initialize_cache(self):
		for (root, dirpaths, filepaths) in os.walk(self.root_dir):

			for filepath in filepaths:
				filename, ext = os.path.splitext(filepath)
				if ext == self.file_ext:
					# path = os.path.join(root, filepath).replace(self.root_dir, '')
					# print path
					# post = Post(path, root_dir=self.root_dir)
					# self._cache[post.urlpath] = post
					path = os.path.join(root, filepath)
					#print path
					post = Post(path)
					#print post
					self._cache[post.urlpath] = post
					#print self._cache

	def get_post_or_404(self,path):
		# print "path:",path
		# print "cache:", self._cache
		try:
			return self._cache[path]
		except KeyError:
			abort(404)



class Post(object):
	def __init__(self, path,root_dir=''):
		self.urlpath = os.path.splitext(path.strip('/'))[0]
		self.filepath = os.path.join(root_dir, path.strip('/'))
		self.published = False
		self._initialize_metadata()

	@cached_property
	def html(self):
		with open(self.filepath, 'r') as fin:
			content = fin.read().split('\n\n',1)[1].strip()
		return markdown.markdown(content)

	@property
	def url(self):
		return url_for('post',path=self.urlpath)

	def _initialize_metadata(self):
		content = ''
		#print self.filepath
		with open(self.filepath, 'r') as fin:
			for line in fin:
				#print line
				if not line.strip():
					break
				content += line
		#print content
		self.__dict__.update(yaml.load(content))


blog = Blog(app, root_dir='posts')

# option 3
@app.template_filter('date')
def format_date(val, format="%B %d, %Y"):
	return val.strftime(format)

# option 1
# @app.context_processor
# def inject_format_date():
# 	return {'format_date':format_date}

# option 2
#app.jinja_env.filters['date'] = format_date

@app.route("/")
def index():
	#posts = [Post('hello.md', root_dir="posts")]
	return render_template('index.html', posts=blog.posts)

@app.route("/blog/<path:path>")
def post(path):
	# print path
	# path = os.path.join('posts', path + POSTS_FILE_EXTENSIION)
	# post = Post(path)
	# ----------------------------------------------------------
	#post = Post(path + POSTS_FILE_EXTENSIION, root_dir="posts")
	post = blog.get_post_or_404(path)
	return render_template("post.html", post_content=post)


if __name__ == '__main__':
	app.run(port=8080,debug=True)