from flask import Flask, render_template, request, redirect, url_for, session
import pickle

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'mysecretkey'

# Mock user data
users = {
    'user1': {
        'username': 'user1',
        'password': 'password1'
    },
    'user2': {
        'username': 'user2',
        'password': 'password2'
    }
}


@app.route('/', methods=['POST', 'GET'])
def home():
    # Check if the user is logged in
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == "POST":
        with open('model.pkl', 'rb') as f:
            data = pickle.load(f)
        max_temp = int(request.form.get('maxtempC', None))
        min_temp = int(request.form.get('mintempC', None))
        cloud_cover = int(request.form.get('cloudcover', None))
        humidity = int(request.form.get('humidity', None))
        sun_hour = float(request.form.get('sunHour', None))
        heat_index = int(request.form.get('HeatIndexC', None))
        pressure = int(request.form.get('pressure', None))
        precipitation = float(request.form.get('precipMM ', None))
        wind_speed = int(request.form.get('windspeedKmph', None))
        print([max_temp, min_temp, cloud_cover, humidity, sun_hour,
              heat_index, precipitation, pressure, wind_speed])
        out = data.predict([[max_temp, min_temp, cloud_cover, humidity,
                           sun_hour, heat_index, precipitation, pressure, wind_speed]])
        out = round(out[0], 2)
        return render_template('123.html', output=out)
    return render_template('123.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if the username and password are correct
        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('home'))

        # If the username or password is incorrect, show an error message
        error = 'Invalid username or password'
        return render_template('login.html', error=error)

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
