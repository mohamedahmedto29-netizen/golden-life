import sqlite3
import tkinter as tk
from tkinter import ttk, filedialog
from datetime import datetime
import customtkinter as ctk
import webbrowser
import tempfile
import os
import csv

# استيراد مكتبة الرسم البياني Matplotlib
import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# ==========================================
# متغيرات الألوان واللغة العامة
# ==========================================
current_mode = "dark"
current_lang = "ar"  # 'ar' أو 'en'


def get_theme_colors(mode):
    if mode == "dark":
        return {
            "BG_MAIN": "#0B132B",
            "PANEL_BG": "#1C2541",
            "TEXT_COLOR": "#FFFFFF",
            "TEXT_MUTED": "#8D99AE",
            "GOLD_ACCENT": "#E0A96D",
            "GOLD_HOVER": "#C58B43",
            "GREEN_BTN": "#2A9D8F",
            "RED_BTN": "#E63946",
            "BLUE_BTN": "#3A86FF",
            "PURPLE_BTN": "#7209B7",
            "TREE_BG": "#1C2541",
            "HEAD_BG": "#0B132B",
            "TOAST_BG": "#131B31",
            "TOAST_BORDER": "#E0A96D"
        }
    else:
        return {
            "BG_MAIN": "#F1F5F9",
            "PANEL_BG": "#FFFFFF",
            "TEXT_COLOR": "#0F172A",
            "TEXT_MUTED": "#64748B",
            "GOLD_ACCENT": "#B45309",
            "GOLD_HOVER": "#D97706",
            "GREEN_BTN": "#059669",
            "RED_BTN": "#DC2626",
            "BLUE_BTN": "#2563EB",
            "PURPLE_BTN": "#7C3AED",
            "TREE_BG": "#FFFFFF",
            "HEAD_BG": "#E2E8F0",
            "TOAST_BG": "#FFFFFF",
            "TOAST_BORDER": "#B45309"
        }


colors = get_theme_colors(current_mode)

FONT_FAMILY = "Segoe UI"
FONT_TITLE = (FONT_FAMILY, 18, "bold")
FONT_SUBTITLE = (FONT_FAMILY, 13, "bold")
FONT_BODY = (FONT_FAMILY, 11)
FONT_BTN = (FONT_FAMILY, 11, "bold")

translations = {
    "ar": {
        "sys_title": "Golden Life - نظام الإدارة المتقدم والذكي",
        "welcome": "مرحباً بك مجدداً 👋",
        "login_hint": "الرجاء إدخال بيانات حسابك للمتابعة",
        "username": "اسم المستخدم",
        "password": "كلمة المرور",
        "show_pass": "إظهار كلمة المرور 👁️",
        "login_btn": "تسجيل الدخول للنظام 🚀",
        "user_placeholder": "أدخل اسم المستخدم هنا...",
        "err_login": "اسم المستخدم أو كلمة المرور غير صحيحة!",
        "logout": "🚪 تسجيل الخروج",
        "theme_dark": "🌙 الوضع الداكن",
        "theme_light": "☀️ الوضع الفاتح"
    },
    "en": {
        "sys_title": "Golden Life - Advanced & Smart Management System",
        "welcome": "Welcome Back 👋",
        "login_hint": "Please enter your account credentials to continue",
        "username": "Username",
        "password": "Password",
        "show_pass": "Show Password 👁️",
        "login_btn": "Login to System 🚀",
        "user_placeholder": "Enter username here...",
        "err_login": "Invalid username or password!",
        "logout": "🚪 Logout",
        "theme_dark": "🌙 Dark Mode",
        "theme_light": "☀️ Light Mode"
    }
}


def t(key):
    return translations[current_lang].get(key, key)


# ==========================================
# 1. تهيئة قاعدة البيانات والجداول
# ==========================================
def init_db():
    conn = sqlite3.connect("golden_life.db")
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT,
                        role TEXT,
                        status TEXT DEFAULT 'offline',
                        last_seen TEXT
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS ac_inventory (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        item_type TEXT,
                        brand TEXT,
                        industry TEXT,
                        quantity INTEGER,
                        buy_price REAL,
                        sell_price REAL
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS ac_sales (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        client_name TEXT,
                        client_phone TEXT,
                        item_desc TEXT,
                        sale_date TEXT,
                        amount_due REAL
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS ac_maintenance (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        client_name TEXT,
                        client_phone TEXT,
                        address TEXT,
                        fault_desc TEXT,
                        maint_date TEXT
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS filter_inventory (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        item_type TEXT,
                        brand TEXT,
                        industry TEXT,
                        quantity INTEGER,
                        buy_price REAL,
                        sell_price REAL
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS filter_sales (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        client_name TEXT,
                        client_phone TEXT,
                        item_desc TEXT,
                        sale_date TEXT,
                        amount_due REAL
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS filter_maintenance (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        client_name TEXT,
                        client_phone TEXT,
                        address TEXT,
                        fault_desc TEXT,
                        maint_date TEXT
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS stock_movements (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        item_name TEXT,
                        movement_type TEXT,
                        quantity_changed INTEGER,
                        performed_by TEXT,
                        timestamp TEXT
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS tools_bags (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        bag_category TEXT,
                        bag_name TEXT,
                        tools_list TEXT
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        amount REAL,
                        status TEXT
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS customer_debts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        phone TEXT,
                        address TEXT,
                        complaint TEXT,
                        debt_amount REAL
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS suppliers (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        phone TEXT,
                        product TEXT
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS group_chat (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        sender TEXT,
                        role TEXT,
                        message TEXT,
                        timestamp TEXT
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS activity_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT,
                        action TEXT,
                        details TEXT,
                        timestamp TEXT
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS tech_shifts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        tech_name TEXT,
                        task_desc TEXT,
                        date_str TEXT
                    )''')

    cursor.execute("SELECT COUNT(*) FROM expenses")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO expenses (title, amount, status) VALUES ('فاتورة الكهرباء والماء السنوية', 12000, 'غير مدفوع')")
        cursor.execute("INSERT INTO expenses (title, amount, status) VALUES ('إيجار المعرض السنوي', 60000, 'مدفوع')")

    cursor.execute(
        "INSERT OR IGNORE INTO users (username, password, role, status) VALUES ('ahmed', '1234', 'manager', 'offline')")
    cursor.execute(
        "INSERT OR IGNORE INTO users (username, password, role, status) VALUES ('mohamed', '1234', 'manager', 'offline')")
    cursor.execute(
        "INSERT OR IGNORE INTO users (username, password, role, status) VALUES ('محمود', '1234', 'employee', 'offline')")
    cursor.execute(
        "INSERT OR IGNORE INTO users (username, password, role, status) VALUES ('إبراهيم', '1234', 'employee', 'offline')")

    conn.commit()
    conn.close()


def log_activity(username, action, details=""):
    try:
        conn = sqlite3.connect("golden_life.db")
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn.cursor().execute("INSERT INTO activity_logs (username, action, details, timestamp) VALUES (?, ?, ?, ?)",
                              (username, action, details, now))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Log error:", e)


def log_stock_movement(item_name, m_type, qty, username):
    try:
        conn = sqlite3.connect("golden_life.db")
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn.cursor().execute(
            "INSERT INTO stock_movements (item_name, movement_type, quantity_changed, performed_by, timestamp) VALUES (?, ?, ?, ?, ?)",
            (item_name, m_type, qty, username, now))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Stock log error:", e)


# ==========================================
# 2. التطبيق الرئيسي
# ==========================================
class GoldenLifeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Golden Life - نظام الإدارة المتقدم والذكي")
        self.geometry("1300x780")
        self.minsize(980, 620)

        global colors
        colors = get_theme_colors(current_mode)
        ctk.set_appearance_mode(current_mode)
        self.configure(fg_color=colors["BG_MAIN"])

        self.current_user = None
        self.current_role = None
        self.sidebar_visible = True  # متغير لإظهار/إخفاء الشريط الجانبي

        self.style_tables()
        self.show_login_frame()

    # 🌟 نظام التنبيهات العصرية المعاصرة (Custom Toast Notifications)
    def show_toast(self, title, message, m_type="info"):
        toast = ctk.CTkToplevel(self)
        toast.overrideredirect(True)
        toast.attributes("-topmost", True)

        if m_type == "success":
            border_col = colors["GREEN_BTN"]
            icon_symbol = "✅"
        elif m_type == "warning":
            border_col = colors["GOLD_ACCENT"]
            icon_symbol = "⚠️"
        elif m_type == "error":
            border_col = colors["RED_BTN"]
            icon_symbol = "❌"
        else:
            border_col = colors["BLUE_BTN"]
            icon_symbol = "🔔"

        toast_width = 360
        toast_height = 95

        self.update_idletasks()
        root_x = self.winfo_x()
        root_y = self.winfo_y()
        root_w = self.winfo_width()
        root_h = self.winfo_height()

        x = root_x + root_w - toast_width - 25
        y = root_y + root_h - toast_height - 35
        toast.geometry(f"{toast_width}x{toast_height}+{x}+{y}")

        card = ctk.CTkFrame(toast, fg_color=colors["TOAST_BG"], corner_radius=14, border_width=2,
                            border_color=border_col)
        card.pack(fill="both", expand=True)

        header_frame = ctk.CTkFrame(card, fg_color="transparent")
        header_frame.pack(fill="x", padx=12, pady=(10, 2))

        ctk.CTkLabel(header_frame, text=f"{icon_symbol}  {title}", font=(FONT_FAMILY, 12, "bold"),
                     text_color=border_col).pack(side="right" if current_lang == "ar" else "left")

        def close_toast():
            try:
                toast.destroy()
            except:
                pass

        close_btn = ctk.CTkButton(header_frame, text="✕", width=22, height=22, fg_color="transparent",
                                  text_color=colors["TEXT_MUTED"], hover_color=colors["PANEL_BG"],
                                  font=(FONT_FAMILY, 10, "bold"), command=close_toast)
        close_btn.pack(side="left" if current_lang == "ar" else "right")

        msg_lbl = ctk.CTkLabel(card, text=message, font=(FONT_FAMILY, 10), text_color=colors["TEXT_COLOR"],
                               wraplength=330, justify="right" if current_lang == "ar" else "left")
        msg_lbl.pack(fill="x", padx=15, pady=(0, 10))

        toast.after(4000, close_toast)

    def style_tables(self):
        global colors
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background=colors["TREE_BG"],
                        foreground=colors["TEXT_COLOR"],
                        rowheight=38,
                        fieldbackground=colors["TREE_BG"],
                        borderwidth=1,
                        relief="flat",
                        font=(FONT_FAMILY, 11))
        style.map('Treeview', background=[('selected', colors["GREEN_BTN"])], foreground=[('selected', '#FFFFFF')])
        style.configure("Treeview.Heading",
                        background=colors["HEAD_BG"],
                        foreground=colors["GOLD_ACCENT"],
                        font=(FONT_FAMILY, 11, 'bold'),
                        borderwidth=1,
                        relief="flat")

    def print_report_modal(self, tree, title_name):
        rows = [tree.item(item)['values'] for item in tree.get_children()]
        if not rows:
            self.show_toast("تنبيه", "القائمة فارغة للطباعة!", "warning")
            return

        def execute_print(paper_size):
            columns = [tree.heading(col)['text'] for col in tree['columns']]
            html_content = f"""
            <html lang="{current_lang}" dir="{'rtl' if current_lang == 'ar' else 'ltr'}">
            <head>
                <meta charset="utf-8">
                <title>تقرير {title_name}</title>
                <style>
                    body {{ font-family: '{FONT_FAMILY}', Tahoma, sans-serif; padding: 20px; color: #0F172A; }}
                    h2 {{ text-align: center; color: #E0A96D; margin-bottom: 5px; }}
                    p {{ text-align: center; color: #64748B; font-size: 12px; margin-bottom: 20px; }}
                    table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
                    th, td {{ border: 1px solid #CBD5E1; padding: 10px; text-align: center; font-size: 13px; }}
                    th {{ background-color: #F1F5F9; color: #E0A96D; }}
                    tr:nth-child(even) {{ background-color: #F8FAFC; }}
                    .footer {{ margin-top: 30px; text-align: {'left' if current_lang == 'en' else 'right'}; font-size: 11px; color: #64748B; }}
                </style>
            </head>
            <body>
                <h2>👑 نظام Golden Life - تقرير {title_name}</h2>
                <p>حجم الورق المخصص: {paper_size} | تاريخ التقرير: {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
                <table>
                    <thead>
                        <tr>{''.join([f'<th>{col}</th>' for col in columns])}</tr>
                    </thead>
                    <tbody>
                        {''.join(['<tr>' + ''.join([f'<td>{cell}</td>' for cell in row]) + '</tr>' for row in rows])}
                    </tbody>
                </table>
                <div class="footer">توقيع المسؤول / المدير: ........................</div>
                <script>window.print();</script>
            </body>
            </html>
            """
            file_path = tempfile.mktemp(suffix='.html')
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            webbrowser.open('file://' + os.path.realpath(file_path))
            p_win.destroy()

        p_win = ctk.CTkToplevel(self)
        p_win.title("🖨️ خيارات طباعة التقرير")
        p_win.geometry("380x280")
        p_win.grab_set()

        ctk.CTkLabel(p_win, text="🖨️ اختر نوع حجم الورق للطباعة", font=FONT_SUBTITLE,
                     text_color=colors["GOLD_ACCENT"]).pack(pady=15)

        paper_var = tk.StringVar(value="A4")
        ctk.CTkRadioButton(p_win, text="ورق A4 قياسي", variable=paper_var, value="A4", font=FONT_BODY).pack(pady=5,
                                                                                                            anchor="e" if current_lang == "ar" else "w",
                                                                                                            padx=40)
        ctk.CTkRadioButton(p_win, text="ورق A5 صغير", variable=paper_var, value="A5", font=FONT_BODY).pack(pady=5,
                                                                                                           anchor="e" if current_lang == "ar" else "w",
                                                                                                           padx=40)
        ctk.CTkRadioButton(p_win, text="ورق Letter أمريكي", variable=paper_var, value="Letter", font=FONT_BODY).pack(
            pady=5, anchor="e" if current_lang == "ar" else "w", padx=40)

        ctk.CTkButton(p_win, text="طباعة التقرير الفورية 🚀", font=FONT_BTN, fg_color=colors["PURPLE_BTN"], width=280,
                      height=38, command=lambda: execute_print(paper_var.get())).pack(pady=15)

    def export_to_excel(self, tree, title):
        rows = [tree.item(item)['values'] for item in tree.get_children()]
        if not rows:
            self.show_toast("تنبيه", "القائمة فارغة للتصدير!", "warning")
            return
        columns = [tree.heading(col)['text'] for col in tree['columns']]
        file_path = tempfile.mktemp(suffix='.csv')
        try:
            with open(file_path, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(columns)
                writer.writerows(rows)
            webbrowser.open('file://' + os.path.realpath(file_path))
            self.show_toast("نجح التصدير", "تم تجهيز ملف Excel/CSV بنجاح!", "success")
        except Exception as e:
            self.show_toast("خطأ", f"حدث خطأ أثناء التصدير: {e}", "error")

    # ==========================================
    # 🌟 شاشة تسجيل الدخول مع زر الثيم واللغة
    # ==========================================
    def show_login_frame(self):
        self.clear_screen()
        global colors
        colors = get_theme_colors(current_mode)
        self.configure(fg_color=colors["BG_MAIN"])

        bg_frame = ctk.CTkFrame(self, fg_color=colors["BG_MAIN"], corner_radius=0)
        bg_frame.pack(fill="both", expand=True)

        def toggle_theme():
            global current_mode
            current_mode = "light" if current_mode == "dark" else "dark"
            ctk.set_appearance_mode(current_mode)
            self.show_login_frame()

        def toggle_lang():
            global current_lang
            current_lang = "en" if current_lang == "ar" else "ar"
            self.show_login_frame()

        theme_btn_text = t("theme_light") if current_mode == "dark" else t("theme_dark")
        theme_toggle_btn = ctk.CTkButton(bg_frame, text=theme_btn_text, font=(FONT_FAMILY, 11, "bold"),
                                         fg_color=colors["PANEL_BG"], text_color=colors["GOLD_ACCENT"], border_width=1,
                                         border_color=colors["GOLD_ACCENT"], width=130, height=36, command=toggle_theme)
        theme_toggle_btn.place(relx=0.94 if current_lang == "ar" else 0.06, rely=0.05,
                               anchor="ne" if current_lang == "ar" else "nw")

        lang_btn_text = "🇬🇧 English" if current_lang == "ar" else "🇸🇦 العربية"
        lang_toggle_btn = ctk.CTkButton(bg_frame, text=lang_btn_text, font=(FONT_FAMILY, 11, "bold"),
                                        fg_color=colors["PANEL_BG"], text_color=colors["GOLD_ACCENT"], border_width=1,
                                        border_color=colors["GOLD_ACCENT"], width=130, height=36, command=toggle_lang)
        lang_toggle_btn.place(relx=0.80 if current_lang == "ar" else 0.20, rely=0.05,
                              anchor="ne" if current_lang == "ar" else "nw")

        main_card = ctk.CTkFrame(bg_frame, width=920, height=540, corner_radius=30, fg_color=colors["PANEL_BG"],
                                 border_width=2, border_color=colors["GOLD_ACCENT"])
        main_card.place(relx=0.5, rely=0.5, anchor="center")
        main_card.pack_propagate(False)

        brand_panel = ctk.CTkFrame(main_card, width=400, height=540, corner_radius=28, fg_color=colors["BG_MAIN"])
        brand_panel.pack(side="right" if current_lang == "ar" else "left", fill="y", padx=2, pady=2)
        brand_panel.pack_propagate(False)

        ctk.CTkLabel(brand_panel, text="💎", font=(FONT_FAMILY, 65), text_color=colors["GOLD_ACCENT"]).pack(
            pady=(100, 5))
        ctk.CTkLabel(brand_panel, text="GOLDEN LIFE", font=(FONT_FAMILY, 24, "bold"),
                     text_color=colors["GOLD_ACCENT"]).pack()
        ctk.CTkLabel(brand_panel, text="نظام تكنولوجيا تكييف الهواء والخدمات الذكية", font=(FONT_FAMILY, 11),
                     text_color=colors["TEXT_MUTED"]).pack(pady=8)

        divider = ctk.CTkFrame(brand_panel, width=150, height=2, fg_color=colors["GOLD_ACCENT"])
        divider.pack(pady=15)

        ctk.CTkLabel(brand_panel, text="الإصدار الاحترافي المتطور 2026 🚀", font=(FONT_FAMILY, 10, "bold"),
                     text_color=colors["GREEN_BTN"]).pack(pady=5)

        form_panel = ctk.CTkFrame(main_card, fg_color="transparent")
        form_panel.pack(side="left" if current_lang == "ar" else "right", fill="both", expand=True, padx=50, pady=45)

        align_dir = "e" if current_lang == "ar" else "w"
        entry_justify = "right" if current_lang == "ar" else "left"

        ctk.CTkLabel(form_panel, text=t("welcome"), font=(FONT_FAMILY, 24, "bold"), text_color=colors["TEXT_COLOR"],
                     anchor=align_dir).pack(fill="x", pady=(0, 5))
        ctk.CTkLabel(form_panel, text=t("login_hint"), font=(FONT_FAMILY, 11), text_color=colors["TEXT_MUTED"],
                     anchor=align_dir).pack(fill="x", pady=(0, 25))

        ctk.CTkLabel(form_panel, text=t("username"), font=FONT_BODY, text_color=colors["GOLD_ACCENT"],
                     anchor=align_dir).pack(fill="x", pady=(0, 2))
        self.user_entry = ctk.CTkEntry(form_panel, height=48, placeholder_text=t("user_placeholder"), font=FONT_BODY,
                                       corner_radius=12, fg_color=colors["BG_MAIN"], text_color=colors["TEXT_COLOR"],
                                       border_color=colors["TEXT_MUTED"], border_width=1.5, justify=entry_justify)
        self.user_entry.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(form_panel, text=t("password"), font=FONT_BODY, text_color=colors["GOLD_ACCENT"],
                     anchor=align_dir).pack(fill="x", pady=(0, 2))
        self.pass_entry = ctk.CTkEntry(form_panel, height=48, placeholder_text="••••••••", show="*", font=FONT_BODY,
                                       corner_radius=12, fg_color=colors["BG_MAIN"], text_color=colors["TEXT_COLOR"],
                                       border_color=colors["TEXT_MUTED"], border_width=1.5, justify=entry_justify)
        self.pass_entry.pack(fill="x", pady=(0, 8))

        self.pass_entry.bind("<Return>", lambda e: self.login())
        self.user_entry.bind("<Return>", lambda e: self.login())

        self.show_pass_var = tk.BooleanVar(value=False)

        def toggle_pass():
            if self.show_pass_var.get():
                self.pass_entry.configure(show="")
            else:
                self.pass_entry.configure(show="*")

        show_pass_chk = ctk.CTkCheckBox(form_panel, text=t("show_pass"), font=(FONT_FAMILY, 11),
                                        variable=self.show_pass_var, command=toggle_pass,
                                        text_color=colors["TEXT_MUTED"], checkbox_width=18, checkbox_height=18,
                                        border_color=colors["GOLD_ACCENT"], fg_color=colors["GOLD_ACCENT"],
                                        hover_color=colors["GOLD_HOVER"])
        show_pass_chk.pack(anchor=align_dir, pady=(0, 20))

        login_btn = ctk.CTkButton(form_panel, text=t("login_btn"), height=50, corner_radius=12,
                                  fg_color=colors["GOLD_ACCENT"], text_color=colors["BG_MAIN"],
                                  hover_color=colors["GOLD_HOVER"], font=(FONT_FAMILY, 12, "bold"), command=self.login)
        login_btn.pack(fill="x", pady=(5, 0))

    def login(self):
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()
        conn = sqlite3.connect("golden_life.db")
        cursor = conn.cursor()
        cursor.execute("SELECT username, role FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        if user:
            self.current_user = user[0]
            self.current_role = user[1]
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            cursor.execute("UPDATE users SET status='online', last_seen=? WHERE username=?", (now, self.current_user))
            conn.commit()
            conn.close()
            log_activity(self.current_user, "تسجيل دخول", "تم الدخول بنجاح")
            self.build_main_interface()
            self.check_system_notifications()
        else:
            conn.close()
            self.show_toast("خطأ في الدخول", t("err_login"), "error")

    def logout(self):
        if self.current_user:
            conn = sqlite3.connect("golden_life.db")
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            conn.cursor().execute("UPDATE users SET status='offline', last_seen=? WHERE username=?",
                                  (now, self.current_user))
            conn.commit()
            conn.close()
            log_activity(self.current_user, "تسجيل خروج", "تم تسجيل الخروج")
        self.show_login_frame()

    def check_system_notifications(self):
        conn = sqlite3.connect("golden_life.db")
        c = conn.cursor()
        unpaid_exp = 0
        debts_count = c.execute("SELECT COUNT(*) FROM customer_debts").fetchone()[0]
        if self.current_role == 'manager':
            unpaid_exp = c.execute("SELECT COUNT(*) FROM expenses WHERE status='غير مدفوع'").fetchone()[0]
        conn.close()

        has_alerts = False
        alert_text = ""

        if unpaid_exp > 0:
            alert_text += f"• يوجد عدد ({unpaid_exp}) مصروفات غير مدفوعة.\n"
            has_alerts = True
        if debts_count > 0:
            alert_text += f"• يوجد عدد ({debts_count}) عملاء مسجلين."
            has_alerts = True

        if has_alerts:
            self.show_toast("تنبيهات النظام الهامة", alert_text, "warning")

    # 🌟 دالة إظهار وإخفاء الشريط الجانبي بالثلاث شرط (Hamburger Toggle)
    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.sidebar.pack_forget()
            self.sidebar_visible = False
        else:
            side_side = "right" if current_lang == "ar" else "left"
            self.sidebar.pack(fill="y", side=side_side, before=self.main_container)
            self.sidebar_visible = True

    def build_main_interface(self):
        self.clear_screen()
        global colors
        colors = get_theme_colors(current_mode)
        self.configure(fg_color=colors["BG_MAIN"])

        side_side = "right" if current_lang == "ar" else "left"

        # الشريط الجانبي القابل للإخفاء والإظهار
        self.sidebar = ctk.CTkFrame(self, width=260, corner_radius=0, fg_color=colors["PANEL_BG"], border_width=1,
                                    border_color=colors["TEXT_MUTED"])
        self.sidebar.pack(fill="y", side=side_side)
        self.sidebar.pack_propagate(False)

        # زر الثلاث شرط (≡) داخل الشريط الجانبي من الأعلى
        top_bar_side = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        top_bar_side.pack(fill="x", padx=15, pady=(15, 5))

        menu_toggle_btn = ctk.CTkButton(top_bar_side, text="≡", width=36, height=36, font=(FONT_FAMILY, 16, "bold"),
                                        fg_color=colors["BG_MAIN"], text_color=colors["GOLD_ACCENT"],
                                        hover_color=colors["PANEL_BG"], command=self.toggle_sidebar)
        menu_toggle_btn.pack(side="left" if current_lang == "ar" else "right")

        ctk.CTkLabel(self.sidebar, text="👑 GOLDEN LIFE", font=(FONT_FAMILY, 18, "bold"),
                     text_color=colors["GOLD_ACCENT"]).pack(pady=(5, 2))
        role_badge = "👔 مدير النظام (صلاحيات كاملة)" if self.current_role == 'manager' else "🧑‍💻 موظف ميداني (صلاحيات مقيدة)"
        ctk.CTkLabel(self.sidebar, text=f"👤 {self.current_user}\n{role_badge}", font=FONT_BODY,
                     text_color=colors["TEXT_MUTED"]).pack(pady=(0, 15))

        # حاوية المحتوى الرئيسي
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, side="left" if current_lang == "ar" else "right", padx=10,
                                 pady=10)

        header_top_bar = ctk.CTkFrame(self.main_container, fg_color=colors["PANEL_BG"], corner_radius=12, height=50)
        header_top_bar.pack(fill="x", pady=(0, 10))
        header_top_bar.pack_propagate(False)

        ext_toggle_btn = ctk.CTkButton(header_top_bar, text="≡", width=38, height=34, font=(FONT_FAMILY, 16, "bold"),
                                       fg_color="transparent", text_color=colors["GOLD_ACCENT"],
                                       hover_color=colors["BG_MAIN"], command=self.toggle_sidebar)
        ext_toggle_btn.pack(side="right" if current_lang == "ar" else "left", padx=15, pady=8)

        ctk.CTkLabel(header_top_bar, text="نظام الإدارة والتشغيل الذكي", font=(FONT_FAMILY, 12, "bold"),
                     text_color=colors["TEXT_MUTED"]).pack(side="left" if current_lang == "ar" else "right", padx=15,
                                                           pady=8)

        self.content_area = ctk.CTkFrame(self.main_container, corner_radius=15, fg_color=colors["BG_MAIN"])
        self.content_area.pack(fill="both", expand=True)

        # 🌟 القائمة الجانبية المحدثة بالأسماء بالكامل
        menu_items = [
            ("📊  القائمة الرئيسية", self.view_dashboard),
        ]

        if self.current_role == 'manager':
            menu_items.append(("❄️  التكيفات", self.view_ac_section))
            menu_items.append(("💧  الفلاتر", self.view_filters_section))
            menu_items.append(("🚚  سجل الموردين المعتمدين", self.view_suppliers_section))
            menu_items.append(("📦  سجل المخزون", self.view_stock_movements_section))

        menu_items.extend([
            ("👷  جدول المهام", self.view_tech_shifts_section),
            ("🧰  إدارة العدة والمعدات", self.view_tools_section),
            ("⚠️  العملاء", self.view_debts_section),
            ("💬  المحادثة", self.view_chat_section),
            ("🔔  التنبيهات", self.view_maintenance_alerts_section),
        ])

        if self.current_role == 'manager':
            menu_items.append(("💸  المصروفات", self.view_expenses_section))
            menu_items.append(("📈  الارباح", self.view_profits_section))
            menu_items.append(("👥  ادارة الحسابات", self.view_user_accounts_section))
            menu_items.append(("📝  سجل الانشطه", self.view_activity_logs_section))

        for text, command in menu_items:
            btn = ctk.CTkButton(self.sidebar, text=text, fg_color="transparent", text_color=colors["TEXT_COLOR"],
                                hover_color=colors["BG_MAIN"], anchor="e" if current_lang == "ar" else "w",
                                font=FONT_BTN, height=40, command=command)
            btn.pack(fill="x", padx=10, pady=2)

        ctk.CTkButton(self.sidebar, text=t("logout"), fg_color=colors["RED_BTN"], hover_color="#991B1B",
                      text_color="white", font=FONT_BTN, height=40, command=self.logout).pack(fill="x", padx=10,
                                                                                              pady=15, side="bottom")

        self.view_dashboard()

    def format_amount(self, amount):
        if amount is None: return "0.00 ج.م"
        if self.current_role == 'manager':
            return f"{amount:,.2f} ج.م"
        else:
            return f"{(amount * 0.10):,.2f} ج.م (عمولة 10%)"

    def format_qty(self, qty):
        if qty is None: return "0"
        if self.current_role == 'manager':
            return str(qty)
        else:
            return f"{int(qty * 0.10)} (10%)"

    def clear_screen(self):
        for widget in self.winfo_children(): widget.destroy()

    def clear_content(self):
        for widget in self.content_area.winfo_children(): widget.destroy()

    def filter_treeview(self, tree, search_query, original_data):
        for item in tree.get_children():
            tree.delete(item)
        query = search_query.strip().lower()
        for row in original_data:
            if not query or any(query in str(cell).lower() for cell in row):
                tree.insert("", "end", values=row)

    # ==========================================
    # 🌟 سجل المخزون
    # ==========================================
    def view_stock_movements_section(self):
        if self.current_role != 'manager':
            self.show_toast("صلاحيات", "هذه الصلاحية للمديرين فقط!", "error")
            return
        self.clear_content()
        box = ctk.CTkFrame(self.content_area, fg_color=colors["PANEL_BG"], corner_radius=18, border_width=1,
                           border_color=colors["TEXT_MUTED"])
        box.pack(fill="both", expand=True, padx=5, pady=5)

        top_f = ctk.CTkFrame(box, fg_color="transparent")
        top_f.pack(fill="x", pady=15, padx=20)
        ctk.CTkLabel(top_f, text="📦 سجل ومراقبة حركات المخزون (وارد وصادر)", font=FONT_TITLE,
                     text_color=colors["GOLD_ACCENT"]).pack(side="right" if current_lang == "ar" else "left")

        btn_fr = ctk.CTkFrame(top_f, fg_color="transparent")
        btn_fr.pack(side="left" if current_lang == "ar" else "right")
        ctk.CTkButton(btn_fr, text="📊 Excel", font=FONT_BTN, fg_color=colors["GREEN_BTN"], width=90, height=36,
                      command=lambda: self.export_to_excel(tree_stk, "سجل المخزون")).pack(side="right", padx=3)
        ctk.CTkButton(btn_fr, text="🖨️ طباعة", font=FONT_BTN, fg_color=colors["PURPLE_BTN"], width=90, height=36,
                      command=lambda: self.print_report_modal(tree_stk, "سجل المخزون")).pack(side="right", padx=3)

        search_entry = ctk.CTkEntry(box, placeholder_text="🔍 ابحث في سجل المخزون...", font=FONT_BODY, height=38,
                                    justify="right" if current_lang == "ar" else "left")
        search_entry.pack(fill="x", padx=20, pady=(0, 5))

        tree_stk = ttk.Treeview(box, columns=("id", "item", "type", "qty", "user", "time"), show="headings", height=11)
        for col, txt in zip(tree_stk["columns"],
                            ["م", "اسم الصنف / الجهاز", "نوع الحركة", "الكمية المتغيرة", "بواسطة المسؤول",
                             "وقت الحركة"]): tree_stk.heading(col, text=txt)
        tree_stk.pack(fill="both", expand=True, padx=20, pady=5)

        conn = sqlite3.connect("golden_life.db")
        all_stk = conn.cursor().execute("SELECT * FROM stock_movements ORDER BY id DESC").fetchall()
        conn.close()

        def load_stk_filtered(query=""):
            for item in tree_stk.get_children(): tree_stk.delete(item)
            q = query.strip().lower()
            for r in all_stk:
                if not q or any(q in str(c).lower() for c in r):
                    tree_stk.insert("", "end", values=r)

        load_stk_filtered()
        search_entry.bind("<KeyRelease>", lambda e: load_stk_filtered(search_entry.get()))

    # ==========================================
    # 🌟 ادارة الحسابات
    # ==========================================
    def view_user_accounts_section(self):
        if self.current_role != 'manager':
            self.show_toast("صلاحيات", "هذه الصلاحية للمديرين فقط!", "error")
            return
        self.clear_content()
        box = ctk.CTkFrame(self.content_area, fg_color=colors["PANEL_BG"], corner_radius=18, border_width=1,
                           border_color=colors["TEXT_MUTED"])
        box.pack(fill="both", expand=True, padx=5, pady=5)

        top_f = ctk.CTkFrame(box, fg_color="transparent")
        top_f.pack(fill="x", pady=15, padx=20)
        ctk.CTkLabel(top_f, text="👥 إدارة وصنع حسابات المستخدمين والصلاحيات", font=FONT_TITLE,
                     text_color=colors["GOLD_ACCENT"]).pack(side="right" if current_lang == "ar" else "left")

        btn_fr = ctk.CTkFrame(top_f, fg_color="transparent")
        btn_fr.pack(side="left" if current_lang == "ar" else "right")
        ctk.CTkButton(btn_fr, text="⚙️ تعديل الحساب", font=FONT_BTN, fg_color=colors["BLUE_BTN"], width=130, height=36,
                      command=self.popup_edit_user).pack(side="right", padx=3)
        ctk.CTkButton(btn_fr, text="🗑️ حذف الحساب", font=FONT_BTN, fg_color=colors["RED_BTN"], width=130, height=36,
                      command=self.delete_selected_user).pack(side="right", padx=3)
        ctk.CTkButton(btn_fr, text="➕ إضافة حساب", font=FONT_BTN, fg_color=colors["GREEN_BTN"], width=120, height=36,
                      command=self.popup_create_user).pack(side="right", padx=3)

        t_box = ctk.CTkFrame(box, fg_color=colors["BG_MAIN"], corner_radius=12, border_width=1,
                             border_color=colors["TEXT_MUTED"])
        t_box.pack(fill="both", expand=True, padx=20, pady=10)

        self.tree_u = ttk.Treeview(t_box, columns=("id", "username", "role", "status", "last"), show="headings",
                                   height=12)
        for col, txt in zip(self.tree_u["columns"],
                            ["م", "اسم المستخدم", "الصلاحية", "حالة الاتصال", "آخر ظهور"]): self.tree_u.heading(col,
                                                                                                                text=txt)
        self.tree_u.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_users_table()

    def load_users_table(self):
        for item in self.tree_u.get_children(): self.tree_u.delete(item)
        conn = sqlite3.connect("golden_life.db")
        for row in conn.cursor().execute("SELECT id, username, role, status, last_seen FROM users"):
            role_str = "مدير النظام" if row[2] == 'manager' else "موظف"
            self.tree_u.insert("", "end", values=(row[0], row[1], role_str, row[3], row[4] or "غير متصل"))
        conn.close()

    def popup_create_user(self):
        pop = ctk.CTkToplevel(self)
        pop.title("إنشاء حساب مستخدم جديد")
        pop.geometry("380x380")
        pop.grab_set()
        ctk.CTkLabel(pop, text="👤 إنشاء حساب جديد", font=FONT_SUBTITLE, text_color=colors["GOLD_ACCENT"]).pack(pady=15)

        e_user = ctk.CTkEntry(pop, width=300, placeholder_text="اسم المستخدم (Username)", font=FONT_BODY)
        e_user.pack(pady=8)
        e_pass = ctk.CTkEntry(pop, width=300, placeholder_text="كلمة المرور", show="*", font=FONT_BODY)
        e_pass.pack(pady=8)

        ctk.CTkLabel(pop, text="اختر دور الصلاحية:", font=FONT_BODY, text_color=colors["TEXT_MUTED"]).pack(
            anchor="e" if current_lang == "ar" else "w", padx=40)
        role_menu = ctk.CTkOptionMenu(pop, width=300, values=["manager", "employee"], fg_color=colors["BLUE_BTN"],
                                      button_color=colors["BLUE_BTN"])
        role_menu.pack(pady=8)

        def save():
            u = e_user.get().strip()
            p = e_pass.get().strip()
            r = role_menu.get()
            if not (u and p):
                self.show_toast("تنبيه", "املأ جميع الحقول المطلوبة!", "warning")
                return
            try:
                conn = sqlite3.connect("golden_life.db")
                conn.cursor().execute(
                    "INSERT INTO users (username, password, role, status) VALUES (?, ?, ?, 'offline')", (u, p, r))
                conn.commit()
                conn.close()
                log_activity(self.current_user, "إضافة مستخدم", f"تم إنشاء حساب جديد: {u} ({r})")
                self.show_toast("نجاح", "تم إنشاء الحساب بنجاح!", "success")
                pop.destroy()
                self.load_users_table()
            except sqlite3.IntegrityError:
                self.show_toast("خطأ", "اسم المستخدم مستخدم بالفعل، اختر اسماً آخر!", "error")

        ctk.CTkButton(pop, text="💾 حفظ الحساب الجديد", font=FONT_BTN, fg_color=colors["GREEN_BTN"], width=300,
                      height=38, command=save).pack(pady=15)

    def popup_edit_user(self):
        selected_item = self.tree_u.selection()
        if not selected_item:
            self.show_toast("تنبيه", "الرجاء اختيار مستخدم من الجدول للتعديل!", "warning")
            return
        row_values = self.tree_u.item(selected_item)['values']
        user_id = row_values[0]
        old_username = row_values[1]

        pop = ctk.CTkToplevel(self)
        pop.title("تعديل بيانات المستخدم")
        pop.geometry("380x400")
        pop.grab_set()
        ctk.CTkLabel(pop, text=f"⚙️ تعديل حساب: {old_username}", font=FONT_SUBTITLE,
                     text_color=colors["GOLD_ACCENT"]).pack(pady=15)

        e_user = ctk.CTkEntry(pop, width=300, font=FONT_BODY)
        e_user.pack(pady=8)
        e_user.insert(0, old_username)

        e_pass = ctk.CTkEntry(pop, width=300, placeholder_text="كلمة المرور الجديدة (اختياري)", show="*",
                              font=FONT_BODY)
        e_pass.pack(pady=8)

        ctk.CTkLabel(pop, text="تعديل الصلاحية:", font=FONT_BODY, text_color=colors["TEXT_MUTED"]).pack(
            anchor="e" if current_lang == "ar" else "w", padx=40)
        role_menu = ctk.CTkOptionMenu(pop, width=300, values=["manager", "employee"], fg_color=colors["BLUE_BTN"],
                                      button_color=colors["BLUE_BTN"])
        role_menu.pack(pady=8)

        def save_changes():
            new_u = e_user.get().strip()
            new_p = e_pass.get().strip()
            new_r = role_menu.get()
            if not new_u:
                self.show_toast("تنبيه", "اسم المستخدم لا يمكن أن يكون فارغاً!", "warning")
                return

            conn = sqlite3.connect("golden_life.db")
            c = conn.cursor()
            if new_p:
                c.execute("UPDATE users SET username=?, password=?, role=? WHERE id=?", (new_u, new_p, new_r, user_id))
            else:
                c.execute("UPDATE users SET username=?, role=? WHERE id=?", (new_u, new_r, user_id))
            conn.commit()
            conn.close()

            log_activity(self.current_user, "تعديل حساب", f"تم تعديل بيانات المستخدم: {old_username} إلى {new_u}")
            self.show_toast("نجاح", "تم تعديل بيانات المستخدم بنجاح!", "success")
            pop.destroy()
            self.load_users_table()

        ctk.CTkButton(pop, text="💾 حفظ التعديلات", font=FONT_BTN, fg_color=colors["GREEN_BTN"], width=300, height=38,
                      command=save_changes).pack(pady=15)

    def delete_selected_user(self):
        selected_item = self.tree_u.selection()
        if not selected_item:
            self.show_toast("تنبيه", "الرجاء اختيار مستخدم من الجدول لحذفه!", "warning")
            return
        row_values = self.tree_u.item(selected_item)['values']
        user_id = row_values[0]
        username_to_delete = row_values[1]

        if username_to_delete == self.current_user:
            self.show_toast("خطأ", "لا يمكنك حذف حسابك الحالي أثناء تسجيل الدخول به!", "error")
            return

        if tk.messagebox.askyesno("⚠️ تأكيد الحذف",
                                  f"هل أنت متأكد من رغبتك في حذف المستخدم '{username_to_delete}' نهائياً؟"):
            conn = sqlite3.connect("golden_life.db")
            conn.cursor().execute("DELETE FROM users WHERE id=?", (user_id,))
            conn.commit()
            conn.close()
            log_activity(self.current_user, "حذف حساب", f"تم حذف المستخدم: {username_to_delete}")
            self.show_toast("نجاح", "تم حذف المستخدم بنجاح!", "success")
            self.load_users_table()

    # ==========================================
    # 🌟 سجل الانشطه
    # ==========================================
    def view_activity_logs_section(self):
        if self.current_role != 'manager':
            self.show_toast("صلاحيات", "هذه الصلاحية للمديرين فقط!", "error")
            return
        self.clear_content()
        box = ctk.CTkFrame(self.content_area, fg_color=colors["PANEL_BG"], corner_radius=18, border_width=1,
                           border_color=colors["TEXT_MUTED"])
        box.pack(fill="both", expand=True, padx=5, pady=5)

        top_f = ctk.CTkFrame(box, fg_color="transparent")
        top_f.pack(fill="x", pady=15, padx=20)
        ctk.CTkLabel(top_f, text="📝 سجل أنشطة وتحركات المستخدمين", font=FONT_TITLE,
                     text_color=colors["GOLD_ACCENT"]).pack(side="right" if current_lang == "ar" else "left")

        btn_f = ctk.CTkFrame(top_f, fg_color="transparent")
        btn_f.pack(side="left" if current_lang == "ar" else "right")
        ctk.CTkButton(btn_f, text="📊 Excel", font=FONT_BTN, fg_color=colors["GREEN_BTN"], width=80, height=36,
                      command=lambda: self.export_to_excel(tree_logs, "سجل الانشطه")).pack(side="right", padx=3)
        ctk.CTkButton(btn_f, text="🖨️ طباعة", font=FONT_BTN, fg_color=colors["PURPLE_BTN"], width=80, height=36,
                      command=lambda: self.print_report_modal(tree_logs, "سجل الانشطه")).pack(side="right", padx=3)
        ctk.CTkButton(btn_f, text="🗑️ مسح", font=FONT_BTN, fg_color=colors["RED_BTN"], width=90, height=36,
                      command=self.clear_activity_logs).pack(side="right", padx=3)

        search_entry = ctk.CTkEntry(box, placeholder_text="🔍 ابحث في سجل الأنشطة...", font=FONT_BODY, height=38,
                                    justify="right" if current_lang == "ar" else "left")
        search_entry.pack(fill="x", padx=20, pady=(0, 5))

        tree_logs = ttk.Treeview(box, columns=("id", "user", "action", "details", "time"), show="headings", height=11)
        for col, txt in zip(tree_logs["columns"], ["م", "المستخدم", "الإجراء", "التفاصيل", "الوقت"]): tree_logs.heading(
            col, text=txt)
        tree_logs.pack(fill="both", expand=True, padx=20, pady=5)

        conn = sqlite3.connect("golden_life.db")
        all_logs = conn.cursor().execute("SELECT * FROM activity_logs ORDER BY id DESC").fetchall()
        conn.close()
        for row in all_logs: tree_logs.insert("", "end", values=row)

        search_entry.bind("<KeyRelease>", lambda e: self.filter_treeview(tree_logs, search_entry.get(), all_logs))

    def clear_activity_logs(self):
        if tk.messagebox.askyesno("⚠️ تأكيد مسح السجل", "هل أنت متأكد من رغبتك في مسح كافة سجلات الأنشطة تماماً؟"):
            conn = sqlite3.connect("golden_life.db")
            conn.cursor().execute("DELETE FROM activity_logs")
            conn.commit()
            conn.close()
            log_activity(self.current_user, "مسح سجل الأنشطة", "تم تفريغ الجدول بالكامل")
            self.show_toast("نجاح", "تم مسح سجل التفاعل بنجاح!", "success")
            self.view_activity_logs_section()

    # ==========================================
    # 🌟 المصروفات وزكاة المال
    # ==========================================
    def view_expenses_section(self):
        if self.current_role != 'manager':
            self.show_toast("صلاحيات", "عذراً، هذه الصلاحية مقتصرة على المديرين فقط!", "error")
            return
        self.clear_content()
        box = ctk.CTkFrame(self.content_area, fg_color=colors["BG_MAIN"], corner_radius=18)
        box.pack(fill="both", expand=True, padx=5, pady=5)

        head_frame = ctk.CTkFrame(box, fg_color=colors["PANEL_BG"], corner_radius=14, border_width=1,
                                  border_color=colors["TEXT_MUTED"])
        head_frame.pack(fill="x", pady=(0, 10), padx=5)

        inner_head = ctk.CTkFrame(head_frame, fg_color="transparent")
        inner_head.pack(fill="x", pady=15, padx=20)
        ctk.CTkLabel(inner_head, text="💸 إدارة المصروفات وحاسبة زكاة المال السنوية", font=FONT_TITLE,
                     text_color=colors["GOLD_ACCENT"]).pack(side="right" if current_lang == "ar" else "left")

        btn_frame = ctk.CTkFrame(inner_head, fg_color="transparent")
        btn_frame.pack(side="left" if current_lang == "ar" else "right")
        ctk.CTkButton(btn_frame, text="📊 Excel", font=FONT_BTN, fg_color=colors["GREEN_BTN"], width=80, height=36,
                      command=lambda: self.export_to_excel(tree_exp, "المصروفات")).pack(side="right", padx=3)
        ctk.CTkButton(btn_frame, text="🖨️ طباعة", font=FONT_BTN, fg_color=colors["PURPLE_BTN"], width=80, height=36,
                      command=lambda: self.print_report_modal(tree_exp, "المصروفات السنوية")).pack(side="right", padx=3)
        ctk.CTkButton(btn_frame, text="🧮 زكاة", font=FONT_BTN, fg_color="#00B4D8", width=90, height=36,
                      command=self.calculate_zakat_modal).pack(side="right", padx=3)
        ctk.CTkButton(btn_frame, text="➕ مصروف", font=FONT_BTN, fg_color=colors["BLUE_BTN"], width=90, height=36,
                      command=self.popup_add_expense).pack(side="right", padx=3)

        t_box = ctk.CTkFrame(box, fg_color=colors["PANEL_BG"], corner_radius=14, border_width=1,
                             border_color=colors["TEXT_MUTED"])
        t_box.pack(fill="both", expand=True, padx=5, pady=5)

        search_entry = ctk.CTkEntry(t_box, placeholder_text="🔍 ابحث في المصروفات...", font=FONT_BODY, height=38,
                                    justify="right" if current_lang == "ar" else "left")
        search_entry.pack(fill="x", padx=15, pady=(15, 5))

        tree_exp = ttk.Treeview(t_box, columns=("icon", "id", "title", "amount", "status"), show="headings", height=10)
        for col, txt in zip(tree_exp["columns"], ["حالة السداد", "م", "بيان المصروف السنوي", "المبلغ المطلوب",
                                                  "الحالة العامة"]): tree_exp.heading(col, text=txt)
        tree_exp.column("icon", width=120, anchor="center")
        tree_exp.pack(fill="both", expand=True, padx=15, pady=5)

        tree_exp.tag_configure('unpaid', foreground='#E63946', font=(FONT_FAMILY, 11, 'bold'))
        tree_exp.tag_configure('paid', foreground='#2A9D8F', font=(FONT_FAMILY, 11))

        conn = sqlite3.connect("golden_life.db")
        all_exp_rows = []
        for row in conn.cursor().execute("SELECT * FROM expenses"):
            status_text = row[3]
            is_unpaid = (status_text == 'غير مدفوع')
            icon_str = "🔴 غير مدفوع" if is_unpaid else "🟢 مدفوع"
            all_exp_rows.append((icon_str, row[0], row[1], f"{row[2]:,.2f} ج.م", status_text))
        conn.close()

        def load_exp_filtered(query=""):
            for item in tree_exp.get_children(): tree_exp.delete(item)
            q = query.strip().lower()
            for r in all_exp_rows:
                if not q or any(q in str(c).lower() for c in r):
                    tag = 'unpaid' if r[4] == 'غير مدفوع' else 'paid'
                    tree_exp.insert("", "end", values=r, tags=(tag,))

        load_exp_filtered()
        search_entry.bind("<KeyRelease>", lambda e: load_exp_filtered(search_entry.get()))

    def calculate_zakat_modal(self):
        conn = sqlite3.connect("golden_life.db")
        c = conn.cursor()
        ac_sales = c.execute("SELECT COALESCE(SUM(amount_due), 0) FROM ac_sales").fetchone()[0]
        flt_sales = c.execute("SELECT COALESCE(SUM(amount_due), 0) FROM filter_sales").fetchone()[0]
        total_rev = ac_sales + flt_sales
        exp_paid = c.execute("SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE status='مدفوع'").fetchone()[0]
        conn.close()
        net_wealth = max(0, total_rev - exp_paid)
        zakat_amount = net_wealth * 0.025

        win = ctk.CTkToplevel(self)
        win.title("🧮 حاسبة زكاة المال السنوية الشرعية")
        win.geometry("460x420")
        win.grab_set()
        ctk.CTkLabel(win, text="🌙 حاسبة زكاة المال السنوية الصافية", font=FONT_TITLE,
                     text_color=colors["GOLD_ACCENT"]).pack(pady=(20, 10))
        card = ctk.CTkFrame(win, fg_color=colors["PANEL_BG"], corner_radius=14, border_width=1,
                            border_color=colors["GOLD_ACCENT"])
        card.pack(fill="both", expand=True, padx=20, pady=10)
        ctk.CTkLabel(card, text=f"💰 إجمالي الإيرادات والوعاء السنوي:\n{self.format_amount(net_wealth)}",
                     font=FONT_SUBTITLE, text_color=colors["TEXT_COLOR"]).pack(pady=(20, 10))
        ctk.CTkLabel(card, text=f"✨ مقدار الزكاة الواجب إخراجها سنويّاً (2.5%):\n{self.format_amount(zakat_amount)}",
                     font=(FONT_FAMILY, 18, "bold"), text_color=colors["GREEN_BTN"]).pack(pady=10)
        ctk.CTkLabel(card, text="💡 تحسب الزكاة بعد مرور الحول القمري على بلوغ النصاب وبعد خصم المصروفات المدفوعة.",
                     font=(FONT_FAMILY, 10), text_color=colors["TEXT_MUTED"]).pack(pady=10)

    # ==========================================
    # 🌟 الارباح
    # ==========================================
    def view_profits_section(self):
        if self.current_role != 'manager':
            self.show_toast("صلاحيات", "عذراً، هذه الصلاحية مقتصرة على المديرين فقط!", "error")
            return
        self.clear_content()
        box = ctk.CTkFrame(self.content_area, fg_color=colors["BG_MAIN"], corner_radius=18)
        box.pack(fill="both", expand=True, padx=5, pady=5)

        top_f = ctk.CTkFrame(box, fg_color=colors["PANEL_BG"], corner_radius=14, border_width=1,
                             border_color=colors["TEXT_MUTED"])
        top_f.pack(fill="x", pady=(0, 10), padx=5)

        inner_top = ctk.CTkFrame(top_f, fg_color="transparent")
        inner_top.pack(fill="x", pady=15, padx=20)
        ctk.CTkLabel(inner_top, text="📈 لوحة تحليلات الأرباح والمكاسب المالية (P&L Dashboard)", font=FONT_TITLE,
                     text_color=colors["GOLD_ACCENT"]).pack(side="right" if current_lang == "ar" else "left")

        conn = sqlite3.connect("golden_life.db")
        c = conn.cursor()
        ac_sales = c.execute("SELECT COALESCE(SUM(amount_due), 0) FROM ac_sales").fetchone()[0]
        flt_sales = c.execute("SELECT COALESCE(SUM(amount_due), 0) FROM filter_sales").fetchone()[0]

        expenses_data = c.execute("SELECT title, amount, status FROM expenses").fetchall()
        total_exp_paid = sum([row[1] for row in expenses_data if row[2] == 'مدفوع'])
        total_exp_unpaid = sum([row[1] for row in expenses_data if row[2] == 'غير مدفوع'])
        conn.close()

        total_rev = ac_sales + flt_sales
        net = total_rev - total_exp_paid
        multiplier = 1.0 if self.current_role == 'manager' else 0.10

        cards_f = ctk.CTkFrame(box, fg_color="transparent")
        cards_f.pack(fill="x", padx=5, pady=5)

        def make_metric_card(parent, title, val, color_bg, color_text):
            card = ctk.CTkFrame(parent, fg_color=color_bg, corner_radius=14, height=90, border_width=1,
                                border_color=colors["TEXT_MUTED"])
            card.pack(side="right" if current_lang == "ar" else "left", fill="x", expand=True, padx=4)
            card.pack_propagate(False)
            ctk.CTkLabel(card, text=title, font=(FONT_FAMILY, 11, "bold"), text_color=colors["TEXT_MUTED"]).pack(
                pady=(12, 2))
            ctk.CTkLabel(card, text=val, font=(FONT_FAMILY, 15, "bold"), text_color=color_text).pack()

        make_metric_card(cards_f, "إجمالي الإيرادات", f"{total_rev * multiplier:,.2f} ج.م", colors["PANEL_BG"],
                         colors["BLUE_BTN"])
        make_metric_card(cards_f, "المصروفات المدفوعة", f"{total_exp_paid * multiplier:,.2f} ج.م", colors["PANEL_BG"],
                         colors["RED_BTN"])
        make_metric_card(cards_f, "صافي الأرباح النهائية", f"{net * multiplier:,.2f} ج.م", colors["PANEL_BG"],
                         colors["GOLD_ACCENT"])

        body_grid = ctk.CTkFrame(box, fg_color="transparent")
        body_grid.pack(fill="both", expand=True, padx=5, pady=5)

        left_panel = ctk.CTkFrame(body_grid, fg_color=colors["PANEL_BG"], corner_radius=14, border_width=1,
                                  border_color=colors["TEXT_MUTED"], width=420)
        left_panel.pack(side="right" if current_lang == "ar" else "left", fill="y", padx=(5, 0))
        left_panel.pack_propagate(False)

        ctk.CTkLabel(left_panel, text="📌 تفصيل مصادر الإيرادات:", font=FONT_SUBTITLE,
                     text_color=colors["GOLD_ACCENT"]).pack(anchor="e" if current_lang == "ar" else "w", padx=20,
                                                            pady=(20, 10))

        details_text = f"• مبيعات التكيفات:\n  {ac_sales * multiplier:,.2f} ج.م\n\n" \
                       f"• مبيعات فلاتر المياه:\n  {flt_sales * multiplier:,.2f} ج.م\n\n" \
                       f"• إجمالي المصروفات غير المدفوعة:\n  {total_exp_unpaid * multiplier:,.2f} ج.م"

        ctk.CTkLabel(left_panel, text=details_text, font=FONT_BODY, text_color=colors["TEXT_COLOR"],
                     justify="right" if current_lang == "ar" else "left").pack(
            anchor="e" if current_lang == "ar" else "w", padx=20, pady=5)

        right_panel = ctk.CTkFrame(body_grid, fg_color=colors["PANEL_BG"], corner_radius=14, border_width=1,
                                   border_color=colors["TEXT_MUTED"])
        right_panel.pack(side="left" if current_lang == "ar" else "right", fill="both", expand=True, padx=(0, 0))

        fig, ax = plt.subplots(figsize=(5, 3), dpi=100)
        fig.patch.set_facecolor(colors["PANEL_BG"])
        ax.set_facecolor(colors["PANEL_BG"])

        categories = ['Ac Sales', 'Filter Sales', 'Expenses', 'Net Profit'] if current_lang == 'en' else [
            'مبيعات تكيفات', 'مبيعات فلاتر', 'مصروفات', 'صافي الأرباح']
        values = [ac_sales * multiplier, flt_sales * multiplier, total_exp_paid * multiplier, net * multiplier]
        colors_list = [colors["BLUE_BTN"], colors["GREEN_BTN"], colors["RED_BTN"], colors["GOLD_ACCENT"]]

        bars = ax.bar(categories, values, color=colors_list, width=0.45)
        ax.set_title("Financial Performance Chart", fontsize=10, fontweight='bold', color=colors["TEXT_COLOR"],
                     fontfamily='sans-serif')
        ax.set_ylabel("Amount (EGP)", fontsize=8, color=colors["TEXT_COLOR"])
        ax.tick_params(colors=colors["TEXT_COLOR"], labelsize=8)
        ax.grid(axis='y', linestyle='--', alpha=0.3)

        canvas = FigureCanvasTkAgg(fig, master=right_panel)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    # ==========================================
    # 🌟 التنبيهات
    # ==========================================
    def view_maintenance_alerts_section(self):
        self.clear_content()
        box = ctk.CTkFrame(self.content_area, fg_color=colors["PANEL_BG"], corner_radius=18, border_width=1,
                           border_color=colors["TEXT_MUTED"])
        box.pack(fill="both", expand=True, padx=5, pady=5)

        head_frame = ctk.CTkFrame(box, fg_color="transparent")
        head_frame.pack(fill="x", pady=15, padx=20)
        ctk.CTkLabel(head_frame, text="🔔 تنبيهات مواعيد الصيانة الدورية للعملاء", font=FONT_TITLE,
                     text_color=colors["GOLD_ACCENT"]).pack(side="right" if current_lang == "ar" else "left")

        btn_fr = ctk.CTkFrame(head_frame, fg_color="transparent")
        btn_fr.pack(side="left" if current_lang == "ar" else "right")
        ctk.CTkButton(btn_fr, text="📊 Excel", font=FONT_BTN, fg_color=colors["GREEN_BTN"], width=90, height=36,
                      command=lambda: self.export_to_excel(tree_m, "التنبيهات")).pack(side="right", padx=3)
        ctk.CTkButton(btn_fr, text="🖨️ طباعة", font=FONT_BTN, fg_color=colors["PURPLE_BTN"], width=90, height=36,
                      command=lambda: self.print_report_modal(tree_m, "التنبيهات")).pack(side="right", padx=3)
        ctk.CTkButton(btn_fr, text="➕ إضافة موعد", font=FONT_BTN, fg_color=colors["BLUE_BTN"], height=36, width=120,
                      command=self.popup_add_maintenance_client).pack(side="right", padx=3)

        t_box = ctk.CTkFrame(box, fg_color=colors["BG_MAIN"], corner_radius=12, border_width=1,
                             border_color=colors["TEXT_MUTED"])
        t_box.pack(fill="both", expand=True, padx=20, pady=10)

        search_entry = ctk.CTkEntry(t_box, placeholder_text="🔍 ابحث بالاسم أو رقم الهاتف أو العنوان...", font=FONT_BODY,
                                    height=38, justify="right" if current_lang == "ar" else "left")
        search_entry.pack(fill="x", padx=10, pady=(10, 5))

        tree_m = ttk.Treeview(t_box, columns=("name", "phone", "addr", "maint", "status"), show="headings", height=10)
        for col, txt in zip(tree_m["columns"],
                            ["اسم العميل", "رقم العميل", "العنوان", "موعد الصيانة المستحق", "الحالة"]): tree_m.heading(
            col, text=txt)
        tree_m.pack(fill="both", expand=True, padx=10, pady=5)

        conn = sqlite3.connect("golden_life.db")
        all_maint = []
        for row in conn.cursor().execute("SELECT client_name, client_phone, address, maint_date FROM ac_maintenance"):
            all_maint.append((row[0], row[1], row[2], row[3], "🔔 تكييف - مستحق صيانة"))
        for row in conn.cursor().execute(
                "SELECT client_name, client_phone, address, maint_date FROM filter_maintenance"):
            all_maint.append((row[0], row[1], row[2], row[3], "💧 فلتر - متابعة دورية"))
        conn.close()

        def load_maint_filtered(query=""):
            for item in tree_m.get_children(): tree_m.delete(item)
            q = query.strip().lower()
            for r in all_maint:
                if not q or any(q in str(c).lower() for c in r):
                    tree_m.insert("", "end", values=r)

        load_maint_filtered()
        search_entry.bind("<KeyRelease>", lambda e: load_maint_filtered(search_entry.get()))

    def popup_add_maintenance_client(self):
        pop = ctk.CTkToplevel(self)
        pop.title("إضافة موعد صيانة لعميل جديد")
        pop.geometry("400x440")
        pop.grab_set()
        ctk.CTkLabel(pop, text="📅 تسجيل عميل جديد للصيانة الدورية", font=FONT_SUBTITLE,
                     text_color=colors["GOLD_ACCENT"]).pack(pady=15)

        e_name = ctk.CTkEntry(pop, width=320, placeholder_text="اسم العميل", font=FONT_BODY)
        e_name.pack(pady=6)
        e_phone = ctk.CTkEntry(pop, width=320, placeholder_text="رقم التلفون", font=FONT_BODY)
        e_phone.pack(pady=6)
        e_addr = ctk.CTkEntry(pop, width=320, placeholder_text="العنوان", font=FONT_BODY)
        e_addr.pack(pady=6)
        e_desc = ctk.CTkEntry(pop, width=320, placeholder_text="نوع الجهاز / طبيعة الصيانة", font=FONT_BODY)
        e_desc.pack(pady=6)
        e_date = ctk.CTkEntry(pop, width=320, placeholder_text="موعد الصيانة (YYYY-MM-DD)", font=FONT_BODY)
        e_date.pack(pady=6)
        e_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

        def save():
            name, phone, addr, desc, m_date = e_name.get().strip(), e_phone.get().strip(), e_addr.get().strip(), e_desc.get().strip(), e_date.get().strip()
            if not (name and phone and desc):
                self.show_toast("تنبيه", "اسم العميل، الهاتف، وتفاصيل الصيانة حقول إلزاميّة!", "warning")
                return
            conn = sqlite3.connect("golden_life.db")
            conn.cursor().execute(
                "INSERT INTO ac_maintenance (client_name, client_phone, address, fault_desc, maint_date) VALUES (?, ?, ?, ?, ?)",
                (name, phone, addr, desc, m_date))
            conn.commit()
            conn.close()
            self.show_toast("نجح الحفظ", "تم حفظ بيانات وموعد صيانة العميل بنجاح!", "success")
            pop.destroy()
            self.view_maintenance_alerts_section()

        ctk.CTkButton(pop, text="💾 حفظ موعد الصيانة", font=FONT_BTN, fg_color=colors["GREEN_BTN"], width=320, height=38,
                      command=save).pack(pady=15)

    # ==========================================
    # 🌟 جدول المهام
    # ==========================================
    def view_tech_shifts_section(self):
        self.clear_content()
        box = ctk.CTkFrame(self.content_area, fg_color=colors["PANEL_BG"], corner_radius=18, border_width=1,
                           border_color=colors["TEXT_MUTED"])
        box.pack(fill="both", expand=True, padx=5, pady=5)
        head_frame = ctk.CTkFrame(box, fg_color="transparent")
        head_frame.pack(fill="x", pady=15, padx=20)
        ctk.CTkLabel(head_frame, text="👷 جدولة مهام وإسناد الفنيين بالاسم", font=FONT_TITLE,
                     text_color=colors["GOLD_ACCENT"]).pack(side="right" if current_lang == "ar" else "left")

        btn_fr = ctk.CTkFrame(head_frame, fg_color="transparent")
        btn_fr.pack(side="left" if current_lang == "ar" else "right")
        ctk.CTkButton(btn_fr, text="📊 Excel", font=FONT_BTN, fg_color=colors["GREEN_BTN"], height=36, width=90,
                      command=lambda: self.export_to_excel(tree_s, "جدول المهام")).pack(side="right", padx=3)
        ctk.CTkButton(btn_fr, text="🖨️ طباعة", font=FONT_BTN, fg_color=colors["PURPLE_BTN"], height=36, width=90,
                      command=lambda: self.print_report_modal(tree_s, "جدول المهام")).pack(side="right", padx=3)
        ctk.CTkButton(btn_fr, text="➕ إسناد مهمة", font=FONT_BTN, fg_color=colors["BLUE_BTN"], height=36, width=120,
                      command=self.popup_add_shift).pack(side="right", padx=3)

        t_box = ctk.CTkFrame(box, fg_color=colors["BG_MAIN"], corner_radius=12, border_width=1,
                             border_color=colors["TEXT_MUTED"])
        t_box.pack(fill="both", expand=True, padx=20, pady=10)

        search_entry = ctk.CTkEntry(t_box, placeholder_text="🔍 ابحث باسم الفني أو تفاصيل المهمة...", font=FONT_BODY,
                                    height=38, justify="right" if current_lang == "ar" else "left")
        search_entry.pack(fill="x", padx=10, pady=(10, 5))

        tree_s = ttk.Treeview(t_box, columns=("id", "tech_name", "task", "date"), show="headings", height=10)
        for col, txt in zip(tree_s["columns"],
                            ["م", "اسم الفني المسؤول", "تفاصيل المهمة / التركيبات", "التاريخ"]): tree_s.heading(col,
                                                                                                                text=txt)
        tree_s.pack(fill="both", expand=True, padx=10, pady=5)

        conn = sqlite3.connect("golden_life.db")
        all_shifts = conn.cursor().execute("SELECT * FROM tech_shifts").fetchall()
        conn.close()

        def load_shifts_filtered(query=""):
            for item in tree_s.get_children(): tree_s.delete(item)
            q = query.strip().lower()
            for r in all_shifts:
                if not q or any(q in str(c).lower() for c in r):
                    tree_s.insert("", "end", values=r)

        load_shifts_filtered()
        search_entry.bind("<KeyRelease>", lambda e: load_shifts_filtered(search_entry.get()))

    def popup_add_shift(self):
        pop = ctk.CTkToplevel(self)
        pop.title("إسناد مهمة لفني بالاسم")
        pop.geometry("400x420")
        pop.grab_set()
        ctk.CTkLabel(pop, text="👷 إسناد مهمة لفني", font=FONT_SUBTITLE, text_color=colors["GOLD_ACCENT"]).pack(pady=15)

        ctk.CTkLabel(pop, text="اختر اسم الفني:", font=FONT_BODY, text_color=colors["TEXT_MUTED"]).pack(
            anchor="e" if current_lang == "ar" else "w", padx=40)
        e_tech = ctk.CTkOptionMenu(pop, width=320,
                                   values=["أحمد", "محمد", "محمود", "إبراهيم", "أحمد + محمد", "محمود + إبراهيم"],
                                   fg_color=colors["BLUE_BTN"], button_color=colors["BLUE_BTN"])
        e_tech.pack(pady=5)

        ctk.CTkLabel(pop, text="تفاصيل المهمة:", font=FONT_BODY, text_color=colors["TEXT_MUTED"]).pack(
            anchor="e" if current_lang == "ar" else "w", padx=40)
        e_task = ctk.CTkEntry(pop, width=320, placeholder_text="مثال: تركيب تكييف - طنطا", font=FONT_BODY)
        e_task.pack(pady=5)

        def save():
            tech_name, t_desc = e_tech.get(), e_task.get().strip()
            if not t_desc:
                self.show_toast("تنبيه", "يرجى كتابة تفاصيل المهمة!", "warning")
                return
            today = datetime.now().strftime("%Y-%m-%d")
            conn = sqlite3.connect("golden_life.db")
            conn.cursor().execute("INSERT INTO tech_shifts (tech_name, task_desc, date_str) VALUES (?, ?, ?)",
                                  (tech_name, t_desc, today))
            conn.commit()
            conn.close()
            self.show_toast("نجح الإسناد", "تم إسناد المهمة للفني بنجاح!", "success")
            pop.destroy()
            self.view_tech_shifts_section()

        ctk.CTkButton(pop, text="💾 حفظ إسناد المهمة", font=FONT_BTN, fg_color=colors["GREEN_BTN"], width=320, height=38,
                      command=save).pack(pady=20)

    # ==========================================
    # 🌟 إدارة العدة والمعدات
    # ==========================================
    def view_tools_section(self):
        self.clear_content()
        outer_box = ctk.CTkFrame(self.content_area, fg_color=colors["BG_MAIN"], corner_radius=0)
        outer_box.pack(fill="both", expand=True, padx=5, pady=5)

        top_bar = ctk.CTkFrame(outer_box, fg_color="transparent")
        top_bar.pack(fill="x", pady=10, padx=10)

        ctk.CTkLabel(top_bar, text="🧰 إدارة العدة والمعدات", font=FONT_TITLE, text_color=colors["GOLD_ACCENT"]).pack(
            side="right" if current_lang == "ar" else "left")
        ctk.CTkButton(top_bar, text="➕ إضافة شنطة جديدة", font=FONT_BTN, fg_color=colors["GOLD_ACCENT"],
                      hover_color=colors["GOLD_HOVER"], text_color=colors["BG_MAIN"], width=160, height=38,
                      command=self.popup_add_bag).pack(side="left" if current_lang == "ar" else "right")

        canvas = ctk.CTkCanvas(outer_box, bg=colors["BG_MAIN"], highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(outer_box, orientation="vertical", command=canvas.yview)
        scrollable_frame = ctk.CTkFrame(canvas, fg_color="transparent")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left" if current_lang == "ar" else "right", fill="both", expand=True, padx=5)
        scrollbar.pack(side="right" if current_lang == "ar" else "left", fill="y")

        conn = sqlite3.connect("golden_life.db")
        bags = conn.cursor().execute("SELECT id, bag_category, bag_name, tools_list FROM tools_bags").fetchall()
        conn.close()

        row_f = None
        for i, (bag_id, cat, name, tools) in enumerate(bags):
            if i % 2 == 0:
                row_f = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
                row_f.pack(fill="x", pady=8, padx=5)

            card = ctk.CTkFrame(row_f, fg_color=colors["PANEL_BG"], corner_radius=16, width=540, height=260,
                                border_width=1, border_color=colors["TEXT_MUTED"])
            card.pack(side="right" if (i % 2 == 0 and current_lang == "ar") or (
                        i % 2 != 0 and current_lang == "en") else "left", padx=10)
            card.pack_propagate(False)

            c_header = ctk.CTkFrame(card, fg_color="transparent")
            c_header.pack(fill="x", padx=15, pady=12)

            badge_lbl = ctk.CTkLabel(c_header, text=f"🧰 {cat}", font=(FONT_FAMILY, 10, "bold"),
                                     fg_color=colors["GREEN_BTN"], text_color="#FFFFFF", corner_radius=6)
            badge_lbl.pack(side="left" if current_lang == "ar" else "right", padx=5)

            title_lbl = ctk.CTkLabel(c_header, text=name, font=(FONT_FAMILY, 13, "bold"),
                                     text_color=colors["TEXT_COLOR"])
            title_lbl.pack(side="right" if current_lang == "ar" else "left", padx=5)

            ctk.CTkLabel(card, text=f"محتويات 🔑 {name}:", font=(FONT_FAMILY, 10), text_color=colors["TEXT_MUTED"],
                         anchor="e" if current_lang == "ar" else "w").pack(fill="x", padx=18, pady=(0, 2))

            txt_box = ctk.CTkTextbox(card, height=75, fg_color=colors["BG_MAIN"], text_color=colors["TEXT_COLOR"],
                                     font=(FONT_FAMILY, 11), corner_radius=8, border_width=1,
                                     border_color=colors["TEXT_MUTED"])
            txt_box.pack(fill="x", padx=15, pady=2)
            txt_box.insert("1.0", tools or "")

            add_f = ctk.CTkFrame(card, fg_color="transparent")
            add_f.pack(fill="x", padx=15, pady=8)

            tool_entry = ctk.CTkEntry(add_f, placeholder_text="أضف أداة...", font=(FONT_FAMILY, 11), height=34,
                                      fg_color=colors["BG_MAIN"], text_color=colors["TEXT_COLOR"],
                                      border_color=colors["TEXT_MUTED"],
                                      justify="right" if current_lang == "ar" else "left")
            tool_entry.pack(side="right" if current_lang == "ar" else "left", fill="x", expand=True,
                            padx=(5, 0) if current_lang == "ar" else (0, 5))

            def add_tool_to_bag(b_id=bag_id, entry=tool_entry, tbox=txt_box):
                new_tool = entry.get().strip()
                if new_tool:
                    current_txt = tbox.get("1.0", "end-1c")
                    updated = f"{current_txt}, {new_tool}" if current_txt else new_tool
                    tbox.delete("1.0", "end")
                    tbox.insert("1.0", updated)
                    entry.delete(0, tk.END)
                    conn = sqlite3.connect("golden_life.db")
                    conn.cursor().execute("UPDATE tools_bags SET tools_list=? WHERE id=?", (updated, b_id))
                    conn.commit()
                    conn.close()

            ctk.CTkButton(add_f, text="+ إضافة", font=(FONT_FAMILY, 11, "bold"), fg_color=colors["GOLD_ACCENT"],
                          hover_color=colors["GOLD_HOVER"], text_color=colors["BG_MAIN"], width=75, height=34,
                          command=add_tool_to_bag).pack(side="left" if current_lang == "ar" else "right")

            footer_f = ctk.CTkFrame(card, fg_color="transparent")
            footer_f.pack(fill="x", padx=15, pady=5)

            def save_bag_changes(b_id=bag_id, tbox=txt_box, b_name=name):
                final_text = tbox.get("1.0", "end-1c")
                conn = sqlite3.connect("golden_life.db")
                conn.cursor().execute("UPDATE tools_bags SET tools_list=? WHERE id=?", (final_text, b_id))
                conn.commit()
                conn.close()
                self.show_toast("نجح الحفظ", f"تم حفظ محتويات شنطة {b_name} بنجاح!", "success")

            ctk.CTkButton(footer_f, text=f"💾 حفظ 🧰 {name}", font=(FONT_FAMILY, 11, "bold"),
                          fg_color=colors["TEXT_MUTED"], hover_color=colors["TEXT_COLOR"], text_color="white",
                          height=32, command=save_bag_changes).pack(fill="x")

    def popup_add_bag(self):
        pop = ctk.CTkToplevel(self)
        pop.title("إضافة شنطة عدة جديدة")
        pop.geometry("380x320")
        pop.grab_set()
        ctk.CTkLabel(pop, text="🧰 إضافة شنطة جديدة", font=FONT_SUBTITLE, text_color=colors["GOLD_ACCENT"]).pack(pady=15)
        e_cat = ctk.CTkEntry(pop, width=280, placeholder_text="التصنيف (مثال: صيانة / عدة)", font=FONT_BODY)
        e_cat.pack(pady=6)
        e_name = ctk.CTkEntry(pop, width=280, placeholder_text="اسم الشنطة (مثال: شنطة الكهرباء 2)", font=FONT_BODY)
        e_name.pack(pady=6)
        e_tools = ctk.CTkEntry(pop, width=280, placeholder_text="المحتويات (مثال: مفك، بانس)", font=FONT_BODY)
        e_tools.pack(pady=6)

        def save():
            cat, name, tools = e_cat.get().strip(), e_name.get().strip(), e_tools.get().strip()
            if not (cat and name):
                self.show_toast("تنبيه", "التصنيف والاسم إلزاميّان!", "warning")
                return
            conn = sqlite3.connect("golden_life.db")
            conn.cursor().execute("INSERT INTO tools_bags (bag_category, bag_name, tools_list) VALUES (?, ?, ?)",
                                  (cat, name, tools))
            conn.commit()
            conn.close()
            self.show_toast("نجح", "تمت إضافة الشنطة بنجاح!", "success")
            pop.destroy()
            self.view_tools_section()

        ctk.CTkButton(pop, text="💾 حفظ الشنطة", font=FONT_BTN, fg_color=colors["GREEN_BTN"], width=280, height=38,
                      command=save).pack(pady=15)

    # ==========================================
    # 🌟 العملاء
    # ==========================================
    def view_debts_section(self):
        self.clear_content()
        box = ctk.CTkFrame(self.content_area, fg_color=colors["PANEL_BG"], corner_radius=18, border_width=1,
                           border_color=colors["TEXT_MUTED"])
        box.pack(fill="both", expand=True, padx=5, pady=5)

        top_f = ctk.CTkFrame(box, fg_color="transparent")
        top_f.pack(fill="x", pady=15, padx=20)
        ctk.CTkLabel(top_f, text="⚠️ إدارة العملاء والديون والشكاوى", font=FONT_TITLE,
                     text_color=colors["GOLD_ACCENT"]).pack(side="right" if current_lang == "ar" else "left")

        btn_fr = ctk.CTkFrame(top_f, fg_color="transparent")
        btn_fr.pack(side="left" if current_lang == "ar" else "right")
        ctk.CTkButton(btn_fr, text="📊 Excel", font=FONT_BTN, fg_color=colors["GREEN_BTN"], width=90, height=36,
                      command=lambda: self.export_to_excel(tree, "العملاء")).pack(side="right", padx=3)
        ctk.CTkButton(btn_fr, text="🖨️ طباعة", font=FONT_BTN, fg_color=colors["PURPLE_BTN"], width=90, height=36,
                      command=lambda: self.print_report_modal(tree, "العملاء")).pack(side="right", padx=3)
        ctk.CTkButton(btn_fr, text="➕ تسجيل شكوى", font=FONT_BTN, fg_color=colors["RED_BTN"], height=36, width=120,
                      command=self.popup_add_complaint).pack(side="right", padx=3)

        search_entry = ctk.CTkEntry(box, placeholder_text="🔍 ابحث في العملاء (اسم العميل، الهاتف)...", font=FONT_BODY,
                                    height=38, justify="right" if current_lang == "ar" else "left")
        search_entry.pack(fill="x", padx=20, pady=(0, 5))

        tree = ttk.Treeview(box, columns=("id", "name", "phone", "addr", "complaint", "debt"), show="headings",
                            height=10)
        for col, txt in zip(tree["columns"], ["م", "اسم العميل", "الهاتف", "العنوان", "تفاصيل الشكوى",
                                              "المبلغ المترتب / الدين"]): tree.heading(col, text=txt)
        tree.pack(fill="both", expand=True, padx=20, pady=5)

        conn = sqlite3.connect("golden_life.db")
        all_debts = []
        for row in conn.cursor().execute("SELECT * FROM customer_debts"):
            all_debts.append((row[0], row[1], row[2], row[3], row[4], self.format_amount(row[5])))
        conn.close()

        def load_debts_filtered(query=""):
            for item in tree.get_children(): tree.delete(item)
            q = query.strip().lower()
            for r in all_debts:
                if not q or any(q in str(c).lower() for c in r):
                    tree.insert("", "end", values=r)

        load_debts_filtered()
        search_entry.bind("<KeyRelease>", lambda e: load_debts_filtered(search_entry.get()))

    def popup_add_complaint(self):
        pop = ctk.CTkToplevel(self)
        pop.title("تسجيل شكوى عميل جديدة")
        pop.geometry("400x450")
        pop.grab_set()
        ctk.CTkLabel(pop, text="⚠️ تسجيل شكوى عميل مع بياناته", font=FONT_SUBTITLE, text_color=colors["RED_BTN"]).pack(
            pady=15)

        e_name = ctk.CTkEntry(pop, width=320, placeholder_text="اسم العميل", font=FONT_BODY)
        e_name.pack(pady=6)
        e_phone = ctk.CTkEntry(pop, width=320, placeholder_text="رقم الهاتف", font=FONT_BODY)
        e_phone.pack(pady=6)
        e_addr = ctk.CTkEntry(pop, width=320, placeholder_text="العنوان", font=FONT_BODY)
        e_addr.pack(pady=6)
        e_comp = ctk.CTkEntry(pop, width=320, placeholder_text="تفاصيل الشكوى", font=FONT_BODY)
        e_comp.pack(pady=6)
        e_debt = ctk.CTkEntry(pop, width=320, placeholder_text="المبلغ المالي المترتب / الدين (اختياري)",
                              font=FONT_BODY)
        e_debt.pack(pady=6)

        def save():
            name, phone, addr, comp = e_name.get().strip(), e_phone.get().strip(), e_addr.get().strip(), e_comp.get().strip()
            debt = float(e_debt.get().strip() or 0)
            if not (name and phone and comp):
                self.show_toast("تنبيه", "الاسم، الهاتف، وتفاصيل الشكوى حقول إلزاميّة!", "warning")
                return
            conn = sqlite3.connect("golden_life.db")
            conn.cursor().execute(
                "INSERT INTO customer_debts (name, phone, address, complaint, debt_amount) VALUES (?, ?, ?, ?, ?)",
                (name, phone, addr, comp, debt))
            conn.commit()
            conn.close()
            log_activity(self.current_user, "تسجيل شكوى", f"عميل: {name} - الشكوى: {comp}")
            self.show_toast("نجاح", "تم تسجيل الشكوى وحفظ بيانات العميل بنجاح!", "success")
            pop.destroy()
            self.view_debts_section()

        ctk.CTkButton(pop, text="💾 حفظ الشكوى والبيانات", font=FONT_BTN, fg_color=colors["GREEN_BTN"], width=320,
                      height=38, command=save).pack(pady=15)

    # ==========================================
    # 🌟 إدارة الموردين
    # ==========================================
    def view_suppliers_section(self):
        if self.current_role != 'manager':
            self.show_toast("صلاحيات", "عذراً، هذه الصلاحية للمديرين فقط!", "error")
            return
        self.clear_content()
        box = ctk.CTkFrame(self.content_area, fg_color=colors["PANEL_BG"], corner_radius=18, border_width=1,
                           border_color=colors["TEXT_MUTED"])
        box.pack(fill="both", expand=True, padx=5, pady=5)

        top_f = ctk.CTkFrame(box, fg_color="transparent")
        top_f.pack(fill="x", pady=15, padx=20)
        ctk.CTkLabel(top_f, text="🚚 سجل الموردين والشركات المعتمدة", font=FONT_TITLE,
                     text_color=colors["GOLD_ACCENT"]).pack(side="right" if current_lang == "ar" else "left")

        btn_fr = ctk.CTkFrame(top_f, fg_color="transparent")
        btn_fr.pack(side="left" if current_lang == "ar" else "right")
        ctk.CTkButton(btn_fr, text="📊 Excel", font=FONT_BTN, fg_color=colors["GREEN_BTN"], width=90, height=36,
                      command=lambda: self.export_to_excel(tree, "الموردين")).pack(side="right", padx=3)
        ctk.CTkButton(btn_fr, text="🖨️ طباعة", font=FONT_BTN, fg_color=colors["PURPLE_BTN"], width=90, height=36,
                      command=lambda: self.print_report_modal(tree, "الموردين")).pack(side="right", padx=3)
        ctk.CTkButton(btn_fr, text="➕ إضافة مورد", font=FONT_BTN, fg_color=colors["BLUE_BTN"], height=36, width=120,
                      command=self.popup_add_supplier).pack(side="right", padx=3)

        search_entry = ctk.CTkEntry(box, placeholder_text="🔍 ابحث في الموردين (اسم الشركة، الصنف)...", font=FONT_BODY,
                                    height=38, justify="right" if current_lang == "ar" else "left")
        search_entry.pack(fill="x", padx=20, pady=(0, 5))

        tree = ttk.Treeview(box, columns=("id", "name", "phone", "prod"), show="headings", height=10)
        for col, txt in zip(tree["columns"],
                            ["م", "اسم المورد / الشركة", "رقم الهاتف", "طبيعة التوريد والأصناف"]): tree.heading(col,
                                                                                                                text=txt)
        tree.pack(fill="both", expand=True, padx=20, pady=5)

        conn = sqlite3.connect("golden_life.db")
        all_sup = conn.cursor().execute("SELECT * FROM suppliers").fetchall()
        conn.close()

        def load_sup_filtered(query=""):
            for item in tree.get_children(): tree.delete(item)
            q = query.strip().lower()
            for r in all_sup:
                if not q or any(q in str(c).lower() for c in r):
                    tree.insert("", "end", values=r)

        load_sup_filtered()
        search_entry.bind("<KeyRelease>", lambda e: load_sup_filtered(search_entry.get()))

    def popup_add_supplier(self):
        pop = ctk.CTkToplevel(self)
        pop.title("إضافة مورد جديد")
        pop.geometry("380x360")
        pop.grab_set()
        ctk.CTkLabel(pop, text="🚚 إضافة بيانات مورد جديد", font=FONT_SUBTITLE, text_color=colors["GOLD_ACCENT"]).pack(
            pady=15)

        e_name = ctk.CTkEntry(pop, width=300, placeholder_text="اسم المورد أو الشركة", font=FONT_BODY)
        e_name.pack(pady=8)
        e_phone = ctk.CTkEntry(pop, width=300, placeholder_text="رقم التليفون", font=FONT_BODY)
        e_phone.pack(pady=8)
        e_prod = ctk.CTkEntry(pop, width=300, placeholder_text="طبيعة التوريد والأصناف", font=FONT_BODY)
        e_prod.pack(pady=8)

        def save():
            name, phone, prod = e_name.get().strip(), e_phone.get().strip(), e_prod.get().strip()
            if not (name and phone):
                self.show_toast("تنبيه", "اسم المورد ورقم الهاتف حقول إلزاميّة!", "warning")
                return
            conn = sqlite3.connect("golden_life.db")
            conn.cursor().execute("INSERT INTO suppliers (name, phone, product) VALUES (?, ?, ?)", (name, phone, prod))
            conn.commit()
            conn.close()
            self.show_toast("نجح", "تمت إضافة المورد بنجاح!", "success")
            pop.destroy()
            self.view_suppliers_section()

        ctk.CTkButton(pop, text="💾 حفظ المورد", font=FONT_BTN, fg_color=colors["GREEN_BTN"], width=300, height=38,
                      command=save).pack(pady=15)

    # ==========================================
    # 🌟 المحادثة
    # ==========================================
    def view_chat_section(self):
        self.clear_content()
        box = ctk.CTkFrame(self.content_area, fg_color=colors["PANEL_BG"], corner_radius=18, border_width=1,
                           border_color=colors["TEXT_MUTED"])
        box.pack(fill="both", expand=True, padx=5, pady=5)

        head_frame = ctk.CTkFrame(box, fg_color="transparent")
        head_frame.pack(fill="x", pady=15, padx=20)
        ctk.CTkLabel(head_frame, text="💬 غرفة محادثة الفريق وحالة الفنيين", font=FONT_TITLE,
                     text_color=colors["GOLD_ACCENT"]).pack(side="right" if current_lang == "ar" else "left")

        call_btns_frame = ctk.CTkFrame(head_frame, fg_color="transparent")
        call_btns_frame.pack(side="left" if current_lang == "ar" else "right")
        ctk.CTkButton(call_btns_frame, text="📞 مكالمة صوتية", font=FONT_BTN, fg_color=colors["GREEN_BTN"], height=36,
                      width=110, command=self.start_voice_call).pack(side="right", padx=3)
        ctk.CTkButton(call_btns_frame, text="🟢 حالة الفنيين", font=FONT_BTN, fg_color=colors["PURPLE_BTN"], height=36,
                      width=110, command=self.open_technicians_status_modal).pack(side="right", padx=3)

        self.chat_box = ctk.CTkFrame(box, fg_color=colors["BG_MAIN"], corner_radius=14, border_width=1,
                                     border_color=colors["TEXT_MUTED"])
        self.chat_box.pack(fill="both", expand=True, padx=20, pady=5)

        input_frame = ctk.CTkFrame(box, fg_color="transparent")
        input_frame.pack(fill="x", pady=15, padx=20)

        ctk.CTkButton(input_frame, text="🎤 فويس", width=70, height=44, fg_color=colors["PURPLE_BTN"], font=FONT_BTN,
                      command=self.send_voice_note).pack(side="right" if current_lang == "ar" else "left", padx=3)
        ctk.CTkButton(input_frame, text="📷 صورة", width=70, height=44, fg_color=colors["BLUE_BTN"], font=FONT_BTN,
                      command=self.send_image_message).pack(side="right" if current_lang == "ar" else "left", padx=3)

        self.msg_entry = ctk.CTkEntry(input_frame, font=FONT_BODY, height=44,
                                      placeholder_text="اكتب رسالتك النصية هنا...",
                                      justify="right" if current_lang == "ar" else "left")
        self.msg_entry.pack(side="right" if current_lang == "ar" else "left", fill="x", expand=True,
                            padx=(8, 3) if current_lang == "ar" else (3, 8))
        self.msg_entry.bind("<Return>", lambda e: self.send_chat_msg())

        ctk.CTkButton(input_frame, text="إرسال 🚀", width=100, height=44, fg_color=colors["GOLD_ACCENT"],
                      text_color=colors["BG_MAIN"], font=FONT_BTN, command=self.send_chat_msg).pack(
            side="left" if current_lang == "ar" else "right")

        self.load_chat_messages()

    def load_chat_messages(self):
        for widget in self.chat_box.winfo_children(): widget.destroy()
        conn = sqlite3.connect("golden_life.db")
        messages = conn.cursor().execute(
            "SELECT sender, role, message, timestamp FROM group_chat ORDER BY id DESC LIMIT 6").fetchall()
        conn.close()
        if not messages:
            ctk.CTkLabel(self.chat_box, text="لا توجد رسائل حديثة.. ابدأ المحادثة الآن! 💡", font=FONT_BODY,
                         text_color=colors["TEXT_MUTED"]).pack(pady=50)
            return
        for sender, role, msg, time_str in reversed(messages):
            is_me = (sender == self.current_user)
            row = ctk.CTkFrame(self.chat_box, fg_color="transparent")
            row.pack(fill="x", pady=6, padx=12)
            bubble = ctk.CTkFrame(row, fg_color=colors["GREEN_BTN"] if is_me else colors["PANEL_BG"], corner_radius=14,
                                  border_width=1, border_color=colors["GOLD_ACCENT"] if is_me else colors["TEXT_MUTED"])
            bubble.pack(
                side="right" if (is_me and current_lang == "ar") or (not is_me and current_lang == "en") else "left",
                padx=5)
            badge = "👑 مدير" if role == 'manager' else "🧑‍💻 موظف"
            ctk.CTkLabel(bubble, text=f"{sender} ({badge}) • {time_str}", font=(FONT_FAMILY, 9, "bold"),
                         text_color=colors["GOLD_ACCENT"] if is_me else colors["TEXT_MUTED"]).pack(
                anchor="e" if current_lang == "ar" else "w", padx=12, pady=(6, 2))
            ctk.CTkLabel(bubble, text=msg, font=FONT_BODY, text_color=colors["TEXT_COLOR"], wraplength=550,
                         justify="right" if current_lang == "ar" else "left").pack(
                anchor="e" if current_lang == "ar" else "w", padx=12, pady=(0, 8))

    def send_chat_msg(self):
        msg = self.msg_entry.get().strip()
        if msg:
            conn = sqlite3.connect("golden_life.db")
            now = datetime.now().strftime("%H:%M")
            conn.cursor().execute("INSERT INTO group_chat (sender, role, message, timestamp) VALUES (?, ?, ?, ?)",
                                  (self.current_user, self.current_role, msg, now))
            conn.commit()
            conn.close()
            self.msg_entry.delete(0, tk.END)
            self.load_chat_messages()

    def send_image_message(self):
        file_path = filedialog.askopenfilename(title="اختر صورة للإرسال",
                                               filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            img_name = os.path.basename(file_path)
            conn = sqlite3.connect("golden_life.db")
            now = datetime.now().strftime("%H:%M")
            msg_text = f"📷 [مرفق صورة]: {img_name}"
            conn.cursor().execute("INSERT INTO group_chat (sender, role, message, timestamp) VALUES (?, ?, ?, ?)",
                                  (self.current_user, self.current_role, msg_text, now))
            conn.commit()
            conn.close()
            self.load_chat_messages()
            self.show_toast("تم الإرسال", "تم إرسال الصورة بنجاح للشات!", "success")

    def send_voice_note(self):
        conn = sqlite3.connect("golden_life.db")
        now = datetime.now().strftime("%H:%M")
        msg_text = "🎤 [رسالة صوتية - Voice Note 0:14s]"
        conn.cursor().execute("INSERT INTO group_chat (sender, role, message, timestamp) VALUES (?, ?, ?, ?)",
                              (self.current_user, self.current_role, msg_text, now))
        conn.commit()
        conn.close()
        self.load_chat_messages()
        self.show_toast("تسجيل صوتي", "تم تسجيل وإرسال الفويس بنجاح!", "success")

    def start_voice_call(self):
        self.show_toast("مكالمة صوتية", f"جاري بدء مكالمة صوتية جماعية مع الفريق...\nمتصل الآن: {self.current_user}",
                        "info")

    def open_technicians_status_modal(self):
        win = ctk.CTkToplevel(self)
        win.title("🟢 حالة اتصال الفنيين والمستخدمين")
        win.geometry("420x450")
        win.grab_set()
        ctk.CTkLabel(win, text="👥 حالة الطاقم والفنيين الميدانيين", font=FONT_TITLE,
                     text_color=colors["GOLD_ACCENT"]).pack(pady=(20, 10))
        box = ctk.CTkFrame(win, fg_color=colors["PANEL_BG"], corner_radius=15, border_width=1,
                           border_color=colors["TEXT_MUTED"])
        box.pack(fill="both", expand=True, padx=20, pady=10)
        conn = sqlite3.connect("golden_life.db")
        users = conn.cursor().execute("SELECT username, role, status, last_seen FROM users").fetchall()
        conn.close()
        for uname, urole, ustat, ulast in users:
            card = ctk.CTkFrame(box, fg_color=colors["BG_MAIN"], corner_radius=10)
            card.pack(fill="x", padx=12, pady=6)
            is_on = (ustat == 'online')
            ctk.CTkLabel(card, text=f"{uname} ({'مدير' if urole == 'manager' else 'فني'})", font=FONT_BTN,
                         text_color=colors["TEXT_COLOR"]).pack(side="right" if current_lang == "ar" else "left",
                                                               padx=14, pady=10)
            ctk.CTkLabel(card, text="🟢 متصل الآن" if is_on else f"⚪ غير متصل ({ulast or 'غير محدد'})",
                         font=(FONT_FAMILY, 9, "bold"),
                         text_color=colors["GREEN_BTN"] if is_on else colors["TEXT_MUTED"]).pack(
                side="left" if current_lang == "ar" else "right", padx=14)

    # ==========================================
    # 🌟 القائمة الرئيسية (Dashboard)
    # ==========================================
    def view_dashboard(self):
        self.clear_content()
        box = ctk.CTkFrame(self.content_area, fg_color=colors["PANEL_BG"], corner_radius=18, border_width=1,
                           border_color=colors["TEXT_MUTED"])
        box.pack(fill="both", expand=True, padx=5, pady=5)
        top = ctk.CTkFrame(box, fg_color="transparent")
        top.pack(fill="x", pady=10, padx=20)
        ctk.CTkLabel(top, text="📊 القائمة الرئيسية والمؤشرات الحية", font=FONT_TITLE,
                     text_color=colors["GOLD_ACCENT"]).pack(side="right" if current_lang == "ar" else "left")

        conn = sqlite3.connect("golden_life.db")
        c = conn.cursor()
        ac_qty = c.execute("SELECT COALESCE(SUM(quantity), 0) FROM ac_inventory").fetchone()[0]
        flt_qty = c.execute("SELECT COALESCE(SUM(quantity), 0) FROM filter_inventory").fetchone()[0]
        ac_sales_tot = c.execute("SELECT COALESCE(SUM(amount_due), 0) FROM ac_sales").fetchone()[0]
        flt_sales_tot = c.execute("SELECT COALESCE(SUM(amount_due), 0) FROM filter_sales").fetchone()[0]
        exp_paid = c.execute("SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE status='مدفوع'").fetchone()[0]
        monthly_profit = max(0, (ac_sales_tot + flt_sales_tot) - exp_paid)
        installations_count = c.execute("SELECT COUNT(*) FROM tech_shifts").fetchone()[0]
        filters_alerts = c.execute("SELECT COUNT(*) FROM filter_inventory WHERE quantity < 5").fetchone()[0]
        debts_tot = c.execute("SELECT COALESCE(SUM(debt_amount), 0) FROM customer_debts").fetchone()[0]
        conn.close()

        cards = ctk.CTkFrame(box, fg_color="transparent")
        cards.pack(fill="x", padx=20, pady=5)

        def add_clickable_card(title, val, col, command):
            c_box = ctk.CTkFrame(cards, height=85, corner_radius=12, fg_color=col, cursor="hand2")
            c_box.pack(side="right" if current_lang == "ar" else "left", fill="x", expand=True, padx=2)
            c_box.pack_propagate(False)
            lbl_title = ctk.CTkLabel(c_box, text=title, font=(FONT_FAMILY, 10, "bold"), text_color="white",
                                     cursor="hand2")
            lbl_title.pack(pady=(8, 2))
            lbl_title.bind("<Button-1>", lambda e: command())
            lbl_val = ctk.CTkLabel(c_box, text=val, font=(FONT_FAMILY, 12, "bold"), text_color="white", cursor="hand2")
            lbl_val.pack()
            lbl_val.bind("<Button-1>", lambda e: command())
            c_box.bind("<Button-1>", lambda e: command())

        display_ac_qty = self.format_qty(ac_qty)
        display_flt_qty = self.format_qty(flt_qty)

        def safe_view_ac():
            if self.current_role == 'manager':
                self.view_ac_section()
            else:
                self.show_toast("صلاحيات", "هذا القسم مخصص للمديرين فقط!", "error")

        def safe_view_filter():
            if self.current_role == 'manager':
                self.view_filters_section()
            else:
                self.show_toast("صلاحيات", "هذا القسم مخصص للمديرين فقط!", "error")

        def safe_view_profits():
            if self.current_role == 'manager':
                self.view_profits_section()
            else:
                self.show_toast("صلاحيات", "هذا القسم مخصص للمديرين فقط!", "error")

        add_clickable_card("❄️ التكيفات", display_ac_qty, colors["BLUE_BTN"], safe_view_ac)
        add_clickable_card("💧 الفلاتر", display_flt_qty, colors["GREEN_BTN"], safe_view_filter)
        add_clickable_card("📈 الارباح", self.format_amount(monthly_profit), colors["GREEN_BTN"], safe_view_profits)
        add_clickable_card("🛠️ التركيبات", f"{installations_count} مهمة", "#00B4D8", self.view_tech_shifts_section)
        add_clickable_card("🔔 صيانة الفلاتر", f"{filters_alerts} تنبيه", colors["GOLD_ACCENT"],
                           self.view_maintenance_alerts_section)
        add_clickable_card("🚨 العملاء", self.format_amount(debts_tot), colors["RED_BTN"], self.view_debts_section)

        summary_frame = ctk.CTkFrame(box, fg_color=colors["BG_MAIN"], corner_radius=12, border_width=1,
                                     border_color=colors["GOLD_ACCENT"])
        summary_frame.pack(fill="x", padx=20, pady=8)
        sum_text = f"✨ ملخص العمليات والأرباح: إجمالي التركيبات ({installations_count}) | عملاء وديون ({self.format_amount(debts_tot)})"
        sum_lbl = ctk.CTkLabel(summary_frame, text=sum_text, font=(FONT_FAMILY, 11, "bold"),
                               text_color=colors["GOLD_ACCENT"])
        sum_lbl.pack(pady=10, padx=15)

        mid = ctk.CTkFrame(box, fg_color="transparent")
        mid.pack(fill="both", expand=True, padx=20, pady=5)
        r_box = ctk.CTkFrame(mid, fg_color=colors["BG_MAIN"], corner_radius=14, border_width=1,
                             border_color=colors["TEXT_MUTED"])
        r_box.pack(side="right" if current_lang == "ar" else "left", fill="both", expand=True,
                   padx=(5, 0) if current_lang == "ar" else (0, 5))
        ctk.CTkLabel(r_box, text="⚡ اختصارات العمليات السريعة", font=FONT_SUBTITLE,
                     text_color=colors["GOLD_ACCENT"]).pack(pady=8, padx=15,
                                                            anchor="e" if current_lang == "ar" else "w")
        b_grid = ctk.CTkFrame(r_box, fg_color="transparent")
        b_grid.pack(fill="x", padx=10)

        if self.current_role == 'manager':
            ctk.CTkButton(b_grid, text="➕ إضافة تكيف", font=FONT_BTN, fg_color=colors["GREEN_BTN"], height=36,
                          text_color="white", command=lambda: self.popup_add_product("ac")).pack(
                side="right" if current_lang == "ar" else "left", fill="x", expand=True, padx=2, pady=2)
            ctk.CTkButton(b_grid, text="➕ إضافة فلتر", font=FONT_BTN, fg_color=colors["BLUE_BTN"], height=36,
                          text_color="white", command=lambda: self.popup_add_product("filter")).pack(
                side="right" if current_lang == "ar" else "left", fill="x", expand=True, padx=2, pady=2)
        ctk.CTkButton(b_grid, text="⚠️ تسجيل شكوى", font=FONT_BTN, fg_color=colors["RED_BTN"], height=36,
                      text_color="white", command=self.popup_add_complaint).pack(
            side="right" if current_lang == "ar" else "left", fill="x", expand=True, padx=2, pady=2)

    # ==========================================
    # ❄️ التكيفات
    # ==========================================
    def view_ac_section(self):
        if self.current_role != 'manager':
            self.show_toast("صلاحيات", "عذراً، هذه الصلاحية للمديرين فقط!", "error")
            return
        self.clear_content()
        box = ctk.CTkFrame(self.content_area, fg_color=colors["PANEL_BG"], corner_radius=18, border_width=1,
                           border_color=colors["TEXT_MUTED"])
        box.pack(fill="both", expand=True, padx=5, pady=5)
        top_f = ctk.CTkFrame(box, fg_color="transparent")
        top_f.pack(fill="x", pady=15, padx=20)
        ctk.CTkLabel(top_f, text="❄️ قسم إدارة وتكيفات الهواء الشامل", font=FONT_TITLE,
                     text_color=colors["GOLD_ACCENT"]).pack(side="right" if current_lang == "ar" else "left")
        btn_fr = ctk.CTkFrame(top_f, fg_color="transparent")
        btn_fr.pack(side="left" if current_lang == "ar" else "right")
        ctk.CTkButton(btn_fr, text="➕ صنف", font=FONT_BTN, fg_color=colors["GREEN_BTN"], height=36, width=70,
                      command=lambda: self.popup_add_product("ac")).pack(
            side="right" if current_lang == "ar" else "left", padx=2)
        ctk.CTkButton(btn_fr, text="➕ بيع", font=FONT_BTN, fg_color=colors["BLUE_BTN"], height=36, width=70,
                      command=lambda: self.popup_add_sale_or_maint("ac", "sale")).pack(
            side="right" if current_lang == "ar" else "left", padx=2)
        ctk.CTkButton(btn_fr, text="➕ صيانة", font=FONT_BTN, fg_color=colors["RED_BTN"], height=36, width=70,
                      command=lambda: self.popup_add_sale_or_maint("ac", "maint")).pack(
            side="right" if current_lang == "ar" else "left", padx=2)

        tabview = ctk.CTkTabview(box, corner_radius=12, segmented_button_selected_color=colors["GOLD_ACCENT"])
        tabview.pack(fill="both", expand=True, padx=20, pady=10)
        t_inv = tabview.add("📦 المخازن")
        t_sales = tabview.add("💰 المبيعات")
        t_maint = tabview.add("📅 الصيانات")
        t_faults = tabview.add("⚠️ الأعطال")

        inv_search = ctk.CTkEntry(t_inv, placeholder_text="🔍 ابحث في المخزن...", font=FONT_BODY, height=36,
                                  justify="right" if current_lang == "ar" else "left")
        inv_search.pack(fill="x", padx=5, pady=(5, 5))
        top_inv_f = ctk.CTkFrame(t_inv, fg_color="transparent")
        top_inv_f.pack(fill="x", pady=(0, 5))
        ctk.CTkButton(top_inv_f, text="🖨️ طباعة المخزن", font=FONT_BTN, fg_color=colors["PURPLE_BTN"], height=32,
                      width=130, command=lambda: self.print_report_modal(tree_inv, "مخزن التكيفات")).pack(
            side="left" if current_lang == "ar" else "right", padx=2)

        tree_inv = ttk.Treeview(t_inv, columns=("id", "type", "brand", "ind", "qty", "buy", "sell"), show="headings",
                                height=7)
        for col, txt in zip(tree_inv["columns"],
                            ["م", "النوع", "الماركة", "الصناعة", "العدد", "سعر الشراء", "سعر البيع"]): tree_inv.heading(
            col, text=txt)
        tree_inv.pack(fill="both", expand=True, padx=5, pady=5)

        sal_search = ctk.CTkEntry(t_sales, placeholder_text="🔍 ابحث في مبيعات التكيفات...", font=FONT_BODY, height=36,
                                  justify="right" if current_lang == "ar" else "left")
        sal_search.pack(fill="x", padx=5, pady=(5, 5))
        top_sal_f = ctk.CTkFrame(t_sales, fg_color="transparent")
        top_sal_f.pack(fill="x", pady=(0, 5))
        ctk.CTkButton(top_sal_f, text="🖨️ طباعة المبيعات", font=FONT_BTN, fg_color=colors["PURPLE_BTN"], height=32,
                      width=130, command=lambda: self.print_report_modal(tree_ac_sales, "مبيعات التكيفات")).pack(
            side="left" if current_lang == "ar" else "right", padx=2)

        tree_ac_sales = ttk.Treeview(t_sales, columns=("id", "name", "phone", "item", "date", "due"), show="headings",
                                     height=7)
        for col, txt in zip(tree_ac_sales["columns"],
                            ["م", "اسم العميل", "رقم تلفون العميل", "تفاصيل الصنف", "تاريخ البيع",
                             "المبلغ المستحق"]): tree_ac_sales.heading(col, text=txt)
        tree_ac_sales.pack(fill="both", expand=True, padx=5, pady=5)

        mai_search = ctk.CTkEntry(t_maint, placeholder_text="🔍 ابحث في الصيانات...", font=FONT_BODY, height=36,
                                  justify="right" if current_lang == "ar" else "left")
        mai_search.pack(fill="x", padx=5, pady=(5, 5))
        top_mai_f = ctk.CTkFrame(t_maint, fg_color="transparent")
        top_mai_f.pack(fill="x", pady=(0, 5))
        ctk.CTkButton(top_mai_f, text="🖨️ طباعة الصيانة", font=FONT_BTN, fg_color=colors["PURPLE_BTN"], height=32,
                      width=130, command=lambda: self.print_report_modal(tree_maint, "صيانة التكيفات")).pack(
            side="left" if current_lang == "ar" else "right", padx=2)

        tree_maint = ttk.Treeview(t_maint, columns=("id", "name", "phone", "addr", "desc", "date"), show="headings",
                                  height=7)
        for col, txt in zip(tree_maint["columns"], ["م", "اسم العميل", "رقم التلفون", "العنوان", "طبيعة الصيانة",
                                                    "موعد الصيانة"]): tree_maint.heading(col, text=txt)
        tree_maint.pack(fill="both", expand=True, padx=5, pady=5)

        fau_search = ctk.CTkEntry(t_faults, placeholder_text="🔍 ابحث في الأعطال...", font=FONT_BODY, height=36,
                                  justify="right" if current_lang == "ar" else "left")
        fau_search.pack(fill="x", padx=5, pady=(5, 5))
        top_fau_f = ctk.CTkFrame(t_faults, fg_color="transparent")
        top_fau_f.pack(fill="x", pady=(0, 5))
        ctk.CTkButton(top_fau_f, text="🖨️ طباعة الأعطال", font=FONT_BTN, fg_color=colors["PURPLE_BTN"], height=32,
                      width=130, command=lambda: self.print_report_modal(tree_faults, "أعطال التكيفات")).pack(
            side="left" if current_lang == "ar" else "right", padx=2)

        tree_faults = ttk.Treeview(t_faults, columns=("id", "name", "phone", "addr", "desc"), show="headings", height=7)
        for col, txt in zip(tree_faults["columns"],
                            ["م", "اسم العميل", "رقم التلفون", "العنوان", "تفاصيل العطل"]): tree_faults.heading(col,
                                                                                                                text=txt)
        tree_faults.pack(fill="both", expand=True, padx=5, pady=5)

        conn = sqlite3.connect("golden_life.db")
        all_ac_inv = [
            (r[0], r[1], r[2], r[3], self.format_qty(r[4]), self.format_amount(r[5]), self.format_amount(r[6])) for r in
            conn.cursor().execute("SELECT * FROM ac_inventory").fetchall()]
        all_ac_sal = [(r[0], r[1], r[2], r[3], r[4], self.format_amount(r[5])) for r in
                      conn.cursor().execute("SELECT * FROM ac_sales").fetchall()]
        all_ac_mai = conn.cursor().execute("SELECT * FROM ac_maintenance").fetchall()
        conn.close()

        def load_inv(q=""):
            for item in tree_inv.get_children(): tree_inv.delete(item)
            qry = q.strip().lower()
            for r in all_ac_inv:
                if not qry or any(qry in str(c).lower() for c in r): tree_inv.insert("", "end", values=r)

        def load_sal(q=""):
            for item in tree_ac_sales.get_children(): tree_ac_sales.delete(item)
            qry = q.strip().lower()
            for r in all_ac_sal:
                if not qry or any(qry in str(c).lower() for c in r): tree_ac_sales.insert("", "end", values=r)

        def load_mai(q=""):
            for item in tree_maint.get_children(): tree_maint.delete(item)
            qry = q.strip().lower()
            for r in all_ac_mai:
                if not qry or any(qry in str(c).lower() for c in r): tree_maint.insert("", "end", values=r)

        def load_fau(q=""):
            for item in tree_faults.get_children(): tree_faults.delete(item)
            qry = q.strip().lower()
            for r in all_ac_mai:
                if not qry or any(qry in str(c).lower() for c in r): tree_faults.insert("", "end", values=r)

        load_inv();
        load_sal();
        load_mai();
        load_fau()
        inv_search.bind("<KeyRelease>", lambda e: load_inv(inv_search.get()))
        sal_search.bind("<KeyRelease>", lambda e: load_sal(sal_search.get()))
        mai_search.bind("<KeyRelease>", lambda e: load_mai(mai_search.get()))
        fau_search.bind("<KeyRelease>", lambda e: load_fau(fau_search.get()))

    # ==========================================
    # 💧 الفلاتر
    # ==========================================
    def view_filters_section(self):
        if self.current_role != 'manager':
            self.show_toast("صلاحيات", "عذراً، هذه الصلاحية للمديرين فقط!", "error")
            return
        self.clear_content()
        box = ctk.CTkFrame(self.content_area, fg_color=colors["PANEL_BG"], corner_radius=18, border_width=1,
                           border_color=colors["TEXT_MUTED"])
        box.pack(fill="both", expand=True, padx=5, pady=5)
        top_f = ctk.CTkFrame(box, fg_color="transparent")
        top_f.pack(fill="x", pady=15, padx=20)
        ctk.CTkLabel(top_f, text="💧 قسم إدارة فلاتر المياه الشامل", font=FONT_TITLE,
                     text_color=colors["GOLD_ACCENT"]).pack(side="right" if current_lang == "ar" else "left")
        btn_fr = ctk.CTkFrame(top_f, fg_color="transparent")
        btn_fr.pack(side="left" if current_lang == "ar" else "right")
        ctk.CTkButton(btn_fr, text="➕ صنف", font=FONT_BTN, fg_color=colors["GREEN_BTN"], height=36, width=70,
                      command=lambda: self.popup_add_product("filter")).pack(
            side="right" if current_lang == "ar" else "left", padx=2)
        ctk.CTkButton(btn_fr, text="➕ بيع", font=FONT_BTN, fg_color=colors["BLUE_BTN"], height=36, width=70,
                      command=lambda: self.popup_add_sale_or_maint("filter", "sale")).pack(
            side="right" if current_lang == "ar" else "left", padx=2)
        ctk.CTkButton(btn_fr, text="➕ صيانة", font=FONT_BTN, fg_color=colors["RED_BTN"], height=36, width=70,
                      command=lambda: self.popup_add_sale_or_maint("filter", "maint")).pack(
            side="right" if current_lang == "ar" else "left", padx=2)

        tabview = ctk.CTkTabview(box, corner_radius=12, segmented_button_selected_color=colors["GOLD_ACCENT"])
        tabview.pack(fill="both", expand=True, padx=20, pady=10)
        t_inv = tabview.add("📦 المخازن")
        t_sales = tabview.add("💰 المبيعات")
        t_maint = tabview.add("📅 الصيانات")
        t_faults = tabview.add("⚠️ الأعطال")

        inv_search = ctk.CTkEntry(t_inv, placeholder_text="🔍 ابحث في مخزن الفلاتر...", font=FONT_BODY, height=36,
                                  justify="right" if current_lang == "ar" else "left")
        inv_search.pack(fill="x", padx=5, pady=(5, 5))
        top_inv_f = ctk.CTkFrame(t_inv, fg_color="transparent")
        top_inv_f.pack(fill="x", pady=(0, 5))
        ctk.CTkButton(top_inv_f, text="🖨️ طباعة المخزن", font=FONT_BTN, fg_color=colors["PURPLE_BTN"], height=32,
                      width=130, command=lambda: self.print_report_modal(tree_inv, "مخزن الفلاتر")).pack(
            side="left" if current_lang == "ar" else "right", padx=2)

        tree_inv = ttk.Treeview(t_inv, columns=("id", "type", "brand", "ind", "qty", "buy", "sell"), show="headings",
                                height=7)
        for col, txt in zip(tree_inv["columns"],
                            ["م", "النوع", "الماركة", "الصناعة", "العدد", "سعر الشراء", "سعر البيع"]): tree_inv.heading(
            col, text=txt)
        tree_inv.pack(fill="both", expand=True, padx=5, pady=5)

        sal_search = ctk.CTkEntry(t_sales, placeholder_text="🔍 ابحث في مبيعات الفلاتر...", font=FONT_BODY, height=36,
                                  justify="right" if current_lang == "ar" else "left")
        sal_search.pack(fill="x", padx=5, pady=(5, 5))
        top_sal_f = ctk.CTkFrame(t_sales, fg_color="transparent")
        top_sal_f.pack(fill="x", pady=(0, 5))
        ctk.CTkButton(top_sal_f, text="🖨️ طباعة المبيعات", font=FONT_BTN, fg_color=colors["PURPLE_BTN"], height=32,
                      width=130, command=lambda: self.print_report_modal(tree_flt_sales, "مبيعات الفلاتر")).pack(
            side="left" if current_lang == "ar" else "right", padx=2)

        tree_flt_sales = ttk.Treeview(t_sales, columns=("id", "name", "phone", "item", "date", "due"), show="headings",
                                      height=7)
        for col, txt in zip(tree_flt_sales["columns"],
                            ["م", "اسم العميل", "رقم تلفون العميل", "تفاصيل الصنف", "تاريخ البيع",
                             "المبلغ المستحق"]): tree_flt_sales.heading(col, text=txt)
        tree_flt_sales.pack(fill="both", expand=True, padx=5, pady=5)

        mai_search = ctk.CTkEntry(t_maint, placeholder_text="🔍 ابحث في صيانة الفلاتر...", font=FONT_BODY, height=36,
                                  justify="right" if current_lang == "ar" else "left")
        mai_search.pack(fill="x", padx=5, pady=(5, 5))
        top_mai_f = ctk.CTkFrame(t_maint, fg_color="transparent")
        top_mai_f.pack(fill="x", pady=(0, 5))
        ctk.CTkButton(top_mai_f, text="🖨️ طباعة الصيانة", font=FONT_BTN, fg_color=colors["PURPLE_BTN"], height=32,
                      width=130, command=lambda: self.print_report_modal(tree_maint, "صيانة الفلاتر")).pack(
            side="left" if current_lang == "ar" else "right", padx=2)

        tree_maint = ttk.Treeview(t_maint, columns=("id", "name", "phone", "addr", "desc", "date"), show="headings",
                                  height=7)
        for col, txt in zip(tree_maint["columns"], ["م", "اسم العميل", "رقم التلفون", "العنوان", "طبيعة الصيانة",
                                                    "موعد الصيانة"]): tree_maint.heading(col, text=txt)
        tree_maint.pack(fill="both", expand=True, padx=5, pady=5)

        fau_search = ctk.CTkEntry(t_faults, placeholder_text="🔍 ابحث في أعطال الفلاتر...", font=FONT_BODY, height=36,
                                  justify="right" if current_lang == "ar" else "left")
        fau_search.pack(fill="x", padx=5, pady=(5, 5))
        top_fau_f = ctk.CTkFrame(t_faults, fg_color="transparent")
        top_fau_f.pack(fill="x", pady=(0, 5))
        ctk.CTkButton(top_fau_f, text="🖨️ طباعة الأعطال", font=FONT_BTN, fg_color=colors["PURPLE_BTN"], height=32,
                      width=130, command=lambda: self.print_report_modal(tree_faults, "أعطال الفلاتر")).pack(
            side="left" if current_lang == "ar" else "right", padx=2)

        tree_faults = ttk.Treeview(t_faults, columns=("id", "name", "phone", "addr", "desc"), show="headings", height=7)
        for col, txt in zip(tree_faults["columns"],
                            ["م", "اسم العميل", "رقم التلفون", "العنوان", "تفاصيل العطل"]): tree_faults.heading(col,
                                                                                                                text=txt)
        tree_faults.pack(fill="both", expand=True, padx=5, pady=5)

        conn = sqlite3.connect("golden_life.db")
        all_flt_inv = [
            (r[0], r[1], r[2], r[3], self.format_qty(r[4]), self.format_amount(r[5]), self.format_amount(r[6])) for r in
            conn.cursor().execute("SELECT * FROM filter_inventory").fetchall()]
        all_flt_sal = [(r[0], r[1], r[2], r[3], r[4], self.format_amount(r[5])) for r in
                       conn.cursor().execute("SELECT * FROM filter_sales").fetchall()]
        all_flt_mai = conn.cursor().execute("SELECT * FROM filter_maintenance").fetchall()
        conn.close()

        def load_inv(q=""):
            for item in tree_inv.get_children(): tree_inv.delete(item)
            qry = q.strip().lower()
            for r in all_flt_inv:
                if not qry or any(qry in str(c).lower() for c in r): tree_inv.insert("", "end", values=r)

        def load_sal(q=""):
            for item in tree_flt_sales.get_children(): tree_flt_sales.delete(item)
            qry = q.strip().lower()
            for r in all_flt_sal:
                if not qry or any(qry in str(c).lower() for c in r): tree_flt_sales.insert("", "end", values=r)

        def load_mai(q=""):
            for item in tree_maint.get_children(): tree_maint.delete(item)
            qry = q.strip().lower()
            for r in all_flt_mai:
                if not qry or any(qry in str(c).lower() for c in r): tree_maint.insert("", "end", values=r)

        def load_fau(q=""):
            for item in tree_faults.get_children(): tree_faults.delete(item)
            qry = q.strip().lower()
            for r in all_flt_mai:
                if not qry or any(qry in str(c).lower() for c in r): tree_faults.insert("", "end", values=r)

        load_inv();
        load_sal();
        load_mai();
        load_fau()
        inv_search.bind("<KeyRelease>", lambda e: load_inv(inv_search.get()))
        sal_search.bind("<KeyRelease>", lambda e: load_sal(sal_search.get()))
        mai_search.bind("<KeyRelease>", lambda e: load_mai(mai_search.get()))
        fau_search.bind("<KeyRelease>", lambda e: load_fau(fau_search.get()))

    # ==========================================
    # النوافذ المنبثقة
    # ==========================================
    def popup_add_product(self, target):
        pop = ctk.CTkToplevel(self)
        pop.title("إضافة منتج للمخزن")
        pop.geometry("400x480")
        pop.grab_set()
        ctk.CTkLabel(pop, text="📦 إضافة صنف جديد للمخازن", font=FONT_SUBTITLE, text_color=colors["GOLD_ACCENT"]).pack(
            pady=15)

        e_type = ctk.CTkEntry(pop, width=320, placeholder_text="النوع (مثال: اسبليت / 7 مراحل)", font=FONT_BODY)
        e_type.pack(pady=6)
        e_brand = ctk.CTkEntry(pop, width=320, placeholder_text="الماركة (مثال: شارب / رويال)", font=FONT_BODY)
        e_brand.pack(pady=6)
        e_ind = ctk.CTkEntry(pop, width=320, placeholder_text="الصناعة (مثال: ياباني / تايواني)", font=FONT_BODY)
        e_ind.pack(pady=6)
        e_qty = ctk.CTkEntry(pop, width=320, placeholder_text="العدد (الكمية)", font=FONT_BODY)
        e_qty.pack(pady=6)
        e_buy = ctk.CTkEntry(pop, width=320, placeholder_text="سعر الشراء", font=FONT_BODY)
        e_buy.pack(pady=6)
        e_sell = ctk.CTkEntry(pop, width=320, placeholder_text="سعر البيع", font=FONT_BODY)
        e_sell.pack(pady=6)

        def save():
            t, b, ind, q, buy, sell = e_type.get().strip(), e_brand.get().strip(), e_ind.get().strip(), e_qty.get().strip(), e_buy.get().strip(), e_sell.get().strip()
            if not (t and q and sell):
                self.show_toast("تنبيه", "املأ الحقول الإلزامية (النوع، العدد، سعر البيع)!", "warning")
                return
            qty_int = int(q)
            conn = sqlite3.connect("golden_life.db")
            tbl = "ac_inventory" if target == "ac" else "filter_inventory"
            conn.cursor().execute(
                f"INSERT INTO {tbl} (item_type, brand, industry, quantity, buy_price, sell_price) VALUES (?, ?, ?, ?, ?, ?)",
                (t, b, ind, qty_int, float(buy or 0), float(sell)))
            conn.commit()
            conn.close()

            log_stock_movement(f"{target.upper()} - {t} ({b})", "➕ توريد وإضافة للمخزن", qty_int, self.current_user)

            self.show_toast("نجح التوريد", "تمت الإضافة للمخزن وتسجيل الحركة بنجاح!", "success")
            pop.destroy()
            if target == "ac":
                self.view_ac_section()
            else:
                self.view_filters_section()

        ctk.CTkButton(pop, text="💾 حفظ الصنف", font=FONT_BTN, fg_color=colors["GREEN_BTN"], width=320, height=38,
                      command=save).pack(pady=15)

    def popup_add_sale_or_maint(self, target, mode):
        pop = ctk.CTkToplevel(self)
        pop.title("تسجيل مبيعات أو صيانة")
        pop.geometry("400x420")
        pop.grab_set()
        title_txt = "💰 تسجيل عملية بيع جديدة" if mode == "sale" else "🛠️ تسجيل صيانة أو عطل"
        ctk.CTkLabel(pop, text=title_txt, font=FONT_SUBTITLE, text_color=colors["GOLD_ACCENT"]).pack(pady=15)

        e_name = ctk.CTkEntry(pop, width=320, placeholder_text="اسم العميل", font=FONT_BODY)
        e_name.pack(pady=6)
        e_phone = ctk.CTkEntry(pop, width=320, placeholder_text="رقم تلفون العميل", font=FONT_BODY)
        e_phone.pack(pady=6)
        e_addr = ctk.CTkEntry(pop, width=320, placeholder_text="العنوان", font=FONT_BODY)
        e_addr.pack(pady=6)
        e_desc = ctk.CTkEntry(pop, width=320, placeholder_text="تفاصيل الصنف أو العطل / الصيانة", font=FONT_BODY)
        e_desc.pack(pady=6)
        e_due = ctk.CTkEntry(pop, width=320, placeholder_text="المبلغ المطلوب / الإجمالي", font=FONT_BODY)
        if mode == "sale": e_due.pack(pady=6)

        def save():
            name, phone, addr, desc = e_name.get().strip(), e_phone.get().strip(), e_addr.get().strip(), e_desc.get().strip()
            if not (name and phone):
                self.show_toast("تنبيه", "اسم العميل ورقم التلفون إلزاميّان!", "warning")
                return
            today = datetime.now().strftime("%Y-%m-%d")
            conn = sqlite3.connect("golden_life.db")
            if mode == "sale":
                due = float(e_due.get().strip() or 0)
                tbl = "ac_sales" if target == "ac" else "filter_sales"
                conn.cursor().execute(
                    f"INSERT INTO {tbl} (client_name, client_phone, item_desc, sale_date, amount_due) VALUES (?, ?, ?, ?, ?)",
                    (name, phone, desc, today, due))

                log_stock_movement(f"{target.upper()} - {desc}", "➖ مبيعات (خروج)", 1, self.current_user)
            else:
                tbl = "ac_maintenance" if target == "ac" else "filter_maintenance"
                conn.cursor().execute(
                    f"INSERT INTO {tbl} (client_name, client_phone, address, fault_desc, maint_date) VALUES (?, ?, ?, ?, ?)",
                    (name, phone, addr, desc, today))
            conn.commit()
            conn.close()
            self.show_toast("نجح", "تم الحفظ وتسجيل الحركة بنجاح!", "success")
            pop.destroy()
            if target == "ac":
                self.view_ac_section()
            else:
                self.view_filters_section()

        ctk.CTkButton(pop, text="💾 حفظ البيانات", font=FONT_BTN, fg_color=colors["GREEN_BTN"], width=320, height=38,
                      command=save).pack(pady=15)

    def popup_add_expense(self):
        pop = ctk.CTkToplevel(self)
        pop.title("إضافة مصروف سنوي")
        pop.geometry("380x350")
        pop.grab_set()
        ctk.CTkLabel(pop, text="💸 تسجيل مصروف سنوي جديد", font=FONT_SUBTITLE, text_color=colors["GOLD_ACCENT"]).pack(
            pady=15)
        e_title = ctk.CTkEntry(pop, width=280, placeholder_text="بيان المصروف (مثال: إيجار سنوي)", font=FONT_BODY)
        e_title.pack(pady=8)
        e_amount = ctk.CTkEntry(pop, width=280, placeholder_text="المبلغ (ج.م)", font=FONT_BODY)
        e_amount.pack(pady=8)
        e_status = ctk.CTkOptionMenu(pop, width=280, values=["مدفوع", "غير مدفوع"], fg_color=colors["BLUE_BTN"],
                                     button_color=colors["BLUE_BTN"])
        e_status.pack(pady=8)

        def save():
            title, amount, status = e_title.get().strip(), e_amount.get().strip(), e_status.get()
            if not (title and amount):
                self.show_toast("تنبيه", "أدخل البيان والمبلغ!", "warning")
                return
            conn = sqlite3.connect("golden_life.db")
            conn.cursor().execute("INSERT INTO expenses (title, amount, status) VALUES (?, ?, ?)",
                                  (title, float(amount), status))
            conn.commit()
            conn.close()
            self.show_toast("نجح", "تم الحفظ بنجاح!", "success")
            pop.destroy()
            self.view_expenses_section()

        ctk.CTkButton(pop, text="💾 حفظ", font=FONT_BTN, fg_color=colors["GREEN_BTN"], width=280, height=38,
                      command=save).pack(pady=15)

if __name__ == "__main__":
    init_db()
    app = GoldenLifeApp()
    app.mainloop()