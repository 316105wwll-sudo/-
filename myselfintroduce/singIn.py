from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import jwt
import datetime
from passlib.context import CryptContext
import os

# 初始化Flask应用
app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 配置数据库（SQLite，开发环境使用）
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # 数据库文件将存放在backend目录
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'  # 用于JWT加密（生产环境需更换为随机密钥）

# 初始化数据库
db = SQLAlchemy(app)

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 用户模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password_hash = pwd_context.hash(password)

    def check_password(self, password):
        return pwd_context.verify(password, self.password_hash)

# 创建数据库表（首次运行时执行）
with app.app_context():
    db.create_all()

# 生成JWT令牌
def generate_token(user_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),  # 过期时间1天
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

# 注册接口
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'code': 0, 'msg': '用户名和密码不能为空'}), 400

    # 检查用户名是否已存在
    if User.query.filter_by(username=username).first():
        return jsonify({'code': 0, 'msg': '用户名已存在'}), 400

    # 创建新用户
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'code': 1, 'msg': '注册成功'})

# 登录接口
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'code': 0, 'msg': '用户名或密码错误'}), 401

    # 生成令牌
    token = generate_token(user.id)
    return jsonify({
        'code': 1,
        'msg': '登录成功',
        'data': {
            'token': token,
            'username': username
        }
    })

# 验证登录状态接口（示例）
@app.route('/api/verify', methods=['GET'])
def verify():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'code': 0, 'msg': '未提供令牌'}), 401

    try:
        # 解析令牌
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = payload['sub']
        user = User.query.get(user_id)
        return jsonify({
            'code': 1,
            'data': {'username': user.username}
        })
    except jwt.ExpiredSignatureError:
        return jsonify({'code': 0, 'msg': '令牌已过期'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'code': 0, 'msg': '无效的令牌'}), 401

if __name__ == '__main__':
    # 启动服务器，默认端口5000，允许外部访问
    app.run(host='0.0.0.0', port=5000, debug=True)