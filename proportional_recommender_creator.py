import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import scipy.stats as stats
import graphlab



survey_prop_sf = graphlab.SFrame('data/survey_proportion.sframe')

shuffle_sf = graphlab.cross_validation.shuffle(survey_prop_sf, random_seed=7)
folds = graphlab.cross_validation.KFold(shuffle_sf, 3)

invasive_params = dict([('user_id', 'site'), ('item_id', 'taxa'), ('target', '%present')])
endangered_params = dict([('user_id', 'taxa'), ('item_id', 'site'), ('target', '%present')])

invasive_rec2_job = graphlab.toolkits.model_parameter_search.create(folds, 
                                                                    graphlab.factorization_recommender.create, 
                                                                    invasive_params, 
                                                                    perform_trial_run=True)

invasive_rec2_results = invasive_rec2_job.get_results()


invasive_rec3_job = graphlab.toolkits.model_parameter_search.create(folds, 
                                                                    graphlab.ranking_factorization_recommender.create, 
                                                                    invasive_params, 
                                                                    perform_trial_run=True)

invasive_rec3_results = invasive_rec3_job.get_results()

endangered_rec2_job = graphlab.toolkits.model_parameter_search.create(folds, 
                                                                      graphlab.factorization_recommender.create, 
                                                                      endangered_params, 
                                                                      perform_trial_run=True)
endangered_rec2_results = endangered_rec2_job.get_results()


endangered_rec3_job = graphlab.toolkits.model_parameter_search.create(folds, 
                                                                      graphlab.ranking_factorization_recommender.create, 
                                                                      endangered_params, 
                                                                      perform_trial_run=True)

endangered_rec3_results = endangered_rec3_job.get_results()

#The sixth model looks like the model for me.
invasive_rec2_results

#Model 3 or 6 look good. probably 6.
invasive_rec3_results

endangered_rec2_results

endangered_rec3_results

invasive_rec2_job.get_best_params()

params = invasive_rec3_job.get_best_params()
invasive_rec3 = graphlab.recommender.ranking_factorization_recommender.create(survey_prop_sf, **params)

params = endangered_rec3_job.get_best_params()
endangered_rec3 = graphlab.recommender.ranking_factorization_recommender.create(survey_prop_sf, **params)

invasive_rec3.save('models/survey_propotional_invasive_recommender')
endangered_rec3.save('models/survey_propotional_endangered_recommender')