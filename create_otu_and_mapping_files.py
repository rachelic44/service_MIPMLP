import pickle
import sys
import os
import numpy as np
#sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
from preprocess_grid import preprocess_data
from plot_rho import draw_X_y_rhos_calculation_figure
from plot_3D_pca import PCA_t_test, plot_data_3d, plot_data_2d



class CreateOtuAndMappingFiles(object):
    # get two relative path of csv files
    def __init__(self, otu_file_path, tags_file_path):
        self.otu_path = otu_file_path
        self.tags_path = tags_file_path
        print('read tag file...')
        self.extra_features_df = pd.read_csv(self.tags_path).drop(['Tag'], axis=1)
        self.tags_df = pd.read_csv(self.tags_path)[['ID', 'Tag']]
        # set index as ID
        self.tags_df = self.tags_df.set_index('ID')
        self.tags_df.index = self.tags_df.index.astype(str)
        self.extra_features_df = self.extra_features_df.set_index('ID')
        # subset of ids according to the tags data frame
        self.ids = self.tags_df.index.tolist()
        self.ids.append('taxonomy')
        print('read otu file...')
        self.otu_features_df = pd.read_csv(self.otu_path)
        self.otu_features_df = self.otu_features_df.set_index('ID')
        self.otu_features_df.index = self.otu_features_df.index.astype(str)
        self.pca_ocj = None
        self.pca_comp = None

    def csv_to_learn(self, task_name, folder, tax):
        tag_ids = list(self.tags_df.index)
        otu_ids = list(self.otu_features_df_b_pca.index)
        mutual_ids = list(set(tag_ids).intersection(set(otu_ids)))
        # use only the samples the correspond to the tag file
        self.otu_features_df = self.otu_features_df.loc[mutual_ids]
        self.tags_df = self.tags_df.loc[mutual_ids]
        # concat with extra features by index
        df = self.otu_features_df.join(self.extra_features_df)
        # create a new csv file
        otu_path = os.path.join(folder, 'OTU_merged_' + str(task_name) + '.csv')
        df.to_csv(otu_path)
        tag_path = os.path.join(folder, 'Tag_file_' + str(task_name) + '.csv')
        self.tags_df.to_csv(tag_path)
        if self.pca_ocj:
            pca_path = os.path.join(folder, "Pca_obj_" + str(task_name) + '.pkl')
            pickle.dump(self.pca_ocj, open(pca_path, "wb"))
        else:
            pca_path = "No pca created"
        with open(os.path.join(folder, "bacteria_tax_level_" + str(tax) + ".txt"), "w") as bact_file:
            for col in self.bacteria:

                bact_file.write(str(col) + "\n")
        return otu_path, tag_path, pca_path

    def preprocess(self, preprocess_params, visualize):
        #print('preprocess...')
        taxnomy_level = int(preprocess_params['taxonomy_level'])
        
        self.otu_features_df, self.otu_features_df_b_pca, self.pca_ocj, self.bacteria, self.pca_comp = preprocess_data(self.otu_features_df, preprocess_params, self.tags_df, visualize_data=visualize)
        # otu_features_df is the processed data, before pca
        if int(preprocess_params['pca'][0]) == 0 :
            self.otu_features_df = self.otu_features_df_b_pca
        
    def rhos_and_pca_calculation(self, task, tax, pca, rhos_folder, pca_folder):
        # -------- rhos calculation --------
        tag_ids = list(self.tags_df.index)
        otu_ids = list(self.otu_features_df.index)
        mutual_ids = list(set(tag_ids).intersection(set(otu_ids)))
        X = self.otu_features_df.loc[mutual_ids]
        y = np.array(list(self.tags_df.loc[mutual_ids]["Tag"])).astype(int)

        if not os.path.exists(rhos_folder):
            os.makedirs(rhos_folder)
        
        bacterias = X.columns
        bacterias_to_dump = []
        for i, bact in enumerate(bacterias):
            f = X[bact]
            num_of_different_values = set(f)
            if len(num_of_different_values) < 2:
                bacterias_to_dump.append(bact)
        print("number of bacterias to dump after intersection: " + str(len(bacterias_to_dump)))
        print("percent of bacterias to dump after intersection: " + str(len(bacterias_to_dump)/len(bacterias) * 100) + "%")
        X = X.drop(columns=bacterias_to_dump)
        self.otu_features_df = X 
               
        draw_X_y_rhos_calculation_figure(X, y, task, tax, save_folder=rhos_folder)

        # -------- PCA visualizations --------
        if not os.path.exists(pca_folder):
            os.makedirs(pca_folder)
        PCA_t_test(group_1=[x for x, y in zip(X.values, y) if y == 0], group_2=[x for x, y in zip(X.values, y) if y == 1],
                   title="T test for PCA dimentions on " + task, save=True, folder=pca_folder)
        if pca >= 2:
            plot_data_2d(X.values, y, data_name=task.capitalize(), save=True, folder=pca_folder)
            if pca >= 3:
               plot_data_3d(X.values, y, data_name=task.capitalize(), save=True, folder=pca_folder)


if __name__ == "__main__":
    task = 'prognostic_VItamin_A_task'
    bactria_as_feature_file = '../pregnancy_diabetes/merged_microbiome_taxonomy.csv'
    samples_data_file = '../pregnancy_diabetes/mapping_table.csv'
    rhos_folder = os.path.join('..', 'pregnancy_diabetes', 'rhos')
    pca_folder = os.path.join('..', 'pregnancy_diabetes', 'pca')

    # parameters for preprocess
    tax = 6
    preprocess_prms = {'taxonomy_level': tax, 'taxnomy_group': 'sub PCA', 'epsilon': 0.1, 'normalization': 'log',
                       'z_scoring': 'No', 'norm_after_rel': '', 'std_to_delete': 0, 'pca': (0, 'PCA')}

    mapping_file = CreateOtuAndMappingFiles(bactria_as_feature_file, samples_data_file)
    mapping_file.preprocess(preprocess_params=preprocess_prms, visualize=False)
    #mapping_file.rhos_and_pca_calculation(task, preprocess_prms['taxonomy_level'], preprocess_prms['pca'],
    #                                      rhos_folder, pca_folder)

    otu_path, tag_path, pca_path = mapping_file.csv_to_learn('VItamin_A_task', os.path.join('..', 'pregnancy_diabetes'), tax=tax)

    print(otu_path)
    print(tag_path)
    print(pca_path)


