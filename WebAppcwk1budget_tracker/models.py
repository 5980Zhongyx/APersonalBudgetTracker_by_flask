# 注意：这里仍然从 app 导入 db，但按上面的 app.py 顺序导入，db 已存在（未绑定）
from app import db

class Income(db.Model):
    __tablename__ = 'income'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)

class Expenditure(db.Model):
    __tablename__ = 'expenditure'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)

class Goal(db.Model):
    __tablename__ = 'goal'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    value = db.Column(db.Float, nullable=False)

print("[DEBUG] models.py 已加载")
