from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:dlQmsdl00@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(5), nullable=False)
    phone = db.Column(db.String(11), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False)
    company = db.Column(db.String(30), nullable=False)
    memo = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Member {self.name}>"


@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/')
def index():
    search = request.args.get('search', '')
    members = Member.query.filter(
        Member.name.contains(search) | Member.phone.contains(search) | Member.company.contains(search)).all()
    return render_template('index.html', members=members)


@app.route('/new', methods=['GET', 'POST'])
def new_member():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        company = request.form['company']
        memo = request.form['memo']
        member = Member(name=name, phone=phone, email=email, company=company, memo=memo)
        db.session.add(member)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('new.html')


@app.route('/detail/<int:member_id>')
def detail(member_id):
    member = Member.query.get(member_id)
    return render_template('detail.html', member=member)


@app.route('/edit/<int:member_id>', methods=['GET', 'POST'])
def edit_member(member_id):
    member = Member.query.get(member_id)
    if request.method == 'POST':
        member.name = request.form['name']
        member.phone = request.form['phone']
        member.email = request.form['email']
        member.company = request.form['company']
        member.memo = request.form['memo']
        db.session.commit()
        return redirect(url_for('detail', member_id=member.id))
    return render_template('edit.html', member=member)


@app.route('/delete/<int:member_id>', methods=['POST'])
def delete_member(member_id):
    member = Member.query.get(member_id)
    db.session.delete(member)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
