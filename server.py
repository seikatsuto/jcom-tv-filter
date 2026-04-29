from flask import Flask, send_file
from scraper import create_csv

app = Flask(__name__)

@app.route("/download")
def download():
    filename = create_csv()
    return send_file(
        filename,
        as_attachment=True
    )

if __name__ == "__main__":
    app.run(port=5000)