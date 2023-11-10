# -*- coding:utf-8 -*-
 
import os
import re
import requests #pip install requests #close proxy
 
UC_PATH = './Cache/'  # 缓存路径 例 D:/CloudMusic/Cache/
MP3_PATH = './'  # 存放歌曲路径
RUL = 'https://api.imjad.cn/cloudmusic/?type=detail&id={0}'
headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
	"Connection": "keep-alive",
	"Accept": "text/html,application/json,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	"Accept-Language": "zh-CN,zh;q=0.8"
}
 
 
class Transform():
	def do_transform(self):
		files = os.listdir(UC_PATH)
		for file in files:
			if not file[-3:] == '.uc':  # 后缀uc结尾为歌曲缓存
				continue
			print(file)
			mp3_content = None
			with open(UC_PATH + file, mode='rb') as uc_file:
				mp3_content = bytearray(uc_file.read())
				for i, byte in enumerate(mp3_content):
					byte ^= 0xa3
					mp3_content[i] = byte
			if not mp3_content:
				continue
				
			song_name = self.get_song_info_by_file(file)
			mp3_file_name = MP3_PATH + '%s.mp3' % (song_name)
			with open(mp3_file_name, 'wb') as mp3_file:
				mp3_file.write(mp3_content)
 
	def get_song_info_by_file(self, file_name):
		match_inst = re.match('\d*', file_name)  # -前面的数字是歌曲ID，例：1347203552-320-0aa1, 1347203552是歌曲ID
		if match_inst:
			song_id = match_inst.group()
		else:
			song_id = file_name
 
		try:
			url = RUL.format(song_id)  # 请求url例子：https://api.imjad.cn/cloudmusic/?type=detail&id=1347203552
			response = requests.get(url, headers=headers)
			jsons = response.json()
			song_name = jsons['songs'][0]['name']
			singer = jsons['songs'][0]['artists'][0]['name']
			return song_name + " - " + singer
		except:
			return song_id
 
 
def check_path():
	global UC_PATH, MP3_PATH
 
	if not os.path.exists(UC_PATH):
		print('缓存路径错误: %s' % UC_PATH)
		return False
	if not os.path.exists(MP3_PATH):
		print('目标路径错误: %s' % MP3_PATH)
		return False
 
	if UC_PATH[-1] != '/':  # 容错处理 防止绝对路径结尾不是/
		UC_PATH += '/'
	if MP3_PATH[-1] != '/':
		MP3_PATH += '/'
	return True
 
 
if __name__ == '__main__':
	if not check_path():
		exit()
 
	transform = Transform()
	transform.do_transform()