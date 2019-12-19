from tasks import create_workers

 
def manage_create_workers_task(url):
    task = create_workers.delay(url)
    task.get(timeout=2)

manage_create_workers_task('https://jsonplaceholder.typicode.com/users')