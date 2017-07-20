import pandas as pd
import pafy
from os import remove
from pydub import AudioSegment

## Check to see if audio URL has cutoff or not
## + if so -- can keep what we have
## + if not -- need to make separate column and calculate

AudioSegment.converter = r"C:\ffmpeg\bin\ffmpeg.exe"
df = pd.read_table('songs.dat', delimiter= ', ')


for index, row in df.iterrows():
	desired_path = './audio/%s.mp3' %row['name']

	try:
		remove(desired_path)
	except WindowsError:
		pass

	try:
		v = pafy.new(row['song_url'])

		for idx, a in enumerate(v.audiostreams):
			if 'm4a@128k' in str(a):
				path = './audio/%s.m4a' %row['name']
				v.audiostreams[idx].download(filepath=path)

		song = AudioSegment.from_file(path, format='m4a')
		remove(path)

		# millisecond format for pydub
		start_time = row['start_time'] * 1000
		ten_seconds = 10 * 1000 
		song = song[start_time:start_time + ten_seconds]
		song.export(desired_path, format='mp3')

	except WindowsError:
		pass
