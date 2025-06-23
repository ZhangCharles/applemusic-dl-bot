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

# Build Downloader
https://github.com/zhaarey/apple-music-downloader

### [MP4Box](https://gpac.io/downloads/gpac-nightly-builds/) Must be Installed
```
git https://github.com/zhaarey/apple-music-downloader.git
cd apple-music-downloader
go build main.go
```

# Run
### Copy Downloader
```
git https://github.com/ZhangCharles/applemusic-dl-bot.git
cp ./applemusic-downloader/main ./applemusic-dl-bot/main
cp ./applemusic-downloader/agent.js ./applemusic-dl-bot/agent.js
cp ./applemusic-downloader/agent-arm64.js ./applemusic-dl-bot/agent-arm64.js
cd applemusic-dl-bot
chomd +x ./main
```
### Edit config
```
cp example.env .env
vi .env
vi config.yaml
```
### Run
```
pip3 install -r requirements.txt
python3 main.py
```
