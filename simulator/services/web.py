import base64
import datetime
from io import BytesIO

import pandas as pd
from flask import Flask
from matplotlib.figure import Figure

from simulator import settings as _settings

app = Flask(__name__)


@app.route("/")
def get_pv_power_plot():
    """
    Plot PV with timestamp
    Note: Using pandas and matplotlib to show the graph here for testing, it's not recommended for production
    """
    # create data for plotting here
    file_name = _settings.LOG_DIR_PATH.joinpath(_settings.LOG_FILE_NAME_TEMPLATE.format(datetime.datetime.now().strftime('%Y-%m-%d')))
    data = pd.read_csv(file_name)
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data = data[['timestamp', 'sum']].rename(
        columns={
            "timestamp": "timestamp",
            "sum": "Power (KW)"
        }
    )

    # Plot data here
    fig = Figure()
    ax = fig.subplots()
    fig.suptitle('PV Simulation (refresh to see current data)', fontsize=20)
    ax.set_xlabel('timestamp', fontsize=18)
    ax.set_ylabel('Power (KW)', fontsize=16)
    data.groupby(data["timestamp"].dt.hour).plot(x='timestamp', y='Power (KW)', ax=ax, legend=False)

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")

    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=7005)
