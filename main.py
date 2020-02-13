import argparse
from datasplit import split_video, split_video_fps
import glob

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a video file")
    parser.add_argument("--file",type=str)
    parser.add_argument("--dir",type=str)
    parser.app_argument("--fps_mode",type=bool)
    parser.add_argument("--output",type=str,required=True)
    parser.add_argument("--fps",type=float,default=25.0)
    parser.add_argument("--olf",type=float,default=0.0)
    parser.add_argument("--olb",type=float,default=0.0)
    parser.add_argument("--al",type=float,default=200.0)
    parser.add_argument("--ol",type=float,default=20.0)
    args = parser.parse_args()
    if args.file:
        if args.fps_mode:
            split_video_fps.delay(args.file,args.output,"000000001",args.fps,args.olf,args.olb)
        else:
            split_video.delay(args.file,args.output,"000000001",args.al,args.ol)
    elif args.dir:
        c = 1
        for file_name in glob.glob("%s/*" % args.dir):
            if args.fps_mode:
                split_video_fps.delay(file_name,args.output,"0000%05d" % c,args.fps,args.olf,args.olb)
            else:
                split_video.delay(file_name,args.output,"0000%05d" % c,args.al,args.ol)
            c = c + 1

