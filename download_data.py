#!/usr/bin/env python
from stravalib.client import Client
import os.path
import pandas as pd
import sys
try:
    import cPickle as pickle
except ImportError:
    import pickle
try:
    from tqdm import trange
except ImportError:
    trange = lambda x: range(x)
import glob
import gpxpy

types = ['time', 'latlng', 'distance', 'altitude', 'velocity_smooth', 'heartrate', 'cadence', 'watts', 'temp',
         'moving', 'grade_smooth']

save_file = 'all_act'


def get_api_values():
    secret_id = pd.read_csv("api.key")
    return secret_id['secret'][0], secret_id['ID'][0]


def split_lat(series):
    lat = series[0]
    return lat


def split_long(series):
    lon = series[1]
    return lon

# This is a hack to get the total number of activities
# because I can't find another way.


def total_num(client):
    activities = client.get_activities()
    for i in range(600):
        try:
            activities.next()
        except:
            return i
    return i


def get_strava_api(secret, ID):
    all_act = []
    client = Client(access_token=secret)
    tot = total_num(client)

    me = client.get_athlete(ID)
    activities = client.get_activities()

    for i in trange(tot):
        df = pd.DataFrame()
        _a = activities.next()

        _streams = client.get_activity_streams(_a.id, types=types)
        for item in types:
            if item in _streams.keys():
                df[item] = pd.Series(_streams[item].data, index=None)
            df['act_id'] = _a.id
            df['act_name'] = _a.name
            df['act_type'] = _a.type

        df['lat'] = map(split_lat, (df['latlng']))
        df['lon'] = map(split_long, (df['latlng']))
        df['time'] = df['distance'] / (df['velocity_smooth'])
        df.fillna(0)
        all_act.append(df)
        del df

    with open(save_file + '.pkl', 'wb') as fp:
        pickle.dump(all_act, fp)

    pd.concat(all_act, ignore_index=True).to_csv(save_file + '.csv')

    return all_act


def get_strava_gpx():
    all_act = []

    activities = glob.glob('activities/*.gpx')
    columns = ['lon', 'lat', 'altitude', 'time', 'speed']
    for _i in trange(len(activities)):
        gpx = gpxpy.parse(open(activities[_i]))
        track = gpx.tracks[0]
        segment = track.segments[0]
        data = []
        for point_idx, point in enumerate(segment.points):
            data.append([point.longitude, point.latitude, point.elevation,
                         point.time, segment.get_speed(point_idx)])
            df = pd.DataFrame(data, columns=columns)
            all_act.append(df)
            del df
    with open(save_file + '.pkl', 'wb') as fp:
        pickle.dump(all_act, fp)

    pd.concat(all_act, ignore_index=True).to_csv(save_file + '.csv')

    return all_act


def get_data():
    if os.path.isfile(save_file + '.pkl'):
        print("Loading Data")
        with open(save_file + '.pkl', 'rb') as fp:
            return pickle.load(fp)
    elif os.path.isdir('activities'):
        print("Loading Data from gpx files")
        get_strava_gpx()
    else:
        try:
            secret, ID = get_api_values()
        except:
            print("Error in get_api_values()")
            print("Make sure your api.key file is correct.")
            sys.exit()

        print("Downloading Data")
        return get_strava_api(secret, ID)

if __name__ == '__main__':
    try:
        get_data()
        print("Done")
    except:
        print("Error in getting data")
        sys.exit()
