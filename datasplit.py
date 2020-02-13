import delegator
import argparse
import logging
from celery import Celery
from worker import app
import os
import math


logging.root.setLevel(logging.NOTSET)

logger = logging.getLogger(__name__)

c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('datasplit_debug.log')

c_handler.setLevel(logging.INFO)
f_handler.setLevel(logging.DEBUG)

c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)

@app.task
def execute_cmd(cmd):
    c = delegator.run(cmd)
    #print(c.out)
    logger.info(cmd)
    return

def get_length(file_path):
    cmd = "ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 %s" % file_path
    c = delegator.run(cmd)
    logger.debug(cmd)
    # Generate the timings
    l = float(c.out)
    logger.info("Detected file length: %f seconds" % l)
    return l

def get_frame_fps(file_path,file_name,fps):
    cmd = "ffmpeg -i %s -r %f -f image2 %s.bmp" % (file_path,fps, file_name)
    #c = delegator.run(cmd)
    execute_cmd.delay(cmd)
    logger.info("Images have been generated")
    logger.debug(cmd)
    return


@app.task
def split_video_fps(file_path,output,append_name="",fps=25.0,olf=0,olb=0):
    file_name = os.path.join(output,"%s%%d" % append_name)
    l = get_length(file_path)
    ts = 1.0/fps
    hts = ts/2.0
    nf = int(math.ceil(l*fps))
    logger.info("Number of frames: %d" % nf)
    for i in range(0,nf):
        tts = i*ts
        file_name_i = file_name % i
        cmd="""ffmpeg -i %s -filter:v \
        "select='lt(prev_pts*TB\,%0.4f)*gte(pts*TB\,%0.4f)'" \
        -vsync drop %s.bmp""" % (file_path,tts,tts,file_name_i)
        # %s_%%03d.bmp
        execute_cmd.delay(cmd)
        et = tts + hts + (hts*olf) if tts<l else l
        st = tts - hts - (hts*olb) if tts>0 else 0.0
        # Generate the wav file
        cmd = "ffmpeg -i %s -acodec copy -ss %0.4f -to %0.4f %s.wav" % (file_path,st,et,file_name_i,)
        execute_cmd.delay(cmd)
        #c = delegator.run(cmd)
        logger.debug(cmd)
        logger.info("Splitting audio from %0.4f to %0.4f for frame %d of duration %0.2fms" % (st,et,i,(et-st)*1000.0))
    return

@app.task
def split_video(file_path,output,append_name="",al=200,ol=20):
    file_name = os.path.join(output,"%s%%d" % append_name)
    l = get_length(file_path)
    total = 0
    i = 0
    alw = al/2.0
    while(total<l):
        file_name_i = file_name % i
        cmd="""ffmpeg -i %s -filter:v \
        "select='lt(prev_pts*TB\,%0.4f)*gte(pts*TB\,%0.4f)'" \
        -vsync drop %s.bmp""" % (file_path,tts,tts,file_name_i)
        # %s_%%03d.bmp
        execute_cmd.delay(cmd)
        et = total+alw if (total_alw)>l else l
        st = total-alw if total>alw else 0.0
        # Generate the wav file
        cmd = "ffmpeg -i %s -acodec copy -ss %0.4f -to %0.4f %s.wav" % (file_path,st,et,file_name_i,)
        execute_cmd.delay(cmd)
        logger.debug(cmd)
        logger.info("Splitting audio from %0.4f to %0.4f for frame %d of duration %0.2fms" % (st,et,i,(et-st)*1000.0))
        total = total+al-ol
        i = i + 1
    return

