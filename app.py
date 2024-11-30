from flask import Flask,render_template,request,url_for,session,redirect;
import os

from werkzeug.utils import secure_filename;

app = Flask(__name__);

app.secret_key = "srilord33"
upload_folder = 'static/uploads';
app.config['UPLOAD_FOLDER'] = upload_folder;


@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        name = request.form['user-name']
        role = request.form['user-role']
        imagepath = None
        cvpath = None
        github = request.form['user-github']
        linkedin = request.form['user-linkedin']
        if 'user-image' in request.files:
            image = request.files['user-image']
            if image.filename != '':
                filename = secure_filename(image.filename)
                imagepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
                print(imagepath)
                image.save(imagepath)
                session['imagepath'] = imagepath
            else:
                print('no image')
        if 'user-cv' in request.files:
            cv = request.files['user-cv']
            if cv.filename != '':
                filename = secure_filename(cv.filename)
                cvpath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
                print(cvpath)
                cv.save(cvpath)
                session['cvpath'] = filename
            else:
                print("Upload cv")
        return render_template(
            'portfolio.html',
            name=name,
            role = role,
            image = session.get('imagepath'),
            cv = session.get('cvpath'),
            github = github,
            linkedin = linkedin);
    return render_template('index.html');

@app.route('/logout')
def logout():
    imagepath = session.get('imagepath')
    if 'imagepath' in session:
        fullpath = os.path.abspath(session['imagepath'])
        if os.path.exists(fullpath):
            os.remove(fullpath)
            session.pop('imagepath')
            print('file cleaned')
        else:
            print('file not found')
    session.clear()
    return redirect(url_for('index'));
if __name__ == '__main__':
    app.run(debug=True)