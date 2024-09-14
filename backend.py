# from flask import Flask, render_template
# import csv

# app = Flask(__name__)
# # Function to read food attributes from CSV file
# def read_food_attributes(food_name):
#     with open('dataset.csv', newline='') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             if row['name'].lower() == food_name.lower():
#                 return {
#                     'Food': row['name'],
#                     'Protein': row['protein'],
#                     'Carbohydrates': row['carbs'],
#                     'Fat': row['fats'],
#                     'Calories': row['calories']
#                 }
#     return None


# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/<food>')
# def food_attributes(food):
#     # Reading attributes for the specified food
#     food_attributes = read_food_attributes(food)
    
#     if food_attributes:
#         return render_template('food.html', food=food_attributes)
#     else:
#         return "Food not found!", 404

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, request, flash, redirect, url_for
import csv

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages

# Function to read attributes from CSV file
def read_attributes(name):
    with open('food_medicine_data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Name'].lower() == name.lower():
                return {
                    'Category': row['Category'],
                    'Name': row['Name'],
                    'Pros': [row['Pros'].split(';')[0], row['Pros'].split(';')[1], row['Pros'].split(';')[2]],
                    'Cons': [row['Cons'].split(';')[0], row['Cons'].split(';')[1], row['Cons'].split(';')[2]],
                    'Description': row['Description'],
                    'Price': row['Price']
                }
    return None

# @app.route('/')
# def index():
#     return render_template('index.html')



@app.route('/', methods=['GET'])
def register_form():
    return render_template('registration.html')

# Route to handle form submission
@app.route('/register', methods=['POST'])
def register_user():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    
    # Simple validation
    if not name or not email or not password:
        flash('All fields are required!', 'error')
        return redirect(url_for('register_form'))
    
    # For example, here you could save the data to a database or perform other actions
    
    flash('Registration successful!', 'success')
    return redirect(url_for('register_form'))




@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    if not query:
        flash('Please enter a name to search.', 'error')
        return redirect(url_for('index'))

    attributes = read_attributes(query)
    if attributes:
        return redirect(url_for('item_attributes', name=query))
    else:
        return render_template('error.html', error_message=f"No results found for '{query}'")

@app.route('/<name>')
def item_attributes(name):
    attributes = read_attributes(name)
    
    if attributes:
        return render_template('food.html', attributes=attributes)
    else:
        return render_template('error.html', error_message=f"Item not found: {name}"), 404

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_message="404: Page not found!"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', error_message="500: Internal Server Error!"), 500

if __name__ == '__main__':
    app.run(debug=True)