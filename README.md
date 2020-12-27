# Python Download Utility  
Youtube video downloader that downloads videos (given a link) and outputs each frame to a directory. Run with `python youtube_utility.py <URL>`. Output directory is inferred from the video title, but can be specified as a secondary argument (after `<URL>`). Each frame is saved in .jpg format before the video is deleted. 

Main intention is that this can be used to download videos with relevant (unlabeled) footage that can then be labeled with a YOLO labeler of your choice to train a YOLO network with custom data. 