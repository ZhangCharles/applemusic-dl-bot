import env
from pyrogram import Client, filters, types
from tinytag import TinyTag
import subprocess
import glob
from PIL import Image
import io
import os

app = Client('amdl-bot',api_id=env.API_ID, api_hash=env.API_HASH, bot_token=env.BOT_TOKEN)

def get_metadata(file):
 tag: TinyTag = TinyTag.get(file)
 return tag

def find_m4a_files(directory):
  return glob.glob(f"{directory}/**/*.m4a", recursive=True)

def find_cover_file(directory):
  return glob.glob(f"{directory}/**/*.jpg", recursive=True)

def create_thumb(image_path):
  img = Image.open(image_path)
  img.thumbnail((320, 320))
  bio = io.BytesIO()
  bio.name = 'thumb.jpg'
  img.save(bio, format='JPEG', quality=85)
  bio.seek(0)
  return bio

@app.on_message(filters.command('amdl'))
async def amdl(client, message: types.Message):
  if str(message.chat.id) in env.CHAT_ID:
    args = message.command
    if args[1]:
      text = ' '.join(args[1:])
      if 'music.apple.com/cn/' in text:
        try:
          cmd = f'./main {text}'
          __path__ = './downloads'
          subprocess.run(cmd, shell=True)
          file_list = find_m4a_files(__path__)
          cover = find_cover_file(__path__)[0] if find_cover_file(__path__) else None
          thumb = create_thumb(cover) if cover else None
          if file_list:
            audio_gourp = []
            for m in file_list:
              tag = get_metadata(m)
              audio_gourp.append(
                types.InputMediaAudio(
                  media=m,
                  duration=int(tag.duration),
                  performer=', '.join(tag.other.get('performer')) if tag.other.get('performer') else tag.artist,
                  title=tag.title,
                  thumb=thumb,
                )
              )
            #Media Group Limit 1-10
            for i in range(0, len(audio_gourp), 10):
              batch = audio_gourp[i:i + 10]
              msg = await message.reply_media_group(media=batch)
              #转发到频道
              if env.CHANNEL:
                ids = []
                for m in msg:
                  ids.append(m.id)
                await app.forward_messages(chat_id=env.CHANNEL, from_chat_id=message.chat.id, message_ids=ids)
            for f in file_list:
              os.remove(f)
            if cover:
              os.remove(cover)
        except Exception as e:
          await message.reply(text='下载失败')
          print(e)
      else:
        await message.reply(
          text='请输入国区AppleMusic链接'
        )
    else:
      await message.reply(
        text='请输入AppleMusic链接'
      )

def main():
  app.run()

if __name__ == "__main__":
  main()