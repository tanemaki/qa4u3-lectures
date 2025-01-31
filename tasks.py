import invoke


@invoke.task
def my_task(ctx):
    ctx.run("echo 'Hello, world!'")
