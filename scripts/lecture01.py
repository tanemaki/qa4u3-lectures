import invoke


@invoke.task
def my_task(ctx):
    ctx.run("echo 'Hello, world!'")


@invoke.task
def my_task2(ctx):
    import numpy as np

    print(np.arange(10))
