import librosa
import numpy as np
import os
import argparse
from tqdm import tqdm

def convert_audio(args):
    song_dir = os.listdir(args.wav_dir)
    if not os.path.exists(args.convert_dir):
        os.makedirs(args.convert_dir)

    for song in tqdm(song_dir):
        for source in os.listdir(f'{args.wav_dir}/{song}'):
            if source.endswith('.wav'):
                source_path = f'{args.wav_dir}/{song}/{source}'
                source_data, sample_rate = librosa.load(source_path, sr=None)
                if not os.path.exists(f'{args.convert_dir}/{song}'):
                    os.makedirs(f'{args.convert_dir}/{song}')
                np.save(f'{args.convert_dir}/{song}/{source[:-4]}.npy', source_data)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--wav_dir', type=str, default='train')
    parser.add_argument('--convert_dir', type=str, default='train_np')
    args = parser.parse_args()
    convert_audio(args)

if __name__ == '__main__':
    main()