import argparse
from datasplit import split_video

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a video file")
    parser.add_argument("--file",type=str)
    parser.add_argument("--dir",type=str)
    parser.add_argument("--output",type=str,required=True)
    parser.add_argument("--fps",type=float,default=25.0)
    parser.add_argument("--olf",type=float,default=0.0)
    parser.add_argument("--olb",type=float,default=0.0)
    args = parser.parse_args()
    if args.file:
        split_video.delay(args.file,args.output,"000000001",args.fps,args.olf,args.olb)
    elif args.dir:
        c = 1
        for file_name in glob.glob("%s/*" % args.dir):
            split_video.delay(file_name,args.output,"0000%05d" % c,args.fps,args.olf,args.olb)
            c = c + 1

