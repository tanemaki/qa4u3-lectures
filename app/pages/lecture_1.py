import time

import numpy as np
import openjij as oj
import pandas as pd
import streamlit as st


def insert_widget_to_get_seed() -> int | None:
    use_seed = st.sidebar.checkbox("乱数シードを固定する")
    if use_seed:
        seed = st.sidebar.number_input("乱数のシード", 0)
    else:
        seed = None
    return seed


def insert_widget_to_get_num_reads():
    num_reads = st.sidebar.text_input("読み出し回数（試行回数）", value="")
    if num_reads == "":
        num_reads = None
    else:
        num_reads = int(num_reads)
        if num_reads <= 0:
            st.error(f"読み出し回数は1以上の整数で指定してください。`{num_reads = }`")
            st.stop()

    return num_reads


def insert_widget_to_get_num_sweeps():
    num_sweeps = st.sidebar.text_input("スイープ回数（更新回数）", value="")
    if num_sweeps == "":
        num_sweeps = None
    else:
        num_sweeps = int(num_sweeps)
        if num_sweeps <= 0:
            st.error(f"スイープ回数は1以上の整数で指定してください。`{num_sweeps = }`")
            st.stop()

    return num_sweeps


def insert_widget_to_get_sampler_name():
    sampler_name = st.sidebar.radio(
        "サンプラーの名前",
        ["ojsa", "ojsqa"],
        captions=["OpenJij's SA sampler", "OpenJij's SQA sampler"],
    )
    return sampler_name


def make_random_qubo(N: int) -> np.ndarray:
    """
    ランダムなQUBO行列を作成する。
    """

    # QUBO（Quadratic Unconstraind Binary Optimization）行列の作成
    QUBO = np.random.randn(N, N)
    # 対称行列にする
    QUBO = (QUBO + QUBO.T) / 2

    return QUBO


def render_page():
    st.title("Hello Lecture 1!")

    seed = insert_widget_to_get_seed()
    if seed is not None:
        np.random.seed(seed)

    N = st.sidebar.number_input("スピン変数の数", 1, 100, 5)
    num_reads = insert_widget_to_get_num_reads()
    num_sweeps = insert_widget_to_get_num_sweeps()
    sampler_name = insert_widget_to_get_sampler_name()

    # if st.button("QUBO行列を作成する"):
    QUBO = make_random_qubo(N)

    if st.sidebar.checkbox("パラメータを表示する", value=True):
        st.write(f"`{N = }`")
        st.write(f"`{num_reads = }`")
        st.write(f"`{num_sweeps = }`")
        st.write(f"`{sampler_name = }`")

    if st.sidebar.checkbox("QUBO行列を表示する", value=True):
        # プラスを赤、マイナスを青で表示する
        st.dataframe(
            pd.DataFrame(QUBO)
            .style.format("{:.3f}")
            .background_gradient(cmap="coolwarm", vmin=-1, vmax=1)
        )

    if sampler_name == "ojsa":
        sampler = oj.SASampler()
    elif sampler_name == "ojsqa":
        sampler = oj.SQASampler()
    else:
        raise ValueError(f"Invalid sampler name: {sampler_name}")

    start = time.time()
    response = sampler.sample_qubo(QUBO, num_reads=num_reads, num_sweeps=num_sweeps)
    elapsed_time = time.time() - start

    # st.write(type(response))
    st.write(f"Elapsed time: {elapsed_time:.3f} [s]")

    st.write("`response.info =`", response.info)


if __name__ == "__main__":
    render_page()
