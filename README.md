# Telegram Bot for AppleMusic Downloader

# Build Wrapper
https://github.com/WorldObservationLog/wrapper

### Build Image
```
docker build --tag wrapper .
```

### Run
```
sudo docker run -v ./wrapper/rootfs/data:/app/rootfs/data -p 10020:10020 -p 20020:20020 -it -e args="-L username:password -H 0.0.0.0" wrapper
```

# Download AMDL
https://github.com/ZhangCharles/apple-music-downloader

### [MP4Box](https://gpac.io/downloads/gpac-nightly-builds/) Must be Installed

# Run
### Move Downloader to Bot rootDir and Change Mode
```
chomd +x ./main
```
### Edit config
```
cp .env.example .env
vi .env
vi config.yaml
```
### Run
```
pip3 install -r requirements.txt
python3 main.py
```
