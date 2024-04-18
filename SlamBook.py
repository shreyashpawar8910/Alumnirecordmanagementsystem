import os
from tkinter import *
import time
from tkinter.filedialog import askopenfilename

import pandas as pd
from PIL import ImageTk, Image
from PIL import ImageFont, ImageDraw
from tkinter import messagebox, ttk
import sqlite3
import matplotlib.pyplot as plot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from resizeimage import resizeimage
from tkcalendar import DateEntry


class SlamBookClass:
    def __init__(self, root_window):
        self.logo_lbl = None
        self.mid_frame_login = None
        self.cur_date = None
        self.exit_btn = None
        self.header_login_frame = None
        self.midd_frame_home = None
        
        self.root = root_window
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#e6ffff")
        self.root.resizable(0, 0)

        # ===== Variables ======
        self.enter_user_name = StringVar()
        self.enter_password = StringVar()

        self.login()

            # ========= Login Frame =================

    def login(self):
        self.header_login_frame = Frame(self.root, bd=5, relief=RIDGE, bg="yellow")
        self.header_login_frame.place(x=0, y=0, height=70, relwidth=1)

        # ===== Title =========
        title_lbl = Label(self.header_login_frame, text="YASHWANTRAO CHAVAN MAHAVIDHYALAYA, ISLAMPUR", bd=0, relief=RIDGE,
                          font=("elephant", 20, "bold"), bg="yellow", fg="red")
        title_lbl.place(x=0, y=0, height=60, relwidth=1)

        # ===== Footer =========
        footer_home = Label(self.root, text="Developed By :-  Shreyash Pawar  ||  Avantika Patil  ||  Shridhar Lokhande  ||  Pratiksha Mali",
                            font=("times new roman", 19, "bold"), bd=5, relief=RIDGE,
                            bg="#e600e6", fg="white")
        footer_home.place(x=0, y=650, height=50, relwidth=1)

        # ====== Date and Time=====
        self.cur_date = Label(self.header_login_frame, text="Date : dd/mm/yy\nTime : h:m:s p",
                              font=("times new roman", 12, "bold"), fg="purple", bg="yellow")
        self.cur_date.place(x=10, y=10)

        # ====== Exit Button ========
        self.exit_btn = Button(self.header_login_frame, text="Exit", font=("times new roman", 16, "bold"), bg="#e600e6",
                               command=self.exit_app, cursor="hand2")
        self.exit_btn.place(x=1200, y=10, height=40, width=135)

        # ====== Middle Frame =====
        self.mid_frame_login = Frame(self.root, bd=3, relief=GROOVE, bg="#e6ffff")
        self.mid_frame_login.place(x=0, y=70, height=580, relwidth=1)

        # ===== image Fream======
        img_frame = Frame(self.mid_frame_login, bd=3, relief=GROOVE, bg="white")
        img_frame.place(x=100, y=50, width=750, height=480)
        self.login_img = Image.open("Images//WhatsApp Image 2022-11-13 at 3.51.25 PM.jpeg")
        self.login_img = self.login_img.resize((750, 470), Image.ANTIALIAS)
        self.login_img = ImageTk.PhotoImage(self.login_img)
        self.login_img_lbl = Label(img_frame, image=self.login_img, bd=0)
        self.login_img_lbl.place(x=0, y=0)

        # ======Login  fream======
        login_frame = Frame(self.mid_frame_login, bd=3, relief=GROOVE, bg="white")
        login_frame.place(x=846, y=50, width=400, height=480)
        self.logo_img = Image.open("Images//Attendance.png")
        self.logo_img = self.logo_img.resize((150, 150), Image.ANTIALIAS)
        self.logo_img = ImageTk.PhotoImage(self.logo_img)
        self.logo_img_lbl = Label(login_frame, image=self.logo_img, bd=0)
        self.logo_img_lbl.place(x=130, y=40)

        self.user_img = Image.open("Images//login 02.png")
        self.user_img = self.user_img.resize((40, 40), Image.ANTIALIAS)
        self.user_img = ImageTk.PhotoImage(self.user_img)
        self.user_img_lbl = Label(login_frame, image=self.user_img, bd=0)
        self.user_img_lbl.place(x=50, y=233)
        self.user_txt = Entry(login_frame, font=("times new roman", 15), bg="light yellow",
                              textvariable=self.enter_user_name)
        self.user_txt.place(x=110, y=240, width=220, height=30)

        self.pass_img = Image.open("Images//Login 03.png")
        self.pass_img = self.pass_img.resize((40, 40), Image.ANTIALIAS)
        self.pass_img = ImageTk.PhotoImage(self.pass_img)
        self.pass_img_lbl = Label(login_frame, image=self.pass_img, bd=0)
        self.pass_img_lbl.place(x=50, y=293)
        self.pass_txt = Entry(login_frame, font=("times new roman", 15), bg="light yellow",
                              textvariable=self.enter_password, show="*")
        self.pass_txt.place(x=110, y=300, width=220, height=30)

        login_btn = Button(login_frame, text="LOGIN", bg="light blue", fg="black", font=("timer new roman", 15, "bold"),
                           cursor="hand2", command=self.login_fn)
        login_btn.place(x=135, y=380, width=120, height=40)

        self.update_clock()

    def login_fn(self):
        conn = sqlite3.connect(database=r'slambook.db')
        cur = conn.cursor()
        try:
            if self.enter_user_name.get() == "" or self.enter_password.get() == "":
                messagebox.showerror("Error", "All Fields are Required ", parent=self.root)
            else:
                cur.execute("SELECT * FROM user WHERE user_Name=? and password=?",
                            (self.enter_user_name.get(), self.enter_password.get()))
                user = cur.fetchone()
                if user is None:
                    messagebox.showerror("Error", "Invalid Username or Password", parent=self.root)
                    self.enter_user_name.set("")
                    self.enter_password.set("")
                else:
                    if user[5] == "Admin":
                        conn.commit()
                        name = user[1]
                        role = user[5]
                        time_now = time.strftime("%I:%M:%S %p")
                        date_today = time.strftime("%d/%m/%Y")
                        cur.execute(
                            "INSERT INTO last_log(name, user_Name, role, in_time, out_time, date) VALUES(?,?,?,?,?,?)",
                            (name, self.enter_user_name.get(), role, time_now, "", date_today))
                        conn.commit()
                        messagebox.showinfo("Welcome", f"Welcome {self.enter_user_name.get()}", parent=self.root)
                        # self.root.destroy()
                        # os.system("python home_page.py")
                        self.header_login_frame.place_forget()
                        self.mid_frame_login.place_forget()
                        self.home_page()
                    else:
                        conn.commit()
                        name = user[1]
                        role = user[5]
                        time_now = time.strftime("%I:%M:%S %p")
                        date_today = time.strftime("%d/%m/%Y")
                        cur.execute(
                            "INSERT INTO last_log(name, user_Name, role, in_time, out_time, date) VALUES(?,?,?,?,?,?)",
                            (name, self.enter_user_name.get(), role, time_now, "", date_today))
                        conn.commit()
                        messagebox.showinfo("Welcome", f"Welcome {self.enter_user_name.get()}", parent=self.root)
                        # self.root.destroy()
                        # os.system("python home_page.py")
                        self.header_login_frame.place_forget()
                        self.mid_frame_login.place_forget()
                        self.home_page()

        except EXCEPTION as error:
            messagebox.showerror("Error", f"Error due to{error}")
        conn.close()

    def update_clock(self):
        cur_date = time.strftime("%d/%m/%Y")
        cur_time = time.strftime("%I:%M:%S %p")
        self.cur_date.config(text=f"Date : {cur_date}\nTime : {cur_time}")
        self.cur_date.after(50, self.update_clock)

    def exit_app(self):
        confirm = messagebox.askyesno("Exit", "Do You Want to Exit ? ", parent=self.root)
        if confirm is True:
            self.root.destroy()
    
    def home_page(self):
         # ===== Header =====
        self.header_home_frame = Frame(self.root, bd=5, relief=RIDGE, bg="yellow")
        self.header_home_frame.place(x=0, y=0, height=70, relwidth=1)

        header_home = Label(self.header_home_frame, text="YASHWANTRAO CHAVAN MAHAVIDLAYA, ISLAMPUR",
                            font=("elephant", 20, "bold"), fg="red", bd=0, bg="yellow")
        header_home.place(x=0, y=10, height=30, relwidth=1)

        welcome_lbl = Label(self.header_home_frame, font=("times new roman", 13, "bold"), text="Welcome: ", bd=0,
                            bg="yellow")
        welcome_lbl.place(x=20, y=38)

        self.welcome_lbl = Label(self.header_home_frame, font=("times new roman", 13), text="", bd=0,
                                 bg="yellow")
        self.welcome_lbl.place(x=100, y=38)

        # ====== Date and Time=====
        self.cur_date_home = Label(self.header_home_frame, text="Date : dd/mm/yy   Time : h:m:s p",
                                   font=("times new roman", 12, "bold"), bg="yellow")
        self.cur_date_home.place(x=1050, y=38, height=20)

        # ====== Footer ======

        footer_home = Label(self.root, text="Developed By :-  Shreyash Pawar  ||  Avantika Patil  ||  Shridhar Lokhande  ||  Pratiksha Mali",
                            font=("times new roman", 19, "bold"), bd=5, relief=RIDGE,
                            bg="#e600e6", fg="white")
        footer_home.place(x=0, y=650, height=50, relwidth=1)

        # ====== btn frame ======

        btn_frame_home = Frame(self.root, bd=3, relief=RIDGE, bg="#e6ffff")
        btn_frame_home.place(x=0, y=70, height=580, width=200)

        # ======= menu buttons =======

        # ====== add users Button =======

        self.add_users_btn_data_home = Button(btn_frame_home, text="Manage User", font=("book antiqua", 15, "bold"),
                                              bd=3, relief=GROOVE, bg="#80ff80", state=DISABLED,
                                              command=self.manage_user, cursor="hand2")
        self.add_users_btn_data_home.place(x=8, y=8, height=35, width=180)

        # ====== Image ===========
        self.logo_lbl = Label(btn_frame_home, bd=2, relief=GROOVE, bg="white")
        self.logo_lbl.place(x=8, y=50, height=246, width=180)
        self.logo_img = Image.open(f"Images\\Home_logo.png")
        self.logo_img = self.logo_img.resize((180, 246), Image.ANTIALIAS)
        self.logo_img = ImageTk.PhotoImage(self.logo_img)
        self.logo_lbl.config(image=self.logo_img)

        # ===== Home ======
        home_btn_data_home = Button(btn_frame_home, text="HOME", font=("book antiqua", 15, "bold"), bd=3, fg="white",
                                    relief=GROOVE, bg="#ff8533", cursor="hand2", command=self.home_midd_frame)
        home_btn_data_home.place(x=8, y=305, height=35, width=180)

        # ====== Add record Button =======
        add_record_btn_data_home = Button(btn_frame_home, text="Add Records", font=("book antiqua", 15, "bold"), bd=3,
                                          relief=GROOVE, bg="#80ff80", command=self.add_student, cursor="hand2")
        add_record_btn_data_home.place(x=8, y=350, height=35, width=180)

        # ====== Search Button =======
        search_btn_data_home = Button(btn_frame_home, text="Search", font=("book antiqua", 15, "bold"), bd=3,
                                      relief=GROOVE, bg="#ffbb33", command= self.search_alumni,cursor="hand2")
        search_btn_data_home.place(x=8, y=395, height=35, width=180)

        # ====== Reports Button =======
        report_btn_data_home = Button(btn_frame_home, text="Reports", font=("book antiqua", 15, "bold"),
                                      bd=3, relief=GROOVE, bg="#66ccff", command=self.generate_report, cursor="hand2")
        report_btn_data_home.place(x=8, y=440, height=35, width=180)

        # ====== Logout Button =======
        logout_btn_data_home = Button(btn_frame_home, text="Logout", font=("book antiqua", 15, "bold"),
                                      bd=3, relief=GROOVE, bg="#ff66cc", command=self.logout_home, cursor="hand2")
        logout_btn_data_home.place(x=8, y=485, height=35, width=180)

        # ====== Exit Button =======
        Exit_btn_data_home = Button(btn_frame_home, text="Exit", font=("book antiqua", 15, "bold"), bd=3, fg="white",
                                    relief=GROOVE, bg="#ff3333", command=self.exit_home, cursor="hand2")
        Exit_btn_data_home.place(x=8, y=530, height=35, width=180)

        # ====== Middle frame ======
        self.midd_frame_home = Frame(self.root, bd=3, relief=RIDGE, bg="#e6ffff")
        self.midd_frame_home.place(x=200, y=70, height=580, width=1150)

        # ==== project name Heading =====
        project_nm_lbl = Label(self.midd_frame_home, text="SlamBook  Record  Management  System",
                               font=("book antiqua", 20, "bold"), bg="#99ccff", bd=3, relief=GROOVE)
        project_nm_lbl.place(x=10, y=10, height=55, width=1125)

        # =================== Middle Content =================
        pie_frame = Frame(self.midd_frame_home, bd=2, relief=GROOVE, bg="white")
        pie_frame.place(x=30, y=95, width=606, height=450)

        self.pie_image_lbl = Label(pie_frame, bd=2, relief=GROOVE, bg="white")
        self.pie_image_lbl.place(x=0, y=0, width=602, height=415)

        title_lbl = Label(pie_frame, text="Alumni-Current Status", bd=0, relief=GROOVE, justify=CENTER, bg="light pink",
                          font=("book antiqua", 15, "bold"))
        title_lbl.place(x=0, y=416, relwidth=1, height=28)

        total_users_frame = Frame(self.midd_frame_home, bd=2, relief=GROOVE, bg="white")
        total_users_frame.place(x=670, y=95, width=210, height=200)
        total_user_lbl = Label(total_users_frame, text="Total Users", bd=2, relief=GROOVE, bg="purple",
                               font=("book antiqua", 15, "bold"), fg="white")
        total_user_lbl.place(x=0, y=0, relwidth=1, height=40)
        self.total_user_lbl = Label(total_users_frame, text="0\nHas Access", bd=2, relief=GROOVE, bg="light yellow",
                                    justify=CENTER, font=("book antiqua", 15, "bold"))
        self.total_user_lbl.place(x=0, y=40, relwidth=1, height=156)

        total_alumni_frame = Frame(self.midd_frame_home, bd=2, relief=GROOVE, bg="white")
        total_alumni_frame.place(x=910, y=95, width=210, height=200)
        total_alumni_lbl = Label(total_alumni_frame, text="Total Alumni", bd=2, relief=GROOVE, bg="purple",
                                 font=("book antiqua", 15, "bold"), fg="white")
        total_alumni_lbl.place(x=0, y=0, relwidth=1, height=40)
        self.total_alumni_lbl = Label(total_alumni_frame, text="0\nAre Registered", bd=2, relief=GROOVE,
                                      bg="light yellow", justify=CENTER, font=("book antiqua", 15, "bold"))
        self.total_alumni_lbl.place(x=0, y=40, relwidth=1, height=156)

        last_log_user_frame = Frame(self.midd_frame_home, bd=2, relief=GROOVE, bg="white")
        last_log_user_frame.place(x=670, y=330, width=450, height=215)
        last_log_text_lbl = Label(last_log_user_frame, text="Last Login", bd=2, relief=GROOVE, bg="purple",
                                  font=("book antiqua", 15, "bold"), fg="white")
        last_log_text_lbl.place(x=0, y=0, relwidth=1, height=40)
        self.last_log_text_lbl = Label(last_log_user_frame, bd=2, relief=GROOVE, bg="light yellow", justify=CENTER,
                                       text="Username:\n"
                                            "Name:\n"
                                            "Role:\n"
                                            "In Time:\n"
                                            "Date:",
                                       font=("book antiqua", 15, "bold"))
        self.last_log_text_lbl.place(x=0, y=40, relwidth=1, height=171)

        self.check_user()
        self.update_clock_home()

    def update_clock_home(self):
        cur_date = time.strftime("%d/%m/%Y")
        cur_time = time.strftime("%I:%M:%S %p")
        self.cur_date_home.config(text=f"Date : {cur_date}   Time : {cur_time}")
        self.cur_date_home.after(50, self.update_clock_home)

    def home_midd_frame(self):
        self.midd_frame_home = Frame(self.root, bd=3, relief=RIDGE, bg="#e6ffff")
        self.midd_frame_home.place(x=200, y=70, height=580, width=1150)

        # ==== project name Heading =====
        project_nm_lbl = Label(self.midd_frame_home, text="SlamBook  Record  Management  System",
                               font=("book antiqua", 20, "bold"), bg="#99ccff", bd=3, relief=GROOVE)
        project_nm_lbl.place(x=10, y=10, height=55, width=1125)

        # =================== Middle Content =================
        pie_frame = Frame(self.midd_frame_home, bd=2, relief=GROOVE, bg="white")
        pie_frame.place(x=30, y=95, width=606, height=450)

        self.pie_image_lbl = Label(pie_frame, bd=2, relief=GROOVE, bg="white")
        self.pie_image_lbl.place(x=0, y=0, width=602, height=415)

        title_lbl = Label(pie_frame, text="Alumni-Current Status", bd=0, relief=GROOVE, justify=CENTER, bg="light pink",
                          font=("book antiqua", 15, "bold"))
        title_lbl.place(x=0, y=416, relwidth=1, height=28)

        total_users_frame = Frame(self.midd_frame_home, bd=2, relief=GROOVE, bg="white")
        total_users_frame.place(x=670, y=95, width=210, height=200)
        total_user_lbl = Label(total_users_frame, text="Total Users", bd=2, relief=GROOVE, bg="purple",
                               font=("book antiqua", 15, "bold"), fg="white")
        total_user_lbl.place(x=0, y=0, relwidth=1, height=40)
        self.total_user_lbl = Label(total_users_frame, text="0\nHas Access", bd=2, relief=GROOVE, bg="light yellow",
                                    justify=CENTER, font=("book antiqua", 15, "bold"))
        self.total_user_lbl.place(x=0, y=40, relwidth=1, height=156)

        total_alumni_frame = Frame(self.midd_frame_home, bd=2, relief=GROOVE, bg="white")
        total_alumni_frame.place(x=910, y=95, width=210, height=200)
        total_alumni_lbl = Label(total_alumni_frame, text="Total Alumni", bd=2, relief=GROOVE, bg="purple",
                                 font=("book antiqua", 15, "bold"), fg="white")
        total_alumni_lbl.place(x=0, y=0, relwidth=1, height=40)
        self.total_alumni_lbl = Label(total_alumni_frame, text="0\nAre Registered", bd=2, relief=GROOVE,
                                      bg="light yellow", justify=CENTER, font=("book antiqua", 15, "bold"))
        self.total_alumni_lbl.place(x=0, y=40, relwidth=1, height=156)

        last_log_user_frame = Frame(self.midd_frame_home, bd=2, relief=GROOVE, bg="white")
        last_log_user_frame.place(x=670, y=330, width=450, height=215)
        last_log_text_lbl = Label(last_log_user_frame, text="Last Login", bd=2, relief=GROOVE, bg="purple",
                                  font=("book antiqua", 15, "bold"), fg="white")
        last_log_text_lbl.place(x=0, y=0, relwidth=1, height=40)
        self.last_log_text_lbl = Label(last_log_user_frame, bd=2, relief=GROOVE, bg="light yellow", justify=CENTER,
                                       text="Username:\n"
                                            "Name:\n"
                                            "Role:\n"
                                            "In Time:\n"
                                            "Date:",
                                       font=("book antiqua", 15, "bold"))
        self.last_log_text_lbl.place(x=0, y=40, relwidth=1, height=171)

        self.check_user()
        self.update_clock_home()

    def draw_pie(self):
        con = sqlite3.connect(database='slambook.db')
        cur = con.cursor()
        try:
            cur.execute("select count(name) from alumni where curr_status='Post Graduation'")
            post_grad = cur.fetchone()[0]
            con.commit()

            cur.execute("select count(name) from alumni where curr_status='Education'")
            Education = cur.fetchone()[0]
            con.commit()

            cur.execute("select count(name) from alumni where curr_status='Business Man'")
            business_man = cur.fetchone()[0]
            con.commit()

            cur.execute("select count(name) from alumni where curr_status='Job'")
            job = cur.fetchone()[0]
            con.commit()

            cur.execute("select count(name) from alumni where curr_status='Self Employed'")
            self_employed = cur.fetchone()[0]
            con.commit()

            cur.execute("select count(name) from alumni where curr_status='Other'")
            other = cur.fetchone()[0]
            con.commit()

            fig = plot.figure(figsize=(5, 5), dpi=115)
            fig.set_size_inches(5, 3.5)

            lbl = ['Post Graduation', 'Education', 'Business Man', 'Job', 'Self Employed', 'Other']
            data = [post_grad, Education, business_man, job, self_employed, other]

            plot.style.use("ggplot")
            plot.pie(data, labels=lbl, radius=1.2, autopct="%1.01f%%", shadow=True, explode=[.05, .2, .05, .2, .05, .2],
                     startangle=60)
            plot.axis('equal')
            plot.savefig("Images\\pie.png", dpi=200, bbox_inches='tight')

            canvas = FigureCanvasTkAgg(fig, self.pie_image_lbl)
            canvas.draw()
            canvas.get_tk_widget().place(x=300, y=210, anchor=CENTER)

            con.commit()
            con.close()

        except EXCEPTION as error:
            messagebox.showerror("Error", f"Error due to {error}", parent=self.root)

    def check_user(self):
        conn = sqlite3.connect(database='slambook.db')
        cur = conn.cursor()
        try:
            self.draw_pie()

            cur.execute("select count(*) from user")
            total_users = cur.fetchone()[0]
            conn.commit()
            self.total_user_lbl.config(text=f"{total_users}\nHas Access")

            cur.execute("select count(name) from alumni")
            total_alumni = cur.fetchone()[0]
            conn.commit()
            self.total_alumni_lbl.config(text=f"{total_alumni}\nAre Registered")

            cur.execute("select user_name, name, role, in_time, date from last_log")
            last_log = cur.fetchall()[-2]
            conn.commit()
            self.last_log_text_lbl.config(text=f"Username: {last_log[0]}\nName: {last_log[1]}\nRole: {last_log[2]}\n"
                                               f"In Time: {last_log[3]}\nDate: {last_log[4]}")

            cur.execute("SELECT * FROM last_log")
            user_data = cur.fetchall()[-1]
            conn.commit()
            conn.close()
            if user_data[3] == "Admin":
                self.welcome_lbl.config(text=f"{user_data[1]}")
                self.add_users_btn_data_home.config(state=NORMAL)
            else:
                self.welcome_lbl.config(text=f"{user_data[1]}")
                self.add_users_btn_data_home.config(state=DISABLED)
        except EXCEPTION as error:
            messagebox.showerror("Error", f"Error due to {error}", parent=self.root)

        # ============== Logout Button on Home page =============

    def logout_home(self):
        self.header_home_frame.place_forget()
        self.midd_frame_home.place_forget()
        self.login()
        self.enter_user_name.set("")
        self.enter_password.set("")

        time_now = time.strftime("%I:%M:%S %p")
        conn = sqlite3.connect(database='slambook.db')
        cur = conn.cursor()

        cur.execute("select id from last_log")
        user_id = cur.fetchall()[-1][0]
        conn.commit()

        cur.execute("update last_log set out_time=? where id=?", (time_now, user_id))
        conn.commit()
        conn.close()

        # ============== Exit Button on Home page =============

    def exit_home(self):
        permission = messagebox.askyesno("Exit", "Do you want to exit ?", parent=self.root)
        if permission is True:
            self.root.destroy()

            time_now = time.strftime("%I:%M:%S %p")
            conn = sqlite3.connect(database='slambook.db')
            cur = conn.cursor()

            cur.execute("select id from last_log")
            user_id = cur.fetchall()[-1][0]
            conn.commit()

            cur.execute("update last_log set out_time=? where id=?", (time_now, user_id))
            conn.commit()
            conn.close()

                # ============== Add Student =============

    def add_student(self):
        self.midd_frame_home.place_forget()

        # ======= Variables =======
        self.data_reg_id = StringVar()
        self.data_name = StringVar()
        self.data_gender = StringVar()
        self.data_date_of_birth = StringVar()
        self.data_city = StringVar()
        self.data_taluka = StringVar()
        self.data_dist = StringVar()
        self.data_department = StringVar()
        self.data_pass_out = StringVar()
        self.data_contact = StringVar()
        self.data_parent_cont = StringVar()
        self.data_email = StringVar()
        self.data_project = StringVar()
        self.data_current = StringVar()
        self.data_extra_info = StringVar()
        self.data_feedback = StringVar()
        self.search_entry_by = StringVar()
        self.search_entry_txt = StringVar()
        self.data_upload_image = []

        # ====== Middle frame ======
        self.midd_frame_data_ent = Frame(self.root, bd=3, relief=RIDGE, bg="#e6ffff")
        self.midd_frame_data_ent.place(x=200, y=70, height=580, width=1150)

        # ===== Title label =====
        title_lbl_register = Label(self.midd_frame_data_ent, text="Alumni Register", font=("book antiqua", 18, "bold"),
                                   bd=0, relief=GROOVE, bg="blue", fg="white")
        title_lbl_register.place(x=0, y=0, height=35, relwidth=1)

        # ======== Database Table View Frame ========
        db_table_view_frame = Frame(self.midd_frame_data_ent, bd=2, relief=RIDGE, bg="white")
        db_table_view_frame.place(x=0, y=360, height=213, relwidth=1)
        scroll_x = Scrollbar(db_table_view_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(db_table_view_frame, orient=VERTICAL)
        self.database_students_view = ttk.Treeview(db_table_view_frame,
                                                   columns=("reg_id", "name", "gender", "date_of_birth", "city",
                                                            "taluka", "dist", "department", "pass_out", "contact",
                                                            "parent_cont", "email", "project", "curr_status",
                                                            "extra_info", "feedback", "last_update", "update_date",
                                                            "update_time"),
                                                   xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.database_students_view.xview)
        scroll_y.config(command=self.database_students_view.yview)

        self.database_students_view.heading("reg_id", text="Reg Id")
        self.database_students_view.heading("name", text="Name")
        self.database_students_view.heading("gender", text="Gender")
        self.database_students_view.heading("date_of_birth", text="Date of Birth")
        self.database_students_view.heading("city", text="City")
        self.database_students_view.heading("taluka", text="Taluka")
        self.database_students_view.heading("dist", text="District")
        self.database_students_view.heading("department", text="Department")
        self.database_students_view.heading("pass_out", text="Pass Out")
        self.database_students_view.heading("contact", text="Contact")
        self.database_students_view.heading("parent_cont", text="Parent cont")
        self.database_students_view.heading("email", text="Email")
        self.database_students_view.heading("project", text="Project")
        self.database_students_view.heading("curr_status", text="Current Status")
        self.database_students_view.heading("extra_info", text="Extra Info")
        self.database_students_view.heading("feedback", text="Feedback")
        self.database_students_view.heading("last_update", text="Last Updated By")
        self.database_students_view.heading("update_date", text="Updated Date")
        self.database_students_view.heading("update_time", text="Update Time")

        self.database_students_view["show"] = "headings"

        self.database_students_view.column("reg_id", width=70)
        self.database_students_view.column("name", width=170)
        self.database_students_view.column("gender", width=80)
        self.database_students_view.column("date_of_birth", width=100)
        self.database_students_view.column("city", width=100)
        self.database_students_view.column("taluka", width=100)
        self.database_students_view.column("dist", width=100)
        self.database_students_view.column("department", width=100)
        self.database_students_view.column("pass_out", width=100)
        self.database_students_view.column("contact", width=100)
        self.database_students_view.column("parent_cont", width=100)
        self.database_students_view.column("email", width=150)
        self.database_students_view.column("project", width=120)
        self.database_students_view.column("curr_status", width=100)
        self.database_students_view.column("extra_info", width=150)
        self.database_students_view.column("feedback", width=150)
        self.database_students_view.column("last_update", width=170)
        self.database_students_view.column("update_date", width=150)
        self.database_students_view.column("update_time", width=150)
        self.database_students_view.pack(fill=BOTH, expand=1)
        self.database_students_view.bind("<ButtonRelease-1>", self.data_get_data)

        # ===== Data Enter ======

        # === Registration ID lable ======
        RID_data_entry = Label(self.midd_frame_data_ent, text="Reg ID", font=("book antiqua", 13, "bold"), bg="#e6ffff",
                               fg="black")
        RID_data_entry.place(x=10, y=50)

        # === Registration ID Text Field
        RID_txt = Entry(self.midd_frame_data_ent, font=("book antiqua", 13), textvariable=self.data_reg_id)
        RID_txt.place(x=170, y=50, height=25, width=200)

        # === Name lable
        name_data_entry = Label(self.midd_frame_data_ent, text="Name", font=("book antiqua", 13, "bold"), bg="#e6ffff",
                                fg="black")
        name_data_entry.place(x=400, y=50)

        # === Name Text Field
        name_data_text = Entry(self.midd_frame_data_ent, font=("book antiqua", 13), textvariable=self.data_name)
        name_data_text.place(x=550, y=50, height=25, width=200)

        # ==== Gender Lable =====
        gender_data_entry = Label(self.midd_frame_data_ent, text="Gender", font=("book antiqua", 13, "bold"), bg="#e6ffff",
                                  fg="black")
        gender_data_entry.place(x=780, y=50)

        # ===== Gender Text Field =====
        gender_data_cmb = ttk.Combobox(self.midd_frame_data_ent, values=("Select", "Male", "Female", "Other"),
                                       font=("book antiqua", 13),
                                       state='readonly', textvariable=self.data_gender, justify=CENTER)
        gender_data_cmb.place(x=930, y=50, height=28, width=200)
        gender_data_cmb.current(0)

        # ====== Date of Birth ======
        date_of_birth_lbl = Label(self.midd_frame_data_ent, text="Date Of Birth", font=("book antiqua", 13, "bold"),
                                  bg="#e6ffff", fg="black")
        date_of_birth_lbl.place(x=10, y=95)

        # ===== Date of Birth ======
        date_of_birth_text = DateEntry(self.midd_frame_data_ent, setmod='day', date_pattern='dd/mm/yyyy',
                                       font=("book antiqua", 13),
                                       textvariable=self.data_date_of_birth, state='readonly', justify=CENTER)
        date_of_birth_text.place(x=170, y=95, height=25, width=200)

        # === City lable
        add_data_entry = Label(self.midd_frame_data_ent, text="City", font=("book antiqua", 13, "bold"), bg="#e6ffff",
                               fg="black")
        add_data_entry.place(x=400, y=95)

        # === Address Text Field
        city_data_text = Entry(self.midd_frame_data_ent, font=("book antiqua", 13), textvariable=self.data_city)
        city_data_text.place(x=550, y=95, width=200, height=25)

        # ===== Taluka Lable =====
        taluka_data_entry = Label(self.midd_frame_data_ent, text="Taluka", font=("book antiqua", 13, "bold"), bg="#e6ffff",
                                  fg="black")
        taluka_data_entry.place(x=780, y=95)

        taluka_data_text = Entry(self.midd_frame_data_ent, font=("book antiqua", 13), textvariable=self.data_taluka)
        taluka_data_text.place(x=930, y=95, height=25, width=200)

        # ====== District Lable ======
        dist_data_entry = Label(self.midd_frame_data_ent, text="District", font=("book antiqua", 13, "bold"), bg="#e6ffff",
                                fg="black")
        dist_data_entry.place(x=10, y=140)

        dist_data_text = Entry(self.midd_frame_data_ent, font=("book antiqua", 13), textvariable=self.data_dist)
        dist_data_text.place(x=170, y=140, height=25, width=200)

        # ====== Department ========
        department_data_entry = Label(self.midd_frame_data_ent, text="Department", font=("book antiqua", 13, "bold"),
                                      bg="#e6ffff", fg="black")
        department_data_entry.place(x=400, y=140)

        department_data_text = ttk.Combobox(self.midd_frame_data_ent, values=("Select", "BCA", "BBA"),
                                            font=("book antiqua", 13),
                                            textvariable=self.data_department, state='readonly', justify=CENTER)
        department_data_text.place(x=550, y=140, height=26, width=200)
        department_data_text.current(0)

        # === passout lable
        pass_out_data_entry = Label(self.midd_frame_data_ent, text="Pass-Out Year", font=("book antiqua", 13, "bold"),
                                    bg="#e6ffff", fg="black")
        pass_out_data_entry.place(x=780, y=140)

        # === passout Text Field
        pass_out_data_text = Entry(self.midd_frame_data_ent, font=("book antiqua", 13), textvariable=self.data_pass_out)
        pass_out_data_text.place(x=930, y=140, height=25, width=200)

        # === contact lable
        contact_entry = Label(self.midd_frame_data_ent, text="Contact", font=("book antiqua", 13, "bold"), bg="#e6ffff",
                              fg="black")
        contact_entry.place(x=10, y=185)

        # === contact Text Field
        contact_text = Entry(self.midd_frame_data_ent, font=("book antiqua", 13), textvariable=self.data_contact)
        contact_text.place(x=170, y=185, height=25, width=200)

        # === Parent's Contact lable
        parent_cont_entry = Label(self.midd_frame_data_ent, text="Parent's Contact", font=("book antiqua", 13, "bold"),
                                  bg="#e6ffff", fg="black")
        parent_cont_entry.place(x=400, y=185)

        # === Parents contact Text Field
        parent_cont_text = Entry(self.midd_frame_data_ent, font=("book antiqua", 13), textvariable=self.data_parent_cont)
        parent_cont_text.place(x=550, y=185, height=25, width=200)

        # === Email Lable
        email_data_entry = Label(self.midd_frame_data_ent, text="Email", font=("book antiqua", 13, "bold"), bg="#e6ffff",
                                 fg="black")
        email_data_entry.place(x=780, y=185)

        email_data_text = Entry(self.midd_frame_data_ent, font=("book antiqua", 13), textvariable=self.data_email)
        email_data_text.place(x=930, y=185, height=25, width=200)

        # ===== Projects ======
        project_data_entry = Label(self.midd_frame_data_ent, text="Final Year Project", font=("book antiqua", 13, "bold"),
                                   bg="#e6ffff", fg="black")
        project_data_entry.place(x=10, y=230)

        project_data_text = Entry(self.midd_frame_data_ent, font=("book antiqua", 13), textvariable=self.data_project)
        project_data_text.place(x=170, y=230, height=25, width=200)

        # ==== current status ======
        curr_status_entry = Label(self.midd_frame_data_ent, text="Current Status", font=("book antiqua", 13, "bold"),
                                  bg="#e6ffff", fg="black")
        curr_status_entry.place(x=400, y=230)
        self.curr_status_cmb = ttk.Combobox(self.midd_frame_data_ent, values=("Select", "Post Graduation", "Education",
                                                                         "Business Man", "Job", "Self Employed",
                                                                         "Other"),
                                            font=("book antiqua", 13), state='readonly', textvariable=self.data_current,
                                            justify=CENTER)
        self.curr_status_cmb.place(x=550, y=230, height=26, width=200)
        self.curr_status_cmb.current(0)

        self.curr_status_text = Entry(self.midd_frame_data_ent, font=("book antiqua", 13), textvariable=self.data_current)
        self.data_current.trace('w', self.switch_to_txt)

        # ======= Extra Information =====
        extra_info_entry = Label(self.midd_frame_data_ent, text="Extra Information", font=("book antiqua", 13, "bold"),
                                 bg="#e6ffff", fg="black")
        extra_info_entry.place(x=780, y=230)

        extra_info_text = Entry(self.midd_frame_data_ent, font=("book antiqua", 13), textvariable=self.data_extra_info)
        extra_info_text.place(x=930, y=230, height=25, width=200)

        # ===== Feedback =========
        feedback_entry = Label(self.midd_frame_data_ent, font=("book antiqua", 13, "bold"), text="Student Feedback",
                               bg="#e6ffff", fg="black")
        feedback_entry.place(x=10, y=275)

        feedback_text = Entry(self.midd_frame_data_ent, font=("book antiqua", 13), textvariable=self.data_feedback)
        feedback_text.place(x=170, y=275, height=25, width=200)

        # ===== File Upload =====
        note_upload_img_data = Label(self.midd_frame_data_ent, text="Photo size must be within 500kb in size !",
                                     bg="#e6ffff", fg="red")
        note_upload_img_data.place(x=365, y=302)
        file_upload_data_ent = Button(self.midd_frame_data_ent, bd=3, relief=RIDGE, text="Upload Image", bg="#ff3399",
                                      fg="white", font=("book antiqua", 13, "bold"), command=lambda: self.upload_img(),
                                      cursor="hand2")
        file_upload_data_ent.place(x=400, y=275, height=30, width=150)

        register_data = Button(self.midd_frame_data_ent, text="Register", bd=3, relief=RIDGE, bg="light green", fg="black",
                               font=("book antiqua", 13, "bold"), cursor="hand2", command=self.registration)
        register_data.place(x=565, y=275, height=30, width=130)

        # clear Button
        clear_data = Button(self.midd_frame_data_ent, text="Clear", bd=3, relief=RIDGE, bg="#ff6666", fg="white",
                            font=("book antiqua", 13, "bold"), cursor="hand2", command=self.clear)
        clear_data.place(x=710, y=275, height=30, width=130)

        # Update Button
        update_data_entry = Button(self.midd_frame_data_ent, text="Update", bd=3, relief=RIDGE, bg="#e066ff", fg="black",
                                   font=("book antiqua", 13, "bold"), command=self.update_record, cursor="hand2")
        update_data_entry.place(x=855, y=275, height=30, width=130)

        # Delete Button
        delete_data_entry = Button(self.midd_frame_data_ent, text="Delete", bd=3, relief=RIDGE, bg="#ff3333", fg="white",
                                   font=("book antiqua", 13, "bold"), command=self.deleat_record, cursor="hand2")
        delete_data_entry.place(x=1000, y=275, height=30, width=130)

        # ======= Search frame ======
        search_entry_frame = Frame(self.midd_frame_data_ent, bd=3, relief=RIDGE, bg="#e6ffff")
        search_entry_frame.place(x=0, y=320, height=45, relwidth=1)

        # ====== Search Dropdown list
        search_drop_search = ttk.Combobox(search_entry_frame, values=("Search By", "Reg_id", "Name", "Department",
                                                                      "Pass_out"), font=("book antiqua", 14, "bold"),
                                          state='readonly', justify=CENTER, textvariable=self.search_entry_by)
        search_drop_search.place(x=5, y=5, height=30, width=150)
        search_drop_search.current(0)

        # ======= search Entry Field ======
        search_Entry_search = Entry(search_entry_frame, font=("book antiqua", 15), bd=3, relief=GROOVE,
                                    bg="light yellow", textvariable=self.search_entry_txt)
        search_Entry_search.place(x=160, y=5, height=32, width=685)

        # ===== search Button db frame ======
        search_button_search = Button(search_entry_frame, text="Search", font=("book antiqua", 15, "bold"),
                                      bg="#ff99ff", fg="black", command=self.search_entry_data, cursor="hand2")
        search_button_search.place(x=850, y=5, height=30, width=140)

        # ====== Clear Button db frame ======
        clear_button_search = Button(search_entry_frame, text="Clear", font=("book antiqua", 15, "bold"),
                                     bg="#ff6666", fg="white", command=self.search_entry_clear, cursor="hand2")
        clear_button_search.place(x=995, y=5, height=30, width=140)

        self.show_data()

    def search_entry_data(self):
        conn = sqlite3.connect(database=r'slambook.db')
        cur = conn.cursor()
        try:
            if self.search_entry_by.get() == "Search By" or self.search_entry_txt.get() == "":
                messagebox.showerror("Error", "All Fields are required", parent=self.root)
            else:
                cur.execute(f"SELECT reg_id, name, gender, date_of_birth, city, taluka, dist, department, pass_out, "
                            f"contact, parent_cont, email, project, curr_status, extra_info, feedback from alumni "
                            f"WHERE {self.search_entry_by.get()} LIKE '%{self.search_entry_txt.get()}%'")
                row = cur.fetchall()
                conn.commit()
                if len(row) > 0:
                    self.database_students_view.delete(*self.database_students_view.get_children())
                    for data in row:
                        self.database_students_view.insert("", END, values=data)
                else:
                    messagebox.showerror("Error", "No Such Records Found", parent=self.root)

        except EXCEPTION as error:
            messagebox.showerror("Error", f"Error due to : {error}", parent=self.root)
        conn.close()

    def search_entry_clear(self):
        self.search_entry_by.set("Search By")
        self.search_entry_txt.set("")

        conn = sqlite3.connect(database=r'slambook.db')
        cur = conn.cursor()
        cur.execute(f"SELECT reg_id, name, gender, date_of_birth, city, taluka, dist, department, pass_out, "
                    f"contact, parent_cont, email, project, curr_status, extra_info, feedback from alumni")
        row = cur.fetchall()
        conn.commit()
        if len(row) > 0:
            self.database_students_view.delete(*self.database_students_view.get_children())
            for data in row:
                self.database_students_view.insert("", END, values=data)
        else:
            messagebox.showerror("Error", "No Such Records Found", parent=self.root)
        conn.close()

    def show_data(self):
        conn = sqlite3.connect(database=r'slambook.db')
        cur = conn.cursor()
        self.clear()
        try:
            cur.execute("SELECT reg_id, name, gender, date_of_birth, city, taluka, dist, department, pass_out, contact,"
                        "parent_cont, email, project, curr_status, extra_info, feedback, last_updated_by, "
                        "updated_date, updated_time from alumni")
            row = cur.fetchall()
            conn.commit()
            self.database_students_view.delete(*self.database_students_view.get_children())
            for data in row:
                self.database_students_view.insert("", END, values=data)
        except EXCEPTION as error:
            messagebox.showerror("Error", f"Error due to :{error}", parent=self.root)
        conn.close()

    def switch_to_txt(self, *args):
        try:
            if self.data_current.get() == "Other":
                self.curr_status_cmb.place_forget()
                self.curr_status_text.place(x=550, y=230, height=26, width=200)

        except EXCEPTION as error:
            messagebox.showerror("Error", f"Error due to {error}", parent=self.root)

    def upload_img(self):
        file = askopenfilename()
        self.data_upload_image.clear()
        if int(os.stat(file).st_size) <= 500000:
            with open(file, "rb") as f:
                img_data = f.read()
                self.data_upload_image.append(img_data)
        else:
            messagebox.showwarning("Warning", "Image must be less than 200kb in size", parent=self.root)

    def registration(self):
        conn = sqlite3.connect(database=r'slambook.db')
        cur = conn.cursor()
        try:
            if self.data_reg_id.get() == "" or self.data_name.get() == "" or self.data_city.get() == "" or \
                    self.data_taluka.get() == "" or self.data_dist.get() == "" or \
                    self.data_department.get() == "Select" or self.data_pass_out.get() == "" or \
                    self.data_contact.get() == "" or self.data_parent_cont.get() == "" or self.data_email.get() == "" \
                    or self.data_project.get() == "" or self.data_gender.get() == "Select":
                messagebox.showerror("Try Again", "All Field are Required", parent=self.root)

            elif len(self.data_upload_image) == 0:
                messagebox.showerror("Error", "Image is Not Selected", parent=self.root)

            else:
                cur.execute("select name from last_log")
                user = cur.fetchall()[-1][0]
                conn.commit()

                date_now = time.strftime("%d/%m/%Y")
                time_now = time.strftime("%I:%M:%S %p")

                cur.execute("select reg_id from alumni")
                user_data = cur.fetchall()
                conn.commit()
                reg_no_list = []
                reg_no_list.clear()
                for i in user_data:
                    reg_no_list.append(i[0])

                if self.data_reg_id.get() in reg_no_list:
                    messagebox.showerror("Error", f"Username already exists !\nTry different one !", parent=self.root)
                else:
                    cur.execute(
                        "INSERT INTO alumni(reg_id, name, gender, date_of_birth, city, taluka, dist, department, "
                        "pass_out, contact, parent_cont, email, project, curr_status, upload_img, extra_info, "
                        "feedback, last_updated_by, updated_date, updated_time) "
                        "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?, ?, ?, ?)",
                        (
                            self.data_reg_id.get(), self.data_name.get(), self.data_gender.get(),
                            self.data_date_of_birth.get(), self.data_city.get(), self.data_taluka.get(),
                            self.data_dist.get(), self.data_department.get(), self.data_pass_out.get(),
                            self.data_contact.get(), self.data_parent_cont.get(), self.data_email.get(),
                            self.data_project.get(), self.data_current.get(), self.data_upload_image[0],
                            self.data_extra_info.get(), self.data_feedback.get(), user, date_now, time_now))
                    self.draw_pie()
                    conn.commit()
                    messagebox.showinfo("Success", f"{self.data_name.get()} Registration Done.", parent=self.root)
                    self.clear()
                    conn.close()

        except Exception as error:
            messagebox.showerror("Error", f"Error Due to : {error}", parent=self.root)

    def update_record(self):
        conn = sqlite3.connect(database=r'slambook.db')
        cur = conn.cursor()
        try:
            if self.data_reg_id.get() == "" or self.data_name.get() == "" or self.data_city.get() == "" or \
                    self.data_taluka.get() == "" or self.data_taluka.get() == "" or self.data_dist.get() == "" or \
                    self.data_pass_out.get() == "" or self.data_contact.get() == "" or \
                    self.data_parent_cont.get() == "" or self.data_email.get() == "" or self.data_project.get() == "":
                messagebox.showerror("Try Again", "All Field are Required", parent=self.root)

            else:
                cur.execute("select name from last_log")
                user = cur.fetchall()[-1][0]
                conn.commit()

                date_now = time.strftime("%d/%m/%Y")
                time_now = time.strftime("%I:%M:%S %p")
                if len(self.data_upload_image) > 0:

                    cur.execute(
                        "UPDATE alumni set name=?, gender=?, date_of_birth=?, city=?, taluka=?, dist=?, department=?, "
                        "pass_out=?, contact=?, parent_cont=?, email=?, project=?, curr_status=?, upload_img=?, "
                        "extra_info=?, feedback=?, last_updated_by=?, updated_date=?, updated_time=? WHERE reg_id=?",
                        (self.data_name.get(), self.data_gender.get(), self.data_date_of_birth.get(),
                         self.data_city.get(), self.data_taluka.get(),
                         self.data_dist.get(), self.data_department.get(), self.data_pass_out.get(),
                         self.data_contact.get(), self.data_parent_cont.get(), self.data_email.get(),
                         self.data_project.get(), self.data_current.get(), self.data_upload_image[0],
                         self.data_extra_info.get(), self.data_feedback.get(), user, date_now, time_now,
                         self.data_reg_id.get()))
                    self.draw_pie()
                    conn.commit()
                    conn.close()
                else:
                    cur.execute(
                        "UPDATE alumni set name=?, gender=?, date_of_birth=?, city=?, taluka=?, dist=?, department=?, "
                        "pass_out=?, contact=?, parent_cont=?, email=?, project=?, "
                        " curr_status=?, extra_info=?, feedback=?, last_updated_by=?,  updated_date=?, updated_time=? "
                        " WHERE reg_id=?", (self.data_name.get(), self.data_gender.get(), self.data_date_of_birth.get(),
                         self.data_city.get(), self.data_taluka.get(), self.data_dist.get(), self.data_department.get(),
                         self.data_pass_out.get(), self.data_contact.get(), self.data_parent_cont.get(),
                         self.data_email.get(), self.data_project.get(), self.data_current.get(),
                         self.data_extra_info.get(), self.data_feedback.get(), user, date_now, time_now,
                         self.data_reg_id.get()))
                    self.draw_pie()
                    conn.commit()
                messagebox.showinfo("success", "Data has been updated successfully", parent=self.root)
                conn.close()
                self.clear()
        except Exception as error:
            messagebox.showerror("Error", f"Error due to {error}", parent=self.root)

    def deleat_record(self):
        conn = sqlite3.connect(database=r'slambook.db')
        cur = conn.cursor()
        try:
            if self.data_reg_id.get() == "" or self.data_name.get() == "" or self.data_city.get() == "" or \
                    self.data_taluka.get() == "" or self.data_dist.get() == "" or self.data_pass_out.get() == "" or \
                    self.data_contact.get() == "" or self.data_parent_cont.get() == "" or self.data_email.get() == "" \
                    or self.data_project.get() == "":
                messagebox.showerror("Try Again", "All Field are Required", parent=self.root)

            else:
                permission = messagebox.askyesno("Delete", "Do yo really want to delete ?", parent=self.root)
                if permission is True:
                    cur.execute("DELETE FROM alumni WHERE reg_id=?", (self.data_reg_id.get(),))
                    conn.commit()
                    messagebox.showinfo("Delete", "Record has been deleted successfully", parent=self.root)
                    conn.close()
                    self.clear()

        except Exception as error:
            messagebox.showerror("Error", f"Error due to {error}", parent=self.root)

    def data_get_data(self, ev):
        f = self.database_students_view.focus()
        content = (self.database_students_view.item(f))
        row = content['values']
        self.data_reg_id.set(row[0])
        self.data_name.set(row[1])
        self.data_gender.set(row[2])
        self.data_date_of_birth.set(row[3])
        self.data_city.set(row[4])
        self.data_taluka.set(row[5])
        self.data_dist.set(row[6])
        self.data_department.set(row[7])
        self.data_pass_out.set(row[8])
        self.data_contact.set(row[9])
        self.data_parent_cont.set(row[10])
        self.data_email.set(row[11])
        self.data_project.set(row[12])
        self.data_current.set(row[13])
        self.data_extra_info.set(row[14])
        self.data_feedback.set(row[15])

    def clear(self):
        date_today = time.strftime("%d/%m/%Y")
        self.data_reg_id.set("")
        self.data_name.set("")
        self.data_gender.set("Select")
        self.data_date_of_birth.set(date_today)
        self.data_city.set("")
        self.data_taluka.set("")
        self.data_dist.set("")
        self.data_department.set("Select")
        self.data_pass_out.set("")
        self.data_contact.set("")
        self.data_parent_cont.set("")
        self.data_email.set("")
        self.data_project.set("")
        self.data_current.set("Select")
        self.data_extra_info.set("")
        self.data_feedback.set("")

        self.curr_status_text.place_forget()
        self.curr_status_cmb.place(x=550, y=230, height=26, width=200)

        conn = sqlite3.connect(database=r'slambook.db')
        cur = conn.cursor()
        try:
            cur.execute(
                "SELECT reg_id, name, gender, date_of_birth, city, taluka, dist, department, pass_out, contact, "
                "parent_cont, email, project, curr_status, extra_info, feedback, last_updated_by, updated_date, updated_time from alumni")
            row = cur.fetchall()
            conn.commit()
            self.database_students_view.delete(*self.database_students_view.get_children())
            for data in row:
                self.database_students_view.insert("", END, values=data)
        except EXCEPTION as error:
            messagebox.showerror("Error", f"Error due to :{error}", parent=self.root)
        conn.close()

            # ============== Add User / Manage User =============

    def manage_user(self):

        self.midd_frame_home.place_forget()

        # variable declaration
        self.user_name = StringVar()
        self.user_email = StringVar()
        self.user_password = StringVar()
        self.user_city = StringVar()
        self.user_contact = StringVar()
        self.user_user = StringVar()
        self.user_role = StringVar()
        self.user_conf_pass = StringVar()
        self.user_search_by = StringVar()
        self.user_search_txt = StringVar()

        # .................Middle Frame...........
        self.middle_frame_user = Frame(self.root, bd=3, relief=GROOVE, bg="#e6ffff")
        self.middle_frame_user.place(x=200, y=70, height=580, width=1150)

        # ===== Title label =====
        title_lbl_register = Label(self.middle_frame_user, text="Manage Users", font=("book antiqua", 18, "bold"),
                                   bd=0, relief=GROOVE, bg="light green")
        title_lbl_register.place(x=0, y=0, height=35, relwidth=1)

        # .............To enter User information..........
        Name_label = Label(self.middle_frame_user, text="Name", font=("book antiqua", 15, "bold"), fg="black", bg="#e6ffff")
        Name_label.place(x=10, y=50)

        Name_text = Entry(self.middle_frame_user, font=("book antiqua", 15), textvariable=self.user_name)
        Name_text.place(x=160, y=50, height=30, width=350)

        City_label = Label(self.middle_frame_user, text="City", font=("book antiqua", 15, "bold"), fg="black", bg="#e6ffff")
        City_label.place(x=550, y=50)

        City_text = Entry(self.middle_frame_user, font=("book antiqua", 15), textvariable=self.user_city)
        City_text.place(x=830, y=50, height=30, width=300)

        Email_label = Label(self.middle_frame_user, text="Email ID", font=("book antiqua", 15, "bold"), fg="black", bg="#e6ffff")
        Email_label.place(x=10, y=95)

        Email_text = Entry(self.middle_frame_user, font=("book antiqua", 15), textvariable=self.user_email)
        Email_text.place(x=160, y=95, height=30, width=350)

        contact_label = Label(self.middle_frame_user, text="Contact", font=("book antiqua", 15, "bold"), fg="black", bg="#e6ffff")
        contact_label.place(x=550, y=95)

        contact_text = Entry(self.middle_frame_user, font=("book antiqua", 15), textvariable=self.user_contact)
        contact_text.place(x=830, y=95, height=30, width=300)

        Uname_label = Label(self.middle_frame_user, text="User Name", font=("book antiqua", 15, "bold"), fg="black", bg="#e6ffff")
        Uname_label.place(x=10, y=140)

        Uname_text = Entry(self.middle_frame_user, font=("book antiqua", 15), textvariable=self.user_user)
        Uname_text.place(x=160, y=140, height=30, width=350)

        Role_label = Label(self.middle_frame_user, text="Role", font=("book antiqua", 15, "bold"), fg="black", bg="#e6ffff")
        Role_label.place(x=550, y=140)

        Role_text = ttk.Combobox(self.middle_frame_user, values=("Select", "Admin", "Lab Instructor", "Teacher"), justify=CENTER,
                                 font=("book antiqua", 15), textvariable=self.user_role, state='readonly')
        Role_text.place(x=830, y=140, height=30, width=300)
        Role_text.current(0)

        password_label = Label(self.middle_frame_user, text="Password", font=("book antiqua", 15, "bold"), fg="black",
                               bg="#e6ffff")
        password_label.place(x=10, y=185)

        password_text = Entry(self.middle_frame_user, font=("book antiqua", 15), textvariable=self.user_password)
        password_text.place(x=160, y=185, height=30, width=350)

        conf_pass_label = Label(self.middle_frame_user, text="Confirm Password", font=("book antiqua", 15, "bold"), fg="black",
                                bg="#e6ffff")
        conf_pass_label.place(x=550, y=185)

        conf_pass_text = Entry(self.middle_frame_user, font=("book antiqua", 15), textvariable=self.user_conf_pass)
        conf_pass_text.place(x=830, y=185, height=30, width=300)

        save_button = Button(self.middle_frame_user, text="Save", font=("book antiqua", 15, "bold"), fg="white", bg="#ff0066",
                             command=self.user_register)
        save_button.place(x=270, y=230, height=30, width=150)

        clear_button = Button(self.middle_frame_user, text="Clear", font=("book antiqua", 15, "bold"), fg="white", bg="#0059b3",
                              command=self.clear_user)
        clear_button.place(x=425, y=230, height=30, width=150)

        update_button = Button(self.middle_frame_user, text="Update", font=("book antiqua", 15, "bold"), bg="yellow",
                               command=self.user_update)
        update_button.place(x=580, y=230, height=30, width=150)

        delete_button = Button(self.middle_frame_user, text="Delete", font=("book antiqua", 15, "bold"), fg="white", bg="red",
                               command=self.user_rec_delete)
        delete_button.place(x=735, y=230, height=30, width=150)

        # ======= Search frame ======
        search_entry_frame = Frame(self.middle_frame_user, bd=3, relief=RIDGE, bg="#e6ffff")
        search_entry_frame.place(x=0, y=275, height=45, relwidth=1)

        # ====== Search Dropdown list
        search_drop_search = ttk.Combobox(search_entry_frame, values=("Search By", "Reg_id", "Name", "Department",
                                                                      "Pass_out"), font=("book antiqua", 14, "bold"),
                                          state='readonly', justify=CENTER, textvariable=self.user_search_by)
        search_drop_search.place(x=5, y=5, height=30, width=150)
        search_drop_search.current(0)

        # ======= search Entry Field ======
        search_Entry_search = Entry(search_entry_frame, font=("book antiqua", 15), bd=3, relief=GROOVE,
                                    bg="light yellow", textvariable=self.user_search_txt)
        search_Entry_search.place(x=160, y=5, height=32, width=685)

        # ===== search Button db frame ======
        search_button_search = Button(search_entry_frame, text="Search", font=("book antiqua", 15, "bold"),
                                      bg="#ff99ff", fg="black", command=self.search_user_data, cursor="hand2")
        search_button_search.place(x=850, y=5, height=30, width=140)

        # ====== Clear Button db frame ======
        clear_button_search = Button(search_entry_frame, text="Clear", font=("book antiqua", 15, "bold"),
                                     bg="#ff6666", fg="white", command=self.search_user_clear, cursor="hand2")
        clear_button_search.place(x=995, y=5, height=30, width=140)

        # ..........Last frame.........
        last = Frame(self.middle_frame_user, bd=3, relief=RIDGE, bg="white")
        last.place(x=0, y=318, height=255, relwidth=1)
        scroll_x = Scrollbar(last, orient=HORIZONTAL)
        scroll_y = Scrollbar(last, orient=VERTICAL)
        self.dashboard_view = ttk.Treeview(last, columns=(
            "user_Name", "name", "city", "email_id", "contact", "role", "password"),
                                           xscrollcommand=scroll_x, yscrollcommand=scroll_y)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.dashboard_view.xview)
        scroll_y.config(command=self.dashboard_view.yview)

        self.dashboard_view.heading("user_Name", text="user_Name")
        self.dashboard_view.heading("name", text="Name")
        self.dashboard_view.heading("city", text="city")
        self.dashboard_view.heading("email_id", text="Email_Id")
        self.dashboard_view.heading("contact", text="contact")
        self.dashboard_view.heading("role", text="role")
        self.dashboard_view.heading("password", text="password")

        self.dashboard_view["show"] = "headings"

        self.dashboard_view.column("user_Name", width=150)
        self.dashboard_view.column("name", width=200)
        self.dashboard_view.column("city", width=150)
        self.dashboard_view.column("email_id", width=250)
        self.dashboard_view.column("contact", width=150)
        self.dashboard_view.column("role", width=150)
        self.dashboard_view.column("password", width=150)

        self.dashboard_view.pack(fill=BOTH, expand=1)
        self.dashboard_view.bind("<ButtonRelease-1>", self.user_get_data)

        self.show_user_data()

    def search_user_data(self):
        conn = sqlite3.connect(database=r'slambook.db')
        cur = conn.cursor()
        try:
            if self.user_search_by.get() == "Search By" or self.user_search_txt.get() == "":
                messagebox.showerror("Error", "All Fields are required", parent=self.root)
            else:
                cur.execute(f"SELECT user_name, name, city, email_id, contact, role, password from user "
                            f"WHERE {self.user_search_by.get()} LIKE '%{self.user_search_txt.get()}%'")
                row = cur.fetchall()
                conn.commit()
                conn.close()
                if len(row) > 0:
                    self.dashboard_view.delete(*self.dashboard_view.get_children())
                    for data in row:
                        self.dashboard_view.insert("", END, values=data)
                else:
                    messagebox.showerror("Error", "No Such Records Found", parent=self.root)

        except EXCEPTION as error:
            messagebox.showerror("Error", f"Error due to : {error}", parent=self.root)

    def search_user_clear(self):
        self.user_search_by.set("Search By")
        self.user_search_txt.set("")

        conn = sqlite3.connect(database=r'slambook.db')
        cur = conn.cursor()
        cur.execute(f"SELECT user_name, name, city, email_id, contact, role, password from user")
        row = cur.fetchall()
        conn.commit()
        if len(row) > 0:
            self.dashboard_view.delete(*self.dashboard_view.get_children())
            for data in row:
                self.dashboard_view.insert("", END, values=data)
        else:
            messagebox.showerror("Error", "No Such Records Found", parent=self.root)

        conn.close()

    def user_register(self):
        conn = sqlite3.connect(r'slambook.db')
        cur = conn.cursor()
        try:
            if self.user_name.get() == "" or self.user_city.get() == "" or self.user_email.get() == "" or \
                    self.user_contact.get() == "" or self.user_user.get() == "" or self.user_role.get() == "Select" or \
                    self.user_password.get() == "" or self.user_conf_pass.get() == "":
                messagebox.showerror("TRY AGAIN", "ALL FIELDS ARE REQUIRED", parent=self.root)

            elif self.user_password.get() != self.user_conf_pass.get():
                messagebox.showerror("TRY AGAIN", "PASSWORD DOESN'T MATCHED", parent=self.root)
            else:
                cur.execute("select user_name from user")
                user_data = cur.fetchall()
                conn.commit()
                user_list = []
                user_list.clear()
                for i in user_data:
                    user_list.append(i[0])

                if self.user_user.get() in user_list:
                    messagebox.showerror("Error", f"Username already exists !\nTry different one !", parent=self.root)
                else:
                    cur.execute(
                        "INSERT INTO user(user_Name, name, city, email_id, contact, role, password, confirm_pasword) "
                        "VALUES(?,?,?,?,?,?,?,?)",
                        (self.user_user.get(), self.user_name.get(), self.user_city.get(), self.user_email.get(),
                         self.user_contact.get(), self.user_role.get(), self.user_password.get(),
                         self.user_conf_pass.get()))
                    conn.commit()
                    messagebox.showinfo("SUCCESS", f"{self.user_name.get()} REGISTRATION IS SUCCESSFUL",
                                        parent=self.root)
                    self.clear()
                    self.show_data()
        except Exception as error:
            messagebox.showerror("error", f"error due to :{error}", parent=self.root)
        conn.close()

    def user_get_data(self, ev):
        f = self.dashboard_view.focus()
        content = (self.dashboard_view.item(f))
        row = content['values']
        self.user_user.set(row[0])
        self.user_name.set(row[1])
        self.user_city.set(row[2])
        self.user_email.set(row[3])
        self.user_contact.set(row[4])
        self.user_role.set(row[5])
        self.user_password.set(row[6])

    def clear_user(self):
        self.user_user.set("")
        self.user_name.set("")
        self.user_city.set("")
        self.user_email.set("")
        self.user_contact.set("")
        self.user_role.set("")
        self.user_password.set("")
        self.user_conf_pass.set("")
        self.user_search_by.set("Search By")
        self.user_search_txt.set("")

        conn = sqlite3.connect(database=r'slambook.db')
        cur = conn.cursor()
        try:
            cur.execute("SELECT user_Name, name, city, email_id, contact, role, password from user")
            row = cur.fetchall()
            conn.commit()
            self.dashboard_view.delete(*self.dashboard_view.get_children())
            for data in row:
                self.dashboard_view.insert("", END, values=data)
        except EXCEPTION as error:
            messagebox.showerror("ERROR", f"Error due to {error}", parent=self.root)
        conn.close()

    def show_user_data(self):
        conn = sqlite3.connect(database=r'slambook.db')
        cur = conn.cursor()
        try:
            cur.execute("SELECT user_Name, name, city, email_id, contact, role, password from user")
            row = cur.fetchall()
            conn.commit()
            self.dashboard_view.delete(*self.dashboard_view.get_children())
            for data in row:
                self.dashboard_view.insert("", END, values=data)
        except EXCEPTION as error:
            messagebox.showerror("Error", f"Error due to{error}", parent=self.root)
        conn.close()

    def user_update(self):
        conn = sqlite3.connect(database=r'slambook.db')
        cur = conn.cursor()
        try:
            if self.user_user.get() == "" or self.user_name.get() == "" or self.user_city.get() == "" or \
                    self.user_email.get() == "" or self.user_contact.get() == "" or self.user_role.get() == "" or \
                    self.user_password.get() == "" or self.user_conf_pass.get() == "":
                messagebox.showerror("Error", "ALL FIELDS ARE REQUIRED !", parent=self.root)
            elif self.user_password.get() != self.user_conf_pass.get():
                messagebox.showerror("Error", "Password Does Not Matched", parent=self.root)
            else:
                cur.execute("UPDATE user set name=?,city=?,email_id=?,contact=?,role=?,password=? WHERE user_Name=?",
                            (self.user_name.get(), self.user_city.get(), self.user_email.get(), self.user_contact.get(),
                             self.user_role.get(),
                             self.user_password.get(), self.user_user.get()))
                conn.commit()
                messagebox.showinfo("Success", "YOUR UPDATE SUCCESSFULLY", parent=self.root)
                self.clear()

        except EXCEPTION as error:
            messagebox.showerror("Error", f"error due to{error}", parent=self.root)
        conn.close()

    def user_rec_delete(self):
        conn = sqlite3.connect(database=r'slambook.db')
        cur = conn.cursor()
        try:
            if self.user_user.get() == "" or self.user_name.get() == "" or self.user_city.get() == "" or \
                    self.user_email.get() == "" or self.user_contact.get() == "" or self.user_role.get() == "" or \
                    self.user_password.get() == "":
                messagebox.showerror("ERROR", "ALL FIELDS ARE REQUIRED", parent=self.root)
            else:
                permission = messagebox.askyesno("DELETE", "DO YOU REALLY WANT TO DELETE?", parent=self.root)
                if permission is True:
                    cur.execute("DELETE FROM user WHERE user_Name=?", (self.user_user.get(),))
                    conn.commit()
                    messagebox.showinfo("DELETE", "RECORD DELETED SUCCESSFULLY", parent=self.root)
                    self.clear()

        except EXCEPTION as error:
            messagebox.showerror("ERROR", f"error due to{error}", parent=self.root)
        conn.close()

        # ============== Search Alumni =============

    def search_alumni(self):

        self.midd_frame_home.place_forget()
        # ====== Variables =======
        self.search_by = StringVar()
        self.search_txt = StringVar()
        self.search_reg_id = StringVar()
        self.search_name = StringVar()
        self.search_gender = StringVar()
        self.search_date_of_birth = StringVar()
        self.search_city = StringVar()
        self.search_taluka = StringVar()
        self.search_dist = StringVar()
        self.search_department = StringVar()
        self.search_pass_out = StringVar()
        self.search_contact = StringVar()
        self.search_parent_cont = StringVar()
        self.search_email = StringVar()
        self.search_project = StringVar()
        self.search_current = StringVar()
        self.search_extra_info = StringVar()
        self.search_feedback = StringVar()

        # ====== Middle frame ======
        self.midd_frame_search = Frame(self.root, bd=3, relief=RIDGE, bg="#e6ffff")
        self.midd_frame_search.place(x=200, y=70, height=580, width=1150)
        # ===== Title label =====
        title_lbl_register = Label(self.midd_frame_search, text="Alumni Record", font=("book antiqua", 18, "bold"),
                                   bd=0, relief=GROOVE, bg="purple", fg="white")
        title_lbl_register.place(x=0, y=0, height=35, relwidth=1)

        # ======== Database table view frame ======
        db_tab_view_frame_search = Frame(self.midd_frame_search, bd=2, relief=RIDGE, bg="white")
        db_tab_view_frame_search.place(x=10, y=95, height=465, width=805)
        search_scroll_x = Scrollbar(db_tab_view_frame_search, orient=HORIZONTAL)
        search_scroll_y = Scrollbar(db_tab_view_frame_search, orient=VERTICAL)
        self.db_tab_view_frame_search = ttk.Treeview(db_tab_view_frame_search,
                                                     columns=(
                                                         "reg_id", "name", "gender", "date_of_birth", "city", "taluka",
                                                         "dist", "department", "pass_out",
                                                         "contact", "parent_cont", "email", "project", "curr_status",
                                                         "extra_info", "feedback"),
                                                     xscrollcommand=search_scroll_y.set,
                                                     yscrollcommand=search_scroll_y.set)
        search_scroll_x.pack(side=BOTTOM, fill=X)
        search_scroll_y.pack(side=RIGHT, fill=Y)
        search_scroll_x.config(command=self.db_tab_view_frame_search.xview)
        search_scroll_y.config(command=self.db_tab_view_frame_search.yview)

        self.db_tab_view_frame_search.heading("reg_id", text="reg_id")
        self.db_tab_view_frame_search.heading("name", text="Name")
        self.db_tab_view_frame_search.heading("gender", text="gender")
        self.db_tab_view_frame_search.heading("date_of_birth", text="date of birth")
        self.db_tab_view_frame_search.heading("city", text="City")
        self.db_tab_view_frame_search.heading("taluka", text="Taluka")
        self.db_tab_view_frame_search.heading("dist", text="District")
        self.db_tab_view_frame_search.heading("department", text="Department")
        self.db_tab_view_frame_search.heading("pass_out", text="Pass out")
        self.db_tab_view_frame_search.heading("contact", text="Contact")
        self.db_tab_view_frame_search.heading("parent_cont", text="Parent cont")
        self.db_tab_view_frame_search.heading("email", text="email")
        self.db_tab_view_frame_search.heading("project", text="Project")
        self.db_tab_view_frame_search.heading("curr_status", text="Current status")
        self.db_tab_view_frame_search.heading("extra_info", text="Extra info")
        self.db_tab_view_frame_search.heading("feedback", text="Feedback")

        self.db_tab_view_frame_search["show"] = "headings"

        self.db_tab_view_frame_search.column("reg_id", width=70)
        self.db_tab_view_frame_search.column("name", width=170)
        self.db_tab_view_frame_search.column("gender", width=80)
        self.db_tab_view_frame_search.column("date_of_birth", width=100)
        self.db_tab_view_frame_search.column("city", width=100)
        self.db_tab_view_frame_search.column("taluka", width=100)
        self.db_tab_view_frame_search.column("dist", width=100)
        self.db_tab_view_frame_search.column("department", width=100)
        self.db_tab_view_frame_search.column("pass_out", width=100)
        self.db_tab_view_frame_search.column("contact", width=100)
        self.db_tab_view_frame_search.column("parent_cont", width=100)
        self.db_tab_view_frame_search.column("email", width=150)
        self.db_tab_view_frame_search.column("project", width=120)
        self.db_tab_view_frame_search.column("curr_status", width=100)
        self.db_tab_view_frame_search.column("extra_info", width=150)
        self.db_tab_view_frame_search.column("feedback", width=150)

        self.db_tab_view_frame_search.pack(fill=BOTH, expand=1)
        self.db_tab_view_frame_search.bind("<ButtonRelease-1>", self.get_data_search_alumni)

        # ======= personal information print frame =======
        info_print_search = Frame(self.midd_frame_search, bd=2, relief=RIDGE, bg="white")
        info_print_search.place(x=830, y=95, height=465, width=303)

        # ====== personal information print label ======
        self.info_lbl = Label(info_print_search, bd=2, relief=GROOVE, bg="white")
        self.info_lbl.place(x=10, y=10, height=391, width=280)

        self.search_logo_img = Image.open("Images//Demo.png")
        self.search_logo_img = self.search_logo_img.resize((280, 391), Image.ANTIALIAS)
        self.search_logo_img = ImageTk.PhotoImage(self.search_logo_img)
        self.info_lbl.config(image=self.search_logo_img)

        # ======= Save Button info table =====
        save_button_search = Button(info_print_search, text="Generate", font=("book antiqua", 15, "bold"), bg="#99ff99",
                                    fg="black", command=self.search_student_display_record, cursor="hand2")
        save_button_search.place(x=10, y=413, height=35, width=135)


        # ======= Clear Button info table =====
        clear_button_search = Button(info_print_search, text="Clear", font=("book antiqua", 15, "bold"), bg="#ff6666",
                                     fg="black", command=self.clear_search_alumni, cursor="hand2")
        clear_button_search.place(x=155, y=413, height=35, width=135)


        # ======= Search frame ======
        search_entry_frame = Frame(self.midd_frame_search, bd=3, relief=RIDGE, bg="#e6ffff")
        search_entry_frame.place(x=0, y=35, height=45, relwidth=1)

        # ====== Search Dropdown list
        search_drop_search = ttk.Combobox(search_entry_frame, values=("Search By", "Reg_id", "Name", "Department",
                                                                      "Pass_out"), font=("book antiqua", 14, "bold"),
                                          state='readonly', justify=CENTER, textvariable=self.search_by)
        search_drop_search.place(x=5, y=5, height=30, width=150)
        search_drop_search.current(0)

        # ======= search Entry Field ======
        search_Entry_search = Entry(search_entry_frame, font=("book antiqua", 15), bd=3, relief=GROOVE,
                                    bg="light yellow", textvariable=self.search_txt)
        search_Entry_search.place(x=160, y=5, height=32, width=685)

        # ===== search Button db frame ======
        search_button_search = Button(search_entry_frame, text="Search", font=("book antiqua", 15, "bold"),
                                      bg="#ff99ff", fg="black", command=self.search_alumni_search, cursor="hand2")
        search_button_search.place(x=850, y=5, height=30, width=140)

        # ====== Clear Button db frame ======
        clear_button_search = Button(search_entry_frame, text="Clear", font=("book antiqua", 15, "bold"),
                                     bg="#ff6666", fg="white", command=self.search_box_clear, cursor="hand2")
        clear_button_search.place(x=995, y=5, height=30, width=140)

        self.search_show_data()

    def clear_search_alumni(self):
        self.search_reg_id.set("")
        self.search_name.set("")
        self.search_gender.set("")
        self.search_date_of_birth.set("")
        self.search_city.set("")
        self.search_taluka.set("")
        self.search_dist.set("")
        self.search_department.set("")
        self.search_pass_out.set("")
        self.search_contact.set("")
        self.search_parent_cont.set("")
        self.search_email.set("")
        self.search_project.set("")
        self.search_current.set("")
        self.search_txt.set("")
        self.search_by.set("Search By")

        conn = sqlite3.connect(database=r'slambook.db')
        cur = conn.cursor()
        cur.execute("SELECT reg_id, name, gender, date_of_birth, city, taluka, dist, department, pass_out, contact,"
                    " parent_cont, email, project, curr_status, extra_info, feedback from alumni")
        row = cur.fetchall()
        conn.commit()
        self.db_tab_view_frame_search.delete(*self.db_tab_view_frame_search.get_children())
        for data in row:
            self.db_tab_view_frame_search.insert("", END, values=data)

        self.search_logo_img = Image.open("Images//Demo.png")
        self.search_logo_img = self.search_logo_img.resize((280, 391), Image.ANTIALIAS)
        self.search_logo_img = ImageTk.PhotoImage(self.search_logo_img)
        self.info_lbl.config(image=self.search_logo_img)
        conn.close()

    def get_data_search_alumni(self, *args):
        f = self.db_tab_view_frame_search.focus()
        content = (self.db_tab_view_frame_search.item(f))
        row = content['values']
        self.search_reg_id.set(row[0])
        self.search_name.set(row[1])
        self.search_gender.set(row[2])
        self.search_date_of_birth.set(row[3])
        self.search_city.set(row[4])
        self.search_taluka.set(row[5])
        self.search_dist.set(row[6])
        self.search_department.set(row[7])
        self.search_pass_out.set(row[8])
        self.search_contact.set(row[9])
        self.search_parent_cont.set(row[10])
        self.search_email.set(row[11])
        self.search_project.set(row[12])
        self.search_current.set(row[13])

        if row[14] == "":
            self.search_extra_info.set(" ")
        else:
            self.search_extra_info.set(row[14])

        if row[15] == "":
            self.search_feedback.set("")
        else:
            self.search_feedback.set(row[15])

        curr_path = os.getcwd()
        os.chdir(f"{curr_path}\\record")
        path = os.getcwd()
        card_location = os.listdir(path)
        card = f"{row[0]}.png"
        curr_path = os.getcwd()
        os.chdir(f"{curr_path}\\..")

        if card in card_location:
            self.search_logo_img = Image.open(f"record\\{row[0]}.png")
            self.search_logo_img = self.search_logo_img.resize((280, 391), Image.ANTIALIAS)
            self.search_logo_img = ImageTk.PhotoImage(self.search_logo_img)
            self.info_lbl.config(image=self.search_logo_img)
        else:
            self.search_logo_img = Image.open(f"Images\\Demo.png")
            self.search_logo_img = self.search_logo_img.resize((280, 391), Image.ANTIALIAS)
            self.search_logo_img = ImageTk.PhotoImage(self.search_logo_img)
            self.info_lbl.config(image=self.search_logo_img)

    def search_student_display_record(self):
        try:
            curr_path = os.getcwd()
            os.chdir(f"{curr_path}\\record")
            path = os.getcwd()
            card_location = os.listdir(path)
            card = f"{self.search_reg_id}.png"
            curr_path = os.getcwd()
            os.chdir(f"{curr_path}\\..")

            if card in card_location:
                gen_again = messagebox.askyesno("Error", f"Alumni card for student id - '{self.search_reg_id.get()}' "
                                                         f"is already Present !\n Do you want to generate it again ?")
                if gen_again is True:
                    self.student_gen_record()
                else:
                    pass
            else:
                self.student_gen_record()

        except Exception as error:
            messagebox.showerror("Error", f"Error due to : {error}.")

    def student_gen_record(self):
        image = Image.new('RGB', (480, 670), (255, 255, 255))
        draw = ImageDraw.Draw(image)

        ImageFont.truetype('arial.ttf', size=45)

        (x, y) = (80, 15)
        message = str(f'ALUMNI RECORD')
        color = 'rgb(255, 0, 0)'
        font_txt = ImageFont.truetype('arial.ttf', size=40)
        draw.text((x, y), message, fill=color, font=font_txt)

        (x, y) = (25, 80)
        name = self.search_name.get()
        f_name = str(f'Name: {name}')
        color = 'rgb(0, 0, 0)'
        font_txt = ImageFont.truetype('arial.ttf', size=20)
        draw.text((x, y), f_name, fill=color, font=font_txt)

        (x, y) = (25, 120)
        id_no = self.search_reg_id.get()
        message = str(f'Reg. No.: {id_no}')
        color = 'rgb(0, 178, 50)'
        font_txt = ImageFont.truetype('arial.ttf', size=20)
        draw.text((x, y), message, fill=color, font=font_txt)

        (x, y) = (25, 160)
        department = self.search_department.get()
        department_txt = str('Department: ' + str(department))
        color = 'rgb(0, 0, 0)'
        draw.text((x, y), department_txt, fill=color, font=font_txt)

        (x, y) = (25, 200)
        gender = self.search_gender.get()
        gender_txt = str('Gender: ' + str(gender))
        color = 'rgb(0, 0, 0)'
        draw.text((x, y), gender_txt, fill=color, font=font_txt)

        (x, y) = (25, 240)
        dob = self.search_date_of_birth.get()
        dob_text = str('DOB : ' + str(dob))
        color = 'rgb(0, 0, 0)'
        draw.text((x, y), dob_text, fill=color, font=font_txt)

        (x, y) = (25, 280)
        contact = self.search_contact.get()
        contact_txt = str('Contact: ' + str(contact))
        color = 'rgb(0, 0, 0)'
        draw.text((x, y), contact_txt, fill=color, font=font_txt)

        (x, y) = (25, 320)
        par_contact = self.search_parent_cont.get()
        par_contact_txt = str('Parent Contact: ' + str(par_contact))
        color = 'rgb(0, 0, 0)'
        draw.text((x, y), par_contact_txt, fill=color, font=font_txt)

        (x, y) = (25, 360)
        email = self.search_email.get()
        email_txt = str('Email ID: ' + str(email))
        color = 'rgb(0, 0, 0)'
        draw.text((x, y), email_txt, fill=color, font=font_txt)

        (x, y) = (25, 400)
        village = self.search_city.get()
        taluka = self.search_taluka.get()
        city = self.search_dist.get()
        if len(village) >= 10:
            if len(taluka) >= 10:
                address = f"A/P: {village}, \n              Tal: {taluka},\n              Dist: {city}"
            else:
                address = f"A/P: {village}, \n              Tal: {taluka},                Dist: {city}"
        elif village.lower().find("post") != -1:
            post = village.split(": ")
            vil = post[0].split(" ")
            address = f"At: {vil[0]} Post: {post[1]}\n              Tal: {taluka},\n              Dist: {city}"
        else:
            address = f"A/P: {village}, Tal: {taluka},\n              Dist: {city}"
        address_txt = str('Address : ' + str(address))
        color = 'rgb(0, 0, 0)'
        draw.text((x, y), address_txt, fill=color, font=font_txt)

        (x, y) = (25, 460)
        project = self.search_project.get()

        if len(project) > 22:
            count_f = len(project.split(" ")[1])
            count_S = len(project.split(" ")[1])
            final_string_count = count_f + count_S + 2
            project_txt = str(
                f"Final Year Project : {project.split(' ')[0]} {project.split(' ')[1]}\n              "
                f"{project[final_string_count:]}")
            color = 'rgb(0, 0, 0)'
            draw.text((x, y), project_txt, fill=color, font=font_txt)

        else:
            project_txt = str('Final Year Project : ' + str(project))
            color = 'rgb(0, 0, 0)'
            draw.text((x, y), project_txt, fill=color, font=font_txt)

        (x, y) = (25, 520)
        current = self.search_current.get()
        current_txt = str('Current Status : ' + str(current))
        color = 'rgb(0, 0, 0)'
        draw.text((x, y), current_txt, fill=color, font=font_txt)

        (x, y) = (25, 560)
        extra = self.search_extra_info.get()
        extra_txt = str('Extra Information : ' + str(extra))
        color = 'rgb(0, 0, 0)'
        draw.text((x, y), extra_txt, fill=color, font=font_txt)

        (x, y) = (25, 600)
        feedback = self.search_feedback.get()
        feedback_txt = str('Student Feedback : ' + str(feedback))
        color = 'rgb(0, 0, 0)'
        draw.text((x, y), feedback_txt, fill=color, font=font_txt)

        image.save(f"record\\{str(id_no) + '.png'}")

        id_template = Image.open(f"record\\{str(id_no) + '.png'}")

        con = sqlite3.connect(database=r'slambook.db')
        cur = con.cursor()
        cur.execute("select upload_img from alumni where reg_id=?", (id_no,))
        database_img = cur.fetchone()[0]
        con.commit()

        with open("record\\database.png", "wb") as f:
            f.write(database_img)
            f.close()

        image = Image.open('record\\database.png')
        image = resizeimage.resize_cover(image, [150, 200])
        id_template.paste(image, (295, 115))

        id_template.save(f"record\\{str(id_no) + '.png'}")


        self.search_logo_img = Image.open(f"record\\{id_no}.png")
        self.search_logo_img = self.search_logo_img.resize((280, 391), Image.ANTIALIAS)
        self.search_logo_img = ImageTk.PhotoImage(self.search_logo_img)
        self.info_lbl.config(image=self.search_logo_img)

        save_permission = messagebox.askyesno("Save", "Do you want to save this card in files ?", parent=self.root)
        if save_permission is False:
            os.chdir(f"record")
            os.system(f"del database.png")
            os.system(f"del {id_no}.png")
            path = os.getcwd()
            os.chdir(f"{path}\\..")
        else:
            os.chdir(f"record")
            os.system(f"del database.png")
            path = os.getcwd()
            os.chdir(f"{path}\\..")
            messagebox.showinfo("Save", f"{id_no}.png card has been successfully saved in record folder.",
                                parent=self.root)
        con.close()

    def search_show_data(self):
        conn = sqlite3.connect(database=r'slambook.db')
        cur = conn.cursor()
        try:
            cur.execute("SELECT reg_id, name, gender, date_of_birth, city, taluka, dist, department, pass_out, contact,"
                        " parent_cont, email, project, curr_status, extra_info, feedback from alumni")
            row = cur.fetchall()
            conn.commit()
            self.db_tab_view_frame_search.delete(*self.db_tab_view_frame_search.get_children())
            for data in row:
                self.db_tab_view_frame_search.insert("", END, values=data)
        except EXCEPTION as error:
            messagebox.showerror("Error", f"Error due to :{error}", parent=self.root)
        conn.close()

    def search_alumni_search(self):
        conn = sqlite3.connect(database=r'slambook.db')
        cur = conn.cursor()
        try:
            if self.search_by.get() == "Search By" or self.search_txt.get() == "":
                messagebox.showerror("Error", "All Fields are required", parent=self.root)
            else:
                cur.execute(
                    f"SELECT reg_id, name, gender, date_of_birth, city, taluka, dist, department, pass_out, contact,"
                    f" parent_cont, email, project, curr_status, extra_info, feedback from alumni "
                    f"WHERE {self.search_by.get()} LIKE '%{self.search_txt.get()}%'")
                row = cur.fetchall()
                conn.commit()
                if len(row) > 0:
                    self.db_tab_view_frame_search.delete(*self.db_tab_view_frame_search.get_children())
                    for data in row:
                        self.db_tab_view_frame_search.insert("", END, values=data)
                else:
                    messagebox.showerror("Error", "No Such Records Found", parent=self.root)

        except EXCEPTION as error:
            messagebox.showerror("Error", f"Error due to : {error}", parent=self.root)
        conn.close()

    def search_box_clear(self):
        self.search_by.set("Search By")
        self.search_txt.set("")
        self.search_show_data()

        # ============== Report =============

    def generate_report(self):

        self.midd_frame_home.place_forget()

        # ===== variables ======
        self.search_by_report = StringVar()
        self.search_txt_report = StringVar()
        self.department_report = StringVar()
        self.pass_out_year_report = StringVar()
        self.cur_status_report = StringVar()
        self.sort_condition_count_report = StringVar()
        self.sort_condition_data = []

        # ====== Middle frame ======
        self.midd_frame_report = Frame(self.root, bd=3, relief=RIDGE, bg="#e6ffff")
        self.midd_frame_report.place(x=200, y=70, height=580, width=1150)

        # ===== Title label =====
        title_lbl_register = Label(self.midd_frame_report, text="Generate Reports", font=("book antiqua", 18, "bold"),
                                   bd=0, relief=GROOVE, bg="light green")
        title_lbl_register.place(x=0, y=0, height=35, relwidth=1)

        # ======= Search frame ======
        search_entry_frame = Frame(self.midd_frame_report, bd=3, relief=RIDGE, bg="#e6ffff")
        search_entry_frame.place(x=0, y=35, height=45, relwidth=1)

        # ====== Search Dropdown list
        search_drop_search = ttk.Combobox(search_entry_frame, values=("Search By", "Reg_id", "Name", "Department",
                                                                      "Pass_out"), font=("book antiqua", 14, "bold"),
                                          state='readonly', justify=CENTER, textvariable=self.search_by_report,
                                          cursor="hand2")
        search_drop_search.place(x=5, y=5, height=30, width=150)
        search_drop_search.current(0)

        # ======= search Entry Field ======
        search_Entry_search = Entry(search_entry_frame, font=("book antiqua", 15), bd=3, relief=GROOVE,
                                    bg="light yellow", textvariable=self.search_txt_report)
        search_Entry_search.place(x=160, y=5, height=32, width=685)

        # ===== search Button db frame ======
        search_button_search = Button(search_entry_frame, text="Search", font=("book antiqua", 15, "bold"),
                                      bg="#ff99ff", fg="black", command=self.search_report_result, cursor="hand2")
        search_button_search.place(x=850, y=5, height=30, width=140)

        # ====== Clear Button db frame ======
        clear_button_search = Button(search_entry_frame, text="Clear", font=("book antiqua", 15, "bold"),
                                     bg="#ff6666", fg="white", command=self.search_report_clear, cursor="hand2")
        clear_button_search.place(x=995, y=5, height=30, width=140)

        # ====== Database table view =========
        report_database_view = Frame(self.midd_frame_report, bd=3, relief=RIDGE)
        report_database_view.place(x=0, y=80, height=494, width=805)

        report_scroll_x = Scrollbar(report_database_view, orient=HORIZONTAL)
        report_scroll_y = Scrollbar(report_database_view, orient=VERTICAL)
        self.report_database_view = ttk.Treeview(report_database_view, columns=(
            "reg_id", "name", "gender", "date_of_birth", "city", "taluka",
            "dist", "department", "pass_out", "contact", "parent_cont", "email", "project", "curr_status"),
                                                 xscrollcommand=report_scroll_x.set, yscrollcommand=report_scroll_y.set)
        report_scroll_x.pack(side=BOTTOM, fill=X)
        report_scroll_y.pack(side=RIGHT, fill=Y)
        report_scroll_x.config(command=self.report_database_view.xview)
        report_scroll_y.config(command=self.report_database_view.yview)

        self.report_database_view.heading("reg_id", text="Reg. ID")
        self.report_database_view.heading("name", text="Name")
        self.report_database_view.heading("gender", text="Gender")
        self.report_database_view.heading("date_of_birth", text="Date of Birth")
        self.report_database_view.heading("city", text="City")
        self.report_database_view.heading("taluka", text="Taluka")
        self.report_database_view.heading("dist", text="District")
        self.report_database_view.heading("department", text="Department")
        self.report_database_view.heading("pass_out", text="Pass out")
        self.report_database_view.heading("contact", text="Contact")
        self.report_database_view.heading("parent_cont", text="Parent cont")
        self.report_database_view.heading("email", text="E-mail")
        self.report_database_view.heading("project", text="Project")
        self.report_database_view.heading("curr_status", text="Current status")

        self.report_database_view["show"] = "headings"

        self.report_database_view.column("reg_id", width=70)
        self.report_database_view.column("name", width=170)
        self.report_database_view.column("gender", width=80)
        self.report_database_view.column("date_of_birth", width=100)
        self.report_database_view.column("city", width=100)
        self.report_database_view.column("taluka", width=100)
        self.report_database_view.column("dist", width=100)
        self.report_database_view.column("department", width=100)
        self.report_database_view.column("pass_out", width=100)
        self.report_database_view.column("contact", width=100)
        self.report_database_view.column("parent_cont", width=100)
        self.report_database_view.column("email", width=150)
        self.report_database_view.column("project", width=120)
        self.report_database_view.column("curr_status", width=100)

        self.report_database_view.pack(fill=BOTH, expand=1)
        self.report_database_view.bind("<ButtonRelease-1>")

        # ====== Report Button frame ========
        report_button_frame = Frame(self.midd_frame_report, bd=3, relief=RIDGE)
        report_button_frame.place(x=860, y=125, height=400, width=225)

        # ====== Report label ======
        report_label = Label(report_button_frame, text="Sorting", font=("book antiqua", 20, "bold"), bd=4,
                             relief=GROOVE, bg="purple", fg="white")
        report_label.place(x=0, y=0, height=45, relwidth=1)

        # ===== Report's Combobox Department ======
        report_department_combo = ttk.Combobox(report_button_frame, values=("Department", "BCA", "BBA"), justify=CENTER,
                                               font=("book antiqua", 15, "bold"), state='readonly', cursor="hand2",
                                               textvariable=self.department_report)
        report_department_combo.place(x=10, y=60, height=30, width=200)
        report_department_combo.current(0)

        # ====== Report's combobox Batch ========
        report_batch_combo = Spinbox(report_button_frame, from_=2009, to=2100, font=("book antiqua", 15, "bold"),
                                     justify=CENTER, textvariable=self.pass_out_year_report)
        report_batch_combo.place(x=10, y=105, height=30, width=200)

        # ====== Report's combobox current status =======
        report_cur_status_combo = ttk.Combobox(report_button_frame, font=("book antiqua", 15, "bold"), justify=CENTER,
                                               values=("Select", "Post Graduation", "Education",
                                                                         "Business Man", "Job", "Self Employed",
                                                                         "Other"), state='readonly',
                                               cursor="hand2", textvariable=self.cur_status_report)
        report_cur_status_combo.place(x=10, y=150, height=30, width=200)
        report_cur_status_combo.current(0)

        # ======= Report's sort Button ========
        # ======= Separation Line ========
        horizon_line = Label(report_button_frame, bd=3, relief=GROOVE)
        horizon_line.place(x=0, y=200, relwidth=1, height=4)

        report_sort_button = Button(report_button_frame, text="Sort", font=("book antiqua", 15, "bold"), bd=2,
                                    relief=GROOVE, bg="light blue", cursor="hand2", command=self.sort_report_data)
        report_sort_button.place(x=10, y=220, height=40, width=200)

        # ======= Report's export Button ========
        report_export_button = Button(report_button_frame, text="Export", font=("book antiqua", 15, "bold"), bd=2,
                                      relief=GROOVE, bg="pink", cursor="hand2", command=self.export_report)
        report_export_button.place(x=10, y=280, height=40, width=200)

        # ======= Report's Clear Button ========
        report_clear_button = Button(report_button_frame, text="Clear", font=("book antiqua", 15, "bold"), bd=2,
                                     relief=GROOVE, bg="red", cursor="hand2", fg="white", command=self.report_clear)
        report_clear_button.place(x=10, y=340, height=40, width=200)

        self.show_data_report()

    def export_report(self):
        con = sqlite3.connect(database=r'slambook.db')
        cur = con.cursor()
        try:
            system_date = time.strftime("%d-%m-%Y")
            time_today = time.strftime("%I.%M.%S %p")

            if len(self.sort_condition_data) > 0:
                if self.sort_condition_count_report.get() == "1":
                    writer = pd.ExcelWriter(f"Reports\\Alumni Report with Department - PassOut Year - Current Status "
                                            f"'{system_date} {time_today}'.xlsx", engine="xlsxwriter")

                    df1 = pd.DataFrame(self.sort_condition_data, columns=['Reg no', 'Name', 'Gender', 'Date of Birth',
                                                                          "City", 'Taluka', 'District', 'Department',
                                                                          'Pass Out Year', 'Contact',
                                                                          "Parent's Contact", 'E-mail', 'Project',
                                                                          'Current Status', 'Extra Information',
                                                                          'Feedback'])
                    df1.to_excel(writer, sheet_name="Depart - PassOut - Curr Status", index=False)
                    writer.save()
                    messagebox.showinfo("Export", "Record has been successfully exported in 'Reports' directory.",
                                        parent=self.root)

                elif self.sort_condition_count_report.get() == "2":
                    writer = pd.ExcelWriter(f"Reports\\Alumni Report with Department - PassOut Year "
                                            f"'{system_date} {time_today}'.xlsx", engine="xlsxwriter")

                    df1 = pd.DataFrame(self.sort_condition_data, columns=['Reg no', 'Name', 'Gender', 'Date of Birth',
                                                                          "City", 'Taluka', 'District', 'Department',
                                                                          'Pass Out Year', 'Contact',
                                                                          "Parent's Contact", 'E-mail', 'Project',
                                                                          'Current Status', 'Extra Information',
                                                                          'Feedback'])
                    df1.to_excel(writer, sheet_name="Depart - PassOut", index=False)
                    writer.save()
                    messagebox.showinfo("Export", "Record has been successfully exported in 'Reports' directory.",
                                        parent=self.root)

                elif self.sort_condition_count_report.get() == "3":
                    writer = pd.ExcelWriter(f"Reports\\Alumni Report with PassOut Year - Current Status "
                                            f"'{system_date} {time_today}'.xlsx", engine="xlsxwriter")

                    df1 = pd.DataFrame(self.sort_condition_data, columns=['Reg no', 'Name', 'Gender', 'Date of Birth',
                                                                          "City", 'Taluka', 'District', 'Department',
                                                                          'Pass Out Year', 'Contact',
                                                                          "Parent's Contact", 'E-mail', 'Project',
                                                                          'Current Status', 'Extra Information',
                                                                          'Feedback'])
                    df1.to_excel(writer, sheet_name="PassOut - Current Status", index=False)
                    writer.save()
                    messagebox.showinfo("Export", "Record has been successfully exported in 'Reports' directory.",
                                        parent=self.root)

                elif self.sort_condition_count_report.get() == "4":
                    writer = pd.ExcelWriter(f"Reports\\Alumni Report with Department - Current Status "
                                            f"'{system_date} {time_today}'.xlsx", engine="xlsxwriter")

                    df1 = pd.DataFrame(self.sort_condition_data, columns=['Reg no', 'Name', 'Gender', 'Date of Birth',
                                                                          "City", 'Taluka', 'District', 'Department',
                                                                          'Pass Out Year', 'Contact',
                                                                          "Parent's Contact", 'E-mail', 'Project',
                                                                          'Current Status', 'Extra Information',
                                                                          'Feedback'])
                    df1.to_excel(writer, sheet_name="Department - Current Status", index=False)
                    writer.save()
                    messagebox.showinfo("Export", "Record has been successfully exported in 'Reports' directory.",
                                        parent=self.root)

                elif self.sort_condition_count_report.get() == "5":
                    writer = pd.ExcelWriter(f"Reports\\Alumni Report with Department "
                                            f"'{system_date} {time_today}'.xlsx", engine="xlsxwriter")

                    df1 = pd.DataFrame(self.sort_condition_data, columns=['Reg no', 'Name', 'Gender', 'Date of Birth',
                                                                          "City", 'Taluka', 'District', 'Department',
                                                                          'Pass Out Year', 'Contact',
                                                                          "Parent's Contact", 'E-mail', 'Project',
                                                                          'Current Status', 'Extra Information',
                                                                          'Feedback'])
                    df1.to_excel(writer, sheet_name="Department - Current Status", index=False)
                    writer.save()
                    messagebox.showinfo("Export", "Record has been successfully exported in 'Reports' directory.",
                                        parent=self.root)

                elif self.sort_condition_count_report.get() == "6":
                    writer = pd.ExcelWriter(f"Reports\\Alumni Report with PassOut - Year "
                                            f"'{system_date} {time_today}'.xlsx", engine="xlsxwriter")

                    df1 = pd.DataFrame(self.sort_condition_data, columns=['Reg no', 'Name', 'Gender', 'Date of Birth',
                                                                          "City", 'Taluka', 'District', 'Department',
                                                                          'Pass Out Year', 'Contact',
                                                                          "Parent's Contact", 'E-mail', 'Project',
                                                                          'Current Status', 'Extra Information',
                                                                          'Feedback'])
                    df1.to_excel(writer, sheet_name="PassOut Year", index=False)
                    writer.save()
                    messagebox.showinfo("Export", "Record has been successfully exported in 'Reports' directory.",
                                        parent=self.root)

                elif self.sort_condition_count_report.get() == "7":
                    writer = pd.ExcelWriter(f"Reports\\Alumni Report with Current Status "
                                            f"'{system_date} {time_today}'.xlsx", engine="xlsxwriter")

                    df1 = pd.DataFrame(self.sort_condition_data, columns=['Reg no', 'Name', 'Gender', 'Date of Birth',
                                                                          "City", 'Taluka', 'District', 'Department',
                                                                          'Pass Out Year', 'Contact',
                                                                          "Parent's Contact", 'E-mail', 'Project',
                                                                          'Current Status', 'Extra Information',
                                                                          'Feedback'])
                    df1.to_excel(writer, sheet_name="Current Status", index=False)
                    writer.save()
                    messagebox.showinfo("Export", "Record has been successfully exported in 'Reports' directory.",
                                        parent=self.root)

            elif self.sort_condition_count_report.get() == "0":
                cur.execute(f"select reg_id, name, gender, date_of_birth, city, taluka, dist, department, pass_out, "
                            f"contact, parent_cont, email, project, curr_status, extra_info, feedback from alumni")
                row = cur.fetchall()
                con.commit()

                for item in row:
                    self.sort_condition_data.append(item)

                writer = pd.ExcelWriter(f"Reports\\Alumni Report '{system_date} {time_today}'.xlsx",
                                        engine="xlsxwriter")

                df1 = pd.DataFrame(self.sort_condition_data, columns=['Reg no', 'Name', 'Gender', 'Date of Birth',
                                                                      "City", 'Taluka', 'District', 'Department',
                                                                      'Pass Out Year', 'Contact',
                                                                      "Parent's Contact", 'E-mail', 'Project',
                                                                      'Current Status', 'Extra Information',
                                                                      'Feedback'])
                df1.to_excel(writer, sheet_name="Alumni", index=False)
                writer.save()
                messagebox.showinfo("Export", "Record has been successfully exported in 'Reports' directory.",
                                    parent=self.root)

            else:
                messagebox.showerror("Error", "No Record found to export !", parent=self.root)

        except Exception as error:
            messagebox.showerror("Error", f"Error due to : {error}", parent=self.root)
        con.commit()
        con.close()

    def sort_report_data(self):
        conn = sqlite3.connect(database=r'slambook.db')
        cur = conn.cursor()
        try:
            if self.department_report.get() != "Department" and self.pass_out_year_report.get() != "Pass-Out Year" \
                    and self.cur_status_report.get() != "Current Status":
                self.sort_condition_count_report.set("1")
                cur.execute(f"select reg_id, name, gender, date_of_birth, city, taluka, dist, department, pass_out, "
                            f"contact, parent_cont, email, project, curr_status, extra_info, feedback from alumni "
                            f"where department='{self.department_report.get()}' AND "
                            f"pass_out='{self.pass_out_year_report.get()}' AND "
                            f"curr_status='{self.cur_status_report.get()}'")
                row = cur.fetchall()
                conn.commit()
                self.sort_condition_data.clear()
                for item in row:
                    self.sort_condition_data.append(item)

                self.report_database_view.delete(*self.report_database_view.get_children())
                for data in row:
                    self.report_database_view.insert("", END, values=data)

            elif self.department_report.get() != "Department" and self.pass_out_year_report.get() != "Pass-Out Year":
                self.sort_condition_count_report.set("2")
                cur.execute("select reg_id, name, gender, date_of_birth, city, taluka, dist, department, pass_out, "
                            "contact, parent_cont, email, project, curr_status, extra_info, feedback from alumni where "
                            "department=? and pass_out=?",
                            (self.department_report.get(), self.pass_out_year_report.get()))
                row = cur.fetchall()
                conn.commit()
                self.sort_condition_data.clear()

                for item in row:
                    self.sort_condition_data.append(item)

                self.report_database_view.delete(*self.report_database_view.get_children())
                for data in row:
                    self.report_database_view.insert("", END, values=data)

            elif self.pass_out_year_report.get() != "Pass-Out Year" and \
                    self.cur_status_report.get() != "Current Status":
                self.sort_condition_count_report.set("3")
                cur.execute("select reg_id, name, gender, date_of_birth, city, taluka, dist, department, pass_out, "
                            "contact, parent_cont, email, project, curr_status, extra_info, feedback from alumni where "
                            "pass_out=? and curr_status=?",
                            (self.pass_out_year_report.get(), self.cur_status_report.get()))
                row = cur.fetchall()
                conn.commit()
                self.sort_condition_data.clear()

                for item in row:
                    self.sort_condition_data.append(item)

                self.report_database_view.delete(*self.report_database_view.get_children())
                for data in row:
                    self.report_database_view.insert("", END, values=data)

            elif self.cur_status_report.get() != "Current Status" and self.department_report.get() != "Department":
                self.sort_condition_count_report.set("4")
                cur.execute("select reg_id, name, gender, date_of_birth, city, taluka, dist, department, pass_out, "
                            "contact, parent_cont, email, project, curr_status, extra_info, feedback from alumni where "
                            "curr_status=? and department=?",
                            (self.cur_status_report.get(), self.department_report.get()))
                row = cur.fetchall()
                conn.commit()
                self.sort_condition_data.clear()

                for item in row:
                    self.sort_condition_data.append(item)

                self.report_database_view.delete(*self.report_database_view.get_children())
                for data in row:
                    self.report_database_view.insert("", END, values=data)

            elif self.department_report.get() != "Department":
                self.sort_condition_count_report.set("5")
                cur.execute("select reg_id, name, gender, date_of_birth, city, taluka, dist, department, pass_out, "
                            "contact, parent_cont, email, project, curr_status, extra_info, feedback from alumni "
                            "where department=?", (self.department_report.get(),))
                row = cur.fetchall()
                conn.commit()
                self.sort_condition_data.clear()

                for item in row:
                    self.sort_condition_data.append(item)

                self.report_database_view.delete(*self.report_database_view.get_children())
                for data in row:
                    self.report_database_view.insert("", END, values=data)

            elif self.pass_out_year_report.get() != "Pass-Out Year":
                self.sort_condition_count_report.set("6")
                cur.execute("select reg_id, name, gender, date_of_birth, city, taluka, dist, department, pass_out, "
                            "contact, parent_cont, email, project, curr_status, extra_info, feedback from alumni "
                            "where pass_out=?", (self.pass_out_year_report.get(),))
                row = cur.fetchall()
                conn.commit()
                self.sort_condition_data.clear()

                for item in row:
                    self.sort_condition_data.append(item)

                self.report_database_view.delete(*self.report_database_view.get_children())
                for data in row:
                    self.report_database_view.insert("", END, values=data)

            elif self.cur_status_report.get() != "Current Status":
                self.sort_condition_count_report.set("7")
                cur.execute("select reg_id, name, gender, date_of_birth, city, taluka, dist, department, pass_out, "
                            "contact, parent_cont, email, project, curr_status, extra_info, feedback from alumni where "
                            "curr_status=?", (self.cur_status_report.get(),))
                row = cur.fetchall()
                conn.commit()
                self.sort_condition_data.clear()

                for item in row:
                    self.sort_condition_data.append(item)

                self.report_database_view.delete(*self.report_database_view.get_children())
                for data in row:
                    self.report_database_view.insert("", END, values=data)
            else:
                messagebox.showerror("Error", "No result found !", parent=self.root)

        except Exception as error:
            messagebox.showerror("Error", f"Error due to : {error}", parent=self.root)
        conn.close()

    def report_clear(self):
        self.search_by_report.set("Search By")
        self.search_txt_report.set("")
        self.department_report.set("Department")
        self.pass_out_year_report.set("Pass-Out Year")
        self.cur_status_report.set("Current Status")
        self.sort_condition_count_report.set("0")
        self.sort_condition_data.clear()

        conn = sqlite3.connect(database=r'slambook.db')
        cur = conn.cursor()

        cur.execute("SELECT reg_id, name, gender, date_of_birth, city, taluka, dist, department, pass_out, contact, "
                    "parent_cont, email, project, curr_status, extra_info, feedback from alumni")
        row = cur.fetchall()
        self.report_database_view.delete(*self.report_database_view.get_children())
        for data in row:
            self.report_database_view.insert("", END, values=data)
        conn.commit()
        conn.close()

    def show_data_report(self):
        conn = sqlite3.connect(database=r'slambook.db')
        cur = conn.cursor()
        self.report_clear()
        try:
            cur.execute(
                "SELECT reg_id, name, gender, date_of_birth, city, taluka, dist, department, pass_out, contact,"
                " parent_cont, email, project, curr_status, extra_info, feedback from alumni")
            row = cur.fetchall()
            self.report_database_view.delete(*self.report_database_view.get_children())
            for data in row:
                self.report_database_view.insert("", END, values=data)
        except EXCEPTION as error:
            messagebox.showerror("Error", f"Error due to :{error}", parent=self.root)
        conn.commit()
        conn.close()

    def search_report_clear(self):
        self.search_by_report.set("Search By")
        self.search_txt_report.set("")

        conn = sqlite3.connect(database=r'slambook.db')
        cur = conn.cursor()

        cur.execute("SELECT reg_id, name, gender, date_of_birth, city, taluka, dist, department, pass_out, contact, "
                    "parent_cont, email, project, curr_status, extra_info, feedback from alumni")
        row = cur.fetchall()
        conn.commit()
        self.report_database_view.delete(*self.report_database_view.get_children())
        for data in row:
            self.report_database_view.insert("", END, values=data)
        conn.close()

    def search_report_result(self):
        conn = sqlite3.connect(r"slambook.db")
        cur = conn.cursor()

        try:
            if self.search_by_report.get() == "Select" or self.search_txt_report.get() == "":
                messagebox.showerror("Error", "All fields are required ", parent=self.root)
            else:
                cur.execute(f"SELECT * from alumni WHERE {self.search_by_report.get()} LIKE "
                            f"'%{self.search_txt_report.get()}%'")
                row = cur.fetchall()
                if len(row) > 0:
                    self.report_database_view.delete(*self.report_database_view.get_children())
                    for data in row:
                        self.report_database_view.insert("", END, values=data)
                else:
                    messagebox.showerror("Error", "No Such Records Found", parent=self.root)

        except EXCEPTION as error:
            messagebox.showerror("Error", f"Error due to {error}", parent=self.root)
        conn.commit()
        conn.close()


root = Tk()
obj = SlamBookClass(root)
root.mainloop()