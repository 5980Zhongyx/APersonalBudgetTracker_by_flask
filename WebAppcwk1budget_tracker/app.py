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
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import inspect, func
from extensions import db
import models

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BudgetTrackerdatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key_here'
db.init_app(app)


# ---------------------- HOME PAGE ----------------------
@app.route('/')
def index():
    """Show total income, expenditure, savings, and goal progress"""
    from models import Income, Expenditure, Goal

    total_income = db.session.query(func.sum(Income.amount)).scalar() or 0
    total_expenditure = db.session.query(func.sum(Expenditure.amount)).scalar() or 0
    savings = total_income - total_expenditure

    # Get current goal
    goal = Goal.query.first()  # Assuming single goal as per requirements
    progress_percentage = 0

    if goal and goal.value > 0:
        progress_percentage = min((savings / goal.value) * 100, 100)

    return render_template(
        'index.html',
        total_income=total_income,
        total_expenditure=total_expenditure,
        savings=savings,
        goal=goal,
        progress_percentage=progress_percentage
    )


# ---------------------- INCOMES ----------------------
@app.route('/incomes', methods=['GET', 'POST'])
def incomes():
    from models import Income

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        amount = request.form.get('amount', '').strip()

        # Server-side validation
        errors = []
        if not name or len(name) < 2:
            errors.append("Income name must be at least 2 characters long")
        try:
            amount = float(amount)
            if amount <= 0:
                errors.append("Amount must be positive")
        except (ValueError, TypeError):
            errors.append("Amount must be a valid number")

        if errors:
            for error in errors:
                flash(error, 'error')
        else:
            new_income = Income(name=name, amount=amount)
            db.session.add(new_income)
            db.session.commit()
            flash('Income added successfully!', 'success')
            return redirect(url_for('incomes'))

    incomes = Income.query.all()
    return render_template('incomes.html', incomes=incomes)


@app.route('/edit_income/<int:id>', methods=['GET', 'POST'])
def edit_income(id):
    from models import Income
    income = Income.query.get_or_404(id)

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        amount = request.form.get('amount', '').strip()

        # Validation
        errors = []
        if not name or len(name) < 2:
            errors.append("Income name must be at least 2 characters long")
        try:
            amount = float(amount)
            if amount <= 0:
                errors.append("Amount must be positive")
        except (ValueError, TypeError):
            errors.append("Amount must be a valid number")

        if errors:
            for error in errors:
                flash(error, 'error')
        else:
            income.name = name
            income.amount = amount
            db.session.commit()
            flash('Income updated successfully!', 'success')
            return redirect(url_for('incomes'))

    return render_template('edit_income.html', income=income)


@app.route('/delete_income/<int:id>', methods=['POST'])
def delete_income(id):
    from models import Income
    income = Income.query.get_or_404(id)
    db.session.delete(income)
    db.session.commit()
    flash('Income deleted successfully!', 'success')
    return redirect(url_for('incomes'))


# ---------------------- EXPENDITURES ----------------------
@app.route('/expenditures', methods=['GET', 'POST'])
def expenditures():
    from models import Expenditure

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        amount = request.form.get('amount', '').strip()

        # Server-side validation
        errors = []
        if not name or len(name) < 2:
            errors.append("Expenditure name must be at least 2 characters long")
        try:
            amount = float(amount)
            if amount <= 0:
                errors.append("Amount must be positive")
        except (ValueError, TypeError):
            errors.append("Amount must be a valid number")

        if errors:
            for error in errors:
                flash(error, 'error')
        else:
            new_expenditure = Expenditure(name=name, amount=amount)
            db.session.add(new_expenditure)
            db.session.commit()
            flash('Expenditure added successfully!', 'success')
            return redirect(url_for('expenditures'))

    expenditures = Expenditure.query.all()
    return render_template('expenditures.html', expenditures=expenditures)


@app.route('/edit_expenditure/<int:id>', methods=['GET', 'POST'])
def edit_expenditure(id):
    from models import Expenditure
    expenditure = Expenditure.query.get_or_404(id)

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        amount = request.form.get('amount', '').strip()

        # Validation
        errors = []
        if not name or len(name) < 2:
            errors.append("Expenditure name must be at least 2 characters long")
        try:
            amount = float(amount)
            if amount <= 0:
                errors.append("Amount must be positive")
        except (ValueError, TypeError):
            errors.append("Amount must be a valid number")

        if errors:
            for error in errors:
                flash(error, 'error')
        else:
            expenditure.name = name
            expenditure.amount = amount
            db.session.commit()
            flash('Expenditure updated successfully!', 'success')
            return redirect(url_for('expenditures'))

    return render_template('edit_expenditure.html', expenditure=expenditure)


@app.route('/delete_expenditure/<int:id>', methods=['POST'])
def delete_expenditure(id):
    from models import Expenditure
    expenditure = Expenditure.query.get_or_404(id)
    db.session.delete(expenditure)
    db.session.commit()
    flash('Expenditure deleted successfully!', 'success')
    return redirect(url_for('expenditures'))


# ---------------------- GOALS ----------------------
@app.route('/goal', methods=['GET', 'POST'])
def goal():
    from models import Goal, Income, Expenditure

    current_goal = Goal.query.first()

    if request.method == 'POST':
        # If there's already a goal, update it instead of creating new
        if current_goal:
            name = request.form.get('name', '').strip()
            value = request.form.get('value', '').strip()

            # Validation
            errors = []
            try:
                value = float(value)
                if value <= 0:
                    errors.append("Goal amount must be positive")
            except (ValueError, TypeError):
                errors.append("Goal amount must be a valid number")

            if errors:
                for error in errors:
                    flash(error, 'error')
            else:
                current_goal.name = name if name else "Savings Goal"
                current_goal.value = value
                db.session.commit()
                flash('Goal updated successfully!', 'success')
        else:
            # Create new goal
            name = request.form.get('name', '').strip()
            value = request.form.get('value', '').strip()

            # Validation
            errors = []
            try:
                value = float(value)
                if value <= 0:
                    errors.append("Goal amount must be positive")
            except (ValueError, TypeError):
                errors.append("Goal amount must be a valid number")

            if errors:
                for error in errors:
                    flash(error, 'error')
            else:
                goal_name = name if name else "Savings Goal"
                new_goal = Goal(name=goal_name, value=value)
                db.session.add(new_goal)
                db.session.commit()
                flash('Goal created successfully!', 'success')

        return redirect(url_for('goal'))

    # Calculate progress for template
    total_income = db.session.query(func.sum(Income.amount)).scalar() or 0
    total_expenditure = db.session.query(func.sum(Expenditure.amount)).scalar() or 0
    savings = total_income - total_expenditure
    progress_percentage = 0

    if current_goal and current_goal.value > 0:
        progress_percentage = min((savings / current_goal.value) * 100, 100)

    return render_template('goal.html',
                           goal=current_goal,
                           savings=savings,
                           progress_percentage=progress_percentage)


@app.route('/edit_goal/<int:id>', methods=['GET', 'POST'])
def edit_goal(id):
    from models import Goal
    goal = Goal.query.get_or_404(id)

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        value = request.form.get('value', '').strip()

        # Validation
        errors = []
        try:
            value = float(value)
            if value <= 0:
                errors.append("Goal amount must be positive")
        except (ValueError, TypeError):
            errors.append("Goal amount must be a valid number")

        if errors:
            for error in errors:
                flash(error, 'error')
        else:
            goal.name = name if name else "Savings Goal"
            goal.value = value
            db.session.commit()
            flash('Goal updated successfully!', 'success')
            return redirect(url_for('goal'))

    return render_template('edit_goal.html', goal=goal)


@app.route('/delete_goal/<int:id>', methods=['POST'])
def delete_goal(id):
    from models import Goal
    goal = Goal.query.get_or_404(id)
    db.session.delete(goal)
    db.session.commit()
    flash('Goal deleted successfully!', 'success')
    return redirect(url_for('goal'))


# ---------------------- MAIN ENTRY ----------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        inspector = inspect(db.engine)
        print("[INFO] Tables:", inspector.get_table_names())
    app.run(debug=True)
