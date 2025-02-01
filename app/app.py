import streamlit as st


def app():
    st.title("Hello World!")

    # QUBO（Quadratic Unconstraind Binary Optimization）行列の作成
    QUBO = np.random.randn(N, N)
    # 対称行列にするぞー
    QUBO = (QUBO + QUBO.T) / 2


if __name__ == "__main__":
    app()
