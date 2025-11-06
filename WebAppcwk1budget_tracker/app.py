# 一、Flask（后端核心）：
# 1、负责路由管理（定义 /sc_data_list /lc_data_list 等访问入口）
# 2、数据库交互（调用 mysqlDao.py 从数据库取数）
# 3、模板渲染（将数据传递给 HTML 动态生成页面）
#
# 二、HTML + CSS/JS（前端展示）
# 1、HTML：作为页面骨架
# 2、CSS：存放在 static/css，负责美化页面（如卡片布局、手机端适配），提升用户体验；
#
# -------协同逻辑：-------
# app.py 从 mysqlDao.py 获取数据库数据；
# 调用 render_template，将数据传入 templates 下的 HTML 模板；
# HTML 借助 Jinja2 语法渲染动态内容，同时引用 static 文件夹的 CSS/JS 实现样式和交互。
#------------------------
#
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import inspect
import os
from extensions import db  
import models

from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import inspect
from extensions import db
import models

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:/python3.13.9/WebAppcwk1budget_tracker/BudgetTrackerdatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/incomes', methods=['GET', 'POST'])
def incomes():
    from models import Income
    if request.method == 'POST':
        name = request.form['name']
        amount = request.form['amount']
        new_income = Income(name=name, amount=float(amount))
        db.session.add(new_income)
        db.session.commit()
        return redirect(url_for('incomes'))

    data = Income.query.all()
    return render_template('incomes.html', incomes=data)

# Delete Income
@app.route('/delete_income/<int:id>', methods=['POST'])
def delete_income(id):
    from models import Income
    item = Income.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('incomes'))


@app.route('/expenditures', methods=['GET', 'POST'])
def expenditures():
    from models import Expenditure
    if request.method == 'POST':
        name = request.form['name']
        amount = request.form['amount']
        new_expenditure = Expenditure(name=name, amount=float(amount))
        db.session.add(new_expenditure)
        db.session.commit()
        return redirect(url_for('expenditures'))

    data = Expenditure.query.all()
    return render_template('expenditures.html', expenditures=data)


@app.route('/delete_expenditure/<int:id>', methods=['POST'])
def delete_expenditure(id):
    from models import Expenditure
    item = Expenditure.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('expenditures'))


@app.route('/goal', methods=['GET', 'POST'])
def goal():
    from models import Goal
    if request.method == 'POST':
        name = request.form['name']
        value = request.form['value']
        new_goal = Goal(name=name, value=float(value))
        db.session.add(new_goal)
        db.session.commit()
        return redirect(url_for('goal'))

    data = Goal.query.all()
    return render_template('goal.html', goals=data)

#
@app.route('/delete_goal/<int:id>', methods=['POST'])
def delete_goal(id):
    from models import Goal
    item = Goal.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('goal'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        inspector = inspect(db.engine)
        print("[INFO] Tables:", inspector.get_table_names())
    app.run(debug=True)
