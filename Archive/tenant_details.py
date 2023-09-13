from flask import Flask, render_template, request
import csv



app = Flask(__name__, template_folder='templates')



def read_csv():
    data = []
    with open('data/form_data.csv', mode='r', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            data.append(row)
    return data

@app.route('/', methods=['GET', 'POST'])
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



if(__name__=='__main__'):
    app.secret_key = 'secretivekey'
    app.run(debug=True)

