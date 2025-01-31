import invoke


@invoke.task
def my_task(ctx):
    ctx.run("echo 'Hello, world!'")


@invoke.task
def my_task2(ctx):
    import numpy as np

    print(np.arange(10))


@invoke.task
def my_task3(
    ctx,
    N: int = 50,
    seed: int | None = None,
    num_reads: int = 100,
    num_sweeps: int = 1000,
    sampler_name: str = "ojsa",
):
    """
    N (int): 変数の数
    seed (int | None): 乱数のシード
    """
    import time

    import numpy as np
    import openjij as oj

    if seed is not None:
        seed = int(seed)
        np.random.seed(seed)

    # QUBO（Quadratic Unconstraind Binary Optimization）行列の作成
    QUBO = np.random.randn(N, N)
    # 対称行列にするぞー
    QUBO = (QUBO + QUBO.T) / 2

    print(QUBO)

    if sampler_name == "ojsa":
        sampler = oj.SASampler()
    elif sampler_name == "ojsqa":
        sampler = oj.SQASampler()
    else:
        raise ValueError(f"Invalid sampler name: {sampler_name}")

    start_time = time.time()
    sampleset = sampler.sample_qubo(QUBO, num_reads=num_reads, num_sweeps=num_sweeps)
    elapsed_time = time.time() - start_time
    unit_elapsed_time = elapsed_time / num_sweeps

    print(sampleset)

    # OpenJijの仕様で、同じ結果が入っていても、num_occurrences（num_oc.）が1になっている
    # print(sampleset.record)  # 重要な情報だけ取り出す

    ene = sampleset.data_vectors["energy"]

    print(f"Elapsed time: {elapsed_time:.3f} sec")
    print(f"Elapsed time per sweep: {unit_elapsed_time:.6f} sec")

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    ax.hist(ene, bins=20)
    ax.set_xlim(ene.min(), ene.min() + 10)
    fig.savefig("outputs/lecture01/hist.png")
