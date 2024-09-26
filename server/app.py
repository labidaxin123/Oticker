
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from collections import OrderedDict

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

# def check(oid):
#     rc = Reconcile.query.get(oid)
#     if rc:
#         rc.check = not rc.check
#         db.session.commit()
#     else:
#         print(f"No record found with ID {oid}")


@app.route('/books', methods=['GET'])
def all_books():
    response_object = {'status': 'success'}
    # 只返回已提交未对账的订单
    books=Reconcile.query.filter(Reconcile.check != True).all()
    response_object['books'] = list(map(to_dict, books))
    return jsonify(response_object)

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
    return jsonify({"message": "Items updated successfully"}), 200

# @app.route('/books/<int:oid>', methods=['PATCH'])
# def handle_patch(oid):
#     check(oid)
#     return "Patch successful", 200


if __name__ == '__main__':
    app.run()