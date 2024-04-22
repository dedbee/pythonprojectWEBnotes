from flask import Flask
from models import Category, db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
db.init_app(app)
app2 = Flask(__name__)
app2.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app2)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print('Создана база данных users')
    with app.app_context():
        db.create_all()
        work_category = Category(name='Работа')
        hobby_category = Category(name='Хобби')
        investment_category = Category(name='Инвестиции')
        db.session.add(work_category)
        db.session.add(hobby_category)
        db.session.add(investment_category)
        db.session.commit()
        print('Созданы категории Работа, Хобби и Инвестиции')
    print('Создана база данных notes')
