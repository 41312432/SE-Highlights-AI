# Feature Extraction from SoccerNet

SoccernNet JSON to CSV

```shell
./create_dataset_csv_files.sh
```

Video(mkv) to Audio(wav)

```shell
./extract_soccernet_wav.sh
```

Audio(wav) to Features(npy)
```shell
python features/extract_vggish_features.py
```
