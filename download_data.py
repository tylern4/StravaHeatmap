from stravalib.client import Client
import os.path
import pandas as pd
try:
    import cPickle as pickle
except ImportError:
    import pickle
try:
    from tqdm import trange
except ImportError:
    trange = lambda x: range(x)

types = ['time', 'latlng', 'distance', 'altitude', 'velocity_smooth', 'heartrate', 'cadence', 'watts', 'temp',
         'moving', 'grade_smooth']

save_file = 'all_act'

def get_api_values():
    secret_id = pd.read_csv("api.key")
    return secret_id['secret'][0],secret_id['ID'][0]

def split_lat(series):
    lat = series[0]
    return lat

def split_long(series):
    lon = series[1]
    return lon

def get_strava(secret,ID):
    all_act = []
    client = Client(access_token=secret)
    me = client.get_athlete(ID)

    activities = client.get_activities()

    for i in trange(71):
        ################Still need to figure out how to get number instead of hardcoding
        _a = activities.next()
        _act_type = _a.type
        df = pd.DataFrame()

        _streams = client.get_activity_streams(_a.id,types=types)
        for item in types:
            if item in _streams.keys():
                df[item] = pd.Series(_streams[item].data,index=None)
            df['act_id'] = _a.id
            df['act_name'] = _a.name
            df['act_type'] = _a.type
        
        df['lat'] = map(split_lat, (df['latlng']))
        df['lon'] = map(split_long, (df['latlng']))
        df['time'] = df['distance']/(df['velocity_smooth'])
        df.fillna(0)
        all_act.append(df)
        del df

    with open(save_file+'.pkl','wb') as fp:
        pickle.dump(all_act,fp)

    pd.concat(all_act, ignore_index=False).to_csv(save_file+'.csv')

    return all_act

def get_data():
    if os.path.isfile(save_file+'.pkl'):
        print("Loading Data")
        with open(save_file+'.pkl', 'rb') as fp:
            return pickle.load(fp)
    else:
        try:
            secret, ID = get_api_values()
        except:
            print("Error in get_api_values()")
            print("Make sure your api.key file is correct.")
        print("Downloading Data")
        return get_strava(secret,ID)