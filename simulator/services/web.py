import csv
from datetime import datetime

from flask import Flask, render_template

from simulator.settings import LOG_DIR_PATH, LOG_FILE_NAME_TEMPLATE

app = Flask(__name__, template_folder='template')


@app.route('/')
def pv_simulator():

    # Create data here for plotting
    file_name = LOG_DIR_PATH.joinpath(LOG_FILE_NAME_TEMPLATE.format(datetime.now().strftime('%Y-%m-%d')))
    timestamp = []
    power = []

    with open(file_name, 'r') as csvfile:
        lines = csv.reader(csvfile, delimiter=',')
        next(lines, None)
        for row in lines:
            timestamp.append(row[0])
            power.append(row[3])
    return render_template("index.html", x=timestamp, y=power)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=7005)
