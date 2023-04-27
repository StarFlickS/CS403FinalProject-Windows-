'''
โปรแกรมจัดการคลังสินค้าสำหรับ Windows
'''
import sqlite3
from tkinter import *
from tkinter import messagebox
from tkmacosx import Button
from datetime import date


def ConnectToDatabase():
    global conn, cursor
    conn = sqlite3.connect("database/database.db")
    cursor = conn.cursor()

def CreateWindowsFrame():
    root = Tk()
    root.title("โปรแกรมจัดการคลังสินค้า ร้านโภทิลาษ")
    x = root.winfo_screenwidth() / 2 - w / 2
    y = root.winfo_screenheight() / 2 - h / 2
    root.geometry("%dx%d+%d+%d" %(w, h, x, y))
    root.rowconfigure((0,1,2), weight=1)  # type: ignore
    root.columnconfigure((0,1,2), weight=1) # type: ignore
    root["bg"] = "white"
    
    return root


def LoginPage():
    global userNameEnt, pwdEnt
    loginFrame = Frame(root, bg="gray")
    loginFrame.rowconfigure((0,1,2), weight=1) # type: ignore
    loginFrame.columnconfigure(0, weight=1)
    loginFrame.grid(row=1, column=1, sticky="news")

    top = Frame(loginFrame, bg="white")
    top.rowconfigure(0, weight=1)
    top.columnconfigure(0, weight=1)
    top.grid(row=0 ,column=0, sticky="news")

    header = Label(top, text="เข้าสู่ระบบ", font="verdana 35 bold", bg="white", fg="black")
    header.grid(row=0, column=0)

    middle = Frame(loginFrame, bg="white")
    middle.rowconfigure((0,1,2,3), weight=1) # type: ignore
    middle.columnconfigure(0, weight=1)
    middle.grid(row=1, column=0, sticky="news")

    Label(middle, text="ชื่อผู้ใช้งาน", fg="black", bg="white", font="verdana 25").grid(row=0, column=0)
    userNameEnt = Entry(middle, textvariable=usernameSpy, width=30)
    userNameEnt.grid(row=1, column=0)

    Label(middle, text="รหัสผ่าน", fg="black", bg="white", font="verdana 25").grid(row=2, column=0)
    pwdEnt = Entry(middle, textvariable=pwdSpy, width=30, show="●")
    pwdEnt.grid(row=3, column=0)

    bot = Frame(loginFrame, bg="white")
    bot.rowconfigure(0, weight=1)
    bot.columnconfigure(0, weight=1)
    bot.grid(row=2, column=0, sticky="news")

    loginBtn = Button(bot, text="เข้าสู่ระบบ", fg="white", bg="gray", command=loginclicked)
    loginBtn.grid(row=0, column=0)


def loginclicked():
    if usernameSpy.get() == "":
        messagebox.showwarning("Admin:", "กรุณากรอกชื่อผู้ใช้งานของท่าน")
        userNameEnt.focus_force()
    else:
        if pwdSpy.get() == "":
                messagebox.showwarning("Admin:", "กรุณากรอกรหัสผ่านของท่าน")
                pwdEnt.focus_force()
        else:
                sql = "SELECT * FROM LoginTable WHERE username = ? AND pwd = ?"
                cursor.execute(sql, [usernameSpy.get(), pwdSpy.get()])
                result = cursor.fetchone()
                if result:
                    messagebox.showinfo("Admin:", "เข้าสู่ระบบสำเร็จ")
                    global permission, name
                    name = result[3]
                    permission = result[4]
                    MainPage()
                else:
                    messagebox.showerror("Admin:", "ชื่อผู้ใช้งานหรือรหัสผ่านไม่ถูกต้อง กรุณาลองใหม่อีกครั้ง")
                    pwdSpy.set("")
                    usernameSpy.set("")
                    userNameEnt.focus_force()


def MainPage():
    global infoFrame, btnlist, warehouseBtn, supplierManagementBtn, productSearchBtn, intelInvestigateBtn, saveIntelBtn, printReportBtn, purchaseManagementBtn, sellManagementBtn, accountManagementBtn
    mainpageFrame = Frame(root, bg="black")
    mainpageFrame.rowconfigure(0, weight=1)
    mainpageFrame.columnconfigure(0, weight=2)
    mainpageFrame.columnconfigure(1, weight=20)
    mainpageFrame.grid(row=0,rowspan=3, column=0, columnspan=3, sticky="news")

    menuFrame = Frame(mainpageFrame, bg="gray")
    menuFrame.columnconfigure((0,1), weight=1) # type: ignore
    menuFrame.rowconfigure((0,1,2,3,4,5,6,7,8,9,10), weight=1) # type: ignore
    menuFrame.grid(row=0, column=0, sticky="news")

    infoFrame = Frame(mainpageFrame, bg="white")
    infoFrame.rowconfigure(0, weight=1)
    infoFrame.columnconfigure(0, weight=1)
    infoFrame.grid(row=0, column=1, sticky="news")

    nameFrame = Frame(menuFrame, bg="gray")
    nameFrame.rowconfigure(0, weight=1)
    nameFrame.columnconfigure(0, weight=1)

    Label(nameFrame, text="ชื่อ: " + name, bg="gray", fg="black", font="verdana 15").grid(row=0, column=0)

    if permission == 0:
        nameFrame.grid(row=9, columnspan=2, sticky="news")
        Label(nameFrame, text="สถานะ: เจ้าของร้าน", bg="gray", fg="black", font="verdana 15").grid(row=1, column=0)
        # คลังสินค้า
        warehouseBtn = Button(menuFrame, text="คลังสินค้า", bg="gray", fg="white", command=warehouseClicked)
        warehouseBtn.grid(row=0, column=0, columnspan=2, sticky="news")

        # จัดการผู้ค้าส่ง
        supplierManagementBtn = Button(menuFrame, text="แก้ไข/บันทึกข้อมูลผู้ค้าส่ง", bg="gray", fg="white", command=supplierManagementClicked)
        supplierManagementBtn.grid(row=1, columnspan=2, sticky="news")

        # จัดการข้อมูลการสั่งซื้อ
        purchaseManagementBtn = Button(menuFrame, text="เพิ่ม/แก้ไขข้อมูลการสั่งซื้อ", bg="gray", fg="white", command=purchaseManagementClicked)
        purchaseManagementBtn.grid(row=2, columnspan=2, sticky="news")
        
        # ขายสินค้า
        sellManagementBtn = Button(menuFrame, text="บันทึกการขายสินค้า", bg="gray", fg="white", command=sellManagementClicked)
        sellManagementBtn.grid(row=3, columnspan=2, sticky="news")

        # ค้นหาสินค้า
        productSearchBtn = Button(menuFrame, text="ค้นหาสินค้า", fg="white", bg="gray", command=productsearchClicked)
        productSearchBtn.grid(row=4, column=0, columnspan=2, sticky="news")
        # ตรวจสอบข้อมูล
        intelInvestigateBtn = Button(menuFrame, text="ตรวจสอบข้อมูลการสั่งซื้อ", fg="white", bg="gray", command=intelinvestigateClicked)
        intelInvestigateBtn.grid(row=5, column=0, columnspan=2, sticky="news")
        # บันทึกข้อมูลจัดส่ง
        saveIntelBtn = Button(menuFrame, text="บันทึกข้อมูลการจัดส่ง", fg="white", bg="gray", command=saveintelClicked)
        saveIntelBtn.grid(row=6, column=0, columnspan=2, sticky="news")

        # จัดพิมพ์รายงานเเสดงผลการดำเนินงาน
        printReportBtn = Button(menuFrame, text="จัดพิมพ์รายงาน", fg="white", bg="gray", command=printreportClicked)
        printReportBtn.grid(row=7, column=0, columnspan=2, sticky="news")
        
        # จัดการบัญชี
        accountManagementBtn = Button(menuFrame, text="จัดการบัญชี", fg="white", bg="gray", command=accountManagementClicked)
        accountManagementBtn.grid(row=8, column=0, columnspan=2, sticky="news")

        # Logout Button
        Button(menuFrame, text="Log out", bg="white", fg="black", command=mainpageFrame.destroy).grid(row=10, column=0)
        # Exit Button
        Button(menuFrame, text="Exit", bg="red", fg="black", command=exit).grid(row=10, column=1)

        btnlist = [warehouseBtn, supplierManagementBtn, productSearchBtn, intelInvestigateBtn, saveIntelBtn, printReportBtn, purchaseManagementBtn, sellManagementBtn, accountManagementBtn]
    else:
        menuFrame.rowconfigure((0,1,2,3,4,5), weight=1) # type: ignore
        nameFrame.grid(row=4, columnspan=2, sticky="news")
        Label(nameFrame, text="สถานะ: ลูกจ้าง", bg="gray", fg="black", font="verdana 15").grid(row=1, column=0)
        warehouseBtn = Button(menuFrame, text="คลังสินค้า", bg="gray", fg="white", command=warehouseClicked)
        warehouseBtn.grid(row=0, column=0, columnspan=2, sticky="news")
        
        # ขายสินค้า
        sellManagementBtn = Button(menuFrame, text="บันทึกการขายสินค้า", bg="gray", fg="white", command=sellManagementClicked)
        sellManagementBtn.grid(row=1, columnspan=2, sticky="news")

        # ค้นหาสินค้า
        productSearchBtn = Button(menuFrame, text="ค้นหาสินค้า", fg="white", bg="gray", command=productsearchClicked)
        productSearchBtn.grid(row=2, column=0, columnspan=2, sticky="news")

        # บันทึกข้อมูลจัดส่ง
        saveIntelBtn = Button(menuFrame, text="บันทึกข้อมูลการจัดส่ง", fg="white", bg="gray", command=saveintelClicked)
        saveIntelBtn.grid(row=3, column=0, columnspan=2, sticky="news")

        # Logout Button
        Button(menuFrame, text="Log out", bg="white", fg="black", command=mainpageFrame.destroy).grid(row=5, column=0)
        # Exit Button
        Button(menuFrame, text="Exit", bg="red", fg="black", command=exit).grid(row=5, column=1)
        btnlist = [warehouseBtn, sellManagementBtn, productSearchBtn, saveIntelBtn]


def clearInfoFrame():
    for widget in infoFrame.winfo_children():
        widget.destroy()


def resetBtnColor():
    for i in range(len(btnlist)):
        btnlist[i]["fg"] = "white"


def warehouseClicked():
    global warehouseTree
    resetBtnColor()
    clearInfoFrame()
    warehouseBtn["fg"] = "blue"
    warehouseFrame = Frame(infoFrame, bg="white")
    warehouseFrame.rowconfigure(0, weight=1) # type: ignore
    warehouseFrame.rowconfigure(1, weight=5)
    warehouseFrame.columnconfigure(0, weight=1)
    warehouseFrame.grid(row=0, column=0, sticky="news")

    top = Frame(warehouseFrame, bg="white")
    top.rowconfigure(0, weight=1)
    top.columnconfigure(0, weight=1)
    top.grid(row=0, column=0, sticky="news")

    middle = Frame(warehouseFrame, bg="white")
    middle.rowconfigure(0, weight=1) #type: ignore

    middle.columnconfigure(0, weight=1)
    middle.grid(row=1, column=0, sticky="news")

    #header
    Label(top, text="คลังสินค้า", fg="black", bg="white", font="verdana 35 bold").grid(row=0, column=0, sticky='s')

    warehouseTree = ttk.Treeview(middle)
    warehouseTree.column("#0", width=0, stretch=NO)
    warehouseTree["columns"] = ("รหัสสินค้า","ชื่อสินค้า", "ราคาต้นทุนต่อหน่วย", "ราคาขายต่อหน่วย", "ปริมาณคงเหลือ", "วันที่บันทึกล่าสุด")

    warehouseTree.column("รหัสสินค้า", width=100, anchor=CENTER)
    warehouseTree.column("ชื่อสินค้า", width=100, anchor=CENTER)
    warehouseTree.column("ราคาต้นทุนต่อหน่วย", width=120, anchor=E)
    warehouseTree.column("ราคาขายต่อหน่วย", width=120, anchor=E)
    warehouseTree.column("ปริมาณคงเหลือ", width=120, anchor=E)
    warehouseTree.column("วันที่บันทึกล่าสุด", width=120, anchor=E)

    warehouseTree.heading("รหัสสินค้า", text="รหัสสินค้า")
    warehouseTree.heading("ชื่อสินค้า", text="ชื่อสินค้า")
    warehouseTree.heading("ราคาต้นทุนต่อหน่วย", text="ราคาต้นทุนต่อหน่วย")
    warehouseTree.heading("ราคาขายต่อหน่วย", text="ราคาขายต่อหน่วย")
    warehouseTree.heading("ปริมาณคงเหลือ", text="ปริมาณคงเหลือ")
    warehouseTree.heading("วันที่บันทึกล่าสุด", text="วันที่บันทึกล่าสุด")


    warehouseTree.grid(row=0, column=0)
    if permission == 0:
        # Add Button
        Button(middle, text="เพิ่มสินค้า", fg="black", bg="green", command=addProductClicked).grid(row=0, column=0, sticky='ne', padx=60, pady=170)

        # Modify Button
        Button(middle, text="แก้ไขสินค้า", fg="black", bg="yellow", command=modifyProductClicked).grid(row=0, column=0, sticky='se', padx=160, pady=170)

        #Delete Button
        Button(middle, text="ลบสินค้า", fg="black", bg="red", command=deleteProductClicked).grid(row=0, column=0, sticky='se', padx=60, pady=170)
    fetchWarehouseTree()
    

def fetchWarehouseTree():
    warehouseTree.delete(*warehouseTree.get_children())
    sql = "SELECT * FROM WareHouseTable"
    cursor.execute(sql)
    res = cursor.fetchall()
    if res:
        for i in range(len(res)):
            warehouseTree.insert("",END, values=(res[i][0],res[i][1], res[i][2], res[i][3], res[i][4], res[i][5]))


def addProductClicked():
    if permission == 1:
        return messagebox.showwarning("Admin:", "คุณไม่มีสิทธิ์เข้าถึง")
    def AddProduct():
        if prodnameSpy.get() == "":
            messagebox.showerror("Admin:", "กรุณาใส่ชื่อสินค้า")
            prodnameEnt.focus_force()
        elif prodnameSpy.get().isnumeric() == True:
            messagebox.showerror("Admin:", "ชื่อสินค้าไม่สามารถเป็นตัวเลขได้")
            prodnameEnt.focus_force()
        elif prodCostEnt.get() == "":
            messagebox.showerror("Admin:", "กรุณาใส่ราคาต้นทุน")
            prodCostEnt.focus_force()
        elif prodCostEnt.get().replace('.', '',1).isnumeric() == False:
            messagebox.showerror("Admin:", "ราคาต้นทุนต้องเป็นจำนวนเต็มบวกเท่านั้น")
            prodCostEnt.focus_force()
        elif prodPriceEnt.get() == "":
            messagebox.showerror("Admin:", "กรุณาใส่ราคาขาย")
            prodPriceEnt.focus_force()
        elif prodPriceEnt.get().replace('.', '',1).isnumeric() == False:
            messagebox.showerror("Admin:", "ราคาขายต้องเป็นจำนวนเต็มบวกเท่านั้น")
            prodPriceEnt.focus_force()
        elif prodQuantityEnt.get() == "":
            messagebox.showerror("Admin:", "กรุณาใส่ปริมาณในคลัง")
            prodQuantityEnt.focus_force()
        elif prodQuantityEnt.get().isnumeric() == False:
            messagebox.showerror("Admin:", "ปริมาณในคลังต้องเป็นตัวเลขจำนวนเต็มบวกเท่านั้นเท่านั้น")
            prodQuantityEnt.focus_force()
        else:
            isValid = True
            sql = "SELECT productName FROM WareHouseTable"
            cursor.execute(sql)
            res = cursor.fetchall()
            for i in range(len(res)):
                if res[i][0] == prodnameSpy.get():
                    messagebox.showerror("Admin:","สินค้าประเภทนี้มีอยู่ในคลังอยู่แล้ว")
                    isValid = False
                    break
            
            if isValid:
                today = date.today()
                d = today.strftime("%d/%m/%y")
                sql = "INSERT INTO WareHouseTable (productName, cost, price, quantity, date) VALUES (?,?,?,?,?)"
                cursor.execute(sql, [prodnameSpy.get(), prodCostEnt.get(), prodPriceEnt.get(), prodQuantityEnt.get(), d])
                conn.commit()
                messagebox.showinfo("Admin:", "สินค้าใหม่ได้ถูกเพิ่มเข้าคลังแล้ว")
                addProductWindow.destroy()
                fetchWarehouseTree()
            else:
                prodnameEnt.focus_force()

    prodnameSpy = StringVar()

    w = 500
    h = 500
    addProductWindow = Toplevel(root)
    addProductWindow.title("เพิ่มสินค้าใหม่")
    addProductWindow.rowconfigure(0, weight=1)
    addProductWindow.columnconfigure(0, weight=1)
    x = root.winfo_screenwidth() / 2 - w / 2
    y = root.winfo_screenheight() / 2 - h / 2
    addProductWindow.geometry("%dx%d+%d+%d" %(w, h, x, y))

    addProductFrame = Frame(addProductWindow, bg="white")
    addProductFrame.rowconfigure((0,1,2,3,4), weight=1) #type: ignore
    addProductFrame.columnconfigure((0,1), weight=1)  # type: ignore
    addProductFrame.grid(row=0, column=0, sticky="news")

    Label(addProductFrame, text="ชื่อสินค้า:", fg="black", bg="white", font="verdana 25").grid(row=0, column=0, sticky='e')
    prodnameEnt = Entry(addProductFrame, textvariable=prodnameSpy, width=20)
    prodnameEnt.grid(row=0, column=1, sticky='w')

    Label(addProductFrame, text="ราคาต้นทุน:", fg="black", bg="white", font="verdana 25").grid(row=1, column=0, sticky='e')
    prodCostEnt = Entry(addProductFrame, width=20)
    prodCostEnt.grid(row=1, column=1, sticky='w')

    Label(addProductFrame, text="ราคาขาย:", fg="black", bg="white", font="verdana 25").grid(row=2, column=0, sticky='e')
    prodPriceEnt = Entry(addProductFrame, width=20)
    prodPriceEnt.grid(row=2, column=1, sticky='w')

    Label(addProductFrame, text="ปริมาณในคลัง:", fg="black", bg="white", font="verdana 25").grid(row=3, column=0, sticky='e')
    prodQuantityEnt = Entry(addProductFrame, width=20)
    prodQuantityEnt.grid(row=3, column=1, sticky='w')

    Button(addProductFrame, text="เพิ่มสินค้า", fg="black", bg="green", font="verdana 25 bold", command=AddProduct).grid(row=4, columnspan=2)


def deleteProductClicked():
    if permission == 1:
        return messagebox.showwarning("Admin:", "คุณไม่มีสิทธิ์เข้าถึง")
    if warehouseTree.focus() == "":
        messagebox.showerror("Admin:", "กรุณาเลือกสินค้าที่ต้องการจะลบ")
    else:
        msg = messagebox.askquestion("Delete", "ต้องการลบสินค้านี้หรือไม่", icon="warning")
        if msg == "yes":
            selectedProd = warehouseTree.item(warehouseTree.focus(), "values")
            selectedProd_id = selectedProd[0]
            sql = '''DELETE FROM WareHouseTable
                        WHERE productID = ?'''
            cursor.execute(sql, [selectedProd_id])
            conn.commit()
            messagebox.showinfo("Admin:", "สินค้าถูกลบออกจากคลังเรียบร้อยแล้ว")
            fetchWarehouseTree()


def modifyProductClicked():
    if permission == 1:
        return messagebox.showwarning("Admin:", "คุณไม่มีสิทธิ์เข้าถึง")
    def ModifyProduct():
        if prodnameSpy.get() == "":
            messagebox.showerror("Admin:", "กรุณาใส่ชื่อสินค้า")
            prodnameEnt.focus_force()
        elif prodnameSpy.get().isnumeric() == True:
            messagebox.showerror("Admin:", "ชื่อสินค้าไม่สามารถเป็นตัวเลขได้")
            prodnameEnt.focus_force()
        elif prodCostEnt.get() == "":
            messagebox.showerror("Admin:", "กรุณาใส่ราคาต้นทุน")
            prodCostEnt.focus_force()
        elif prodCostEnt.get().replace('.', '',1).isnumeric() == False:
            messagebox.showerror("Admin:", "ราคาต้นทุนต้องเป็นตัวเลขเท่านั้น")
            prodCostEnt.focus_force()
        elif prodPriceEnt.get() == "":
            messagebox.showerror("Admin:", "กรุณาใส่ราคาขาย")
            prodPriceEnt.focus_force()
        elif prodPriceEnt.get().replace('.', '',1).isnumeric() == False:
            messagebox.showerror("Admin:", "ราคาขายต้องเป็นตัวเลขเท่านั้น")
            prodPriceEnt.focus_force()
        elif prodQuantityEnt.get() == "":
            messagebox.showerror("Admin:", "กรุณาใส่ปริมาณในคลัง")
            prodQuantityEnt.focus_force()
        elif prodQuantityEnt.get().isnumeric() == False:
            messagebox.showerror("Admin:", "ปริมาณในคลังต้องเป็นตัวเลขจำนวนเต็มเท่านั้นเท่านั้น")
            prodQuantityEnt.focus_force()
        else:
            isValid = True
            sql = "SELECT productName, productID FROM WareHouseTable"
            cursor.execute(sql)
            res = cursor.fetchall()
            for i in range(len(res)):
                if res[i][0] == prodnameSpy.get() and res[i][1] != selectedProd_id:
                    messagebox.showerror("Admin:","สินค้าประเภทนี้มีอยู่ในคลังอยู่แล้ว")
                    isValid = False
                    break
            
            if isValid:
                today = date.today()
                d = today.strftime("%d/%m/%y")
                sql = "UPDATE WareHouseTable SET productName = ?, cost = ?, price = ?, quantity = ?, date = ? WHERE productID = ?"
                cursor.execute(sql, [prodnameSpy.get(), prodCostEnt.get(), prodPriceEnt.get(), prodQuantityEnt.get(), d, selectedProd_id])
                conn.commit()
                messagebox.showinfo("Admin:", "แก้ไขสินค้าเรียบร้อยแล้ว")
                modifyWindow.destroy()
                fetchWarehouseTree()
            else:
                prodnameEnt.focus_force()

    if warehouseTree.focus() == "":
        messagebox.showerror("Admin:", "กรุณาเลือกสินค้าที่ต้องการจะแก้ไข")
    else:
        selectedProd = warehouseTree.item(warehouseTree.focus(), "values")
        selectedProd_id = int(selectedProd[0])
        selectedProd_name = selectedProd[1]
        selectedProd_cost = selectedProd[2]
        selectedProd_price = selectedProd[3]
        selectedProd_quantity = selectedProd[4]

        prodnameSpy = StringVar()
        prodnameSpy.set(selectedProd_name)
        w = 500
        h = 500
        modifyWindow = Toplevel(root)
        modifyWindow.title("แก้ไขสินค้า")
        modifyWindow.rowconfigure(0, weight=1)
        modifyWindow.columnconfigure(0, weight=1)
        x = root.winfo_screenwidth() / 2 - w / 2
        y = root.winfo_screenheight() / 2 - h / 2
        modifyWindow.geometry("%dx%d+%d+%d" %(w, h, x, y))

        modifyFrame = Frame(modifyWindow, bg="white")
        modifyFrame.rowconfigure((0,1,2,3,4), weight=1) #type: ignore
        modifyFrame.columnconfigure((0,1), weight=1)  # type: ignore
        modifyFrame.grid(row=0, column=0, sticky="news")

        Label(modifyFrame, text="ชื่อสินค้า:", fg="black", bg="white", font="verdana 25").grid(row=0, column=0, sticky='e')
        prodnameEnt = Entry(modifyFrame, textvariable=prodnameSpy, width=20)
        prodnameEnt.grid(row=0, column=1, sticky='w')

        Label(modifyFrame, text="ราคาต้นทุน:", fg="black", bg="white", font="verdana 25").grid(row=1, column=0, sticky='e')
        prodCostEnt = Entry(modifyFrame, width=20)
        prodCostEnt.insert(END, selectedProd_cost)
        prodCostEnt.grid(row=1, column=1, sticky='w')

        Label(modifyFrame, text="ราคาขาย:", fg="black", bg="white", font="verdana 25").grid(row=2, column=0, sticky='e')
        prodPriceEnt = Entry(modifyFrame, width=20)
        prodPriceEnt.insert(END, selectedProd_price)
        prodPriceEnt.grid(row=2, column=1, sticky='w')

        Label(modifyFrame, text="ปริมาณในคลัง:", fg="black", bg="white", font="verdana 25").grid(row=3, column=0, sticky='e')
        prodQuantityEnt = Entry(modifyFrame, width=20)
        prodQuantityEnt.insert(END, selectedProd_quantity)
        prodQuantityEnt.grid(row=3, column=1, sticky='w')

        Button(modifyFrame, text="แก้ไขสินค้า", fg="black", bg="yellow", font="verdana 25 bold", command=ModifyProduct).grid(row=4, columnspan=2)


def supplierManagementClicked():
    if permission == 1:
        return messagebox.showwarning("Admin:", "คุณไม่มีสิทธิ์เข้าถึง")
    global supplierTree
    resetBtnColor()
    clearInfoFrame()
    supplierManagementBtn["fg"] = "blue"
    supplierManageFrame = Frame(infoFrame, bg="white")
    supplierManageFrame.rowconfigure(0, weight=1) # type: ignore
    supplierManageFrame.rowconfigure(1, weight=5)
    supplierManageFrame.columnconfigure(0, weight=1)
    supplierManageFrame.grid(row=0, column=0, sticky="news")

    top = Frame(supplierManageFrame, bg="white")
    top.rowconfigure(0, weight=1)
    top.columnconfigure(0, weight=1)
    top.grid(row=0, column=0, sticky="news")

    middle = Frame(supplierManageFrame, bg="white")
    middle.rowconfigure(0, weight=1) #type: ignore

    middle.columnconfigure(0, weight=1)
    middle.grid(row=1, column=0, sticky="news")

    #header
    Label(top, text="แก้ไข/บันทึกผู้ค้าส่ง", fg="black", bg="white", font="verdana 35 bold").grid(row=0, column=0, sticky='s')

    supplierTree = ttk.Treeview(middle)
    supplierTree.column("#0", width=0, stretch=NO)
    supplierTree["columns"] = ("รหัสผู้ค้าส่ง","ชื่อร้าน/สวน", "ชื่อผู้ติดต่อ", "เบอร์โทรศัพท์")

    supplierTree.column("รหัสผู้ค้าส่ง", width=100, anchor=CENTER)
    supplierTree.column("ชื่อร้าน/สวน", width=100, anchor=CENTER)
    supplierTree.column("ชื่อผู้ติดต่อ", width=120, anchor=CENTER)
    supplierTree.column("เบอร์โทรศัพท์", width=120, anchor=CENTER)

    supplierTree.heading("รหัสผู้ค้าส่ง", text="รหัสผู้ค้าส่ง")
    supplierTree.heading("ชื่อร้าน/สวน", text="ชื่อร้าน/สวน")
    supplierTree.heading("ชื่อผู้ติดต่อ", text="ชื่อผู้ติดต่อ")
    supplierTree.heading("เบอร์โทรศัพท์", text="เบอร์โทรศัพท์")

    supplierTree.grid(row=0, column=0)

    # Add Button
    Button(middle, text="เพิ่มผู้ค้าส่ง", fg="black", bg="green", command=addSupplierClicked).grid(row=0, column=0, sticky='ne', padx=180, pady=170)

    # Modify Button
    Button(middle, text="แก้ไขผู้ค้าส่ง", fg="black", bg="yellow", command=modifySupperlierClicked).grid(row=0, column=0, sticky='se', padx=280, pady=170)

    #Delete Button
    Button(middle, text="ลบผู้ค้าส่ง", fg="black", bg="red", command=deleteSupplierClicked).grid(row=0, column=0, sticky='se', padx=180, pady=170)
    
    fetchSupplierTree()
    

def fetchSupplierTree():
    supplierTree.delete(*supplierTree.get_children())
    sql = "SELECT * FROM SupplierContactTable"
    cursor.execute(sql)
    res = cursor.fetchall()
    if res:
        for i in range(len(res)):
            supplierTree.insert("",END, values=(res[i][0],res[i][1], res[i][2], res[i][3]))


def addSupplierClicked():
    def AddSupplier():
        if supplierNameEnt.get() == "":
            messagebox.showerror("Admin:", "กรุณาใส่ชื่อร้าน/สวน")
            supplierNameEnt.focus_force()
        elif supplierNameEnt.get().isnumeric() == True:
            messagebox.showerror("Admin:", "ชื่อร้าน/สวนไม่สามารถเป็นตัวเลขได้")
            supplierNameEnt.focus_force()
        elif contactNameEnt.get() == "":
            messagebox.showerror("Admin:", "กรุณาใส่ชื่อผู้ติดต่อ")
            contactNameEnt.focus_force()
        elif contactNameEnt.get().isnumeric() == True:
            messagebox.showerror("Admin:", "ชื่อผู้ติดต่อไม่ถูกต้อง")
            contactNameEnt.focus_force()
        elif phoneEnt.get() == "":
            messagebox.showerror("Admin:", "กรุณาใส่เบอร์โทรศัพท์")
            phoneEnt.focus_force()
        elif phoneEnt.get().replace('-', '').isnumeric() == False or (len(phoneEnt.get().replace('-', '')) != 10 and len(phoneEnt.get().replace('-', '')) != 9):
            messagebox.showerror("Admin:", "เบอร์โทรศัพท์ไม่ถูกต้อง")
            phoneEnt.focus_force()
        elif addressEnt.get("1.0", END) == "":
            messagebox.showerror("Admin:", "กรุณากรอกที่อยู่")
            addressEnt.focus_force()
        else:
            isValid = True
            sql = "SELECT supplierName FROM SupplierContactTable"
            cursor.execute(sql)
            res = cursor.fetchall()
            for i in range(len(res)):
                if res[i][0] == supplierNameEnt.get():
                    messagebox.showerror("Admin:","มีค้าส่งรายนี้ในฐานข้อมูลแล้ว")
                    isValid = False
                    break
            
            if isValid:
                sql = "INSERT INTO SupplierContactTable (supplierName, contactName, phone, address) VALUES (?,?,?,?)"
                cursor.execute(sql, [supplierNameEnt.get(), contactNameEnt.get(), phoneEnt.get().replace('-',''), addressEnt.get("1.0", END)])
                conn.commit()
                messagebox.showinfo("Admin:", "ผู้ค้าส่งใหม่ได้ถูกเพิ่มเข้าสู่ฐานระบบแล้ว")
                addSupplierWindow.destroy()
                fetchSupplierTree()
            else:
                supplierNameEnt.focus_force()
    

    w = 500
    h = 500
    addSupplierWindow = Toplevel(root)
    addSupplierWindow.title("เพิ่มผู้ค้าส่งใหม่")
    addSupplierWindow.rowconfigure(0, weight=1)
    addSupplierWindow.columnconfigure(0, weight=1)
    x = root.winfo_screenwidth() / 2 - w / 2
    y = root.winfo_screenheight() / 2 - h / 2
    addSupplierWindow.geometry("%dx%d+%d+%d" %(w, h, x, y))

    addSupplierFrame = Frame(addSupplierWindow, bg="white")
    addSupplierFrame.rowconfigure((0,1,2,3,4), weight=1) #type: ignore
    addSupplierFrame.columnconfigure((0,1), weight=1)  # type: ignore
    addSupplierFrame.grid(row=0, column=0, sticky="news")

    Label(addSupplierFrame, text="ชื่อร้าน/สวน:", fg="black", bg="white", font="verdana 25").grid(row=0, column=0, sticky='e')
    supplierNameEnt = Entry(addSupplierFrame, width=20)
    supplierNameEnt.grid(row=0, column=1, sticky='w')

    Label(addSupplierFrame, text="ชื่อผู้ติดต่อ:", fg="black", bg="white", font="verdana 25").grid(row=1, column=0, sticky='e')
    contactNameEnt = Entry(addSupplierFrame, width=20)
    contactNameEnt.grid(row=1, column=1, sticky='w')

    Label(addSupplierFrame, text="เบอร์โทรศัพท์ติดต่อ:", fg="black", bg="white", font="verdana 25").grid(row=2, column=0, sticky='e')
    phoneEnt = Entry(addSupplierFrame, width=20)
    phoneEnt.grid(row=2, column=1, sticky='w')

    Label(addSupplierFrame, text="ที่อยู่ติดต่อ", fg="black", bg="white", font="verdana 25").grid(row=3,column=0,sticky='ne')
    addressEnt = Text(addSupplierFrame, width=60, height=5)
    addressEnt.grid(row=3, column=0, columnspan=2, sticky='s')

    Button(addSupplierFrame, text="เพิ่มผู้ค้าส่ง", fg="black", bg="green", font="verdana 25 bold", command=AddSupplier).grid(row=4, columnspan=2)


def modifySupperlierClicked():
    def ModifySupplier():
        if supplierNameEnt.get() == "":
            messagebox.showerror("Admin:", "กรุณาใส่ชื่อร้าน/สวน")
            supplierNameEnt.focus_force()
        elif supplierNameEnt.get().isnumeric() == True:
            messagebox.showerror("Admin:", "ชื่อสินค้าร้าน/สวน ไม่ถูกต้อง")
            supplierNameEnt.focus_force()
        elif contactNameEnt.get() == "":
            messagebox.showerror("Admin:", "กรุณาใส่ชื่อผู้ติดต่อ")
            contactNameEnt.focus_force()
        elif contactNameEnt.get().isnumeric() == True:
            messagebox.showerror("Admin:", "ชื่อผู้ติดต่อไม่ถูกต้อง")
            contactNameEnt.focus_force()
        elif phoneEnt.get() == "":
            messagebox.showerror("Admin:", "กรุณาใส่เบอร์โทรศัพท์ติดต่อ")
            phoneEnt.focus_force()
        elif phoneEnt.get().replace('-', '').isnumeric() == False or (len(phoneEnt.get().replace('-', '')) != 10 and len(phoneEnt.get().replace('-', '')) != 9):
            messagebox.showerror("Admin:", "เบอร์โทรศัพท์ไม่ถูกต้อง")
            phoneEnt.focus_force()
        else:
            isValid = True
            sql = "SELECT supplierName, supplierID FROM SupplierContactTable"
            cursor.execute(sql)
            res = cursor.fetchall()
            for i in range(len(res)):
                if res[i][0] == supplierNameEnt.get() and res[i][1] != selectedSupp_id:
                    messagebox.showerror("Admin:","มีผู้ค้าส่งนี้อยู่ในฐานระบบแล้ว")
                    isValid = False
                    break
            
            if isValid:
                sql = "UPDATE SupplierContactTable SET supplierName = ?, contactName = ?, phone = ? WHERE supplierID = ?"
                cursor.execute(sql, [supplierNameEnt.get(), contactNameEnt.get(), phoneEnt.get().replace('-',''), selectedSupp_id])
                conn.commit()
                messagebox.showinfo("Admin:", "แก้ไขผู้ค้าส่งเรียบร้อยแล้ว")
                modifyWindow.destroy()
                fetchSupplierTree()
            else:
                supplierNameEnt.focus_force()

    if supplierTree.focus() == "":
        messagebox.showerror("Admin:", "กรุณาเลือกผู้ค้าส่งที่ต้องการจะแก้ไข")
    else:
        selectedSupp = supplierTree.item(supplierTree.focus(), "values")
        selectedSupp_id = int(selectedSupp[0])
        selectedSupp_name = selectedSupp[1]
        selectedSupp_contact = selectedSupp[2]
        selectedSupp_phone = selectedSupp[3]

        w = 500
        h = 500
        modifyWindow = Toplevel(root)
        modifyWindow.title("แก้ไขผู้ค้าส่ง")
        modifyWindow.rowconfigure(0, weight=1)
        modifyWindow.columnconfigure(0, weight=1)
        x = root.winfo_screenwidth() / 2 - w / 2
        y = root.winfo_screenheight() / 2 - h / 2
        modifyWindow.geometry("%dx%d+%d+%d" %(w, h, x, y))

        modifyFrame = Frame(modifyWindow, bg="white")
        modifyFrame.rowconfigure((0,1,2,3), weight=1) #type: ignore
        modifyFrame.columnconfigure((0,1), weight=1)  # type: ignore
        modifyFrame.grid(row=0, column=0, sticky="news")

        Label(modifyFrame, text="ชื่อร้าน/สวน:", fg="black", bg="white", font="verdana 25").grid(row=0, column=0, sticky='e')
        supplierNameEnt = Entry(modifyFrame, width=20)
        supplierNameEnt.insert(END, selectedSupp_name)
        supplierNameEnt.grid(row=0, column=1, sticky='w')

        Label(modifyFrame, text="ชื่อผู้ติดต่อ:", fg="black", bg="white", font="verdana 25").grid(row=1, column=0, sticky='e')
        contactNameEnt = Entry(modifyFrame, width=20)
        contactNameEnt.insert(END, selectedSupp_contact)
        contactNameEnt.grid(row=1, column=1, sticky='w')

        Label(modifyFrame, text="เบอร์โทรศัพท์:", fg="black", bg="white", font="verdana 25").grid(row=2, column=0, sticky='e')
        phoneEnt = Entry(modifyFrame, width=20)
        phoneEnt.insert(END, selectedSupp_phone)
        phoneEnt.grid(row=2, column=1, sticky='w')

        Button(modifyFrame, text="แก้ไขผู้ค้าส่ง", fg="black", bg="yellow", font="verdana 25 bold", command=ModifySupplier).grid(row=3, columnspan=2)


def deleteSupplierClicked():
    if supplierTree.focus() == "":
        messagebox.showerror("Admin:", "กรุณาเลือกผู้ค้าส่งที่ต้องการจะลบ")
    else:
        msg = messagebox.askquestion("Delete", "ต้องการจะลบผู้ค้าส่งนี้หรือไม่", icon="warning")
        if msg == "yes":
            selectedSupp = supplierTree.item(supplierTree.focus(), "values")
            selectedSupp_id= selectedSupp[0]
            sql = '''DELETE FROM SupplierContactTable
                        WHERE supplierID = ?'''
            cursor.execute(sql, [selectedSupp_id])
            conn.commit()
            messagebox.showinfo("Admin:", "ผู้ค้าส่งถูกลบออกจากฐานข้อมูลเรียบร้อยแล้ว")
            fetchSupplierTree()


def productsearchClicked():
    global prodSearchFrame, searchBar
    resetBtnColor()
    clearInfoFrame()
    productSearchBtn["fg"] = "blue"
    prodSearchFrame = Frame(infoFrame, bg="white")
    prodSearchFrame.rowconfigure(0, weight=1)
    prodSearchFrame.rowconfigure(1, weight=3)
    prodSearchFrame.columnconfigure(0, weight=3)
    prodSearchFrame.columnconfigure(1, weight=1)
    prodSearchFrame.grid(row=0, column=0, sticky="news")
    # head
    Label(prodSearchFrame, text="ค้นหาสินค้า", fg="black", bg="white", font="verdana 35 bold").grid(row=0, column=0,
                                                                                                    columnspan=2,
                                                                                                    sticky="n")
    searchBar = Entry(prodSearchFrame, width=70)
    searchBar.grid(row=0, column=0)
    searchBtn = Button(prodSearchFrame, text="ค้นหา", command=createProdSearchTree)
    searchBtn.grid(row=0, column=1)


def createProdSearchTree():
    global prodserachedTree

    prodserachedTree = ttk.Treeview(prodSearchFrame)
    prodserachedTree.column("#0", width=0, stretch=NO)
    prodserachedTree["columns"] = ("ชื่อสินค้า", "จำนวน", "ราคา/หน่วย", "วันที่สั่ง")

    prodserachedTree.column("ชื่อสินค้า", width=120, anchor=CENTER)
    prodserachedTree.column("จำนวน", width=120, anchor=CENTER)
    prodserachedTree.column("ราคา/หน่วย", width=120, anchor=CENTER)
    prodserachedTree.column("วันที่สั่ง", width=120, anchor=CENTER)

    prodserachedTree.heading("ชื่อสินค้า", text="ชื่อสินค้า")
    prodserachedTree.heading("จำนวน", text="จำนวน")
    prodserachedTree.heading("ราคา/หน่วย", text="ราคา/หน่วย")
    prodserachedTree.heading("วันที่สั่ง", text="วันที่สั่ง")

    if searchBar.get().replace(" ", "") != "":
        prodserachedTree.grid(row=1, column=0, columnspan=2)
        fetchProdSearchedTree()


def fetchProdSearchedTree():
    prodserachedTree.delete(*prodserachedTree.get_children())
    sql = "SELECT * FROM WareHouseTable"
    cursor.execute(sql)
    res = cursor.fetchall()
    if res:
        if searchBar.get().replace(" ", "") == "":
            pass
        else:
            for i in range(len(res)):
                if searchBar.get() in res[i][1]:
                    prodserachedTree.insert("", END, values=(res[i][1], res[i][4], res[i][3], res[i][5]))


def intelinvestigateClicked():
    if permission == 1:
        return messagebox.showwarning("Admin:", "คุณไม่มีสิทธิ์เข้าถึง")
    global dateSelectSpy,intelInvestigateTree, searchTypeSpy, intelSearchBar, dayIntelSpy, monthIntelSpy, yearIntelSpy
    resetBtnColor()
    clearInfoFrame()
    intelInvestigateBtn["fg"] = "blue"
    intelinvestigateFrame = Frame(infoFrame, bg="white")
    intelinvestigateFrame.rowconfigure((0, 1, 2), weight=1)
    intelinvestigateFrame.columnconfigure(0, weight=2)
    intelinvestigateFrame.columnconfigure((1, 2), weight=1)
    intelinvestigateFrame.grid(row=0, column=0, sticky="news")
    # head
    Label(intelinvestigateFrame, text="ตรวจสอบข้อมูลการสั่งซื้อ", fg="black", bg="white", font="verdana 35 bold").grid(
        row=0, column=0, columnspan=3)
    # middle
    intelSearchBar = Entry(intelinvestigateFrame, width=60)
    intelSearchBar.grid(row=1, column=0,sticky="ne")

    searchType = ["สินค้า", "ผู้ค้าส่ง"]

    searchTypeSpy = StringVar()
    searchTypeSpy.set(searchType[0])

    OptionMenu(intelinvestigateFrame, searchTypeSpy, *searchType).grid(row=1, column=1,sticky="n")  # type: ignore

    intelSearchBtn = Button(intelinvestigateFrame, text="ค้นหา", fg="black", bg="lime", font="verdana 16",
                            command=fetchintelinvestigatesearchtree)
    intelSearchBtn.grid(row=1, column=2, sticky="n")

    dateSelect = ["เวลาใดก็ได้", "เลือกเอง"]

    dateSelectSpy = StringVar()
    dateSelectSpy.set(dateSelect[0])

    days = [x for x in range(1, 32)]
    months = [x for x in range(1, 13)]
    years = [x for x in range(2023, 2033)]

    dayIntelSpy = IntVar()
    dayIntelSpy.set(days[0])

    monthIntelSpy = IntVar()
    monthIntelSpy.set(months[0])

    yearIntelSpy = IntVar()
    yearIntelSpy.set(years[0])

    OptionMenu(intelinvestigateFrame, dateSelectSpy, *dateSelect, command=lambda c:dateselectswitch(c)).grid(row=1, column=1)

    def dateselectswitch(option):
        global day, month, year
        if option == "เลือกเอง" :
            day = OptionMenu(intelinvestigateFrame, dayIntelSpy, *days)
            month = OptionMenu(intelinvestigateFrame, monthIntelSpy, *months)
            year = OptionMenu(intelinvestigateFrame, yearIntelSpy, *years)
            day.grid(row=1, column=0, sticky="w", padx=50)  # type: ignore
            month.grid(row=1, column=0)  # type: ignore
            year.grid(row=1, column=0, sticky="e", padx=50)  # type: ignore
        else:
            day.destroy()
            month.destroy()
            year.destroy()

    # bottom
    intelInvestigateTree = ttk.Treeview(intelinvestigateFrame)
    intelInvestigateTree.column("#0", width=0, stretch=NO)
    intelInvestigateTree["columns"] = ("ชื่อสินค้า", "จำนวน", "ราคา/หน่วย", "วันที่สั่ง", "ผู้ค้าส่ง")

    intelInvestigateTree.column("ชื่อสินค้า", width=120, anchor=CENTER)
    intelInvestigateTree.column("จำนวน", width=120, anchor=CENTER)
    intelInvestigateTree.column("ราคา/หน่วย", width=120, anchor=CENTER)
    intelInvestigateTree.column("วันที่สั่ง", width=120, anchor=CENTER)
    intelInvestigateTree.column("ผู้ค้าส่ง", width=120, anchor=CENTER)

    intelInvestigateTree.heading("ชื่อสินค้า", text="ชื่อสินค้า")
    intelInvestigateTree.heading("จำนวน", text="จำนวน")
    intelInvestigateTree.heading("ราคา/หน่วย", text="ราคา/หน่วย")
    intelInvestigateTree.heading("วันที่สั่ง", text="วันที่สั่ง")
    intelInvestigateTree.heading("ผู้ค้าส่ง", text="ผู้ค้าส่ง")

    intelInvestigateTree.grid(row=2, column=0, columnspan=3, sticky="n")


def fetchintelinvestigatesearchtree() :
    intelInvestigateTree.delete(*intelInvestigateTree.get_children())
    sql = "SELECT * FROM PurchaseOrderTable"
    cursor.execute(sql)
    res = cursor.fetchall()
    if res:
        for i in range(len(res)):
            if searchTypeSpy.get() == "สินค้า" and dateSelectSpy.get() == "เวลาใดก็ได้":
                if intelSearchBar.get() in res[i][4] :
                    intelInvestigateTree.insert("", END, values=(res[i][4], res[i][5], res[i][6], res[i][1], res[i][3]))
            elif searchTypeSpy.get() == "ผู้ค้าส่ง" and dateSelectSpy.get() == "เวลาใดก็ได้" :
                if intelSearchBar.get() in res[i][3] :
                    intelInvestigateTree.insert("", END, values=(res[i][4], res[i][5], res[i][6], res[i][1], res[i][3]))
            elif searchTypeSpy.get() == "สินค้า" and dateSelectSpy.get() == "เลือกเอง" :
                if intelSearchBar.get() in res[i][4] and "%d/%d/%d" % (dayIntelSpy.get(), monthIntelSpy.get(), yearIntelSpy.get()) == res[i][1] :
                    intelInvestigateTree.insert("", END, values=(res[i][4], res[i][5], res[i][6], res[i][1], res[i][3]))
            elif searchTypeSpy.get() == "ผู้ค้าส่ง" and dateSelectSpy.get() == "เลือกเอง" :
                if intelSearchBar.get() in res[i][3] and "%d/%d/%d" % (dayIntelSpy.get(), monthIntelSpy.get(), yearIntelSpy.get()) == res[i][1] :
                    intelInvestigateTree.insert("", END, values=(res[i][4], res[i][5], res[i][6], res[i][1], res[i][3]))



def saveintelClicked() :
    resetBtnColor()
    clearInfoFrame()


    def getOrderID():
        list = []
        sql = "SELECT orderID FROM SellOrderTable WHERE type = 1"
        cursor.execute(sql)
        res = cursor.fetchall()
        if res:
            for i in range(len(res)):
                list.append(res[i][0])
        return tuple(list)


    def saveClicked() :
        if idCombo.get() == "":
            messagebox.showerror("Admin:", "กรุณาเลือกหมายเลขคำสั่งซื้อ")
            idCombo.focus_force()
        elif clientName.get() == "":
            messagebox.showerror("Admin:", "กรุณาใส่ชื่อลูกค้า")
            clientName.focus_force()
        elif telNumber.get() == "":
            messagebox.showerror("Admin:", "กรุณาใส่เบอร์โทรศัพท์")
            telNumber.focus_force()
        elif telNumber.get().replace('-', '').isnumeric() == False or (len(telNumber.get().replace('-', '')) != 10 and len(telNumber.get().replace('-', '')) != 9):
            messagebox.showerror("Admin:", "เบอร์โทรศัพท์ไม่ถูกต้อง")
            telNumber.focus_force()
        elif deliverForm.get() == "":
            messagebox.showerror("Admin:", "กรุณาเลือกวิธีการจัดส่ง")
        elif transportName.get() == "" and deliverForm.get() == "บริษัทิขนส่ง":
            messagebox.showerror("Admin:", "กรุณากรอกชื่อบริษัทขนส่ง")
            transportName.focus_force()
        elif prodID.get() == "" and deliverForm.get() == "บริษัทิขนส่ง":
            messagebox.showerror("Admin:", "กรุณากรอกหมายเลขพัสดุ")
            prodID.focus_force()
        elif clientAddress.get("1.0", END) == "":
            messagebox.showerror("Admin:", "กรุณากรอกที่อยู่")
            clientAddress.focus_force()
        elif transportName.get() != "" and deliverForm.get() == "ทางร้านจัดส่ง":
            messagebox.showerror("Admin:", "ทางร้านเป็นผู้จัดส่ง")
            transportName.delete(0, END)
        elif prodID.get() != "" and deliverForm.get() == "ทางร้านจัดส่ง":
            messagebox.showerror("Admin:", "ทางร้านเป็นผู้จัดส่ง")
            prodID.delete(0, END)
        else:
            if deliverForm.get() == "บริษัทิขนส่ง": 
                sql = "INSERT INTO DeliveryTable (name, date, phone, type, deliveryName, trackingID, adress) VALUES (?,?,?,?,?,?,?)"
                cursor.execute(sql, [clientName.get(), "%d/%d/%d" % (daySpy.get(), monthSpy.get(), yearSpy.get()), telNumber.get().replace('-', ''), 1, transportName.get(), prodID.get(), clientAddress.get("1.0", END)])
            else:
                sql = "INSERT INTO DeliveryTable (name, date, phone, type, adress) VALUES (?,?,?,?,?)"
                cursor.execute(sql, [clientName.get(), "%d/%d/%d" % (daySpy.get(), monthSpy.get(), yearSpy.get()), telNumber.get().replace('-', ''), 0, clientAddress.get("1.0", END)])
            conn.commit()
            sql = '''SELECT seq FROM sqlite_sequence WHERE name = "DeliveryTable"'''
            cursor.execute(sql)
            id = cursor.fetchone()
            id = id[0]

            sql = "UPDATE SellOrderTable SET deliveryID = ? WHERE orderID = ?"
            cursor.execute(sql, [id, idCombo.get()])
            conn.commit()
            messagebox.showinfo("Admin:", "บันทึกเรียบร้อยแล้ว")
            clearInfoFrame()


    saveIntelBtn["fg"] = "blue"
    saveIntelFrame = Frame(infoFrame, bg="white")
    saveIntelFrame.columnconfigure((0, 1, 2), weight=1)
    saveIntelFrame.rowconfigure((0, 2), weight=1)
    saveIntelFrame.rowconfigure(1, weight=8)
    saveIntelFrame.grid(row=0, column=0, sticky="news")
    # header
    Label(saveIntelFrame, text="บันทึกข้อมูลการจัดส่ง", fg="black", bg="white", font="verdana 35 bold").grid(row=0, column=0, columnspan=3)
    #middle
    intelFrame = Frame(saveIntelFrame, bg="white")
    intelFrame.columnconfigure((0, 1, 2), weight=1)
    intelFrame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
    intelFrame.grid(row=1, column=0, columnspan=3, sticky="news")

    Label(intelFrame, text="หมายเลขคำสั่งซื้อ", fg="black", bg="white", justify=RIGHT).grid(row=0, column=0, sticky="e")
    idCombo = ttk.Combobox(intelFrame, width=20, values=getOrderID(), state="readonly")
    idCombo.grid(row=0, column=1, sticky="w")

    days = [x for x in range(1, 32)]
    months = [x for x in range(1, 13)]
    years = [x for x in range(2023, 2033)]

    daySpy = IntVar()
    daySpy.set(days[0])

    monthSpy = IntVar()
    monthSpy.set(months[0])

    yearSpy = IntVar()
    yearSpy.set(years[0])

    Label(intelFrame, text="วันที่ส่ง", fg="black", bg="white", justify=RIGHT).grid(row=0, column=2, sticky="w")
    OptionMenu(intelFrame, daySpy, *days).grid(row=0, column=2, sticky="w", padx=40)  # type: ignore
    OptionMenu(intelFrame, monthSpy, *months).grid(row=0, column=2)  # type: ignore
    OptionMenu(intelFrame, yearSpy, *years).grid(row=0, column=2, sticky="e", padx=30)  # type: ignore

    Label(intelFrame, text="ชื่อลูกค้า", fg="black", bg="white", justify=RIGHT).grid(row=1, column=0, sticky="e")
    clientName = Entry(intelFrame, width=70)
    clientName.grid(row=1, column=1, columnspan=2, sticky="w")

    Label(intelFrame, text="เบอร์โทรศัพท์", fg="black", bg="white", justify=RIGHT).grid(row=2, column=0, sticky="e")
    telNumber = Entry(intelFrame, width=70)
    telNumber.grid(row=2, column=1, columnspan=2, sticky="w")

    Label(intelFrame, text="รูปแบบจัดส่ง", fg="black", bg="white", justify=RIGHT).grid(row=3, column=0, sticky="e")
    deliverForm = ttk.Combobox(intelFrame, width=35, values=["ทางร้านจัดส่ง", "บริษัทขนส่ง"], state="readonly")
    deliverForm.grid(row=3, column=1, columnspan=2, sticky="w")
    
    Label(intelFrame, text="ชื่อบริษัทขนส่ง", fg="black", bg="white", justify=RIGHT).grid(row=4, column=0, sticky="e")
    transportName = Entry(intelFrame, width=70)
    transportName.grid(row=4, column=1, columnspan=2, sticky="w")

    Label(intelFrame, text="หมายเลขพัสดุ", fg="black", bg="white", justify=RIGHT).grid(row=5, column=0, sticky="e")
    prodID = Entry(intelFrame, width=70)
    prodID.grid(row=5, column=1, columnspan=2, sticky="w")

    Label(intelFrame, text="ที่อยู่จัดส่ง", fg="black", bg="white", justify=RIGHT).grid(row=6, column=0, sticky="e")
    clientAddress = Text(intelFrame, width=70, height=3) # .get ได้เลย
    clientAddress.grid(row=7, column=0, columnspan=3,sticky="n")

    # bottom
    saveBtn = Button(saveIntelFrame, text="บันทึก", fg="black", bg="lime", font="verdana 25 bold",command=saveClicked)
    saveBtn.grid(row=2, column=2)


def printreportClicked() :
    if permission == 1:
        return messagebox.showwarning("Admin:", "คุณไม่มีสิทธิ์เข้าถึง")
    global reportdaySpy, reportmonthSpy, reportyearSpy, reportdaySpy2, reportmonthSpy2, reportyearSpy2
    resetBtnColor()
    clearInfoFrame()
    printReportBtn["fg"] = "blue"
    printReportFrame = Frame(infoFrame, bg="white")
    printReportFrame.rowconfigure((0, 2), weight=1)
    printReportFrame.rowconfigure(1, weight=3)
    printReportFrame.columnconfigure((0, 1), weight=1)
    printReportFrame.grid(row=0, column=0, sticky="news")
    # head
    headFrame = Frame(printReportFrame, bg="white")
    headFrame.rowconfigure(0, weight=1)
    headFrame.columnconfigure((0, 1, 2), weight=1)
    headFrame.grid(row=0, column=0, columnspan=2, sticky="news")

    subheadFrame1 = Frame(headFrame, bg="white")
    subheadFrame1.rowconfigure(0, weight=1)
    subheadFrame1.columnconfigure((0, 1, 2), weight=1)
    subheadFrame1.grid(row=0, column=0, sticky="s", ipadx=20)

    subheadFrame2 = Frame(headFrame, bg="white")
    subheadFrame2.rowconfigure(0, weight=1)
    subheadFrame2.columnconfigure((0, 1, 2), weight=1)
    subheadFrame2.grid(row=0, column=1, sticky="s", ipadx=20)

    subheadFrame3 = Frame(headFrame, bg="white")
    subheadFrame3.rowconfigure(0, weight=1)
    subheadFrame3.columnconfigure((0, 1, 2), weight=1)
    subheadFrame3.grid(row=0, column=2, sticky="ws", ipadx=20)
    # middle
    middleFrame = Frame(printReportFrame, bg="white")
    middleFrame.rowconfigure(0, weight=1)
    middleFrame.columnconfigure(0, weight=1)
    middleFrame.grid(row=1, column=0, columnspan=2, sticky="news")
    # bottom
    printBtn = Button(printReportFrame, text="พิมพ์", fg="black", bg="yellow", font="verdana 20", command=printClicked)
    printBtn.grid(row=2, column=1, sticky="e", padx=10)
    # head buttons
    purchaseReportBtn = Button(headFrame, text="รายงานสรุปข้อมูลการสั่งซื้อ", font="verdana 16", fg="black", bg="white",
                               command=lambda: reportChange("purchase", middleFrame))
    purchaseReportBtn.grid(row=0, column=0, sticky="ew")
    sellingReportBtn = Button(headFrame, text="รายงานสรุปข้อมูลการขาย", font="verdana 16", fg="black", bg="white",
                              command=lambda: reportChange("selling", middleFrame))
    sellingReportBtn.grid(row=0, column=1, sticky="ew")
    sumReportBtn = Button(headFrame, text="รายงานสรุปรายรับ-รายจ่าย", font="verdana 16", fg="black", bg="white",
                          command=lambda: reportChange("sum", middleFrame))
    sumReportBtn.grid(row=0, column=2, columnspan=2, sticky="ew")

    Label(headFrame, text="-", fg="black", bg="white", font="verdana 16").grid(row=0, column=0, columnspan=2, sticky="s")

    days = [x for x in range(1, 32)]
    months = [x for x in range(1, 13)]
    years = [x for x in range(2023, 2033)]

    today = date.today()

    reportdaySpy = StringVar()
    reportdaySpy.set(today.strftime("%d"))

    reportmonthSpy = StringVar()
    reportmonthSpy.set(today.strftime("%m"))

    reportyearSpy = StringVar()
    reportyearSpy.set(today.strftime("20%y"))

    OptionMenu(subheadFrame1, reportdaySpy, *days).grid(row=0, column=0, sticky="w")  # type: ignore
    OptionMenu(subheadFrame1, reportmonthSpy, *months).grid(row=0, column=1)  # type: ignore
    OptionMenu(subheadFrame1, reportyearSpy, *years).grid(row=0, column=2, sticky="e")  # type: ignore

    reportdaySpy2 = StringVar()
    reportdaySpy2.set(today.strftime("%d"))

    reportmonthSpy2 = StringVar()
    reportmonthSpy2.set(today.strftime("%m"))

    reportyearSpy2 = StringVar()
    reportyearSpy2.set(today.strftime("20%y"))

    OptionMenu(subheadFrame2, reportdaySpy2, *days).grid(row=0, column=0, sticky="w")  # type: ignore
    OptionMenu(subheadFrame2, reportmonthSpy2, *months).grid(row=0, column=1)  # type: ignore
    OptionMenu(subheadFrame2, reportyearSpy2, *years).grid(row=0, column=2, sticky="e")  # type: ignore

    searchBtn = Button(subheadFrame3, text="ยืนยัน", font="verdana 16", fg="black", bg="lime", command=lambda: reportChange("", middleFrame))
    searchBtn.grid(row=0, column=2, sticky="w")


def reportChange(name, frame) :
    for child in frame.winfo_children() :
        child.destroy()

    subFrame = Frame(frame, bg="white")
    subFrame.rowconfigure(0, weight=1)
    subFrame.rowconfigure(1, weight=3)
    subFrame.columnconfigure((0, 1), weight=1)
    subFrame.grid(row=0, column=0, sticky="news")

    Label(subFrame, text="ร้านผลไม้โผทิลาษ", font="verdana 18 bold", fg="black", bg="white").grid(row=0, column=0, sticky="nw",padx=10)

    if name == "purchase" :
        Label(subFrame, text="รายงานสรุปข้อมูลการสั่งซื้อ", font="verdana 12", fg="black", bg="white").grid(row=0, column=0, sticky="w", padx=10)
    elif name == "selling" :
        Label(subFrame, text="รายงานสรุปข้อมูลการขาย", font="verdana 12", fg="black", bg="white").grid(row=0, column=0, sticky="w", padx=10)
    elif name == "sum" :
        Label(subFrame, text="รายงานสรุปรายรับ-รายจ่าย", font="verdana 12", fg="black", bg="white").grid(row=0, column=0, sticky="w", padx=10)

    Label(subFrame, text="ตั้งแต่วันที่ %s/%s/%s - %s/%s/%s" %(reportdaySpy.get(), reportmonthSpy.get(), reportyearSpy.get(), reportdaySpy2.get(), reportmonthSpy2.get(),
    reportyearSpy2.get()),
          font="verdana 12", fg="black", bg="white").grid(row=0, column=1, sticky="w")

    today = date.today()
    d = today.strftime("%d/%m/%y")
    Label(subFrame, text="พิมพ์วันที่ " + d, font="verdana 12", fg="black", bg="white").grid(row=0, column=0, sticky="ws", padx=10, pady=10)

    reportFrame = Frame(subFrame, bg="white")
    reportFrame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)
    reportFrame.columnconfigure((0, 1, 2, 3, 4), weight=1)
    reportFrame.grid(row=1, column=0, columnspan=2, sticky="news")

    if name == "purchase" :
        Label(reportFrame, text="รหัสสินค้า", font="verdana 12", fg="black", bg="white").grid(row=0, column=0)
        Label(reportFrame, text="ชื่อสินค้า", font="verdana 12", fg="black", bg="white").grid(row=0, column=1)
        Label(reportFrame, text="จำนวน", font="verdana 12", fg="black", bg="white").grid(row=0, column=2)
        Label(reportFrame, text="ราคา", font="verdana 12", fg="black", bg="white").grid(row=0, column=3)
        Label(reportFrame, text="รวม", font="verdana 12", fg="black", bg="white").grid(row=0, column=4)
        for i in range(9) :
            Label(reportFrame, bg="white").grid(row=i+1,column=0)
        idprodList = []
        prodList = []
        quanList = []
        costList = []
        dummy1 = []
        sql = "SELECT date,productList,quantities,costPerUnit,status FROM PurchaseOrderTable"
        cursor.execute(sql)
        res = cursor.fetchall()
        if res:
            for i in range(len(res)):
                if res[i][4] == 1 and eval(
                        ("%s+%s+%s" % (reportdaySpy.get(), reportmonthSpy.get(), reportyearSpy.get())).replace("+0","+")) <= eval(res[i][0].replace("/", "+")) <= eval(("%s+%s+%s" % (reportdaySpy.get(), reportmonthSpy.get(), reportyearSpy.get())).replace("+0", "+")):
                    if len(res[i][1].split()) > 1 :
                        dummy1 = res[i][1].split()
                        dummy2 = res[i][2].split()
                        dummy3 = res[i][3].split()
                        for x in range(len(dummy1)) :
                            if dummy1[x] not in prodList :
                                prodList.append(dummy1[x])
                            print(i)
                            if len(quanList) == len(prodList) :
                                dummy2[x] = eval(dummy2[x] + "+" + quanList[prodList.index(dummy1[x])])
                                quanList.append(dummy2[x])
                            else :
                                quanList.append(dummy2[x])
                            if len(costList) == len(prodList):
                                dummy3[x] = eval(dummy3[x] + "+" + costList[prodList.index(dummy1[x])])
                                costList.append(dummy3[x])
                            else :
                                costList.append(dummy3[x])
        sql = "SELECT productID, productName FROM WareHouseTable"
        cursor.execute(sql)
        res = cursor.fetchall()
        if res:
            for i in range(len(res)) :
                if res[i][0] not in idprodList and (res[i][1] in dummy1) :
                    idprodList.append(res[i][0])
        sum = 0
        con = 0
        for i in range(len(idprodList)) :
            Label(reportFrame, text=str(idprodList[i]), font="verdana 12", fg="black", bg="white").grid(row=i+1, column=0)
            Label(reportFrame, text=str(prodList[i]), font="verdana 12", fg="black", bg="white").grid(row=i+1, column=1)
            Label(reportFrame, text=str(quanList[i]), font="verdana 12", fg="black", bg="white").grid(row=i + 1,column=2)
            Label(reportFrame, text=str(costList[i]), font="verdana 12", fg="black", bg="white").grid(row=i + 1,column=3)
            sum = float(quanList[i]) * float(costList[i])
            Label(reportFrame, text=str(sum), font="verdana 12", fg="black", bg="white").grid(row=i + 1,column=4)
            con += sum
        Label(reportFrame, text="รวม", font="verdana 12", fg="black", bg="white").grid(row=9, column=3, sticky="e")
        Label(reportFrame, text=con, font="verdana 12", fg="black", bg="white").grid(row=9, column=4)
    elif name == "selling" :
        Label(reportFrame, text="รหัสสินค้า", font="verdana 12", fg="black", bg="white").grid(row=0, column=0)
        Label(reportFrame, text="ชื่อสินค้า", font="verdana 12", fg="black", bg="white").grid(row=0, column=1)
        Label(reportFrame, text="จำนวน", font="verdana 12", fg="black", bg="white").grid(row=0, column=2)
        Label(reportFrame, text="ราคา", font="verdana 12", fg="black", bg="white").grid(row=0, column=3)
        Label(reportFrame, text="รวม", font="verdana 12", fg="black", bg="white").grid(row=0, column=4)
        for i in range(9) :
            Label(reportFrame, bg="white").grid(row=i+1,column=0)
    elif name == "sum" :
        Label(reportFrame, text="สินค้าที่ซื้อ", font="verdana 12", fg="black", bg="white").grid(row=0, column=1)
        Label(reportFrame, text="ชื่อสินค้า", font="verdana 12", fg="black", bg="white").grid(row=1, column=0)
        Label(reportFrame, text="จำนวน", font="verdana 12", fg="black", bg="white").grid(row=1, column=1)
        Label(reportFrame, text="ราคา", font="verdana 12", fg="black", bg="white").grid(row=1, column=2, sticky="w")
        Label(reportFrame, text="สินค้าที่ซื้อ", font="verdana 12", fg="black", bg="white").grid(row=0, column=3)
        Label(reportFrame, text="ชื่อสินค้า", font="verdana 12", fg="black", bg="white").grid(row=1, column=2, sticky="e")
        Label(reportFrame, text="จำนวน", font="verdana 12", fg="black", bg="white").grid(row=1, column=3)
        Label(reportFrame, text="ราคา", font="verdana 12", fg="black", bg="white").grid(row=1, column=4)
        for i in range(9) :
            Label(reportFrame, bg="white").grid(row=i+1,column=0)



def printClicked() :
    return


def purchaseManagementClicked():
    if permission == 1:
        return messagebox.showwarning("Admin:", "คุณไม่มีสิทธิ์เข้าถึง")
    global purchaseTree
    resetBtnColor()
    clearInfoFrame()
    purchaseManagementBtn["fg"] = "blue"
    purchaseMangementFrame = Frame(infoFrame, bg="white")
    purchaseMangementFrame.grid(row=0, column=0, sticky="news")

    purchaseMangementFrame.rowconfigure(0, weight=1) # type: ignore
    purchaseMangementFrame.rowconfigure(1, weight=5)
    purchaseMangementFrame.columnconfigure(0, weight=1)
    purchaseMangementFrame.grid(row=0, column=0, sticky="news")

    top = Frame(purchaseMangementFrame, bg="white")
    top.rowconfigure(0, weight=1)
    top.columnconfigure(0, weight=1)
    top.grid(row=0, column=0, sticky="news")

    middle = Frame(purchaseMangementFrame, bg="white")
    middle.rowconfigure(0, weight=1) #type: ignore

    middle.columnconfigure(0, weight=1)
    middle.grid(row=1, column=0, sticky="news")

    #header
    Label(top, text="เพิ่ม/แก้ไขข้อมูลการสั่งซื้อ", fg="black", bg="white", font="verdana 35 bold").grid(row=0, column=0, sticky='s')

    purchaseTree = ttk.Treeview(middle)
    purchaseTree.column("#0", width=0, stretch=NO)
    purchaseTree["columns"] = ("รหัสสั่งซื้อ","วันที่สั่งซื้อ", "ชื่อผู้สั่งซื้อ", "ชื่อผู้ค้าส่ง", "รายการสินค้า", "ปริมาณการสั่งซื้อ", "ราคาซื้อต่อหน่วย", "ค่าใช้จ่าย", "สถานะ")

    purchaseTree.column("รหัสสั่งซื้อ", width=90, anchor=CENTER)
    purchaseTree.column("วันที่สั่งซื้อ", width=90, anchor=CENTER)
    purchaseTree.column("ชื่อผู้สั่งซื้อ", width=90, anchor=CENTER)
    purchaseTree.column("ชื่อผู้ค้าส่ง", width=90, anchor=CENTER)
    purchaseTree.column("รายการสินค้า", width=90, anchor=E)
    purchaseTree.column("ปริมาณการสั่งซื้อ", width=90, anchor=E)
    purchaseTree.column("ราคาซื้อต่อหน่วย", width=90, anchor=E)
    purchaseTree.column("ค่าใช้จ่าย", width=90, anchor=CENTER)
    purchaseTree.column("สถานะ", width=90, anchor=CENTER)

    purchaseTree.heading("รหัสสั่งซื้อ", text="รหัสสั่งซื้อ")
    purchaseTree.heading("วันที่สั่งซื้อ", text="วันที่สั่งซื้อ")
    purchaseTree.heading("ชื่อผู้สั่งซื้อ", text="ชื่อผู้สั่งซื้อ")
    purchaseTree.heading("ชื่อผู้ค้าส่ง", text="ชื่อผู้ค้าส่ง")
    purchaseTree.heading("รายการสินค้า", text="รายการสินค้า")
    purchaseTree.heading("ปริมาณการสั่งซื้อ", text="ปริมาณการสั่งซื้อ")
    purchaseTree.heading("ราคาซื้อต่อหน่วย", text="ราคาซื้อต่อหน่วย")
    purchaseTree.heading("ค่าใช้จ่าย", text="ค่าใช้จ่าย")
    purchaseTree.heading("สถานะ", text="สถานะ")

    purchaseTree.grid(row=0, column=0)

    # Add Button
    Button(middle, text="สร้างรายการสั่งซื้อใหม่", fg="black", bg="green", command=addPurchaseClicked).grid(row=0, column=0, sticky='ne', padx=15, pady=170)

    # Modify Button
    Button(middle, text="แก้ไขคำสั่งซื้อ", fg="black", bg="yellow", command=modifyPurchaseClicked).grid(row=0, column=0, sticky='se', padx=160, pady=170)

    # Confirm Button
    Button(middle, text="ยืนยันคำสั่งซื้อ", fg="black", bg="green", command=confrimPurchaseClicked).grid(row=0, column=0, sticky='se', padx=280, pady=170)

    #Delete Button
    Button(middle, text="ลบ/ยกเลิกคำสั่งซื้อ", fg="black", bg="red", command=deletePurchaseClicked).grid(row=0, column=0, sticky='se', padx=15, pady=170)
    

    fetchPurchaseTree()


def fetchPurchaseTree():
    purchaseTree.delete(*purchaseTree.get_children())
    sql = "SELECT * FROM PurchaseOrderTable"
    cursor.execute(sql)
    res = cursor.fetchall()
    if res:
        for i in range(len(res)):
            status = "กำลังดำเนินการ"
            if res[i][8] == 1:
                status = "สมบูรณ์"
            purchaseTree.insert("",END, values=(res[i][0],res[i][1], res[i][2], res[i][3], res[i][4], res[i][5], res[i][6], res[i][7], status))


def deletePurchaseClicked():
    if purchaseTree.focus() == "":
        messagebox.showerror("Admin:", "กรุณาเลือกคำสั่งซื้อที่ต้องการจะลบหรือยกเลิก")
    elif purchaseTree.item(purchaseTree.focus(), "values")[8] == "สมบูรณ์":
        messagebox.showerror("Admin:", "รายการสั่งซื้อดำเนินการเสร็จสมบูรณ์แล้ว ไม่สามารถยกเลิก/ลบได้")
    else:
        msg = messagebox.askquestion("Delete", "ต้องการลบ/ยกเลิกคำสั่งซื้อนี้หรือไม่", icon="warning")
        if msg == "yes":
            selectedProd = purchaseTree.item(purchaseTree.focus(), "values")
            
            selectedProd_id = selectedProd[0]
            sql = '''DELETE FROM PurchaseOrderTable
                        WHERE orderID = ?'''
            cursor.execute(sql, [selectedProd_id])
            conn.commit()
            messagebox.showinfo("Admin:", "คำสั่งซื้อถูกลบ/ยกเลิกเรียบร้อยแล้ว")
            fetchPurchaseTree()


def getSupplier():
    returnlist = []
    sql = "SELECT supplierName FROM SupplierContactTable"
    cursor.execute(sql)
    res = cursor.fetchall()
    if res:
        for i in range(len(res)):
            returnlist.append(res[i][0])
    return returnlist

def getProduct():
    sql = "SELECT * FROM WareHouseTable"
    cursor.execute(sql)
    res = cursor.fetchall()
    if res:
        return res
    

def getTotalCost(list):
    total = 0.00
    for i in range(len(list)):
        cost = float(list[i][2]) * float(list[i][3])
        total += cost
    return total


def addPurchaseClicked():
    def AddPurchaseOrder():
        if supplierCombo.get() == "":
            messagebox.showerror("Admin:", "กรุณาเลือกผู้ค้าส่ง")
            supplierCombo.focus_force()
        elif infoTree.get_children() == ():
            messagebox.showerror("Admin:", "ไม่มีรายการสินค้าที่ต้องการจะสั่งซื้อ")
        else:
            sql = '''INSERT INTO PurchaseOrderTable (date, ordererName, supplierName, productList, quantities, costPerUnit, totalCost, status)
                     VALUES (?,?,?,?,?,?,?,?)'''
            date = "%d/%d/%d" %(daySpy.get(), monthSpy.get(), yearSpy.get())
            ordererName = name
            supplierName = supplierCombo.get()
            productList = ""
            quantities = ""
            costPerUnit = ""
            for i in range(len(orderProdlist)):
                if i == len(orderProdlist) - 1:
                    productList += orderProdlist[i][1]
                    quantities += orderProdlist[i][3]
                    costPerUnit += orderProdlist[i][2]
                else:
                    productList += orderProdlist[i][1] + "\n"
                    quantities += orderProdlist[i][3] + "\n"
                    costPerUnit += orderProdlist[i][2] + "\n"
            totalCost = getTotalCost(orderProdlist)
            status = 0
            cursor.execute(sql, [date, ordererName, supplierName, productList, quantities, costPerUnit, totalCost, status])
            conn.commit()
            fetchPurchaseTree()
            messagebox.showinfo("Admin:", "เพิ่มรายการสั่งซื้อดังกล่าวแล้ว")
            addPurchaseWindow.destroy()
        
    
    def fetchinfoTree():
        infoTree.delete(*infoTree.get_children())
        for i in range(len(orderProdlist)):
            infoTree.insert("",END, values=(orderProdlist[i][0],orderProdlist[i][1],orderProdlist[i][2],orderProdlist[i][3]))
    

    def updateTotalLabel():
        totalLabel["text"] = "ค่าใช้จ่าย %.2f บาท"  %getTotalCost(orderProdlist) 
        

    def addProductlist():
        def fetchWarehouseTree():
            alreadyAddedId = [int(orderProdlist[i][0]) for i in range(len(orderProdlist))]
            warehouseTree.delete(*warehouseTree.get_children())
            sql = "SELECT * FROM WareHouseTable"
            cursor.execute(sql)
            res = cursor.fetchall()
            if res:
                for i in range(len(res)):
                    if res[i][0] not in alreadyAddedId:
                        warehouseTree.insert("",END, values=(res[i][0],res[i][1], res[i][2], res[i][4]))
        
        
        def warehouseTreeclicked(event):
            selected_prod = warehouseTree.item(warehouseTree.focus(), "values")
            costEnt.delete(0, END)
            costEnt.insert(END, selected_prod[2])


        def addToProductListClicked():
            if warehouseTree.focus() == "":
                messagebox.showerror("Admin:", "เลือกสินค้าที่ต้องการเพิ่มลงในรายการสั่งซื้อ")
            elif costEnt.get() == "" or costEnt.get().replace('.', '',1).isnumeric() == False:
                messagebox.showerror("Admin:", "ราคาซื้อต่อหน่วยต้องเป็นจำนวนจริงเท่านั้น")
                costEnt.focus_force()
            elif orderQuantityEnt.get() == "" or orderQuantityEnt.get().isnumeric() == False:
                messagebox.showerror("Admin:", "ปริมาณสั่งซื้อต้องเป็นจำนวนเต็มบวกเท่านั้น")
                orderQuantityEnt.focus_force()
            else:
                selected_prod = warehouseTree.item(warehouseTree.focus(), "values")
                info = (selected_prod[0], selected_prod[1], costEnt.get(), orderQuantityEnt.get())
                info = tuple(info)
                orderProdlist.append(info)
                warehouseTree.delete(warehouseTree.focus())
                costEnt.delete(0, END)
                orderQuantityEnt.delete(0, END)
                updateTotalLabel()
                messagebox.showinfo("Admin:", "เพิ่มสินค้าดังกล่าวลงในรายการสั่งซื้อแล้ว")
        
        
        def confirmClicked():
            addProductlistWindow.destroy()
            fetchinfoTree()
        
        w = 600
        h = 500
        addProductlistWindow = Toplevel(root)
        addProductlistWindow.title("รายการสินค้า")
        addProductlistWindow.rowconfigure(0, weight=1)
        addProductlistWindow.columnconfigure(0, weight=1)
        x = root.winfo_screenwidth() / 2 - w / 2
        y = root.winfo_screenheight() / 2 - h / 2
        addProductlistWindow.geometry("%dx%d+%d+%d" %(w, h, x, y))
        
        addProductListFrame = Frame(addProductlistWindow, bg="white")
        addProductListFrame.columnconfigure(0, weight=1)
        addProductListFrame.rowconfigure((0,1), weight=1) # type: ignore
        addProductListFrame.grid(row=0, column=0, sticky="news")

        top = Frame(addProductListFrame, bg="white")
        top.rowconfigure((0,1), weight=1) # type: ignore
        top.columnconfigure((0,1), weight=1) # type: ignore
        top.grid(row=0, column=0, sticky="news")
        
        bot = Frame(addProductListFrame, bg="white")
        bot.rowconfigure((0,1), weight=1) # type: ignore
        bot.columnconfigure(0, weight=1)
        bot.grid(row=1, column=0, sticky="news")

        Label(top, text="ราคาซื้อต่อหน่วย:", fg="black", bg="white", font="verdana 25").grid(row=0, column=0, sticky='e')
        costEnt = Entry(top, width=20)
        costEnt.grid(row=0, column=1, sticky='w')

        Label(top, text="ปริมาณที่สั่งซื้อ:", fg="black", bg="white", font="verdana 25").grid(row=1, column=0, sticky='e')
        orderQuantityEnt = Entry(top, width=20)
        orderQuantityEnt.grid(row=1, column=1, sticky='w')

        warehouseTree = ttk.Treeview(bot)
        warehouseTree.column("#0", width=0, stretch=NO)
        warehouseTree["columns"] = ("รหัสสินค้า","ชื่อสินค้า", "ราคาต้นทุนต่อหน่วย", "ปริมาณคงเหลือ")

        warehouseTree.column("รหัสสินค้า", width=100, anchor=CENTER)
        warehouseTree.column("ชื่อสินค้า", width=100, anchor=CENTER)
        warehouseTree.column("ราคาต้นทุนต่อหน่วย", width=120, anchor=CENTER)
        warehouseTree.column("ปริมาณคงเหลือ", width=120, anchor=CENTER)

        warehouseTree.heading("รหัสสินค้า", text="รหัสสินค้า")
        warehouseTree.heading("ชื่อสินค้า", text="ชื่อสินค้า")
        warehouseTree.heading("ราคาต้นทุนต่อหน่วย", text="ราคาต้นทุนต่อหน่วย")
        warehouseTree.heading("ปริมาณคงเหลือ", text="ปริมาณคงเหลือ")
        warehouseTree.grid(row=0, column=0)

        warehouseTree.bind('<Double-1>', warehouseTreeclicked)

        fetchWarehouseTree()

        Button(bot, text="เพิ่มรายการสินค้า", fg="black", bg="green", command=addToProductListClicked).grid(row=1, column=0, sticky='e', padx=120)
        
        Button(bot, text="ยืนยัน", fg="black", bg="green", command=confirmClicked).grid(row=1, column=0, sticky='e', padx=20)


    orderProdlist = []

    w = 500
    h = 500
    addPurchaseWindow = Toplevel(root)
    addPurchaseWindow.title("สร้างรายการสั่งซื้อใหม่")
    addPurchaseWindow.rowconfigure(0, weight=1)
    addPurchaseWindow.columnconfigure(0, weight=1)
    x = root.winfo_screenwidth() / 2 - w / 2
    y = root.winfo_screenheight() / 2 - h / 2
    addPurchaseWindow.geometry("%dx%d+%d+%d" %(w, h, x, y))

    addPurchaseFrame = Frame(addPurchaseWindow, bg="white")
    addPurchaseFrame.rowconfigure((0,1,2,3,4,5,6), weight=1) #type: ignore
    addPurchaseFrame.columnconfigure((0,1), weight=1)  # type: ignore
    addPurchaseFrame.grid(row=0, column=0, sticky="news")

    suppliers = getSupplier()


    Label(addPurchaseFrame, text="วันที่สั่งซื้อ", fg="black", bg="white", font="verdana 25").grid(row=0, column=0, sticky='e')
    tmpFrame = Frame(addPurchaseFrame, bg="white")
    tmpFrame.rowconfigure(0, weight=1)
    tmpFrame.columnconfigure((0,1,2), weight=1) # type: ignore
    tmpFrame.grid(row=0, column=1, sticky="news")

    days = [x for x in range(1, 32)]
    months = [x for x in range(1, 13)]
    years = [x for x in range(2023, 2033)]

    daySpy = IntVar()
    daySpy.set(days[0])

    monthSpy = IntVar()
    monthSpy.set(months[0])

    yearSpy = IntVar()
    yearSpy.set(years[0])
    
    OptionMenu(tmpFrame, daySpy, *days).grid(row=0, column=0) #type: ignore
    OptionMenu(tmpFrame, monthSpy, *months).grid(row=0, column=1) #type: ignore
    OptionMenu(tmpFrame, yearSpy, *years).grid(row=0, column=2) #type: ignore



    Label(addPurchaseFrame, text="ผู้สั่งซื้อ:", fg="black", bg="white", font="verdana 25").grid(row=1, column=0, sticky='e')
    ordererNameCombo = Label(addPurchaseFrame, text=name, fg="black", bg="white", font="verdana 25")
    ordererNameCombo.grid(row=1, column=1, sticky='w')

    Label(addPurchaseFrame, text="ผู้ค้าส่ง:", fg="black", bg="white", font="verdana 25").grid(row=2, column=0, sticky='e')
    supplierCombo = ttk.Combobox(addPurchaseFrame, values=suppliers, state="readonly")
    supplierCombo.grid(row=2, column=1, sticky='w')

    Label(addPurchaseFrame, text="รายการสินค้า:", fg="black", bg="white", font="verdana 25").grid(row=3, column=0, sticky='e')
    Button(addPurchaseFrame, text="เลือกรายการสินค้า", fg="white", bg="gray", font="verdana 15", command=addProductlist).grid(row=3, column=1, sticky='w', padx=5)

    infoTree = ttk.Treeview(addPurchaseFrame)
    infoTree.column("#0", width=0, stretch=NO)
    infoTree["columns"] = ("รหัสสินค้า","ชื่อสินค้า", "ราคาซื้อต่อหน่วย", "ปริมาณสั่งซื้อ")

    infoTree.column("รหัสสินค้า", width=100, anchor=CENTER)
    infoTree.column("ชื่อสินค้า", width=100, anchor=CENTER)
    infoTree.column("ราคาซื้อต่อหน่วย", width=120, anchor=CENTER)
    infoTree.column("ปริมาณสั่งซื้อ", width=120, anchor=CENTER)

    infoTree.heading("รหัสสินค้า", text="รหัสสินค้า")
    infoTree.heading("ชื่อสินค้า", text="ชื่อสินค้า")
    infoTree.heading("ราคาซื้อต่อหน่วย", text="ราคาซื้อต่อหน่วย")
    infoTree.heading("ปริมาณสั่งซื้อ", text="ปริมาณสั่งซื้อ")
    infoTree.grid(row=4, columnspan=2)

    fetchinfoTree()
    totalCost = getTotalCost(orderProdlist)

    totalLabel = Label(addPurchaseFrame, text="ค่าใช้จ่าย: " + str(totalCost) + " บาท", fg="red", bg="white", font="verdana 20 bold")
    totalLabel.grid(row=5, columnspan=2)


    Button(addPurchaseFrame, text="เพิ่มรายการสั่งซื้อ", fg="black", bg="green", font="verdana 25 bold", command=AddPurchaseOrder).grid(row=6, columnspan=2)


def modifyPurchaseClicked():
    def ModifyPurchaseOrder():
        if infoTree.get_children() == ():
            messagebox.showerror("ไม่มีรายการสินค้า")
        else:
            sql = '''UPDATE PurchaseOrderTable
                    set date = ?, ordererName = ?, supplierName = ?, productList = ?, quantities = ?, costPerUnit = ?, totalCost = ?
                    WHERE orderID = ?'''
            date = "%d/%d/%d" %(daySpy.get(), monthSpy.get(), yearSpy.get())
            ordererName = name
            supplierName = supplierCombo.get()
            productList = ""
            quantitiesStr = ""
            costPerUnit = ""
            for i in range(len(productsName)):
                if i == len(productsName) - 1:
                    productList += productsName[i]
                    quantitiesStr += quantities[i]
                    costPerUnit += costs[i]
                else:
                    productList += productsName[i] + "\n"
                    quantitiesStr += quantities[i] + "\n"
                    costPerUnit += costs[i] + "\n"
            totalCost = getTotal()
            cursor.execute(sql, [date, ordererName, supplierName, productList, quantitiesStr, costPerUnit, totalCost, oldPurchase[0]])
            conn.commit()
            fetchPurchaseTree()
            messagebox.showinfo("Admin:", "แก้ไขรายการสั่งซื้อดังกล่าวแล้ว")
            modifyPurchaseWindow.destroy()
            
    def updateTotalLabel():
        totalLabel["text"] = "ค่าใช้จ่าย %.2f บาท"  %getTotal() 
    def addProductlist():
        def fetchWarehouseTree():
            alreadyAddedId = [int(getProductID(productsName[i])) for i in range(len(productsName))]
            warehouseTree.delete(*warehouseTree.get_children())
            sql = "SELECT * FROM WareHouseTable"
            cursor.execute(sql)
            res = cursor.fetchall()
            if res:
                for i in range(len(res)):
                    if res[i][0] not in alreadyAddedId:
                        warehouseTree.insert("",END, values=(res[i][0],res[i][1], res[i][2], res[i][4]))
        
        
        def warehouseTreeclicked(event):
            selected_prod = warehouseTree.item(warehouseTree.focus(), "values")
            costEnt.delete(0, END)
            costEnt.insert(END, selected_prod[2])


        def addToProductListClicked():
            if warehouseTree.focus() == "":
                messagebox.showerror("Admin:", "เลือกสินค้าที่ต้องการเพิ่มลงในรายการสั่งซื้อ")
            elif costEnt.get() == "" or costEnt.get().replace('.', '',1).isnumeric() == False:
                messagebox.showerror("Admin:", "ราคาซื้อต่อหน่วยต้องเป็นจำนวนจริงเท่านั้น")
                costEnt.focus_force()
            elif orderQuantityEnt.get() == "" or orderQuantityEnt.get().isnumeric() == False:
                messagebox.showerror("Admin:", "ปริมาณสั่งซื้อต้องเป็นจำนวนเต็มบวกเท่านั้น")
                orderQuantityEnt.focus_force()
            else:
                selected_prod = warehouseTree.item(warehouseTree.focus(), "values")
                productsName.append(selected_prod[1])
                costs.append(selected_prod[2])
                quantities.append(selected_prod[3])
                warehouseTree.delete(warehouseTree.focus())
                costEnt.delete(0, END)
                orderQuantityEnt.delete(0, END)
                updateTotalLabel()
                messagebox.showinfo("Admin:", "เพิ่มสินค้าดังกล่าวลงในรายการสั่งซื้อแล้ว")
        
        
        def confirmClicked():
            addProductlistWindow.destroy()
            fetchinfoTree()
        
        w = 600
        h = 500
        addProductlistWindow = Toplevel(root)
        addProductlistWindow.title("รายการสินค้า")
        addProductlistWindow.rowconfigure(0, weight=1)
        addProductlistWindow.columnconfigure(0, weight=1)
        x = root.winfo_screenwidth() / 2 - w / 2
        y = root.winfo_screenheight() / 2 - h / 2
        addProductlistWindow.geometry("%dx%d+%d+%d" %(w, h, x, y))
        
        addProductListFrame = Frame(addProductlistWindow, bg="white")
        addProductListFrame.columnconfigure(0, weight=1)
        addProductListFrame.rowconfigure((0,1), weight=1) # type: ignore
        addProductListFrame.grid(row=0, column=0, sticky="news")

        top = Frame(addProductListFrame, bg="white")
        top.rowconfigure((0,1), weight=1) # type: ignore
        top.columnconfigure((0,1), weight=1) # type: ignore
        top.grid(row=0, column=0, sticky="news")
        
        bot = Frame(addProductListFrame, bg="white")
        bot.rowconfigure((0,1), weight=1) # type: ignore
        bot.columnconfigure(0, weight=1)
        bot.grid(row=1, column=0, sticky="news")

        Label(top, text="ราคาซื้อต่อหน่วย:", fg="black", bg="white", font="verdana 25").grid(row=0, column=0, sticky='e')
        costEnt = Entry(top, width=20)
        costEnt.grid(row=0, column=1, sticky='w')

        Label(top, text="ปริมาณที่สั่งซื้อ:", fg="black", bg="white", font="verdana 25").grid(row=1, column=0, sticky='e')
        orderQuantityEnt = Entry(top, width=20)
        orderQuantityEnt.grid(row=1, column=1, sticky='w')

        warehouseTree = ttk.Treeview(bot)
        warehouseTree.column("#0", width=0, stretch=NO)
        warehouseTree["columns"] = ("รหัสสินค้า","ชื่อสินค้า", "ราคาต้นทุนต่อหน่วย", "ปริมาณคงเหลือ")

        warehouseTree.column("รหัสสินค้า", width=100, anchor=CENTER)
        warehouseTree.column("ชื่อสินค้า", width=100, anchor=CENTER)
        warehouseTree.column("ราคาต้นทุนต่อหน่วย", width=120, anchor=CENTER)
        warehouseTree.column("ปริมาณคงเหลือ", width=120, anchor=CENTER)

        warehouseTree.heading("รหัสสินค้า", text="รหัสสินค้า")
        warehouseTree.heading("ชื่อสินค้า", text="ชื่อสินค้า")
        warehouseTree.heading("ราคาต้นทุนต่อหน่วย", text="ราคาต้นทุนต่อหน่วย")
        warehouseTree.heading("ปริมาณคงเหลือ", text="ปริมาณคงเหลือ")
        warehouseTree.grid(row=0, column=0)

        warehouseTree.bind('<Double-1>', warehouseTreeclicked)

        fetchWarehouseTree()

        Button(bot, text="เพิ่มรายการสินค้า", fg="black", bg="green", command=addToProductListClicked).grid(row=1, column=0, sticky='e', padx=120)
        
        Button(bot, text="ยืนยัน", fg="black", bg="green", command=confirmClicked).grid(row=1, column=0, sticky='e', padx=20)


    def modifyProductlist():
        if infoTree.focus() == "":
            messagebox.showerror("Admin:", "กรุณาเลือกสินค้าที่ต้องการจะแก้ไข")
        else:
            def modifyProductListClicked():
                if costEnt.get() == "" or costEnt.get().replace('.', '',1).isnumeric() == False:
                    messagebox.showerror("Admin:", "ราคาซื้อต่อหน่วยต้องเป็นจำนวนจริงเท่านั้น")
                    costEnt.focus_force()
                elif orderQuantityEnt.get() == "" or orderQuantityEnt.get().isnumeric() == False:
                    messagebox.showerror("Admin:", "ปริมาณสั่งซื้อต้องเป็นจำนวนเต็มบวกเท่านั้น")
                    orderQuantityEnt.focus_force()
                else:
                    for i in range(len(productsName)):
                        if productsName[i] == selectedProd[1]:
                            costs[i] = costEnt.get()
                            quantities[i] = orderQuantityEnt.get()
                    fetchinfoTree()
                    modifyProductlistWindow.destroy()
                    updateTotalLabel()
            
            
            def deleteProductListClicked():
                for i in range(len(productsName)):
                    if productsName[i] == selectedProd[1]:
                        costs.pop(productsName.index(productsName[i]))
                        quantities.pop(productsName.index(productsName[i]))
                        productsName.remove(productsName[i])
                        break
                fetchinfoTree()
                modifyProductlistWindow.destroy()
                updateTotalLabel()


            w = 600
            h = 500
            selectedProd = infoTree.item(infoTree.focus(), "values")
            selectedcost = selectedProd[2]
            selectedquan = selectedProd[3]
            modifyProductlistWindow = Toplevel(root)
            modifyProductlistWindow.title("แก้ไขรายการสินค้า")
            modifyProductlistWindow.rowconfigure(0, weight=1)
            modifyProductlistWindow.columnconfigure(0, weight=1)
            x = root.winfo_screenwidth() / 2 - w / 2
            y = root.winfo_screenheight() / 2 - h / 2
            modifyProductlistWindow.geometry("%dx%d+%d+%d" %(w, h, x, y))
            
            modifyProductListFrame = Frame(modifyProductlistWindow, bg="white")
            modifyProductListFrame.columnconfigure((0,1), weight=1) # type: ignore
            modifyProductListFrame.rowconfigure((0,1,2), weight=1) # type: ignore
            modifyProductListFrame.grid(row=0, column=0, sticky="news")


            Label(modifyProductListFrame, text="ราคาซื้อต่อหน่วย:", fg="black", bg="white", font="verdana 25").grid(row=0, column=0, sticky='e')
            costEnt = Entry(modifyProductListFrame, width=20)
            costEnt.insert(END, selectedcost)
            costEnt.grid(row=0, column=1, sticky='w')

            Label(modifyProductListFrame, text="ปริมาณที่สั่งซื้อ:", fg="black", bg="white", font="verdana 25").grid(row=1, column=0, sticky='e')
            orderQuantityEnt = Entry(modifyProductListFrame, width=20)
            orderQuantityEnt.insert(END, selectedquan)
            orderQuantityEnt.grid(row=1, column=1, sticky='w')


            Button(modifyProductListFrame, text="แก้ไขรายการสินค้า", fg="black", bg="green", command=modifyProductListClicked).grid(row=2, columnspan=2, sticky='e', padx=120)
            
            Button(modifyProductListFrame, text="ลบสินค้า", fg="black", bg="green", command=deleteProductListClicked).grid(row=2, columnspan=2, sticky='e', padx=20)


    def fetchinfoTree():
        infoTree.delete(*infoTree.get_children())
        for i in range(len(productsName)):
            infoTree.insert("",END, values=(getProductID(productsName[i]),productsName[i],costs[i],quantities[i]))


    def getProductID(name):
        sql = "SELECT productID FROM WareHouseTable WHERE productName = ?"
        cursor.execute(sql, [name])
        res = cursor.fetchone()
        return res[0]
    
    def getTotal():
        total = 0.0
        for i in range(len(quantities)):
            total += float(quantities[i]) * float(costs[i])
        return total
    
    def getName(id):
        sql = "SELECT ordererName FROM PurchaseOrderTable WHERE orderID = ?"
        cursor.execute(sql, [id])
        res = cursor.fetchone()
        return res[0]

    if purchaseTree.focus() == "":
        messagebox.showerror("Admin:", "กรุณาเลือกคำสั่งซื้อที่ต้องการจะแก้ไข")
    elif purchaseTree.item(purchaseTree.focus(), "values")[8] == "สมบูรณ์":
        messagebox.showerror("Admin:", "รายการสั่งซื้อดำเนินการเสร็จสมบูรณ์แล้ว ไม่สามารถแก้ไขได้")
    else:
        oldPurchase = purchaseTree.item(purchaseTree.focus(), "values")
        id = oldPurchase[0]
        date = oldPurchase[1].split("/")
        productsName = oldPurchase[4].split("\n")
        quantities = oldPurchase[5].split("\n")
        costs = oldPurchase[6].split("\n")
        totalCost = oldPurchase[7]

        w = 500
        h = 500
        modifyPurchaseWindow = Toplevel(root)
        modifyPurchaseWindow.title("แก้ไขรายการสั่งซื้อ")
        modifyPurchaseWindow.rowconfigure(0, weight=1)
        modifyPurchaseWindow.columnconfigure(0, weight=1)
        x = root.winfo_screenwidth() / 2 - w / 2
        y = root.winfo_screenheight() / 2 - h / 2
        modifyPurchaseWindow.geometry("%dx%d+%d+%d" %(w, h, x, y))

        modifyPurchaseFrame = Frame(modifyPurchaseWindow, bg="white")
        modifyPurchaseFrame.rowconfigure((0,1,2,3,4,5,6), weight=1) #type: ignore
        modifyPurchaseFrame.columnconfigure((0,1), weight=1)  # type: ignore
        modifyPurchaseFrame.grid(row=0, column=0, sticky="news")

        suppliers = getSupplier()
        name = getName(id)

        Label(modifyPurchaseFrame, text="วันที่สั่งซื้อ", fg="black", bg="white", font="verdana 25").grid(row=0, column=0, sticky='e')
        tmpFrame = Frame(modifyPurchaseFrame, bg="white")
        tmpFrame.rowconfigure(0, weight=1)
        tmpFrame.columnconfigure((0,1,2), weight=1) # type: ignore
        tmpFrame.grid(row=0, column=1, sticky="news")

        days = [x for x in range(1, 32)]
        months = [x for x in range(1, 13)]
        years = [x for x in range(2023, 2033)]

        daySpy = IntVar()
        daySpy.set(int(date[0]))

        monthSpy = IntVar()
        monthSpy.set(int(date[1]))

        yearSpy = IntVar()
        yearSpy.set(int(date[2]))
        
        OptionMenu(tmpFrame, daySpy, *days).grid(row=0, column=0) #type: ignore
        OptionMenu(tmpFrame, monthSpy, *months).grid(row=0, column=1) #type: ignore
        OptionMenu(tmpFrame, yearSpy, *years).grid(row=0, column=2) #type: ignore

        Label(modifyPurchaseFrame, text="ผู้สั่งซื้อ:", fg="black", bg="white", font="verdana 25").grid(row=1, column=0, sticky='e')
        ordererNameCombo = Label(modifyPurchaseFrame, text=name, fg="black", bg="white", font="verdana 25")
        ordererNameCombo.grid(row=1, column=1, sticky='w')

        Label(modifyPurchaseFrame, text="ผู้ค้าส่ง:", fg="black", bg="white", font="verdana 25").grid(row=2, column=0, sticky='e')
        supplierCombo = ttk.Combobox(modifyPurchaseFrame, values=suppliers, state="readonly")
        supplierCombo.current(suppliers.index(oldPurchase[3]))
        supplierCombo.grid(row=2, column=1, sticky='w')

        Label(modifyPurchaseFrame, text="รายการสินค้า:", fg="black", bg="white", font="verdana 25").grid(row=3, column=0, sticky='e')
        Button(modifyPurchaseFrame, text="เพิ่มรายการสินค้า", fg="white", bg="gray", font="verdana 15", command=addProductlist).grid(row=3, column=1, sticky='w', padx=5)
        Button(modifyPurchaseFrame, text="แก้ไขสินค้า", fg="white", bg="gray", font="verdana 15", command=modifyProductlist).grid(row=3, column=1, sticky='e', padx=10)


        infoTree = ttk.Treeview(modifyPurchaseFrame)
        infoTree.column("#0", width=0, stretch=NO)
        infoTree["columns"] = ("รหัสสินค้า","ชื่อสินค้า", "ราคาซื้อต่อหน่วย", "ปริมาณสั่งซื้อ")

        infoTree.column("รหัสสินค้า", width=100, anchor=CENTER)
        infoTree.column("ชื่อสินค้า", width=100, anchor=CENTER)
        infoTree.column("ราคาซื้อต่อหน่วย", width=120, anchor=CENTER)
        infoTree.column("ปริมาณสั่งซื้อ", width=120, anchor=CENTER)

        infoTree.heading("รหัสสินค้า", text="รหัสสินค้า")
        infoTree.heading("ชื่อสินค้า", text="ชื่อสินค้า")
        infoTree.heading("ราคาซื้อต่อหน่วย", text="ราคาซื้อต่อหน่วย")
        infoTree.heading("ปริมาณสั่งซื้อ", text="ปริมาณสั่งซื้อ")
        infoTree.grid(row=4, columnspan=2)

        fetchinfoTree()
        totalCost = getTotal()

        totalLabel = Label(modifyPurchaseFrame, text="ค่าใช้จ่าย: " + str(totalCost) + " บาท", fg="red", bg="white", font="verdana 20 bold")
        totalLabel.grid(row=5, columnspan=2)


        Button(modifyPurchaseFrame, text="แก้ไขรายการสั่งซื้อ", fg="black", bg="green", font="verdana 25 bold", command=ModifyPurchaseOrder).grid(row=6, columnspan=2)


def confrimPurchaseClicked():
    if purchaseTree.focus() == "":
        messagebox.showerror("Admin:", "กรุณาเลือกคำสั่งซื้อที่ต้องการจะยืนยัน")
    elif purchaseTree.item(purchaseTree.focus(), "values")[8] == "สมบูรณ์":
        messagebox.showerror("Admin:", "รายการสั่งซื้อดำเนินการเสร็จสมบูรณ์แล้ว")
    else:
        msg = messagebox.askquestion("Confirm", "ต้องการยืนยันคำสั่งซื้อนี้หรือไม่", icon="warning")
        if msg == "yes":
            selectedProd = purchaseTree.item(purchaseTree.focus(), "values")
            selectedProd_id = selectedProd[0]
            sql = "UPDATE PurchaseOrderTable SET status = 1 WHERE orderID = ?"
            cursor.execute(sql, [selectedProd_id])
            conn.commit()
            fetchPurchaseTree()

            today = date.today()
            d = today.strftime("%d/%m/%y")
            prodNames = selectedProd[4].split("\n")
            prodQuan = selectedProd[5].split("\n")
            prodCost = selectedProd[6].split("\n")
            for i in range(len(prodNames)):
                sql = "SELECT quantity FROM WareHouseTable WHERE productName = ?"
                cursor.execute(sql, [prodNames[i]])
                originalQuan = cursor.fetchone()
                originalQuan = originalQuan[0]
                sql = "UPDATE WareHouseTable SET cost = ?, quantity = ?, date = ? WHERE productName = ?"
                cursor.execute(sql, [prodCost[i], int(prodQuan[i]) + originalQuan, d, prodNames[i]])
                conn.commit()
            messagebox.showinfo("Admin:", "รายการสั่งซื้อได้รับการยืนยันแล้ว รายการสินค้าจะถูกเพิ่มเข้าคลังอัตโนมัติ")


def sellManagementClicked():
    orderProdlist = []
    def fetchsellTree():
        sellTree.delete(*sellTree.get_children())
        sql = "SELECT * FROM SellOrderTable"
        cursor.execute(sql)
        res = cursor.fetchall()
        if res:
            for i in range(len(res)):
                deType = "หน้าร้าน"
                if res[i][7] == 1:
                    deType = "จัดส่ง"
                sellTree.insert("", END, values=(res[i][0], res[i][1], res[i][2], res[i][3], res[i][4], res[i][5], res[i][6], deType))


    def addSellClicked():
        def addOrder():
            if infoTree.get_children() == ():
                messagebox.showerror("Admin:", "ไม่มีรายการขาย")
            else:
                sql = '''INSERT INTO SellOrderTable (orderID, date, seller, products, quantities, prices, totalPrice, type)
                     VALUES (?,?,?,?,?,?,?,?)'''
                orderID = orderIDSpy.get()
                today = date.today()
                d = today.strftime("%d/%m/%y")
                seller = name
                productList = ""
                quantities = ""
                pricePerUnit = ""
                for i in range(len(orderProdlist)):
                    if i == len(orderProdlist) - 1:
                        productList += orderProdlist[i][1]
                        quantities += orderProdlist[i][3]
                        pricePerUnit += orderProdlist[i][2]
                    else:
                        productList += orderProdlist[i][1] + "\n"
                        quantities += orderProdlist[i][3] + "\n"
                        pricePerUnit += orderProdlist[i][2] + "\n"
                totalPrice = getTotalPrice()
                type = 0
                if sellTypeSpy.get() == "จัดส่ง":
                    type = 1
                cursor.execute(sql, [orderID, d, seller, productList, quantities, pricePerUnit, totalPrice, type])
                conn.commit()
                fetchsellTree()
                messagebox.showinfo("Admin:", "เพิ่มรายการขายดังกล่าวแล้ว")
                addSellWindow.destroy()

                products = productList.split("\n")
                quan = quantities.split("\n")
                price = pricePerUnit.split("\n")
                for i in range(len(products)):
                    sql = "SELECT quantity FROM WareHouseTable WHERE productName = ?"
                    cursor.execute(sql, [products[i]])
                    originalQuan = cursor.fetchone()
                    originalQuan = originalQuan[0]
                    sql = "UPDATE WareHouseTable SET price = ?, quantity = ?, date = ? WHERE productName = ?"
                    cursor.execute(sql, [pricePerUnit[i], originalQuan - int(quan[i]), d, products[i]])
                    conn.commit()

        def fetchinfoTree():
            infoTree.delete(*infoTree.get_children())
            for i in range(len(orderProdlist)):
                infoTree.insert("",END, values=(orderProdlist[i][0],orderProdlist[i][1],orderProdlist[i][2],orderProdlist[i][3]))


        def generateID():
            id = ""
            today = date.today()
            d = today.strftime("%d%m%y")
            id += d
            sql = "SELECT * FROM SellOrderTable"
            cursor.execute(sql)
            res = cursor.fetchall()

            return id + str(len(res) + 1)
        

        def addProductlist():
            def fetchWarehouseTree():
                alreadyAddedId = [int(orderProdlist[i][0]) for i in range(len(orderProdlist))]
                warehouseTree.delete(*warehouseTree.get_children())
                sql = "SELECT * FROM WareHouseTable"
                cursor.execute(sql)
                res = cursor.fetchall()
                if res:
                    for i in range(len(res)):
                        if res[i][0] not in alreadyAddedId:
                            warehouseTree.insert("",END, values=(res[i][0],res[i][1], res[i][3], res[i][4]))
            
        
            def warehouseTreeclicked(event):
                selected_prod = warehouseTree.item(warehouseTree.focus(), "values")
                priceEnt.delete(0, END)
                priceEnt.insert(END, selected_prod[2])

            
            def CheckifLowerThanBuyPrice(prodID,sellprice):
                sql = "SELECT cost FROM WareHouseTable WHERE productID = ?"
                cursor.execute(sql, [prodID])
                res = cursor.fetchone()
                res= res[0]
                return res > sellprice


            def addToProductListClicked():
                if warehouseTree.focus() == "":
                    messagebox.showerror("Admin:", "เลือกสินค้าที่ต้องการเพิ่มลงในรายการขาย")
                elif priceEnt.get() == "" or priceEnt.get().replace('.', '',1).isnumeric() == False:
                    messagebox.showerror("Admin:", "ราคาขายต่อหน่วยต้องเป็นจำนวนจริงเท่านั้น")
                    priceEnt.focus_force()
                elif sellQuantityEnt.get() == "" or sellQuantityEnt.get().isnumeric() == False or sellQuantityEnt.get() == "0":
                    messagebox.showerror("Admin:", "ปริมาณขายต้องเป็นจำนวนเต็มบวกเท่านั้น")
                    sellQuantityEnt.focus_force()
                else:
                    selected_prod = warehouseTree.item(warehouseTree.focus(), "values")
                    if int(sellQuantityEnt.get()) > int(selected_prod[3]):
                        messagebox.showinfo("Admin:", "ปริมาณที่ขายมีมากกว่าปริมาณที่มีอยู่ในคลัง")
                        sellQuantityEnt.focus_force()
                    elif CheckifLowerThanBuyPrice(int(selected_prod[0]), int(priceEnt.get())):
                        messagebox.showerror("Admin:", "ราคาขายต่ำกว่าราคาซื้อ")
                        priceEnt.focus_force()
                    else:
                        info = (selected_prod[0], selected_prod[1], priceEnt.get(), sellQuantityEnt.get())
                        info = tuple(info)
                        orderProdlist.append(info)
                        warehouseTree.delete(warehouseTree.focus())
                        priceEnt.delete(0, END)
                        sellQuantityEnt.delete(0, END)
                        updatePriceLabel()
                        messagebox.showinfo("Admin:", "เพิ่มสินค้าดังกล่าวลงในรายการขายแล้ว")

            def confirmClicked():
                    addProductlistWindow.destroy()
                    fetchinfoTree()
        
            w = 600
            h = 500
            addProductlistWindow = Toplevel(root)
            addProductlistWindow.title("รายการสินค้า")
            addProductlistWindow.rowconfigure(0, weight=1)
            addProductlistWindow.columnconfigure(0, weight=1)
            x = root.winfo_screenwidth() / 2 - w / 2
            y = root.winfo_screenheight() / 2 - h / 2
            addProductlistWindow.geometry("%dx%d+%d+%d" %(w, h, x, y))
            
            addProductListFrame = Frame(addProductlistWindow, bg="white")
            addProductListFrame.columnconfigure(0, weight=1)
            addProductListFrame.rowconfigure((0,1), weight=1) # type: ignore
            addProductListFrame.grid(row=0, column=0, sticky="news")

            top = Frame(addProductListFrame, bg="white")
            top.rowconfigure((0,1), weight=1) # type: ignore
            top.columnconfigure((0,1), weight=1) # type: ignore
            top.grid(row=0, column=0, sticky="news")
            
            bot = Frame(addProductListFrame, bg="white")
            bot.rowconfigure((0,1), weight=1) # type: ignore
            bot.columnconfigure(0, weight=1)
            bot.grid(row=1, column=0, sticky="news")

            Label(top, text="ราคาขายต่อหน่วย:", fg="black", bg="white", font="verdana 25").grid(row=0, column=0, sticky='e')
            priceEnt = Entry(top, width=20)
            priceEnt.grid(row=0, column=1, sticky='w')

            Label(top, text="ปริมาณที่ขาย:", fg="black", bg="white", font="verdana 25").grid(row=1, column=0, sticky='e')
            sellQuantityEnt = Entry(top, width=20)
            sellQuantityEnt.grid(row=1, column=1, sticky='w')

            warehouseTree = ttk.Treeview(bot)
            warehouseTree.column("#0", width=0, stretch=NO)
            warehouseTree["columns"] = ("รหัสสินค้า","ชื่อสินค้า", "ราคาขายต่อหน่วย", "ปริมาณคงเหลือ")

            warehouseTree.column("รหัสสินค้า", width=100, anchor=CENTER)
            warehouseTree.column("ชื่อสินค้า", width=100, anchor=CENTER)
            warehouseTree.column("ราคาขายต่อหน่วย", width=120, anchor=CENTER)
            warehouseTree.column("ปริมาณคงเหลือ", width=120, anchor=CENTER)

            warehouseTree.heading("รหัสสินค้า", text="รหัสสินค้า")
            warehouseTree.heading("ชื่อสินค้า", text="ชื่อสินค้า")
            warehouseTree.heading("ราคาขายต่อหน่วย", text="ราคาขายต่อหน่วย")
            warehouseTree.heading("ปริมาณคงเหลือ", text="ปริมาณคงเหลือ")
            warehouseTree.grid(row=0, column=0)

            warehouseTree.bind('<Double-1>', warehouseTreeclicked)

            fetchWarehouseTree()

            Button(bot, text="เพิ่มรายการสินค้า", fg="black", bg="green", command=addToProductListClicked).grid(row=1, column=0, sticky='e', padx=120)
            
            Button(bot, text="ยืนยัน", fg="black", bg="green", command=confirmClicked).grid(row=1, column=0, sticky='e', padx=20)

        
        def getTotalPrice():
            price = 0.0
            for i in range(len(orderProdlist)):
              price += float(orderProdlist[i][2]) * int(orderProdlist[i][3])
            return price


        def updatePriceLabel():
            totalLabel["text"] = "ราคารวม: %.2f บาท" %getTotalPrice()
                
        w = 500
        h = 500
        addSellWindow = Toplevel(root)
        addSellWindow.title("สร้างรายการขายใหม่")
        addSellWindow.rowconfigure(0, weight=1)
        addSellWindow.columnconfigure(0, weight=1)
        x = root.winfo_screenwidth() / 2 - w / 2
        y = root.winfo_screenheight() / 2 - h / 2
        addSellWindow.geometry("%dx%d+%d+%d" %(w, h, x, y))

        addSellFrame = Frame(addSellWindow, bg="white")
        addSellFrame.rowconfigure((0,1,2,3,4,5,6,7), weight=1) #type: ignore
        addSellFrame.columnconfigure((0,1), weight=1)  # type: ignore
        addSellFrame.grid(row=0, column=0, sticky="news")

        suppliers = getSupplier()

        orderIDSpy = StringVar()
        orderIDSpy.set(generateID())

        Label(addSellFrame, text="หมายเลขคำสั่งซื้อ", fg="black", bg="white", font="verdana 25").grid(row=0, column=0, sticky='e')
        Label(addSellFrame, textvariable=orderIDSpy, fg="black", bg="white", font="verdana 25").grid(row=0, column=1, sticky='w')

        Label(addSellFrame, text="ผู้ขาย:", fg="black", bg="white", font="verdana 25").grid(row=1, column=0, sticky='e')
        sellerNameCombo = Label(addSellFrame, text=name, fg="black", bg="white", font="verdana 25")
        sellerNameCombo.grid(row=1, column=1, sticky='w')

        Label(addSellFrame, text="รายการสินค้า:", fg="black", bg="white", font="verdana 25").grid(row=2, column=0, sticky='e')
        Button(addSellFrame, text="เลือกรายการสินค้า", fg="white", bg="gray", font="verdana 15", command=addProductlist).grid(row=2, column=1, sticky='w', padx=5)

        infoTree = ttk.Treeview(addSellFrame)
        infoTree.column("#0", width=0, stretch=NO)
        infoTree["columns"] = ("รหัสสินค้า","ชื่อสินค้า", "ราคาขายต่อหน่วย", "ปริมาณที่ขาย")

        infoTree.column("รหัสสินค้า", width=100, anchor=CENTER)
        infoTree.column("ชื่อสินค้า", width=100, anchor=CENTER)
        infoTree.column("ราคาขายต่อหน่วย", width=120, anchor=CENTER)
        infoTree.column("ปริมาณที่ขาย", width=120, anchor=CENTER)

        infoTree.heading("รหัสสินค้า", text="รหัสสินค้า")
        infoTree.heading("ชื่อสินค้า", text="ชื่อสินค้า")
        infoTree.heading("ราคาขายต่อหน่วย", text="ราคาขายต่อหน่วย")
        infoTree.heading("ปริมาณที่ขาย", text="ปริมาณที่ขาย")
        infoTree.grid(row=3, columnspan=2)

        fetchinfoTree()
        totalPrice = getTotalPrice()

        sellTypeSpy = StringVar()
        sellType = ["หน้าร้าน", "จัดส่ง"]
        sellTypeSpy.set(sellType[0])

        Label(addSellFrame, text="ประเภทการจัดส่ง:", fg="black", bg="white", font="verdana 25").grid(row=4, column=0, sticky='e')
        OptionMenu(addSellFrame, sellTypeSpy, *sellType, ).grid(row=4, column=1, sticky='w')

        totalLabel = Label(addSellFrame, text="ราคารวม: " + str(totalPrice) + " บาท", fg="green", bg="white", font="verdana 20 bold")
        totalLabel.grid(row=5, columnspan=2)


        Button(addSellFrame, text="เพิ่มรายการขาย", fg="black", bg="green", font="verdana 25 bold", command=addOrder).grid(row=6, columnspan=2)


    resetBtnColor()
    clearInfoFrame()
    sellManagementBtn["fg"] = "blue"
    sellFrame = Frame(infoFrame, bg="white")
    sellFrame.rowconfigure(0, weight=1) # type: ignore
    sellFrame.rowconfigure(1, weight=5)
    sellFrame.columnconfigure(0, weight=1)
    sellFrame.grid(row=0, column=0, sticky="news")

    top = Frame(sellFrame, bg="white")
    top.rowconfigure(0, weight=1)
    top.columnconfigure(0, weight=1)
    top.grid(row=0, column=0, sticky="news")

    middle = Frame(sellFrame, bg="white")
    middle.rowconfigure(0, weight=1) #type: ignore

    middle.columnconfigure(0, weight=1)
    middle.grid(row=1, column=0, sticky="news")

    #header
    Label(top, text="บันทึกการขายสินค้า", fg="black", bg="white", font="verdana 35 bold").grid(row=0, column=0, sticky='s')

    # Add Button
    Button(middle, text="เพิ่มรายการขาย", fg="black", bg="green", command=addSellClicked).grid(row=0, column=0, sticky='ne', padx=60, pady=170)
    

    sellTree = ttk.Treeview(middle)
    sellTree.column("#0", width=0, stretch=NO)
    sellTree["columns"] = ("หมายเลขการสั่งซื้อ","วันที่ขาย", "ชื่อผู้ขาย", "รายการสินค้า", 'ปริมาณที่ขาย', "ราคาขายต่อหน่วย", "ราคารวม", "ประเภทจัดส่ง")

    sellTree.column("หมายเลขการสั่งซื้อ", width=100, anchor=CENTER)
    sellTree.column("วันที่ขาย", width=100, anchor=CENTER)
    sellTree.column("ชื่อผู้ขาย", width=120, anchor=CENTER)
    sellTree.column("รายการสินค้า", width=90, anchor=CENTER)
    sellTree.column("ปริมาณที่ขาย", width=120, anchor=CENTER)
    sellTree.column("ราคาขายต่อหน่วย", width=120, anchor=CENTER)
    sellTree.column("ราคารวม", width=90, anchor=CENTER)
    sellTree.column("ประเภทจัดส่ง", width=90, anchor=CENTER)

    sellTree.heading("หมายเลขการสั่งซื้อ", text="หมายเลขการสั่งซื้อ")
    sellTree.heading("วันที่ขาย", text="วันที่ขาย")
    sellTree.heading("ชื่อผู้ขาย", text="ชื่อผู้ขาย")
    sellTree.heading("รายการสินค้า", text="รายการสินค้า")
    sellTree.heading("ปริมาณที่ขาย", text="ปริมาณที่ขาย")
    sellTree.heading("ราคาขายต่อหน่วย", text="ราคาขายต่อหน่วย")
    sellTree.heading("ราคารวม", text="ราคารวม")
    sellTree.heading("ประเภทจัดส่ง", text="ประเภทจัดส่ง")
    sellTree.grid(row=0, column=0)

    fetchsellTree()


def accountManagementClicked():
    if permission == 1:
        return messagebox.showwarning("Admin:", "คุณไม่มีสิทธิ์เข้าถึง")
    def addAccountClicked():
        def AddAccout():
            if fullnameEnt.get() == "":
                messagebox.showerror("Admin:", "กรุณาใส่ชื่อ")
                fullnameEnt.focus_force()
            elif fullnameEnt.get().isnumeric() == True:
                messagebox.showerror("Admin:", "ชื่อไม่สามารถเป็นตัวเลขได้")
                fullnameEnt.focus_force()
            elif usernameEnt.get() == "":
                messagebox.showerror("Admin:", "กรุณาใส่ Username")
                usernameEnt.focus_force()
            elif pwdEnt.get() == "":
                messagebox.showerror("Admin:", "กรุณากรอกรหัสผ่าน")
                pwdEnt.focus_force()
            else:
                isValid = True
                sql = "SELECT name FROM LoginTable"
                cursor.execute(sql)
                res = cursor.fetchall()
                for i in range(len(res)):
                    if res[i][0] == fullnameEnt.get():
                        messagebox.showerror("Admin:","มีบัญชีผู้ใช้รายนี้ในฐานข้อมูลแล้ว")
                        isValid = False
                        break
                
                if isValid:
                    sql = "INSERT INTO LoginTable (username, pwd, name, permission) VALUES (?,?,?,?)"
                    per = 0
                    if perSpy.get() == "ลูกจ้าง":
                        per = 1
                    cursor.execute(sql, [usernameEnt.get(), pwdEnt.get(), fullnameEnt.get(), per])
                    conn.commit()
                    messagebox.showinfo("Admin:", "บัญชีผู้ใช้ใหม่ได้ถูกเพิ่มเข้าสู่ฐานระบบแล้ว")
                    addAccoutWindow.destroy()
                    fetchaccoutTree()
                else:
                    fullnameEnt.focus_force()

        w = 500
        h = 500
        addAccoutWindow = Toplevel(root)
        addAccoutWindow.title("เพิ่มบัญชีใหม่")
        addAccoutWindow.rowconfigure(0, weight=1)
        addAccoutWindow.columnconfigure(0, weight=1)
        x = root.winfo_screenwidth() / 2 - w / 2
        y = root.winfo_screenheight() / 2 - h / 2
        addAccoutWindow.geometry("%dx%d+%d+%d" %(w, h, x, y))

        addAccoutFrame = Frame(addAccoutWindow, bg="white")
        addAccoutFrame.rowconfigure((0,1,2,3,4), weight=1) #type: ignore
        addAccoutFrame.columnconfigure((0,1), weight=1)  # type: ignore
        addAccoutFrame.grid(row=0, column=0, sticky="news")

        Label(addAccoutFrame, text="ชื่อ:", fg="black", bg="white", font="verdana 25").grid(row=0, column=0, sticky='e')
        fullnameEnt = Entry(addAccoutFrame, width=20)
        fullnameEnt.grid(row=0, column=1, sticky='w')

        Label(addAccoutFrame, text="Username:", fg="black", bg="white", font="verdana 25").grid(row=1, column=0, sticky='e')
        usernameEnt = Entry(addAccoutFrame, width=20)
        usernameEnt.grid(row=1, column=1, sticky='w')

        Label(addAccoutFrame, text="รหัสผ่าน", fg="black", bg="white", font="verdana 25").grid(row=2, column=0, sticky='e')
        pwdEnt = Entry(addAccoutFrame, width=20, show="●")
        pwdEnt.grid(row=2, column=1, sticky='w')
        
        perSpy = StringVar()
        perList = ["เจ้าของร้าน", "ลูกจ้าง"]
        perSpy.set(perList[1])
        Label(addAccoutFrame, text="สถานะ", fg="black", bg="white", font="verdana 25").grid(row=3, column=0, sticky='e')
        OptionMenu(addAccoutFrame, perSpy, *perList).grid(row=3, column=1, sticky='w')

        Button(addAccoutFrame, text="เพิ่มบัญชีผู้ใช้", fg="black", bg="green", font="verdana 25 bold", command=AddAccout).grid(row=4, columnspan=2)

    def modifyAccoutClicked():
        def ModifyAccout():
            if fullnameEnt.get() == "":
                messagebox.showerror("Admin:", "กรุณาใส่ชื่อ")
                fullnameEnt.focus_force()
            elif fullnameEnt.get().isnumeric() == True:
                messagebox.showerror("Admin:", "ชื่อไม่สามารถเป็นตัวเลขได้")
                fullnameEnt.focus_force()
            elif usernameEnt.get() == "":
                messagebox.showerror("Admin:", "กรุณาใส่ Username")
                usernameEnt.focus_force()
            elif pwdEnt.get() == "":
                messagebox.showerror("Admin:", "กรุณากรอกรหัสผ่าน")
                pwdEnt.focus_force()
            else:
                isValid = True
                sql = "SELECT userID, name FROM LoginTable"
                cursor.execute(sql)
                res = cursor.fetchall()
                for i in range(len(res)):
                    if res[i][0] == fullnameEnt.get() and res[i][1] != selectedAcc_id:
                        messagebox.showerror("Admin:","มีบัญชีผู้ใช้รายนี้ในฐานข้อมูลแล้ว")
                        isValid = False
                        break
        
                if isValid:
                    per = 0
                    if perSpy.get() == "ลูกจ้าง":
                        per = 1
                    sql = "UPDATE LoginTable SET username = ?, pwd = ?, name = ?, permission = ? WHERE userID = ?"
                    cursor.execute(sql, [usernameEnt.get(), pwdEnt.get(), fullnameEnt.get(), per, selectedAcc_id])
                    conn.commit()
                    messagebox.showinfo("Admin:", "แก้ไขบัญชีผู้ใช้เรียบร้อยแล้ว")
                    modifyWindow.destroy()
                    fetchaccoutTree()
                else:
                    fullnameEnt.focus_force()

        if accountTree.focus() == "":
            messagebox.showerror("Admin:", "กรุณาเลือกบัญชีที่ต้องการจะแก้ไข")
        else:
            def getPwd():
                sql = "SELECT pwd FROM LoginTable WHERE userID = ?"
                cursor.execute(sql, [selectedAcc_id])
                res = cursor.fetchone()
                return res[0]
            
            selectedAcc = accountTree.item(accountTree.focus(), "values")
            selectedAcc_id = int(selectedAcc[0])
            selectedAcc_username = selectedAcc[1]
            selectedAcc_pwd = getPwd()
            selectedAcc_name = selectedAcc[2]
            selectedAcc_per = selectedAcc[3]

            w = 500
            h = 500
            modifyWindow = Toplevel(root)
            modifyWindow.title("แก้ไขบัญชี")
            modifyWindow.rowconfigure(0, weight=1)
            modifyWindow.columnconfigure(0, weight=1)
            x = root.winfo_screenwidth() / 2 - w / 2
            y = root.winfo_screenheight() / 2 - h / 2
            modifyWindow.geometry("%dx%d+%d+%d" %(w, h, x, y))

            modifyFrame = Frame(modifyWindow, bg="white")
            modifyFrame.rowconfigure((0,1,2,3,4), weight=1) #type: ignore
            modifyFrame.columnconfigure((0,1), weight=1)  # type: ignore
            modifyFrame.grid(row=0, column=0, sticky="news")

            Label(modifyFrame, text="ชื่อ:", fg="black", bg="white", font="verdana 25").grid(row=0, column=0, sticky='e')
            fullnameEnt = Entry(modifyFrame, width=20)
            fullnameEnt.insert(END, selectedAcc_name)
            fullnameEnt.grid(row=0, column=1, sticky='w')

            Label(modifyFrame, text="Username:", fg="black", bg="white", font="verdana 25").grid(row=1, column=0, sticky='e')
            usernameEnt = Entry(modifyFrame, width=20)
            usernameEnt.insert(END, selectedAcc_username)
            usernameEnt.grid(row=1, column=1, sticky='w')

            Label(modifyFrame, text="รหัสผ่าน", fg="black", bg="white", font="verdana 25").grid(row=2, column=0, sticky='e')
            pwdEnt = Entry(modifyFrame, width=20, show="●")
            pwdEnt.insert(END, selectedAcc_pwd)
            pwdEnt.grid(row=2, column=1, sticky='w')
            
            perSpy = StringVar()
            perList = ["เจ้าของร้าน", "ลูกจ้าง"]
            perSpy.set(selectedAcc_per)
            Label(modifyFrame, text="สถานะ", fg="black", bg="white", font="verdana 25").grid(row=3, column=0, sticky='e')
            OptionMenu(modifyFrame, perSpy, *perList).grid(row=3, column=1, sticky='w')

            Button(modifyFrame, text="แก้ไขบัญชีผู้ใช้", fg="black", bg="yellow", font="verdana 25 bold", command=ModifyAccout).grid(row=4, columnspan=2)


    def deleteAccoutClicked():
        if accountTree.focus() == "":
            messagebox.showerror("Admin:", "กรุณาเลือกบัญชีที่ต้องการจะลบ")
        else:
            msg = messagebox.askquestion("Delete", "ต้องการจะลบผู้ใช้นี้หรือไม่", icon="warning")
            if msg == "yes":
                selectedAcc = accountTree.item(accountTree.focus(), "values")
                selectedAcc_id= selectedAcc[0]
                sql = '''DELETE FROM LoginTable
                            WHERE userID = ?'''
                cursor.execute(sql, [selectedAcc_id])
                conn.commit()
                messagebox.showinfo("Admin:", "ผู้ใช้ถูกลบออกจากฐานข้อมูลเรียบร้อยแล้ว")
                fetchaccoutTree()


    def fetchaccoutTree():
        accountTree.delete(*accountTree.get_children())
        sql = "SELECT * FROM LoginTable"
        cursor.execute(sql)
        res = cursor.fetchall()
        if res:
            for i in range(len(res)):
                per = "ลูกจ้าง"
                if res[i][4] == 0:
                    per = "เจ้าของร้าน"
                accountTree.insert("",END, values=(res[i][0],res[i][1], res[i][3], per))

    clearInfoFrame()
    resetBtnColor()

    accountManagementBtn["fg"] = "blue"
    accountManageFrame = Frame(infoFrame, bg="white")
    accountManageFrame.rowconfigure(0, weight=1) # type: ignore
    accountManageFrame.rowconfigure(1, weight=5)
    accountManageFrame.columnconfigure(0, weight=1)
    accountManageFrame.grid(row=0, column=0, sticky="news")

    top = Frame(accountManageFrame, bg="white")
    top.rowconfigure(0, weight=1)
    top.columnconfigure(0, weight=1)
    top.grid(row=0, column=0, sticky="news")

    middle = Frame(accountManageFrame, bg="white")
    middle.rowconfigure(0, weight=1) #type: ignore

    middle.columnconfigure(0, weight=1)
    middle.grid(row=1, column=0, sticky="news")

    #header
    Label(top, text="จัดการบัญชีผู้ใช้", fg="black", bg="white", font="verdana 35 bold").grid(row=0, column=0, sticky='s')

    accountTree = ttk.Treeview(middle)
    accountTree.column("#0", width=0, stretch=NO)
    accountTree["columns"] = ("หมายเลขผู้ใช้งาน","Username", "ชื่อ", "สถานะ")

    accountTree.column("หมายเลขผู้ใช้งาน", width=100, anchor=CENTER)
    accountTree.column("Username", width=100, anchor=CENTER)
    accountTree.column("ชื่อ", width=120, anchor=CENTER)
    accountTree.column("สถานะ", width=120, anchor=CENTER)

    accountTree.heading("หมายเลขผู้ใช้งาน", text="หมายเลขผู้ใช้งาน")
    accountTree.heading("Username", text="Username")
    accountTree.heading("ชื่อ", text="ชื่อ")
    accountTree.heading("สถานะ", text="สถานะ")

    accountTree.grid(row=0, column=0)

    # Add Button
    Button(middle, text="เพิ่มบัญชี", fg="black", bg="green", command=addAccountClicked).grid(row=0, column=0, sticky='ne', padx=180, pady=170)

    # Modify Button
    Button(middle, text="แก้ไขบัญชี", fg="black", bg="yellow", command=modifyAccoutClicked).grid(row=0, column=0, sticky='se', padx=280, pady=170)

    #Delete Button
    Button(middle, text="ลบบัญชี", fg="black", bg="red", command=deleteAccoutClicked).grid(row=0, column=0, sticky='se', padx=180, pady=170)
    
    fetchaccoutTree()


w = 1024
h = 720

root = CreateWindowsFrame()
ConnectToDatabase()

# Login Spies
usernameSpy = StringVar()
pwdSpy = StringVar()

LoginPage()
root.mainloop()

cursor.close()
conn.close()
