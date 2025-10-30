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
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import inspect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:/python3.13.9/WebAppcwk1budget_tracker/BudgetTrackerdatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db = SQLAlchemy()
import models
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/incomes')
def incomes():
    from models import Income
    with app.app_context():
        data = Income.query.all()
    return render_template('incomes.html', incomes=data)

@app.route('/expenditures')
def expenditures():
    from models import Expenditure
    with app.app_context():
        data = Expenditure.query.all()
    return render_template('expenditures.html', expenditures=data)

@app.route('/goal')
def goal():
    from models import Goal
    with app.app_context():
        data = Goal.query.all()
    return render_template('goal.html', goals=data)


def init_database():
    """检测并创建数据库"""
    db_path = os.path.abspath(os.path.join(os.getcwd(), 'BudgetTrackerdatabase.db'))
    print(f"[DEBUG] 当前工作目录: {os.getcwd()}")
    print(f"[DEBUG] 预期数据库路径: {db_path}")

    with app.app_context():
        db.create_all()
        print("[INFO] 调用 db.create_all() 完成")

        # ✅ 在上下文中调用 inspect 就不会报错
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"[INFO] 当前数据库中的表：{tables}")

        if os.path.exists(db_path):
            print(f"[SUCCESS] ✅ 数据库文件已生成: {db_path}")
        else:
            print(f"[WARNING] ⚠️ 数据库文件未出现在磁盘！")


if __name__ == '__main__':
    # 如果你想重新创建请先删除 BudgetTrackerdatabase.db，然后运行
    init_database()
    app.run(debug=True)
