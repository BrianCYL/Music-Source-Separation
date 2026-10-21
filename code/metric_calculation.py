import os
import numpy as np
import pandas as pd
import json
import argparse

def metric_calculate(args):
    SDR, SIR, SAR, ISR = [], [], [], []
    if not args.folder_dir.endswith('test'):
        args.folder_dir = os.path.join(args.folder_dir, 'test')
    for file in os.listdir(args.folder_dir):
        file_dir = os.path.join(args.folder_dir, file)
        with open(file_dir) as f:
            data = json.load(f)
        df = pd.DataFrame(data['targets'][1]['frames'])
        df['SDR'] = df['metrics'].apply(lambda x: x['SDR'])
        df['SIR'] = df['metrics'].apply(lambda x: x['SIR'])
        df['SAR'] = df['metrics'].apply(lambda x: x['SAR'])
        df['ISR'] = df['metrics'].apply(lambda x: x['ISR'])
        df = df.drop(columns=['metrics'])
        df = df.fillna(0)
        SDR.append(df['SDR'].median())
        SIR.append(df['SIR'].median())
        SAR.append(df['SAR'].median())
        ISR.append(df['ISR'].median())
    print(f'SDR: {np.median(SDR)}')
    print(f'SIR: {np.median(SIR)}')
    print(f'SAR: {np.median(SAR)}')
    print(f'ISR: {np.median(ISR)}')
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder_dir', type=str, default='data/eval')
    args = parser.parse_args()
    metric_calculate(args)

if __name__ == '__main__':
    main()