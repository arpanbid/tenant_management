from flask import Flask, render_template, request, redirect, url_for, session
import csv
from werkzeug.security import check_password_hash, generate_password_hash
import os


app = Flask(__name__, template_folder='templates')


users = {
    'user1': {'username': 'user1', 'password': generate_password_hash('password1')},
    'user2': {'username': 'user2', 'password': generate_password_hash('password2')}
}

def is_authenticated(username, password):
    user = users.get(username)
    if user and check_password_hash(user['password'], password):
        return True
    return False




@app.route("/")
def home():
    if 'username' in session:
        return f'Hello, {session["username"]}! <a href="/admin_dashboard">Dashboard</a> | <a href="/logout">Logout</a>'
    return 'Welcome! Please <a href="/login">login</a>.'



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if is_authenticated(username, password):
            session['username'] = username
            return redirect('/admin_dashboard')
        return 'Login failed. <a href="/login">Try again</a>'
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')


@app.route("/admin_dashboard")
def admin_dashboard():
    if 'username' in session:
        return render_template("admin_dashboard.html")
    return render_template('login.html')



@app.route("/inputtenant")
def inputtenant():
    return render_template("Tenant_Form.html")



@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        fname = request.form['fname']
        address = request.form['address']
        phone = request.form['mobile']
        email = request.form['email']
        room = request.form['room']
        gender = request.form['gender']
        ishostel = request.form.get('ishostel')
        if ishostel == 'on':
            ishostel = 'Yes'
        else:
            ishostel = 'No'  
        comments = request.form['comments']

        # Save the form data to a CSV file
        with open('data/form_data.csv', 'a', newline='') as csvfile:
            fieldnames = ['Sl No','Name','Father Name', 'Address', 'Phone', 'Email', 'Room', 'Gender', 'Is Hostel', 'Comments']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if csvfile.tell() == 0:
                writer.writeheader()

            
            sl_no=len(read_csv())+1

            writer.writerow({'Sl No':sl_no, 'Name': name, 'Father Name':fname, 'Address':address, 'Phone':phone, 'Email': email, 'Room':room,  'Gender': gender, 'Is Hostel': ishostel, 'Comments': comments})

        return 'Form data has been submitted and saved to form_data.csv. <a href="/admin_dashboard">Dashboard</a>'





def read_csv():
    data = []
    with open('data/form_data.csv', mode='r', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            data.append(row)
    return data

@app.route('/get_tenant', methods=['GET', 'POST'])
def tenantdetails():
    data = read_csv()

    if request.method == 'POST':
        selected_item = request.form.get('dropdown')
        filtered_data = [item for item in data if item['Name'] == selected_item]
    else:
        selected_item = None
        filtered_data = data

    categories = set(item['Name'] for item in data)

    return render_template('Tenant_Details_output.html', data=filtered_data, selected_item=selected_item, categories=categories)

#------------

app.config['UPLOAD_FOLDER'] = 'UploadedDocs'

@app.route('/doc_upload_by_admin')
def upload_form():
    data = read_csv()
    names = set()
    for item in data:
        names.add(item['Name'])
    
    return render_template('doc_upload.html', categories=names)



@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        option = request.form['option']

        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return f'Selected Option: {option}<br>Uploaded File Name: {file.filename}. <a href="/admin_dashboard">Dashboard</a>'

    return 'Upload failed. Please try again. <a href="/doc_upload_by_admin">Try again</a>'







if(__name__=='__main__'):
    app.secret_key = 'secretivekey'
    app.run(debug=True)

