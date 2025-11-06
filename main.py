import env
from pyrogram import Client, filters, types
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from tinytag import TinyTag
import subprocess
import glob
import requests
from bs4 import BeautifulSoup
from PIL import Image
import io
import os
import uuid
import shutil

wait_list = []
url_cache = {}

app = Client('amdl-bot',api_id=env.API_ID, api_hash=env.API_HASH, bot_token=env.BOT_TOKEN)

def download_music(url, outputDir):
  cmd = f'./main --song -o {outputDir} {url}' if '?i=' in url else f'./main -o {outputDir} {url}'
  subprocess.run(cmd, shell=True)
  file_list = find_m4a_files(outputDir)
  cover = find_cover_file(outputDir)[0] if find_cover_file(outputDir) else None
  thumb = create_thumb(cover) if cover else None
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
  print("下载完成,正在上传")
  return audio_gourp

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

@app.on_message(filters.command('search'))
async def search(client: Client, message: types.Message):
  if str(message.chat.id) in env.CHAT_ID:
    args = message.command
    if args and len(args)>1:
      text = ' '.join(args[1:])
      resp = requests.get(f'https://music.apple.com/cn/search?term={text}')
      resp.encoding = 'utf-8'
      soup = BeautifulSoup(resp.text, 'html.parser')
      results = soup.find_all(attrs={'data-testid':'grid-item'})
      buttons = []
      url_cache.clear()
      for item in results:
        i = item.find(attrs={'data-testid':'click-action'})
        label = i['aria-label']
        title = label.split('·')[0].strip()
        category = label.split('·')[1].strip()
        url = i['href']
        if '艺人' not in category:
          key = str(uuid.uuid4())[:8]
          url_cache[key] = {"title":title, "url": url}
          buttons.append([InlineKeyboardButton(text=label, callback_data=f'select:{message.from_user.id}:{key}')])
      await message.reply(
        "请选择需要下载的歌曲/专辑",
        reply_markup=InlineKeyboardMarkup(buttons)
      )

@app.on_callback_query(filters.regex(r"^select:(\d+):(.+)$"))
async def on_select(client: Client, callback_query: types.CallbackQuery):
  user_id_str, key = callback_query.data.split(":")[1:]
  info = url_cache.get(key, None)
  if info:
    title = info["title"]
    url = info["url"]
  else:
    await callback_query.message.edit_text(
        f"搜索已过期"
      )
    return
  if callback_query.from_user.id != int(user_id_str):
    await callback_query.answer(
      "这不是你的搜索结果",
      show_alert=True
    )
  else:
    try:
      id = callback_query.id
      outputDir = f'./downloads/{id}'
      await callback_query.message.edit_text(
        f"正在下载：{title}"
      )
      audio_gourp = download_music(url, outputDir)
      for i in range(0, len(audio_gourp), 10):
        batch = audio_gourp[i:i + 10]
        await callback_query.message.reply_media_group(media=batch)
      shutil.rmtree(outputDir, ignore_errors=True)
      print("已上传")
    except Exception as e:
      await callback_query.message.reply(text='下载失败')
      print(e)

@app.on_message(filters.command('amdl'))
async def amdl(client: Client, message: types.Message):
  if str(message.chat.id) in env.CHAT_ID:
    args = message.command
    if args and len(args) > 1:
      text = ' '.join(args[1:])
      if 'music.apple.com/cn/' in text:
        try:
          id = message.id
          outputDir = f'./downloads/{id}'
          audio_gourp = download_music(text, outputDir)
            #Media Group Limit 1-10
          for i in range(0, len(audio_gourp), 10):
            batch = audio_gourp[i:i + 10]
            await message.reply_media_group(media=batch)
          shutil.rmtree(outputDir)
          print("已上传")
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