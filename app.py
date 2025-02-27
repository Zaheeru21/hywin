from flask import Flask, request, render_template
import mysql.connector
from flask_mail import Mail, Message

app = Flask(__name__)  # Corrected the variable name

# Configure MySQL connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",    
        user="root",         
        password="1234",         
        database="enquiry_db" 
    )

app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Example for Gmail SMTP server
app.config['MAIL_PORT'] = 465  # Secure SSL port
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'sendmemail303@gmail.com'  # Your email address here
app.config['MAIL_PASSWORD'] = 'snwp kpny pgst pugf'  # Your email password here (use App Password if 2FA enabled)
app.config['MAIL_DEFAULT_SENDER'] = 'sendmemail303@gmail.com'  # Your email address here

mail = Mail(app)

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/enquiry', methods=['GET', 'POST'])
def enquiry():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        
        # Send email first
        try:
            msg = Message(
                'New Enquiry Submission',  # Subject
                recipients=['sendmemail303@gmail.com'],  # Send to this email address
                body=f'You have a new enquiry from {name}.\n\n'
                     f'Email: {email}\n'
                     f'Phone: {phone}\n'
                     f'Message: {message}'
            )
            
            # Send the email
            mail.send(msg)
        except Exception as e:
            return f"An error occurred while sending the email: {str(e)}"
        
        # Now, connect to the database and save the enquiry
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

@app.route('/acinstallation', methods=['GET', 'POST'])
def ac():
    return render_template("acinstallation.html")

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template("about.html")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template("contact.html")

@app.route('/broucher', methods=['GET', 'POST'])
def broucher():
    return render_template("broucher.html")

@app.route('/career', methods=['GET', 'POST'])
def career():
    return render_template("career.html")

@app.route('/fabrication', methods=['GET', 'POST'])
def fab():
    return render_template("fabrication.html")

@app.route('/repairs', methods=['GET', 'POST'])
def repairs():
    return render_template("repairs.html")
# Corrected this line to check for '__name__'
if __name__ == '__main__':
    app.run(debug=True, port=5001)
