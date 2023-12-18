import game
import mysql.connector

mydb = mysql.connector.connect(
    host = '127.0.0.1',
    port = 3306,
    user = 'root',
    password = 'mysql',
    database = 'ltm'
)
mycursor = mydb.cursor()


def dang_nhap():
    # lay thong tin username, password
    username, password = [], []
    username_query = "select username from account"
    sql_query = f"{username_query}"
    mycursor.execute(sql_query)
    myresult1 = mycursor.fetchall()
    for i in myresult1:
        username.append(i[0])

    password_query = "select password from account"
    sql_query = f"{password_query}"
    mycursor.execute(sql_query)
    myresult2 = mycursor.fetchall()
    for i in myresult2:
        password.append(i[0])
    
    dangnhap = '0'
    next = '~'
    while True:
        print("Mời bạn đăng nhập")
        tdn = input("Tên đăng nhập: ")
        mk = input("Mật khẩu: ")
        if tdn in username:
            index = username.index(tdn)
            if mk == password[index]:
                dangnhap = '1'
                next = '~'
                print("Bạn đã đăng nhập thành công")
                break
        
        if dangnhap == '0':
            print("""Nếu chưa có tài khoản, mời bạn ấn phím 1 để đăng ký. Nếu muốn tiếp tục đăng nhập nhấn phím bất kỳ (khác 1):""")
            next = input()  # dang ky
            if next == '1':
                break
    return next

def dang_ky():
    print("=== ĐĂNG KÝ ===")
    dk_tdn = input("Tên đăng nhập: ")
    dk_mk = input("Mật khẩu: ")
    dk_mk = input("Nhập lại mật khẩu: ")
    dk_confirm = input("Nhấn phím 'C' để xác nhận đăng ký!")

    if dk_confirm == 'C' or dk_confirm == 'c':
        query_insert = "insert into account(username, password) values('{}', '{}')".format(dk_tdn, dk_mk)
        mycursor.execute(query_insert)
        mydb.commit()


dangnhap = dang_nhap()
if dangnhap == '1':
    dang_ky()
    dangnhap = dang_nhap()
if dangnhap == '~':
    game.main()


