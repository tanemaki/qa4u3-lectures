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


@invoke.task
def my_task4(
    ctx,
    N: int = 50,
    seed: int | None = None,
    num_reads: int = 1,
    num_sweeps: int = 1000,
    sampler_name: str = "ojsa",
):
    """
    キュリー・ワイスモデルのハミルトニアンを作成する。
    """

    import dimod
    import matplotlib.pyplot as plt
    import numpy as np
    import openjij as oj

    Jmat = np.zeros([N, N])
    hvec = np.zeros(N)

    for i in range(N):
        for j in range(N):
            Jmat[i, j] = -1 / (2 * N)

    model = dimod.BinaryQuadraticModel(hvec, Jmat, 0.0, vartype=dimod.SPIN)
    qubo, offset = model.to_qubo()

    if sampler_name == "ojsa":
        sampler = oj.SASampler()
    elif sampler_name == "ojsqa":
        sampler = oj.SQASampler()
    else:
        raise ValueError(f"Invalid sampler name: {sampler_name}")

    beta_list = np.linspace(0.1, 2.0, 20)
    mag_list = []
    var_list = []

    for beta in beta_list:
        sampleset = sampler.sample_qubo(
            qubo, beta_max=beta, num_reads=num_reads, num_sweeps=num_sweeps
        )

        m2_list = []
        # ひとつひとつ調べよう
        for k in range(num_reads):
            binary = sampleset.record[k][0]
            spin = 2 * binary - 1
            m2 = spin.mean() ** 2  # 業界的には2乗でやる。でも、絶対値でも全然良い。
            # m2 = np.abs(spin.mean())
            # プラスで揃っても、マイナスで揃っても、同じなので二乗する
            m2_list.append(m2)

        m2_array = np.array(m2_list)
        print(f"beta={beta:.3f}, mean={m2_array.mean():.3f}, std={m2_array.std():.3f}")

        # magnetization
        mag_list.append(m2_array.mean())
        var_list.append(m2_array.std())

    print(mag_list)
    print(var_list)

    fig, ax = plt.subplots()
    # ax.plot(beta_list, mag_list, label="magnetization")
    ax.errorbar(x=beta_list, y=mag_list, yerr=var_list, label="magnetization")
    ax.set_xlabel("beta")
    ax.set_ylabel("magnetization")
    ax.legend()
    ax.set_ylim(0, 1)
    fig.savefig("outputs/lecture01/magnetization.png")
