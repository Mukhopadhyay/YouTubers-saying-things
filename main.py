import json
import warnings
import pandas as pd
from utils import utils

# Avoiding selenium warnings
warnings.filterwarnings('ignore')

def main() -> None:
    with open('metadata.json', 'r') as file:
        meta = json.load(file)
    dfs = []
    for channel in meta:
        df = utils.get_channel_info(channel, './chromedriver', verbose=False)
        if not isinstance(df, pd.DataFrame):
            continue
        df['Category'] = ','.join(channel['category'])
        dfs.append(df)
    
    dataset = pd.concat(dfs)
    dataset.CC = dataset.CC.apply(lambda x: 1 if isinstance(x, str) else 0)
    dataset = dataset[~dataset.Id.str.contains('&pp=')]

    print(dataset.head())
    dataset.to_csv('videoes.csv', index=False)

if __name__ == '__main__':
    main()

# After wards use 

'''
from youtube_transcript_api import YouTubeTranscriptApi
YouTubeTranscriptApi.get_transcript(VIDEO_ID, ('en', ))
'''