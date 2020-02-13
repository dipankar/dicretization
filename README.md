To get a 200ms dataset
python main.py --file swwv9a.mpg --output data --fps 7.5 --olf 0.5 --olb 0.5

To setup the inital directory
./setup.sh

Run this in a screen
./run_worker.sh

Then run it 
python main.py --dir video --output data --fps 7.5 --olf 0.5 --olb 0.5
