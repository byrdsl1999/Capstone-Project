import graphlab
import pandas as pd

binary_sf = graphlab.load_sframe('data/presence_absence.sframe/')
proportional_sf = graphlab.load_sframe('data/survey_proportion.sframe/')

proportional_df = proportional_sf.to_dataframe()
proportional_lookup_table = proportional_df.pivot_table(values= '%present', index='site', columns='taxa', fill_value=0.)

binary_df = binary_sf.to_dataframe()
binary_lookup_table = binary_df.pivot_table(values= 'present', index='site', columns='taxa', fill_value=0)

