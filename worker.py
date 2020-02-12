from celery import Celery

app = Celery(__name__)
app.conf.update({
    'broker_url': 'filesystem://',
    'broker_transport_options': {
        'data_folder_in': '/home/dipankar/Projects/datasplitter/broker/out',
        'data_folder_out': '/home/dipankar/Projects/datasplitter/broker/out',
        'data_folder_processed': '/home/dipankar/Projects/datasplitter/broker/processed'
    },
    'imports': ('datasplit',),
    'result_persistent': False,
    'task_serializer': 'json',
    'result_serializer': 'json',
    'accept_content': ['json']})
