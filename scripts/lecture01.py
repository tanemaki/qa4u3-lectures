import invoke


@invoke.task
def my_task(ctx):
    ctx.run("echo 'Hello, world!'")


@invoke.task
def my_task2(ctx):
    import numpy as np

    print(np.arange(10))


@invoke.task
def my_task3(ctx, N: int = 50, seed: int | None = None):
    """
    N (int): 変数の数
    """
    import numpy as np

    if seed is not None:
        seed = int(seed)
        np.random.seed(seed)

    # QUBO（Quadratic Unconstraind Binary Optimization）行列の作成
    QUBO = np.random.randn(N, N)
    # 対称行列にするぞー
    QUBO = (QUBO + QUBO.T) / 2

    print(QUBO)
