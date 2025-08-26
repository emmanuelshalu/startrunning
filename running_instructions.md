//if you want to run the app

'''
//Create a virtual environment(replace 'mix' with any name you want)- one time activity
python -m venv mix
'''

//first activate the virtual environment
source mix/bin/activate

//then install requirements
pip install -r requirements.txt

//then run the app- every time
python runmix.py
-----------------------------------------------------------------

//if you just want to download music from spotify playlist
python spotify_downloader.py
-----------------------------------------------------------------

//if you want to run the flask app
flask run
-----------------------------------------------------------------