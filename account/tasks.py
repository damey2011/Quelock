from Quelock.celery import app


@app.task(name='add_two_nos', typing=False)
def add_numbers(string):
    print('HELLO')
    return string
    # print(x + y)
    # return 'HEY, THIS WORKS'
