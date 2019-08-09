from flask import Flask, render_template, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

class Postit(db.Model):
	"""The model of a post-it note"""
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(50))
	#Can not be null/empty
	content = db.Column(db.String(250), nullable=False)
	def __repr__(self):
		return f'<Post-it {self.id} created>'

	def __str__(self):
		return __repr__()

@app.route('/', methods=['POST', 'GET'])
def home():
	if request.method == 'POST':
		post_content = request.form['content']
		post_title = request.form['title']
		new_post = Postit(content=post_content, title=post_title)

		try: 
			db.session.add(new_post)
			db.session.commit()
			flash('New post added')
			return redirect('/')
		except:
			return redirect('/')
	else:
		posts = Postit.query.order_by(Postit.id).all()
		return render_template('home.html', posts=posts) 

@app.route('/delete/<int:id>')
def delete(id):
	post_to_delete = Postit.query.get_or_404(id)

	try:
		db.session.delete(post_to_delete)
		db.session.commit()
		return redirect('/')
	except:
		return "'Twas a problem deleting"

if __name__ == '__main__':
	app.run(debug=false)