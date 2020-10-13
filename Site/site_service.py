from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)


bp = Blueprint('mipmlp', __name__, url_prefix='/mipmlp')


@bp.route('/Home', methods=('GET', 'POST'))
def home_page():
    message = None
    if request.method == 'POST':
        otu_file = request.form['otu_file']
        tag_file = request.form['tag_file']
        taxonomy_level = request.form['taxonomy_level']
        taxnomy_group = request.form['taxnomy_group']
        epsilon = request.form['epsilon']
        z_scoring = request.form['z_scoring']
        PCA = request.form['PCA']
        normalization = request.form['normalization']
        norm_after_rel = request.form['norm_after_rel']

        error = None


        # input validation

        flash(error)
        if not error:

            return render_template('home.html', active='Home', otu_file=otu_file)
    return render_template('home.html', active='Home')


@bp.route('/Help')
def help_page():
    return render_template('help.html', active='Help')


@bp.route('/Example')
def example_page():
    return render_template('example.html', active='Example')


@bp.route('/About')
def about_page():
    return render_template('about.html', active='About')
