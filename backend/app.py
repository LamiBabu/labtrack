from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from functools import wraps
from datetime import date
import re

app = Flask(__name__)
app.secret_key = "labassetsecretkey"

DB = dict(host="localhost", user="root", password="lami@123", database="lab_asset_db")

def get_conn():
    return mysql.connector.connect(**DB)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def student_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'student_user_id' not in session:
            return redirect(url_for('student_login'))
        return f(*args, **kwargs)
    return decorated_function


# ================= ADMIN LOGIN =================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
        admin = cursor.fetchone()
        conn.close()
        if admin:
            session['admin_username'] = admin['username']
            return redirect(url_for('home'))
        return render_template('login.html', error="Invalid Username or Password")
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ================= HOME =================
@app.route('/')
@login_required
def home():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM equipment")
    total_equipment = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM issue_records WHERE status='Issued'")
    current_issued = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM issue_records WHERE status='Returned'")
    total_returned = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(fine) FROM issue_records")
    result = cursor.fetchone()[0]
    total_fine = result if result else 0

    cursor.execute("SELECT COUNT(*) FROM equipment WHERE available_quantity = 0")
    out_of_stock = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM equipment WHERE available_quantity > 0 AND available_quantity <= 2")
    low_stock = cursor.fetchone()[0]

    conn2 = get_conn()
    cursor2 = conn2.cursor(dictionary=True)
    cursor2.execute("""
        SELECT category, SUM(total_quantity) as total, SUM(available_quantity) as available,
               SUM(damaged_quantity) as damaged
        FROM equipment GROUP BY category
    """)
    chart_data = [{'category': r['category'], 'total': int(r['total'] or 0), 'available': int(r['available'] or 0), 'damaged': int(r['damaged'] or 0)} for r in cursor2.fetchall()]

    cursor2.execute("""
        SELECT DATE_FORMAT(issue_date, '%Y-%m') as month, COUNT(*) as count
        FROM issue_records GROUP BY month ORDER BY month DESC LIMIT 6
    """)
    issue_trend = [{'month': r['month'], 'count': int(r['count'])} for r in cursor2.fetchall()]

    conn.close()
    conn2.close()

    return render_template('index.html',
        total_students=total_students, total_equipment=total_equipment,
        current_issued=current_issued, total_returned=total_returned,
        total_fine=total_fine, out_of_stock=out_of_stock, low_stock=low_stock,
        chart_data=chart_data, issue_trend=issue_trend)


# ================= STUDENTS =================
@app.route('/students', methods=['GET', 'POST'])
@login_required
def students():
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)
    search_query = request.args.get('search')

    if request.method == 'POST':
        name = request.form['name']
        department = request.form['department']
        year = request.form['year']
        phone = request.form['phone']

        if not re.match(r'^[A-Z][a-z]+( [A-Z][a-z]+)*$', name):
            conn.close(); return "Invalid Name Format"
        if department not in ['CSE','CE','IT','ECE','EEE','ME','RA','EL','SF']:
            conn.close(); return "Invalid Department"
        if not year.isdigit() or int(year) < 1 or int(year) > 4:
            conn.close(); return "Year must be between 1 and 4"
        if not re.match(r'^[0-9]{10}$', phone):
            conn.close(); return "Phone must be 10 digits"

        cursor.execute("INSERT INTO students (name, department, year, phone) VALUES (%s, %s, %s, %s)", (name, department, year, phone))
        conn.commit()
        new_id = cursor.lastrowid
        username = name.lower().replace(' ', '')
        password = username + '456'
        cursor.execute("INSERT INTO student_users (student_id, username, password) VALUES (%s, %s, %s)", (new_id, username, password))
        conn.commit()
        flash(f'Student {name} added! Login: {username} / {password}', 'success')

    if search_query:
        cursor.execute("SELECT * FROM students WHERE name LIKE %s OR department LIKE %s OR student_id LIKE %s",
                       (f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"))
    else:
        cursor.execute("SELECT * FROM students")

    students_list = cursor.fetchall()
    conn.close()
    return render_template('students.html', students=students_list)


@app.route('/edit_student/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_student(id):
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        name = request.form['name']
        department = request.form['department']
        year = request.form['year']
        phone = request.form['phone']

        if not re.match(r'^[A-Z][a-z]+( [A-Z][a-z]+)*$', name):
            conn.close(); return "Invalid Name Format"
        if department not in ['CSE','CE','IT','ECE','EEE','ME','RA','EL','SF']:
            conn.close(); return "Invalid Department"
        if not year.isdigit() or int(year) < 1 or int(year) > 4:
            conn.close(); return "Year must be between 1 and 4"
        if not re.match(r'^[0-9]{10}$', phone):
            conn.close(); return "Phone must be 10 digits"

        cursor.execute("UPDATE students SET name=%s, department=%s, year=%s, phone=%s WHERE student_id=%s",
                       (name, department, year, phone, id))
        conn.commit()
        flash('Student updated successfully!', 'success')
        conn.close()
        return redirect(url_for('students'))

    cursor.execute("SELECT * FROM students WHERE student_id=%s", (id,))
    student = cursor.fetchone()
    conn.close()
    return render_template('edit_student.html', student=student)


@app.route('/delete_student/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_student(id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE student_id=%s", (id,))
    conn.commit()
    flash('Student deleted.', 'warning')
    conn.close()
    return redirect(url_for('students'))


# ================= EQUIPMENT =================
@app.route('/equipment', methods=['GET', 'POST'])
@login_required
def equipment():
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)
    search_query = request.args.get('search', '')

    if request.method == 'POST':
        name = request.form.get('equipment_name')
        category = request.form.get('category')
        total = request.form.get('total_quantity')
        lab_id = request.form.get('lab_id')

        if name and category and total and lab_id:
            if not re.match(r'^[A-Z][a-zA-Z]*( [A-Z][a-zA-Z]*)*$', name):
                conn.close()
                flash('Invalid Equipment Name: each word must start with a capital letter', 'error')
                return redirect(url_for('equipment'))
            if not re.match(r'^[A-Z][a-zA-Z]*( [A-Z][a-zA-Z]*)*$', category):
                conn.close()
                flash('Invalid Category: each word must start with a capital letter', 'error')
                return redirect(url_for('equipment'))
            total = int(total)
            cursor.execute("""
                INSERT INTO equipment (equipment_name, category, total_quantity, available_quantity, lab_id)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, category, total, total, lab_id))
            conn.commit()
            flash(f'Equipment {name} added successfully!', 'success')

    query = "SELECT e.*, l.lab_name FROM equipment e LEFT JOIN labs l ON e.lab_id = l.lab_id WHERE 1=1"
    params = []
    if search_query:
        query += " AND (e.equipment_name LIKE %s OR e.category LIKE %s OR e.equipment_id LIKE %s)"
        params += [f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"]

    cursor.execute(query, params)
    equipment_list = cursor.fetchall()
    conn.close()
    return render_template('equipment.html', equipment=equipment_list, search_query=search_query)


@app.route('/edit_equipment/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_equipment(id):
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        eq_name = request.form['equipment_name']
        eq_category = request.form['category']

        if not re.match(r'^[A-Z][a-zA-Z]*( [A-Z][a-zA-Z]*)*$', eq_name):
            conn.close(); return "Invalid Equipment Name: each word must start with a capital letter"
        if not re.match(r'^[A-Z][a-zA-Z]*( [A-Z][a-zA-Z]*)*$', eq_category):
            conn.close(); return "Invalid Category: each word must start with a capital letter"

        new_total = int(request.form['total_quantity'])
        cursor.execute("""
            SELECT available_quantity, damaged_quantity,
                   (SELECT COUNT(*) FROM issue_records WHERE equipment_id=%s AND status='Issued') AS issued_count
            FROM equipment WHERE equipment_id=%s
        """, (id, id))
        current = cursor.fetchone()

        if current and new_total < current['available_quantity']:
            conn.close(); return "Total quantity cannot be less than available quantity"

        new_available = min(max(0, new_total - current['damaged_quantity'] - current['issued_count']), new_total)
        cursor.execute("""
            UPDATE equipment SET equipment_name=%s, category=%s, total_quantity=%s, available_quantity=%s, lab_id=%s
            WHERE equipment_id=%s
        """, (eq_name, eq_category, new_total, new_available, request.form['lab_id'], id))
        conn.commit()
        flash('Equipment updated successfully!', 'success')
        conn.close()
        return redirect(url_for('equipment'))

    cursor.execute("SELECT * FROM equipment WHERE equipment_id=%s", (id,))
    equip = cursor.fetchone()
    conn.close()
    return render_template('edit_equipment.html', equip=equip)


@app.route('/delete_equipment/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_equipment(id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM equipment WHERE equipment_id=%s", (id,))
    conn.commit()
    flash('Equipment deleted.', 'warning')
    conn.close()
    return redirect(url_for('equipment'))


@app.route('/mark_damaged/<int:id>')
@login_required
def mark_damaged(id):
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT available_quantity, damaged_quantity FROM equipment WHERE equipment_id=%s", (id,))
    equip = cursor.fetchone()

    if equip and equip['available_quantity'] > 0:
        new_damaged = equip['damaged_quantity'] + 1
        cursor.execute("SELECT COUNT(*) AS issued_count FROM issue_records WHERE equipment_id=%s AND status='Issued'", (id,))
        issued = cursor.fetchone()['issued_count']
        cursor.execute("SELECT total_quantity FROM equipment WHERE equipment_id=%s", (id,))
        total = cursor.fetchone()['total_quantity']
        new_available = max(0, min(total, total - new_damaged - issued))
        cursor.execute("UPDATE equipment SET damaged_quantity=%s, available_quantity=%s WHERE equipment_id=%s", (new_damaged, new_available, id))
        conn.commit()
        flash('Equipment marked as damaged.', 'warning')

    conn.close()
    return redirect(url_for('equipment'))


@app.route('/undo_damage/<int:id>')
@login_required
def undo_damage(id):
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT damaged_quantity FROM equipment WHERE equipment_id=%s", (id,))
    equip = cursor.fetchone()

    if equip and equip['damaged_quantity'] > 0:
        new_damaged = equip['damaged_quantity'] - 1
        cursor.execute("SELECT COUNT(*) AS issued_count FROM issue_records WHERE equipment_id=%s AND status='Issued'", (id,))
        issued = cursor.fetchone()['issued_count']
        cursor.execute("SELECT total_quantity FROM equipment WHERE equipment_id=%s", (id,))
        total = cursor.fetchone()['total_quantity']
        new_available = max(0, min(total, total - new_damaged - issued))
        cursor.execute("UPDATE equipment SET damaged_quantity=%s, available_quantity=%s WHERE equipment_id=%s", (new_damaged, new_available, id))
        conn.commit()
        flash('Damage undone successfully!', 'success')

    conn.close()
    return redirect(url_for('equipment'))


# ================= LABS =================
@app.route('/labs')
@login_required
def labs():
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT l.*, COUNT(DISTINCT e.equipment_id) AS total_equipment,
               COALESCE(SUM(e.available_quantity), 0) AS total_available,
               COALESCE(SUM(e.damaged_quantity), 0) AS total_damaged
        FROM labs l
        LEFT JOIN equipment e ON e.lab_id = l.lab_id
        GROUP BY l.lab_id ORDER BY l.lab_name
    """)
    lab_list = cursor.fetchall()
    conn.close()
    return render_template('labs.html', lab_list=lab_list)


# ================= ISSUES =================
@app.route('/issues')
@login_required
def issues():
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT ir.issue_id, s.name AS student_name, e.equipment_name,
               ir.issue_date, ir.return_date, ir.status, ir.fine
        FROM issue_records ir
        JOIN students s ON ir.student_id = s.student_id
        JOIN equipment e ON ir.equipment_id = e.equipment_id
        ORDER BY ir.issue_id ASC
    """)
    issue_list = cursor.fetchall()
    today = date.today()
    for issue in issue_list:
        if issue['status'] == 'Issued':
            total_days = (today - issue['issue_date']).days
        elif issue['return_date']:
            total_days = (issue['return_date'] - issue['issue_date']).days
        else:
            total_days = 0
        issue['late_days'] = max(0, total_days - 5)

    cursor.execute("SELECT student_id, name FROM students")
    students_list = cursor.fetchall()
    cursor.execute("SELECT equipment_id, equipment_name FROM equipment WHERE available_quantity > 0")
    equipment_list = cursor.fetchall()
    conn.close()
    return render_template('issues.html', issue_list=issue_list, students=students_list, equipment_list=equipment_list)


@app.route('/add_issue', methods=['POST'])
@login_required
def add_issue():
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)
    student_id = request.form['student_id']
    equipment_id = request.form['equipment_id']

    cursor.execute("SELECT available_quantity FROM equipment WHERE equipment_id=%s", (equipment_id,))
    equip = cursor.fetchone()

    if equip and equip['available_quantity'] > 0:
        cursor.execute("INSERT INTO issue_records (student_id, equipment_id, issue_date, status, fine) VALUES (%s, %s, CURDATE(), 'Issued', 0)", (student_id, equipment_id))
        conn.commit()
        flash('Equipment issued successfully!', 'success')

    conn.close()
    return redirect(url_for('issues'))


@app.route('/return_equipment/<int:id>')
@login_required
def return_equipment(id):
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT issue_date, equipment_id, status FROM issue_records WHERE issue_id=%s", (id,))
    record = cursor.fetchone()

    if record and record.get('status') == 'Issued':
        equipment_id = record['equipment_id']
        today = date.today()
        late_days = max(0, (today - record['issue_date']).days - 5)
        fine = late_days * 10
        cursor.execute("UPDATE issue_records SET return_date=%s, status='Returned', fine=%s WHERE issue_id=%s", (today, fine, id))
        conn.commit()
        flash(f'Equipment returned. Fine: ₹{fine}', 'success' if fine == 0 else 'warning')

    conn.close()
    return redirect(url_for('issues'))


@app.route('/undo_return/<int:id>')
@login_required
def undo_return(id):
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT equipment_id FROM issue_records WHERE issue_id=%s AND status='Returned'", (id,))
    record = cursor.fetchone()

    if record:
        equipment_id = record['equipment_id']
        cursor.execute("UPDATE issue_records SET return_date=NULL, status='Issued', fine=0 WHERE issue_id=%s", (id,))
        conn.commit()
        flash('Return undone successfully!', 'success')

    conn.close()
    return redirect(url_for('issues'))


# ================= STUDENT LOGIN =================
@app.route('/student/login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT su.*, s.name FROM student_users su
            JOIN students s ON su.student_id = s.student_id
            WHERE su.username=%s AND su.password=%s
        """, (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            session['student_user_id'] = user['student_id']
            session['student_name'] = user['name']
            flash('Login successful!', 'success')
            return redirect(url_for('student_dashboard'))
        return render_template('student_login.html', error="Invalid Username or Password")
    return render_template('student_login.html')


@app.route('/student/logout')
def student_logout():
    session.pop('student_user_id', None)
    session.pop('student_name', None)
    return redirect(url_for('student_login'))


# ================= STUDENT DASHBOARD =================
@app.route('/student/dashboard')
@student_login_required
def student_dashboard():
    student_id = session['student_user_id']
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT ir.issue_id, e.equipment_name, ir.issue_date, ir.return_date, ir.status, ir.fine
        FROM issue_records ir
        JOIN equipment e ON ir.equipment_id = e.equipment_id
        WHERE ir.student_id = %s ORDER BY ir.issue_date DESC
    """, (student_id,))
    my_issues = cursor.fetchall()
    today = date.today()
    for issue in my_issues:
        if issue['status'] == 'Issued':
            total_days = (today - issue['issue_date']).days
        elif issue['return_date']:
            total_days = (issue['return_date'] - issue['issue_date']).days
        else:
            total_days = 0
        issue['late_days'] = max(0, total_days - 5)

    cursor.execute("""
        SELECT c.*, e.equipment_name FROM complaints c
        LEFT JOIN equipment e ON c.equipment_id = e.equipment_id
        WHERE c.student_id = %s ORDER BY c.submitted_at DESC
    """, (student_id,))
    my_complaints = cursor.fetchall()

    conn.close()
    return render_template('student_dashboard.html', my_issues=my_issues, my_complaints=my_complaints)


# ================= RAISE COMPLAINT =================
@app.route('/student/complaint', methods=['GET', 'POST'])
@student_login_required
def raise_complaint():
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        equipment_id = request.form.get('equipment_id') or None
        complaint_type = request.form['complaint_type']
        message = request.form['message']
        cursor.execute("INSERT INTO complaints (student_id, student_name, equipment_id, complaint_type, message) VALUES (%s, %s, %s, %s, %s)",
                       (session['student_user_id'], session.get('student_name', ''), equipment_id, complaint_type, message))
        conn.commit()
        conn.close()
        flash('Complaint submitted successfully!', 'success')
        return redirect(url_for('student_dashboard'))

    cursor.execute("SELECT equipment_id, equipment_name FROM equipment")
    equipment_list = cursor.fetchall()
    conn.close()
    return render_template('raise_complaint.html', equipment_list=equipment_list)


# ================= ADMIN COMPLAINTS =================
@app.route('/complaints')
@login_required
def complaints():
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.*, e.equipment_name FROM complaints c
        LEFT JOIN equipment e ON c.equipment_id = e.equipment_id
        ORDER BY c.submitted_at DESC
    """)
    complaint_list = cursor.fetchall()
    conn.close()
    return render_template('complaints.html', complaint_list=complaint_list)


@app.route('/complaints/resolve/<int:id>')
@login_required
def resolve_complaint(id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("UPDATE complaints SET status='Resolved' WHERE complaint_id=%s", (id,))
    conn.commit()
    conn.close()
    flash('Complaint marked as resolved.', 'success')
    return redirect(url_for('complaints'))


@app.route('/complaints/pending/<int:id>')
@login_required
def pending_complaint(id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("UPDATE complaints SET status='Pending' WHERE complaint_id=%s", (id,))
    conn.commit()
    conn.close()
    flash('Complaint marked as pending.', 'warning')
    return redirect(url_for('complaints'))


@app.route('/student/complaint/delete/<int:id>', methods=['POST'])
@student_login_required
def delete_complaint(id):
    student_id = session['student_user_id']
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM complaints WHERE complaint_id=%s AND student_id=%s", (id, student_id))
    conn.commit()
    conn.close()
    flash('Complaint deleted.', 'warning')
    return redirect(url_for('student_dashboard'))


if __name__ == "__main__":
    app.run(debug=True)
