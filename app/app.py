from flask import Flask, request, render_template
import cPickle as pickle
import pandas as pd
import numpy
import graphlab
app = Flask(__name__)


# Creating/importing useful objects/lists
species_df= pd.read_csv('data/species_table.csv')
species_list = set(species_df['scientific_name'].str.upper())
common_name_list = set(species_df['common_name'].str.upper())

introduced_list = set(pd.read_csv('data/introduced_species.csv', header= None)[0].str.upper())
endangered_list = set(pd.read_csv('data/endangered_species.csv', header= None)[0].str.upper())

site_prefixes=pd.read_csv('data/gridsquareprefixesCombined.csv', header=None, na_filter=False)
sites = set()
for prefix in site_prefixes[0]:
    for i in xrange(10):
        for j in xrange(10):
            sites.add(prefix+str(i)+str(j))

regions = pd.read_csv('data/Region_names.csv', header=None, na_filter=False)
region_dict = regions.set_index([0]).to_dict()[1]



# home page
@app.route('/home')
@app.route('/')
def index():
    return render_template('index.html')

    # return '''

    #     <form action="/invasive" method='POST' >
    #         <input type="text" name="user_input2" />
    #         <input type="submit" />
    #     </form>
    #     <p>
    #     Enter a site ID(eg SU56, NG25), and press 'submit query'. The most likely invasive species will then be returned.
    #     </p>

    #     <p> OR </p>
    #     <form action="/endangered" method='POST' >
    #         <input type="text" name="user_input" />
    #         <input type="submit" />
    #     <p>
    #     Enter a flowering plant species(latin name, eg Alisma gramineum), and press 'submit query'. The best sites for relocation will then be returned.
    #     </p>
    #     '''


#invasive prediction page

@app.route('/invasive', methods=['POST'] )
def inv_submit():
    inquiry = [str(request.form['user_input2']).upper()]
    if (inquiry[0] not in sites):
        return """
    The site: """+inquiry[0]+""" does not appear to be in our database.
    <a href="/home">Return home.</a>
    """
    prediction = invasive_recommender.recommend(inquiry, k=50).to_dataframe()
    prediction_html = prediction.to_html()
    prediction['taxa'].iloc[0]
    table_data=""
    for i in xrange(len(prediction)):
        flags = ""
        print i
        if str(prediction['taxa'][i]).upper() in introduced_list:
            flags += 'invasive '
        if str(prediction['taxa'][i]).upper() in endangered_list:
            flags += 'protected '

        map_url = 'https://data.nbn.org.uk/img/hundredKmSelector/'+str(prediction['site'][i])[:-2]+'.gif'
        plant_url = 'https://en.wikipedia.org/wiki/'+ str(prediction['taxa'][i]).split()[0]
        table_data= table_data+'''
            <tr>
            <td>'''+ '<a href="' +plant_url+ '" target="_blank">'+ str(prediction['taxa'][i]) +'</a>' +'''</td>
            <td>'''+ str(prediction['rank'][i]) +'''</td>
            <td>'''+ str(prediction['site'][i]) +'''</td>
            <td>'''+ '<a href="'+map_url+'" target="_blank">'+region_dict[str(prediction['site'][i])[:-2]]+'</a>' +'''</td>
            <td>'''+ str(prediction['score'][i]) +'''</td>
            <td>'''+ flags +'''</td>
            </tr>
            '''

    page = '''
    <!DOCTYPE html>
<html class="full" lang="en">
<!-- Make sure the <html> tag is set to the .full CSS class. Change the background image in the full.css file. -->


<head>

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>Invasive Species Predictor</title>

    <!-- Bootstrap Core CSS -->
    <link href="../static/css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom CSS -->
    <link href="../static/css/sb-admin-2.css" rel="stylesheet">

    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
        <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
        <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->

</head>

<body>
    
<table class="table">
                  <thead>
                      <tr class="filters">
                          <th><input type="text" class="form-control" placeholder="Taxa" disabled></th>
                          <th><input type="text" class="form-control" placeholder="Rank" disabled></th>
                          <th><input type="text" class="form-control" placeholder="Site" disabled></th>
                          <th><input type="text" class="form-control" placeholder="Region" disabled></th>
                          <th><input type="text" class="form-control" placeholder="Score" disabled></th>
                          <th><input type="text" class="form-control" placeholder="Flags" disabled></th>
                      </tr>
                  </thead>
                  <tbody>''' + table_data + '''

                  </tbody>
              </table>
</body>

</html>

    '''
    print inquiry
    return page


# #endangered prediction page
@app.route('/endangered', methods=['POST'] )
def end_submit():
    inquiry = str(request.form['user_input'])
    print inquiry, inquiry.upper(), 1
    if (inquiry.upper() not in species_list) and (inquiry.upper() not in common_name_list):
        return """
    The taxon: """+inquiry+""" does not appear to be in our database.
    <p></p>
    <a href="/home">Return home.</a>
    """
        print inquiry, inquiry.upper(), 2
    elif (inquiry.upper() not in species_list) and (inquiry.upper() in common_name_list):
        print inquiry, inquiry.upper(), 2.5, species_df['common_name'].str.upper()
        inquiry = species_df[species_df['common_name'].str.upper()==inquiry]
        print inquiry, 2.6
        inquiry = [inquiry.reset_index()['scientific_name'][0]][0]
    print inquiry, inquiry.upper(), 3
    prediction = endangered_recommender.recommend([inquiry], k=50).to_dataframe()
    print inquiry, inquiry.upper(), 4
    prediction_html = prediction.to_html()
    prediction['taxa'].iloc[0]
    table_data=""
    for i in xrange(len(prediction)):
        flags = ""
        if str(prediction['taxa'][i]).upper() in introduced_list:
            flags += 'invasive '
        if str(prediction['taxa'][i]).upper() in endangered_list:
            flags += 'protected '

        map_url = 'https://data.nbn.org.uk/img/hundredKmSelector/'+str(prediction['site'][i])[:-2]+'.gif'
        plant_url = 'https://en.wikipedia.org/wiki/'+ str(prediction['taxa'][i]).split()[0]
        table_data= table_data+'''
            <tr>
            <td>'''+ '<a href="' +plant_url+ '" target="_blank">'+ str(prediction['taxa'][i]) +'</a>' +'''</td>
            <td>'''+ str(prediction['rank'][i]) +'''</td>
            <td>'''+ str(prediction['site'][i]) +'''</td>
            <td>'''+ '<a href="'+map_url+'" target="_blank">'+region_dict[str(prediction['site'][i])[:-2]]+'</a>' +'''</td>
            <td>'''+ str(prediction['score'][i]) +'''</td>
            <td>'''+ flags +'''</td>
            </tr>
            '''
# map_url = 'https://data.nbn.org.uk/img/hundredKmSelector/'+str(prediction['site'][i])[:-2]+'.gif'
# '<a href="https://data.nbn.org.uk/img/hundredKmSelector/"'+str(prediction['site'][i])[:-2]+".gif">region_dict[str(prediction['site'][i])[:-2]]</a>
# https://data.nbn.org.uk/img/hundredKmSelector/SP.gif

#'<a href="'+map_url+'">'+region_dict[str(prediction['site'][i])[:-2]]+'</a>'

    page = '''
    <!DOCTYPE html>
<html class="full" lang="en">
<!-- Make sure the <html> tag is set to the .full CSS class. Change the background image in the full.css file. -->


<head>

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>Remediation sites</title>

    <!-- Bootstrap Core CSS -->
    <link href="../static/css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom CSS -->
    <link href="../static/css/sb-admin-2.css" rel="stylesheet">

    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
        <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
        <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->

</head>

<body>
    
<table class="table">
                  <thead>
                      <tr class="filters">
                          <th><input type="text" class="form-control" placeholder="Taxa" disabled></th>
                          <th><input type="text" class="form-control" placeholder="Rank" disabled></th>
                          <th><input type="text" class="form-control" placeholder="Site" disabled></th>
                          <th><input type="text" class="form-control" placeholder="Region" disabled></th>
                          <th><input type="text" class="form-control" placeholder="Score" disabled></th>
                          <th><input type="text" class="form-control" placeholder="Flags" disabled></th>
                      </tr>
                  </thead>
                  <tbody>''' + table_data + '''

                  </tbody>
              </table>
</body>

</html>

    '''
    return page


#Map page
@app.route('/map')
def show_map():
    return '<table border="1" class="dataframe">\n  <thead>\n    <tr style="text-align: right;">\n      <th></th>\n      <th>observation_count</th>\n      <th>common_name</th>\n      <th>scientific_name</th>\n      <th>species_key</th>\n      <th>rank</th>\n      <th>record_count</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>0</th>\n      <td>1</td>\n      <td>None</td>\n      <td>Abelia</td>\n      <td>NBNORG0000052930</td>\n      <td>Genus</td>\n      <td>2</td>\n    </tr>\n    <tr>\n      <th>1</th>\n      <td>1</td>\n      <td>None</td>\n      <td>Abutilon</td>\n      <td>NBNORG0000052939</td>\n      <td>Genus</td>\n      <td>304</td>\n    </tr>\n    <tr>\n      <th>2</th>\n      <td>283</td>\n      <td>Velvetleaf</td>\n      <td>Abutilon theophrasti</td>\n      <td>NBNORG0000052941</td>\n      <td>Species</td>\n      <td>300</td>\n    </tr>\n    <tr>\n      <th>3</th>\n      <td>16</td>\n      <td>None</td>\n      <td>Acacia</td>\n      <td>NBNORG0000052942</td>\n      <td>Genus</td>\n      <td>87</td>\n    </tr>\n    <tr>\n      <th>4</th>\n      <td>3</td>\n      <td>Hickory Wattle</td>\n      <td>Acacia falciformis</td>\n      <td>NBNORG0000025007</td>\n      <td>Species</td>\n      <td>3</td>\n    </tr>\n  </tbody>\n</table>'

#Testing
@app.route('/about')
def test():
    return render_template('about.html',
                           title = 'Test',
                           user = user)



if __name__ == '__main__':
    ##Import Model Here.
    invasive_recommender = graphlab.load_model('models/trimmed_survey_propotional_invasive_recommender')
    endangered_recommender = graphlab.load_model('models/trimmed_binary_endangered_recommender')
    app.run(host='0.0.0.0', port=8080, debug=True)