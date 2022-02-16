from flask import Flask, render_template, jsonify, request, redirect
from flask_sqlalchemy import SQLAlchemy
from config import Testing, DbConfigProd, DbConfigTest
from logger import WriteToLog
from datetime import datetime, timezone
import re


# App Configuration.
app = Flask(__name__)
if Testing == True:
    app.config.from_object(DbConfigTest)
else:
    app.config.from_object(DbConfigProd)
db = SQLAlchemy(app)


# Redirect to Home Page.
@app.route("/nft-rarity-distributions")
def homepage1():
    return redirect("/nft-rarity-distributions/all")

# Redirect to Home Page.
@app.route("/nft-rarity-distributions/")
def homepage2():
    return redirect("/nft-rarity-distributions/all")

# PRODUCTION: All Collections.
@app.route("/nft-rarity-distributions/all")
def all_collections():
    page = request.args.get('page', 1, type=int)
    all_collections = db.session.query(Collection).order_by(Collection.name).paginate(page=page, per_page=40)
    return render_template("collections_all.html", collections = all_collections)


# PRODUCTION: Irregular Collections.
@app.route("/nft-rarity-distributions/irregular")
def irregular_collections():
    page = request.args.get('page', 1, type=int)
    collections = db.session.query(Collection).filter((Collection.irregular_distribution == 1) | (Collection.irregular_distribution == 3)).order_by(Collection.irregular_distribution.asc(), Collection.name.asc()).paginate(page=page, per_page=40)
    return render_template("collections_irregular.html", collections = collections)


# TEST: New Collections.
@app.route("/nft-rarity-distributions/new")
def new_collections():
    collections = db.session.query(Collection).order_by(Collection.id.desc())
    return render_template("collections_new.html", collections = collections[0:40])


# PRODUCTION: Search.
@app.route("/nft-rarity-distributions/search/<string:address>")
def search_collections(address):
    # If 'None', return error.
    if address == 'None':
        return render_template('error.html', message = (address, "Invalid contract address."))
    try:
        # Verify submitted address is valid; chain, contract, etc.
        x = re.search("(^0x[A-Fa-f0-9]{40})", address)
        if x:
            job_exists = db.session.query(db.exists().where(Job.address == address))
            if(str(job_exists.scalar()) == "False"):
                # Valid Ethereum Address: If not in Jobs, submit to Jobs, display submitted.html
                date = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
                job = Job(address=address, date_submitted=date, status='queued', data=0)
                db.session.add(job)
                db.session.commit()
                return render_template('submitted.html', job = job)
            else:
                # If in Jobs, check if processed.
                job = db.session.query(Job).filter(Job.address == address).one()
                if job.status == 'processed' and job.data == 1:
                    # If Job processed already, get Collection, display collection.html
                    col_exists = db.session.query(db.exists().where(Collection.address == address))
                    if (str(col_exists.scalar()) == "True"):
                        collection = db.session.query(Collection).filter(Collection.address == address).one()
                        return render_template('collection.html', collection = collection)
                    else:
                        return render_template('submitted.html', job = job)
                else:
                    # If Job isn't 'processed' return status.
                    return render_template('submitted.html', job = job)
        else:
            return render_template('error.html', message = (address, "Invalid contract address."))
    except Exception as ex:
        WriteToLog('error', 'error searching for address: {}\nError: {}'.format(address, ex))
        if hasattr(ex, 'message'):
            return render_template('error.html', message = (address, ex.message))
        else:
            return render_template('error.html', message = (address, ex))


# TEST: Home Page.
@app.route("/nft-rarity-distributions-TEST")
def test_homepage():
    return redirect("/nft-rarity-distributions-TEST/all")

# TEST: All Collections.
@app.route("/nft-rarity-distributions-TEST/all")
def test_all_collections():
    # Set the pagination configuration
    page = request.args.get('page', 1, type=int)
    collections = db.session.query(Collection).order_by(Collection.name).paginate(page=page, per_page=40)
    return render_template("test_collections_all.html", collections = collections)

# TEST: Irregular Collections.
@app.route("/nft-rarity-distributions-TEST/irregular")
def test_irregular_collections():
    page = request.args.get('page', 1, type=int)
    collections = db.session.query(Collection).filter((Collection.irregular_distribution == 1) | (Collection.irregular_distribution == 3)).order_by(Collection.irregular_distribution.asc(), Collection.name.asc()).paginate(page=page, per_page=40)
    return render_template("test_collections_irregular.html", collections = collections)

# TEST: New Collections.
@app.route("/nft-rarity-distributions-TEST/new")
def test_new_collections():
    collections = db.session.query(Collection).order_by(Collection.id.desc())
    return render_template("test_collections_new.html", collections = collections[0:40])

# TEST: Search.
@app.route("/nft-rarity-distributions-TEST/search/<string:address>")
def test_search_collections(address):
    try:
        back = request.referrer
        # Verify submitted address is valid; chain, contract, etc.
        x = re.search("(^0x[A-Fa-f0-9]{40})", address)
        if x:
            job_exists = db.session.query(db.exists().where(Job.address == address))
            if(str(job_exists.scalar()) == "False"):
                # Valid Ethereum Address: If not in Jobs, submit to Jobs, display submitted.html
                date = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
                job = Job(address=address, date_submitted=date, status='queued', data=0)
                db.session.add(job)
                db.session.commit()
                return render_template('submitted.html', job = job)
            else:
                # If in Jobs, check if processed.
                job = db.session.query(Job).filter(Job.address == address).one()
                if job.status == 'processed' and job.data == 1:
                    # If Job processed already, get Collection, display collection.html
                    col_exists = db.session.query(db.exists().where(Collection.address == address))
                    if (str(col_exists.scalar()) == "True"):
                        collection = db.session.query(Collection).filter(Collection.address == address).one()
                        return render_template('test_collection.html', collection = collection)
                    else:
                        return render_template('submitted.html', job = job)
                else:
                    # If Job isn't 'processed' return status.
                    return render_template('submitted.html', job = job)
                #else:
                    #return render_template('error.html', 'Error with job, Status: {}\nID: {}\nAddress: {}.'.format(job.status, job.id, job.address))
        else:
            return render_template('error.html', "Invalid contract address.", back=back)
    except Exception as ex:
        WriteToLog('error', 'error searching for address: {}\nError: {}'.format(address, ex))
        if hasattr(ex, 'message'):
            return render_template('error.html', ex.message)
        else:
            return render_template('error.html', ex)




class Job(db.Model):
    __tablename__ = "jobs"
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(64), nullable=False)
    date_submitted = db.Column(db.DateTime, nullable=False)
    last_updated = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(10), nullable=False, default="queued")
    data = db.Column(db.Integer, nullable=False, default=0)
    error_message = db.Column(db.String(255), nullable=True)

class Collection(db.Model):
    __tablename__ = "collections"
    id = db.Column(db.Integer, primary_key=True)
    chain = db.Column(db.String(255), nullable=False)
    token_schema = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(64), nullable=False)
    owner_address = db.Column(db.String(64), nullable=False)
    irregular_distribution = db.Column(db.Integer, nullable=True)
    collection_image_url = db.Column(db.String(255), nullable=True)
    rarity_image_url = db.Column(db.String(255), nullable=False)
    metadata_url = db.Column(db.String(255), nullable=True)
    token_table_url = db.Column(db.String(255), nullable=True)
    marketplace_url = db.Column(db.String(255), nullable=False)
    explorer_url = db.Column(db.String(255), nullable=False)
    twitter_url = db.Column(db.String(255), nullable=True)
    discord_url = db.Column(db.String(255), nullable=True)
    medium_url = db.Column(db.String(255), nullable=True)
    instagram_url = db.Column(db.String(255), nullable=True)
    telegram_url = db.Column(db.String(255), nullable=True)
    wiki_url = db.Column(db.String(255), nullable=True)
    last_updated = db.Column(db.DateTime, nullable=False)