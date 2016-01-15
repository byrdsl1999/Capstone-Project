
import scipy.stats as stats
import graphlab


'''
The final optimized parameters are:

invasive_rec3_job.get_best_params()
{'regularization': 1e-08, 'user_id': 'site', 'num_factors': 16, 'binary_target': True,
 'ranking_regularization': 0.1, 'num_sampled_negative_examples': 4, 'target': 'dummy',
  'item_id': 'taxa', 'max_iterations': 25} 


endangered_rec3_job.get_best_params()

def make_recommender():
{'regularization': 0.0001, 'user_id': 'taxa', 'num_factors': 32, 'binary_target': True,
 'ranking_regularization': 0.5, 'num_sampled_negative_examples': 8, 'target': 'dummy',
  'item_id': 'site', 'max_iterations': 25} 

'''
  survey_prop_sf = graphlab.SFrame('data/presence_absence.sframe')
  survey_prop_sf['dummy']=1

  shuffle_sf = graphlab.cross_validation.shuffle(survey_prop_sf, random_seed=7)
  folds = graphlab.cross_validation.KFold(shuffle_sf, 3)

  invasive_params = dict([('user_id', 'site'), ('item_id', 'taxa'), ('target', 'dummy'), ('binary_target', True)])
  endangered_params = dict([('user_id', 'taxa'), ('item_id', 'site'), ('target', 'dummy'), ('binary_target', True)])

  invasive_rec2_job = graphlab.toolkits.model_parameter_search.create(folds, 
                                                                      graphlab.factorization_recommender.create, 
                                                                      invasive_params, 
                                                                      return_model=True,
                                                                      perform_trial_run=True)

  invasive_rec2_results = invasive_rec2_job.get_results()


  invasive_rec3_job = graphlab.toolkits.model_parameter_search.create(folds, 
                                                                      graphlab.ranking_factorization_recommender.create, 
                                                                      invasive_params, 
                                                                      return_model=True,
                                                                      perform_trial_run=True)

  invasive_rec3_results = invasive_rec3_job.get_results()

  endangered_rec2_job = graphlab.toolkits.model_parameter_search.create(folds, 
                                                                        graphlab.factorization_recommender.create, 
                                                                        endangered_params, 
                                                                        return_model=True,
                                                                        perform_trial_run=True)
  endangered_rec2_results = endangered_rec2_job.get_results()


  endangered_rec3_job = graphlab.toolkits.model_parameter_search.create(folds, 
                                                                        graphlab.ranking_factorization_recommender.create, 
                                                                        endangered_params, 
                                                                        return_model=True,
                                                                        perform_trial_run=True)

  endangered_rec3_results = endangered_rec3_job.get_results()

  #The sixth model looks like the model for me.
  print invasive_rec2_results

  #Model 3 or 6 look good. probably 6.
  print invasive_rec3_results

  endangered_rec2_results

  endangered_rec3_results

  invasive_rec2_job.get_best_params()

  params = invasive_rec3_job.get_best_params()
  print params, "params = invasive_rec3_job.get_best_params()"
  params2 = endangered_rec3_job.get_best_params()
  print params2, "endangered_rec3_job.get_best_params()"
  invasive_rec3 = graphlab.recommender.ranking_factorization_recommender.create(survey_prop_sf, **params)

  params = endangered_rec3_job.get_best_params()
  endangered_rec3 = graphlab.recommender.ranking_factorization_recommender.create(survey_prop_sf, **params)

  invasive_rec3.save('models/binary_invasive_recommender')
  endangered_rec3.save('models/binary_endangered_recommender')

if __name__ == "__main__":
  make_recommender()