
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from collections import OrderedDict
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'data.sqlite') 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Reconcile(db.Model):
    __tablename__ = 'bill_order_reconcile'
    order_id=db.Column(db.Integer,primary_key=True)
    sales_order = db.Column(db.String(100), unique=True)
    deal_time = db.Column(db.DateTime)
    settle_time = db.Column(db.DateTime)
    order_sum =db.Column(db.DECIMAL(20, 2))
    bill_sum =db.Column(db.DECIMAL(20, 2))
    variance = db.Column(db.DECIMAL(20, 2))
    reason=db.Column(db.Text)
    modified_sum=db.Column(db.DECIMAL(20, 2))  # 默认modified_sum=bill_sum
    check=db.Column(db.Boolean)
    submit=db.Column(db.Boolean)
    confirm=db.Column(db.Boolean)

def to_dict(books):
    return OrderedDict(
        order_id=books.order_id,
        sales_order=books.sales_order,
        deal_time=datetime.strftime(books.deal_time,'%Y-%m-%d %H:%M:%S'),
        settle_time=datetime.strftime(books.settle_time,'%Y-%m-%d %H:%M:%S'),
        order_sum=books.order_sum,
        bill_sum=books.bill_sum,
        variance=books.variance,
        reason=books.reason,
        modified_sum=books.modified_sum,
        check=books.check
    )


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Reconcile=Reconcile)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# 回传所有未对账的订单
@app.route('/books', methods=['GET'])
def unchecked_books():
    response_object = {'status': 'success'}
    try:
        # 只返回已提交未对账的订单
        books=Reconcile.query.filter(Reconcile.check != True).all()
        response_object['books'] = list(map(to_dict, books))
    except Exception as e:
        return jsonify({"error": str(e)}), 405
    return jsonify(response_object)

# 回传所有已对账的订单
@app.route('/books/checked', methods=['GET'])
def checked_books():
    response_object = {'status': 'success'}
    try:
        # 只返回已提交未对账的订单
        books=Reconcile.query.filter(Reconcile.check == True).all()
        response_object['books'] = list(map(to_dict, books))
    except Exception as e:
        return jsonify({"error": str(e)}), 405
    return jsonify(response_object)

# 处理“全部提交”按钮
@app.route('/books/submit', methods=['POST'])
def import_data():
    # 从请求中获取JSON数据
    data = request.get_json()  # 请求体需要是JSON格式
    # 检查数据是否存在
    if not data or not isinstance(data, list):
        return jsonify({"error": "Invalid data format"}), 400
    for item_data in data:
        item = Reconcile.query.get(item_data['order_id'])
        if item:
            item.reason = item_data.get('reason', item.reason)
            item.modified_sum = item_data.get('modified_sum', item.modified_sum)
            item.check = item_data.get('check', item.check)
    db.session.commit()
    return jsonify({"message": "全部【已对账】提交成功！【未对账】已暂存！"}), 200

# 处理每行的“提交”和“暂存”按钮
@app.route('/books/<id>', methods=['POST'])
def handle_patch(id):
    data = request.get_json()  # 请求体需要是JSON格式
    if not data:
        return jsonify({"error": "Invalid data format"}), 400
    order = Reconcile.query.filter(Reconcile.order_id==id).first()
    if order:
        so=order.sales_order
        order.reason = data.get('reason')
        order.modified_sum = data.get('modified_sum')
        order.check = data.get('check')
        db.session.commit()
        if order.check:
            return jsonify({"message": "【订单"+str(so)+"】【已对账】提交成功！"}), 200
        else:
            return jsonify({"message": "【订单"+str(so)+"】暂存成功！"}), 200
    else:
        return jsonify({"error": "订单"+str(so)+"未找到"}), 404



if __name__ == '__main__':
    app.run()