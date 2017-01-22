# StravaHeatmap
Make a simple heatmap from your strava data

![heatmap](heatmap.png)

## Make your own!
* Put your api key and client id into the api.key file
* `python make_heatmap.py`

## Getting started
To get started you need your secret key and client id from [strava](https://strava.github.io/api/#access). Signing up to be a developer is simple and free. If you already have a developer account you can find your secret and client id at the bottom of your strava settings online. Edit the `api.key.template` with your values and move it to `api.key`.

For the required python libraries you will need to:
```
pip install stravalib pandas gmplot
```

For a progress of downloading data you can also install tqdm:
```
pip install tqdm
```

## Output
The make_heatmap.py file will output a csv of all your activities, a pickle of an array of dataframes with each dataframe representing an idivuidual activity, and an html file which makes an interactive heatmap on a google map.

If you would only like the data you can also just run the download_data.py file which will give you the csv and the pickle so you can look at the data yourself.

A handy thing about saving the data means you don't have to constatnly make api calls which strava limits. If you have new activities you want to add them to the data just delete the csv and pkl file and it will redownload the newest data.