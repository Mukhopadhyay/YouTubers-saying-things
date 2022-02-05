import json
import warnings
import pandas as pd
from utils import utils
from typing import Optional, Dict
from youtube_transcript_api import YouTubeTranscriptApi

# Avoiding selenium warnings
warnings.filterwarnings('ignore')

def main(save: Optional[bool] = True, verbose: Optional[bool] = False) -> pd.DataFrame:
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

    if verbose:
        print(dataset.head())
    
    if save:
        dataset.to_csv('videoes.csv', index=False)
    return dataset


def generate_transcripts(df: pd.DataFrame):
    # Split the channelss
    channel_dfs: Dict[pd.DataFrame] = {}
    for channel in df.Channel.unique():
        channel_dfs[channel] = df[df.Channel == channel]
    
    dfs_with_transcripts = []
    for cname, temp in channel_dfs.items():
        print('Currently working: {}'.format(cname))
        transcripts = {}
        n = temp.shape[0]
        for i, idx in enumerate(temp.Id.tolist(), start=1):
            try:
                t = YouTubeTranscriptApi.get_transcript(idx, languages=('en',))
            except Exception as err:
                transcripts[idx] = f'ERR: {str(err)}'
            else:
                transcripts[idx] = ' '.join([x['text'] for x in t])
            print(f'{i}/{n}', end='\r', flush=True)
        temp['Transcript'] = temp.Id.apply(lambda x: transcripts.get(x))
        dfs_with_transcripts.append(temp)
    data = pd.concat(dfs_with_transcripts)
    return data[~data.Transcript.str.startswith('ERR: ')]


# Driver code
if __name__ == '__main__':
    df = main()
    
