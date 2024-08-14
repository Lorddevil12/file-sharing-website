from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
import os
import uuid

app = Flask(__name__)
app.secret_key = 'supersecretkey'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file:
            unique_filename = str(uuid.uuid4()) + "_" + file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
            flash(f'File sent successfully! Share this code with the recipient: {unique_filename}')
            return redirect(url_for('index'))

    return render_template('send.html')

@app.route('/receive', methods=['GET', 'POST'])
def receive():
    if request.method == 'POST':
        file_code = request.form['file_code']
        if file_code == '':
            flash('Please enter a file code')
            return redirect(request.url)

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_code)
        if os.path.exists(file_path):
            return send_from_directory(app.config['UPLOAD_FOLDER'], file_code, as_attachment=True)
        else:
            flash('File not found')
            return redirect(request.url)

    return render_template('receive.html')

if __name__ == '__main__':
    app.run(debug=True)