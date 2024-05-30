from flask import Blueprint, jsonify, render_template

# Create a Blueprint instance
wiki = Blueprint('wiki', __name__)

@wiki.route('/')
def wiki_index():
    return render_template("wiki/index.html")

@wiki.route('/software/faq')
def software_faq():
    return render_template("/wiki/sw_faq.html")

@wiki.route('/software/doku')
def software_doku():
    return 200

@wiki.route('/software/definitions')
def software_definitions():
    return render_template("wiki/sw_definitionen.html")