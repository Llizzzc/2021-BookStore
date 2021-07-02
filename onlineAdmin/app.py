from flask import Flask, request
from flask_cors import CORS
from model import User, Shop, DBSession, Book, BSconfig, Address, Order, POconfig, Admin
import json
import decimal

app = Flask(__name__)
CORS(app, supports_credentials=True)  # 解决跨域问题


# 解决decimal不能转json的问题
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)


@app.route('/')
def hello():
    return 'hello world'


# 管理员登录逻辑
@app.route('/admin', methods=['POST', 'GET'])
def admin():
    session = DBSession()
    adminInfo = request.json
    admin = session.query(Admin).filter(Admin.name == adminInfo['name']).first()
    if adminInfo['password'] != admin.password:
        session.close()
        return 'error'
    else:
        session.close()
        return admin.to_json()


# 注册逻辑
@app.route('/register', methods=['POST', 'GET'])
def register():
    session = DBSession()
    register_user = request.json  # 获取post数据
    find_user = session.query(User).filter(User.username == register_user['username']).first()
    # 如果有记录代表该用户名存在
    if find_user is not None:
        session.close()
        return 'exist'
    # 否则添加进数据库
    else:
        new_user = User(username=register_user['username'], password=register_user['password'])
        session.add(new_user)
        session.commit()
        session.close()
        return 'ok'


# 登录逻辑
@app.route('/login', methods=['POST', 'GET'])
def login():
    session = DBSession()
    login_user = request.json  # 获得post数据
    # 判断是否存在该用户
    find_user = session.query(User).filter(User.username == login_user['username']).first()
    if find_user is None:
        session.close()
        return 'none'
    # 比较用户名和密码是否正确
    elif login_user['username'] != find_user.username or login_user['password'] != find_user.password:
        session.close()
        return 'error'
    else:
        session.close()
        return find_user.to_json()


# 改密逻辑
@app.route('/pswChange', methods=['POST', 'GET'])
def pswChange():
    session = DBSession()
    userInfo = request.json
    find_user = session.query(User).filter(User.id == userInfo['id']).first()
    find_user = find_user.to_json()
    if find_user['password'] != userInfo['password']:
        session.close()
        return 'error'
    elif userInfo['newpswword'] == find_user['password']:
        session.close()
        return 'again'
    else:
        res = session.query(User).filter(User.id == userInfo['id']). \
            update({'password': userInfo['newpswword']})
        session.commit()
        session.close()
        return 'ok'


# 改名逻辑
@app.route('/usernameChange', methods=['POST', 'GET'])
def usernameChange():
    session = DBSession()
    userInfo = request.json
    find_name = session.query(User).filter(User.username == userInfo['username']). \
        filter(User.id != userInfo['id']).first()
    find_user = session.query(User).filter(User.id == userInfo['id']).first()
    find_user = find_user.to_json()
    if find_name is not None:
        session.close()
        return 'exist'
    elif find_user['username'] == userInfo['username']:
        session.close()
        return 'again'
    else:
        res = session.query(User).filter(User.id == userInfo['id']). \
            update({'username': userInfo['username']})
        session.commit()
        find_user = session.query(User).filter(User.id == userInfo['id']).first()
        session.close()
        return find_user.to_json()


# 注销逻辑
@app.route('/deleteUser', methods=['POST', 'GET'])
def deleteUser():
    session = DBSession()
    userInfo = request.json
    order = session.query(Order).filter(Order.user_id == userInfo['id']).all()
    for item in order:
        session.delete(item)
        session.commit()
    address = session.query(Address).filter(Address.user_id == userInfo['id']).all()
    for item in address:
        session.delete(item)
        session.commit()
    user = session.query(User).filter(User.id == userInfo['id']).first()
    session.delete(user)
    session.commit()
    session.close()
    return 'ok'


# 附近店铺展示逻辑
@app.route('/showNearby', methods=['POST', 'GET'])
def showNearby():
    session = DBSession()
    shops = session.query(Shop).all()
    li = []
    for item in shops:
        shop = item.to_json()
        shop['imgUrl'] = "http://localhost:5000/" + shop['imgUrl']
        li.append(shop)  # model转为json存放list
    dic = {'key': li}  # list转为dict
    string = json.dumps(dic)  # dict转为json
    session.close()
    return string


# 当前商铺展示逻辑
@app.route('/showShop', methods=['POST', 'GET'])
def showShop():
    session = DBSession()
    _id = request.args.to_dict()  # 获取get数据转为字典
    shop = session.query(Shop).filter(Shop.id == _id['id']).first()  # 查询当前店铺信息
    string = shop.to_json()
    string['imgUrl'] = "http://localhost:5000/" + string['imgUrl']
    session.close()
    return string  # 转为json返回


# 当前商铺书籍展示逻辑
@app.route('/showBook', methods=['POST', 'GET'])
def showBook():
    session = DBSession()
    gets = request.args.to_dict()
    config_book = session.query(BSconfig). \
        filter(BSconfig.shop_id == gets['id']).all()  # 查询当前书店下所有书信息
    li = []
    for item in config_book:  # 将关系表数据转为字典
        config_info = item.to_json()
        book_info = session.query(Book).filter(Book.id == config_info['book_id']). \
            filter(Book.tab == gets['tab']).first()  # 查找满足条件的书
        if book_info is not None:
            book_info = book_info.to_json()
            book_info['imgUrl'] = "http://localhost:5000/static/img/books/" \
                                  + book_info['tab'] + '/' + book_info['imgUrl']
            book = dict(config_info, **book_info)  # 字典合并
            li.append(book)
    dic = {'key': li}
    string = json.dumps(dic, cls=DecimalEncoder)
    session.close()
    return string


# 订单逻辑
@app.route('/order', methods=['POST', 'GET'])
def order():
    session = DBSession()
    if request.method == 'POST':  # 传入订单逻辑
        gets = request.json  # 获取post数据
        # 加入订单
        new_order = Order(address_id=gets['addressId'], shop_id=gets['shopId'], user_id=gets['userId'],
                          shopName=gets['shopName'], isCanceled=gets['isCanceled'])
        session.add(new_order)
        session.commit()
        new_order_id = new_order.id
        products = gets['products']
        for item in products:
            if gets['isCanceled'] == False:
                book = session.query(BSconfig).filter(BSconfig.shop_id == gets['shopId']). \
                    filter(BSconfig.book_id == item['id']).first()
                book = book.to_json()
                new_stock = book['stock'] - item['num']
                res = session.query(BSconfig).filter(BSconfig.shop_id == gets['shopId']). \
                    filter(BSconfig.book_id == item['id']).update({'stock': new_stock})
                session.commit()
            product = POconfig(order_id=new_order_id, book_id=item['id'], book_sales=item['num'])
            session.add(product)
            session.commit()
        session.close()
        return 'ok'
    elif request.method == 'GET':  # 展示订单逻辑
        gets = request.args.to_dict() # 获取get数据
        orderInfo = session.query(Order).filter(Order.user_id == gets['id']).all() # 查找所有订单
        li1 = []
        for _order in orderInfo:
            _order = _order.to_json()
            del _order['address_id']
            del _order['user_id']
            li2 = []
            books_sales = session.query(POconfig).filter(POconfig.order_id == _order['id']).all()
            for book_sales in books_sales:
                book_sales = book_sales.to_json()
                del book_sales['order_id']
                book_price = session.query(BSconfig).filter(BSconfig.shop_id == _order['shop_id']). \
                    filter(BSconfig.book_id == book_sales['book_id']).first()
                book_price = book_price.to_json()
                del book_price['shop_id']
                del book_price['book_id']
                book = session.query(Book).filter(Book.id == book_sales['book_id']).first()
                book = book.to_json()
                book['imgUrl'] = "http://localhost:5000/static/img/books/" \
                                 + book['tab'] + '/' + book['imgUrl']
                del book['id']
                bookInfo = dict(book_price, **book)
                book = {'bookInfo': bookInfo}
                bookInfo = dict(book_sales, **book)
                del bookInfo['book_id']
                li2.append(bookInfo)
            books = {'books': li2}
            books = dict(_order, **books)
            del books['id']
            del books['shop_id']
            li1.append(books)
        dic = {"orders": li1}
        session.close()
        return json.dumps(dic, cls=DecimalEncoder)


# 地址展示逻辑
@app.route('/showAddress', methods=['POST', 'GET'])
def showAddress():
    session = DBSession()
    _id = request.args.to_dict()
    addresses = session.query(Address).filter(Address.user_id == _id['id']).all()
    li = []
    for item in addresses:
        li.append(item.to_json())
    dic = {'key': li}
    string = json.dumps(dic)
    session.close()
    return string


# 获取一条地址逻辑
@app.route('/oneAddress', methods=['POST', 'GET'])
def oneAddress():
    session = DBSession()
    _id = request.args.to_dict()  # 获取get数据转为字典
    if _id['addressId'] == '0':
        address = session.query(Address).filter(Address.user_id == _id['userId']).first()
        if address is None:
            session.close()
            return 'None'
        else:
            session.close()
            return address.to_json()  # 转为json返回
    else:
        address = session.query(Address).filter(Address.id == _id['addressId']).first()
        if address is not None:
            session.close()
            return address.to_json()  # 转为json返回
        else:
            session.close()
            return 'None'


# 增加地址逻辑
@app.route('/addAddress', methods=['POST', 'GET'])
def addAddress():
    session = DBSession()
    addressInfo = request.json
    new_address = Address(city=addressInfo['city'], name=addressInfo['name'],
                          phone=addressInfo['phone'], houseNumber=addressInfo['houseNumber'],
                          user_id=addressInfo['userId'], department=addressInfo['department'])
    session.add(new_address)
    session.commit()
    session.close()
    return 'ok'


# 当前地址展示逻辑
@app.route('/currentAddress', methods=['POST', 'GET'])
def currentAddress():
    session = DBSession()
    _id = request.args.to_dict()  # 获取get数据转为字典
    address = session.query(Address).filter(Address.id == _id['id']).first()  # 查询当前地址信息
    session.close()
    return address.to_json()  # 转为json返回


# 修改地址逻辑
@app.route('/updateAddress', methods=['POST', 'GET'])
def updateAddress():
    session = DBSession()
    addressInfo = request.json
    for item in addressInfo:
        if item == 'id':
            continue
        if addressInfo[item] != '':
            res = session.query(Address).filter(Address.id == addressInfo['id']). \
                update({item: addressInfo[item]})
            session.commit()
            new_address = session.query(Address).filter(Address.id == addressInfo['id']).first()
            new_address = new_address.to_json()
            if new_address[item] != addressInfo[item]:
                session.rollback()
    session.close()
    return 'ok'


# 删除地址逻辑
@app.route('/deleteAddress', methods=['POST', 'GET'])
def deleteAddress():
    session = DBSession()
    addressInfo = request.json
    address = session.query(Address).filter(Address.id == addressInfo['id']).first()
    order = session.query(Order).filter(Order.address_id == addressInfo['id']).all()
    for item in order:
        session.delete(item)
        session.commit()
    session.delete(address)
    session.commit()
    session.close()
    return 'ok'


# 修改店铺信息逻辑
@app.route('/updateShop', methods=['POST', 'GET'])
def updateShop():
    session = DBSession()
    shopInfo = request.json
    shop = session.query(Shop).filter(Shop.title == shopInfo['title']).first()
    if shop is not None:
        session.close()
        return 'exist'
    else:
        for item in shopInfo:
            if item == 'id':
                continue
            if shopInfo[item] != '':
                if item == 'imgUrl':
                    shopInfo[item] = "static" + '/' + "img" + '/' + "shops" + '/' + shopInfo[item]
                res = session.query(Shop).filter(Shop.id == shopInfo['id']). \
                    update({item: shopInfo[item]})
                session.commit()
                new_Info = session.query(Shop).filter(Shop.id == shopInfo['id']).first()
                new_Info = new_Info.to_json()
                if new_Info[item] != shopInfo[item]:
                    session.rollback()
    session.close()
    return 'ok'


# 新开店铺逻辑
@app.route('/addShop', methods=['POST', 'GET'])
def addShop():
    session = DBSession()
    shopInfo = request.json
    shop = session.query(Shop).filter(Shop.title == shopInfo['title']).first()
    if shop is not None:
        session.close()
        return 'exist'
    else:
        shopInfo['imgUrl'] = "static" + '/' + "img" + '/' + "shops" + '/' + shopInfo['imgUrl']
        new_shop = Shop(title=shopInfo['title'], sales=shopInfo['sales'], expressLimit=shopInfo['expressLimit'],
                        expressPrice=shopInfo['expressPrice'], slogan=shopInfo['slogan'], imgUrl=shopInfo['imgUrl'])
        session.add(new_shop)
        session.commit()
        session.close()
        return 'ok'


# 关闭店铺逻辑
@app.route('/deleteShop', methods=['POST', 'GET'])
def deleteShop():
    session = DBSession()
    shopInfo = request.json
    shop = session.query(Shop).filter(Shop.id == shopInfo['id']).first()
    session.delete(shop)
    session.commit()
    session.close()
    return 'ok'


# 增加店铺书籍逻辑
@app.route('/addShopBook', methods=['POST', 'GET'])
def addShopBook():
    session = DBSession()
    bookInfo = request.json
    book = session.query(Book).filter(Book.name == bookInfo['name']).first()
    book = book.to_json()
    print(book['id'])
    bookId = session.query(BSconfig).filter(BSconfig.book_id == book['id'])\
        .filter(BSconfig.shop_id == bookInfo['shopId']).first()
    if bookId is not None:
        session.close()
        return 'exist'
    else:
        new_book = BSconfig(shop_id=bookInfo['shopId'], book_id=book['id'],
                                 stock=bookInfo['stock'], sales=bookInfo['sales'],
                                 price=bookInfo['price'], oldPrice=bookInfo['oldPrice'])
        session.add(new_book)
        session.commit()
        session.close()
        return 'ok'


# 获得当前店铺待操作书籍逻辑
@app.route('/theShopBook', methods=['POST', 'GET'])
def theShopBook():
    session = DBSession()
    bookInfo = request.args.to_dict()
    book1 = session.query(Book).filter(Book.id == bookInfo['bookId']).first()
    book1 = book1.to_json()
    book2 = session.query(BSconfig).filter(BSconfig.book_id == bookInfo['bookId']). \
        filter(BSconfig.shop_id == bookInfo['shopId']).first()
    book2 = book2.to_json()
    book = dict(book1, **book2)
    book = json.dumps(book, cls=DecimalEncoder)
    session.close()
    return book


# 编辑店铺书籍逻辑
@app.route('/updateShopBook', methods=['POST', 'GET'])
def updateShopBook():
    session = DBSession()
    bookInfo = request.json
    for item in bookInfo:
        if item == 'shopId' or item == 'bookId':
            continue
        if bookInfo[item] != '':
            res = session.query(BSconfig).filter(BSconfig.shop_id == bookInfo['shopId']). \
                filter(BSconfig.book_id == bookInfo['bookId']).update({item: bookInfo[item]})
            session.commit()
            new_book = session.query(BSconfig).filter(BSconfig.book_id == bookInfo['bookId']). \
                filter(BSconfig.shop_id == bookInfo['shopId']).first()
            new_book = new_book.to_json()
            if new_book[item] != bookInfo[item]:
                session.rollback()
    session.close()
    return 'ok'


# 删除店铺书籍逻辑
@app.route('/deleteShopBook', methods=['POST', 'GET'])
def deleteShopBook():
    session = DBSession()
    bookInfo = request.json
    book = session.query(BSconfig).filter(BSconfig.book_id == bookInfo['bookId']). \
        filter(BSconfig.shop_id == bookInfo['shopId']).first()
    session.delete(book)
    session.commit()
    session.close()
    return 'ok'


# 展示所有书籍逻辑
@app.route('/showAllBook', methods=['POST', 'GET'])
def showAllBook():
    session = DBSession()
    gets = request.args.to_dict()
    books = session.query(Book).filter(Book.tab == gets['tab']).all()
    li = []
    for item in books:
        item = item.to_json()
        item['imgUrl'] = "http://localhost:5000/static/img/books/" \
                              + item['tab'] + '/' + item['imgUrl']
        li.append(item)
    dic = {'key': li}
    session.close()
    return dic


# 增加书籍逻辑
@app.route('/addBook', methods=['POST', 'GET'])
def addBook():
    session = DBSession()
    bookInfo = request.json
    book = session.query(Book).filter(Book.name == bookInfo['name']).first()
    if book is not None:
        session.close()
        return 'exist'
    else:
        new_book = Book(tab=bookInfo['tab'], name=bookInfo['name'],
                        imgUrl=bookInfo['imgUrl'])
        session.add(new_book)
        session.commit()
        session.close()
        return 'ok'


# 获得当前书籍逻辑
@app.route('/theBook', methods=['POST', 'GET'])
def theBook():
    session = DBSession()
    bookInfo = request.args.to_dict()
    book = session.query(Book).filter(Book.id == bookInfo['bookId']).first()
    book = book.to_json()
    session.close()
    return book


# 修改书籍逻辑
@app.route('/updateBook', methods=['POST', 'GET'])
def updateBook():
    session = DBSession()
    bookInfo = request.json
    book = session.query(Book).filter(Book.name == bookInfo['name']).first()
    if book is not None:
        session.close()
        return 'exist'
    else:
        for item in bookInfo:
            if item == 'bookId':
                continue
            if bookInfo[item] != '':
                res = session.query(Book).filter(Book.id == bookInfo['bookId']). \
                    update({item: bookInfo[item]})
                session.commit()
                new_book = session.query(Book).filter(Book.id == bookInfo['bookId']).first()
                new_book = new_book.to_json()
                if new_book[item] != bookInfo[item]:
                    session.rollback()
        session.close()
        return 'ok'


# 删除书籍逻辑
@app.route('/deleteBook', methods=['POST', 'GET'])
def deleteBook():
    session = DBSession()
    bookInfo = request.json
    book = session.query(Book).filter(Book.id == bookInfo['bookId']).first()
    session.delete(book)
    session.commit()
    session.close()
    return 'ok'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
