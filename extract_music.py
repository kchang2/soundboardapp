import pandas as pd
import pafy
from os import remove
from pydub import AudioSegment

## Check to see if audio URL has cutoff or not
## + if so -- can keep what we have
## + if not -- need to make separate column and calculate

AudioSegment.converter = r"C:\ffmpeg\bin\ffmpeg.exe"
df = pd.read_table('songs.dat', delimiter= ', ')

# throttled by network connectivity, so easier to update manually. See commented code below.
for index, row in df.iterrows():
	# if row['name'] not in ['Yaz']: 
	# 	continue
	# print row

	desired_path = './audio/%s.mp3' %row['name']

	try:
		v = pafy.new(row['song_url'])

		for idx, a in enumerate(v.audiostreams):
			if 'm4a@128k' in str(a):
				path = './audio/%s.m4a' %row['name']
				v.audiostreams[idx].download(filepath=path)

		song = AudioSegment.from_file(path, format='m4a')
		remove(path)

	except WindowsError:
		continue

	try:
		remove(desired_path)
	except WindowsError:
		pass

	# millisecond format for pydub
	## try start time
	try:
		t_i = row['start_time'].split(':')
		start_time = (int(t_i[0]) * 60 + int(t_i[1])) * 1000
	except:
		start_time = 0

	## end time
	try:
		t_f = row['end_time'].split(':')
		end_time = (int(t_f[0]) * 60 + int(t_f[1])) * 1000
	except:
		end_time = start_time + 10 * 1000
		
	song = song[start_time:end_time]
	song.export(desired_path, format='mp3')
