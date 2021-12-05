# dataset-extraction

Dataset Collection: Run datafromtwitter.py, This will collect data from twitter and store it in data.json.

Dataset Cleaning: Run ner, this will clean the data collect entities from data using spacy and store it in predict.json in the format required by PCNN. Run covidnewsner to get data from covid news dataset. Run nerscispacy to get Bio data.

Relations from PCNN are converted to json using pcnntojson.ipynb

Data is converted to fewrel format using data_to_fewrel.ipynb

