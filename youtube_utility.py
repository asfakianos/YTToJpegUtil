import os
import sys
import cv2
import datetime

from pytube import YouTube

def main(args):
	"""
	Arguments:
	1. Video URL (required)
	2. Destination directory (optional) If not specified, saves to video's title + res
	"""
	try:
		url = str(args[0])
	except:
		sys.exit("No url provided")

	try:
		dest = str(args[1])	
	except:
		dest = None

	# Reference all of the videos for the given URL with a .mp4 extension
	mp4 = YouTube(url).streams.filter(file_extension='mp4')

	max_stream = mp4[0]

	for stream in mp4[1:]:
		try:
			if int(stream.resolution[:-1]) > int(max_stream.resolution[:-1]):
				max_stream = stream
		except: # NoneType
			pass

	# Metadata for saving frames as imgs
	title = max_stream.title
	res = max_stream.resolution

	# Only operate on the video if the video name doesn't exist as a directory already
	if f"{max_stream.title}" not in os.listdir() and dest not in os.listdir():
		download = max_stream.download() # Download the highest res stream (saves to current dir)
		
		# Create dest if it didn't already exist
		if not dest:
			dest = max_stream.title

		if not os.path.isdir(dest):
			os.mkdir(dest)
			print(f"Created {dest}")

		# Write video metadata to the file
		with open(os.path.join(dest, f'{title}.META'), 'a') as metafile:
			metafile.write(f"Title: {title}\nURL: {url}\nResolution: {res}\nDownloaded on {datetime.datetime.now()}")

		# Open the file and begin writing to target destination
		video = cv2.VideoCapture(download)
		frame = 0 # Mostly just for naming purposes at this point

		while video.isOpened():
			success, image = video.read()

			if not success: # End of video
				break

			cv2.imwrite(os.path.join(dest, f"{frame}.jpg"), image)
			frame += 1

		print(f"Finished writing to {dest}.")

		# Cleanup
		video.release()
		cv2.destroyAllWindows()
		os.remove(title + ".mp4")

		print(f"Deleted {title}.mp4")

	else:
		sys.exit("Video download already exists.")


if __name__ == '__main__':
	main(sys.argv[1:])