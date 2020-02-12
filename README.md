To get a 200ms dataset
python main.py --file swwv9a.mpg --output data --fps 7.5 --olf 0.5 --olb 0.5

Run this in a screen
celery worker --app=worker.app --loglevel=INFO

Then run it 
python main.py --dir video --output data --fps 7.5 --olf 0.5 --olb 0.5
