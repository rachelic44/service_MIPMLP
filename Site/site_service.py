from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)


bp = Blueprint('mipmlp', __name__, url_prefix='/mipmlp')


@bp.route('/Home', methods=('GET', 'POST'))
def home_page():
    message = None
    if request.method == 'POST':
        otu_file = request.files['otu_file']
        tag_file = request.files['tag_file']
        taxonomy_level = request.form['taxonomy_level']
        taxnomy_group = request.form['taxnomy_group']
        epsilon = request.form['epsilon']
        z_scoring = request.form['z_scoring']
        PCA = request.form['PCA']
        normalization = request.form['normalization']
        norm_after_rel = request.form['norm_after_rel']

        otu_file.save("OTU.csv")
        tag_file.save("TAG.csv")
        params = {'taxonomy_level': taxonomy_level, 'taxnomy_group': taxnomy_group, 'epsilon': epsilon,
                  'normalization': normalization, 'z_scoring': z_scoring, 'norm_after_rel': norm_after_rel,
                  'std_to_delete': 0, 'pca': (PCA, 'PCA')}
        # service.evaluate(params)
        #
        # # create a ZipFile object
        # with ZipFile('sampleDir.zip', 'w') as zipObj:
        #     # Iterate over all the files in directory
        #     for folderName, subfolders, filenames in os.walk("Mucositis"):
        #         for filename in filenames:
        #             # create complete filepath of file in directory
        #             filePath = os.path.join(folderName, filename)
        #             # Add file to zip
        #             zipObj.write(filePath, basename(filePath))
        #     for folderName, subfolders, filenames in os.walk("preprocess_plots"):
        #         for filename in filenames:
        #             # create complete filepath of file in directory
        #             filePath = os.path.join(folderName, filename)
        #             # Add file to zip
        #             zipObj.write(filePath, basename(filePath))

        image1 = 'Site\preprocess_plots\correlation_heatmap_patient.png'

        images_names = [
            'Site\preprocess_plots\correlation_heatmap_patient.png',
            'Site/preprocess_plots/Correlation_between_each_component_and_the_labelprognosistask.svg',
            'Site/preprocess_plots/Correlation_between_each_component_and_the_labelprognosistask.svg',
            'Site/preprocess_plots/correlation_heatmap_patient.png',
            'Site/preprocess_plots/correlation_heatmap_bacteria.png',
            'Site\preprocess_plots\Correlation_between_each_component_and_the_labelprognosistask.svg'
        ]
        # return send_file("sampleDir.zip", mimetype='zip', as_attachment=True,)

        error = None

        # input validation

        flash(error)
        if not error:
            return render_template('home.html', active='Home', otu_file=otu_file, tag_file=tag_file,
                                   taxonomy_level=taxonomy_level,
                                   taxnomy_group=taxnomy_group, epsilon=epsilon, z_scoring=z_scoring, PCA=PCA,
                                   normalization=normalization,
                                   norm_after_rel=norm_after_rel,
                                   images_names=images_names,
                                   image1=image1)

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
