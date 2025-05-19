import os
from flask import Flask, request, render_template
from flask_mail import Mail, Message
from dotenv import load_dotenv
import psycopg2

# Load environment variables from a .env file
load_dotenv()

app = Flask(__name__)

# Configure Mail using environment variables
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

mail = Mail(app)

# PostgreSQL connection function
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        dbname=os.getenv('DB_NAME'),
        port=os.getenv('DB_PORT', 5432)  # Optional: defaults to 5432
    )

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/enquiry', methods=['GET', 'POST'])
def enquiry():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        
        # Send email
        try:
            msg = Message(
                'New Enquiry Submission',
                recipients=[os.getenv('MAIL_USERNAME')],
                body=f'You have a new enquiry from {name}.\n\n'
                     f'Email: {email}\n'
                     f'Phone: {phone}\n'
                     f'Message: {message}'
            )
            mail.send(msg)
        except Exception as e:
            return f"An error occurred while sending the email: {str(e)}"
        
        # Save to PostgreSQL
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO enquiries (name, email, phone, message)
                VALUES (%s, %s, %s, %s)
            """, (name, email, phone, message))
            conn.commit()
            cursor.close()
            conn.close()
            return "Enquiry submitted successfully! We will get back to you soon."
        
        except Exception as e:
            return f"An error occurred while saving the enquiry: {str(e)}"
        
    return render_template('enquiry.html')

# Additional routes
@app.route('/acinstallation', methods=['GET'])
def ac():
    return render_template("acinstallation.html")

@app.route('/about', methods=['GET'])
def about():
    return render_template("about.html")

@app.route('/contact', methods=['GET'])
def contact():
    return render_template("contact.html")

@app.route('/broucher', methods=['GET'])
def broucher():
    return render_template("broucher.html")

@app.route('/career', methods=['GET'])
def career():
    return render_template("career.html")

@app.route('/fabrication', methods=['GET'])
def fab():
    return render_template("fabrication.html")

@app.route('/repairs', methods=['GET'])
def repairs():
    return render_template("repairs.html")

# Run app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
