
# A very simple Flask Hello World app for you to get started with...

from datetime import datetime

from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


@app.route("/nft-rarity-distributions")
def main():
    ip = request.headers.get("X-Real-Ip", "")
    now = datetime.utcnow().isoformat()
    job_id = f"{ip}{now}"

    data = Job(slug=job_id)
    db.session.add(data)
    db.session.commit()

    return render_template("main.html", job_id=job_id)


@app.route("/query", methods=["POST"])
def query():
    job_id = request.form["id"]
    data = Job.query.filter_by(slug=job_id).first()
    return jsonify(
        {
            "state": data.state,
            "result": data.result,
        }
    )


class Job(db.Model):
    __tablename__ = "jobs"
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(64), nullable=False)
    state = db.Column(db.String(10), nullable=False, default="queued")
    result = db.Column(db.Integer, default=0)