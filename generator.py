from flask import Flask, render_template
from werkzeug import cached_property
import markdown
import os
import yaml

POSTS_FILE_EXTENSIION = '.md'
app = Flask(__name__)



class Post(object):
	def __init__(self, path):
		self.path = path
		self._initialize_metadata()

	@cached_property
	def html(self):
		with open(self.path, 'r') as fin:
			content = fin.read().split('\n\n',1)[1].strip()
		return markdown.markdown(content)

	def _initialize_metadata(self):
		content = ''
		with open(self.path, 'r') as fin:
			for line in fin:
				if not line.strip():
					break
				content += line
		self.__dict__.update(yaml.load(content))

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
	return '<b> Hello </b>'

@app.route("/blog/post/<path:path>")
def post(path):
	path = os.path.join('posts', path + POSTS_FILE_EXTENSIION)
	post = Post(path)
	return render_template("post.html", post_content=post)


if __name__ == '__main__':
	app.run(port=8080,debug=True)