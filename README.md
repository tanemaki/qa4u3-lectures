# qa4u3-lectures

[QA4U3](https://altema.is.tohoku.ac.jp/QA4U3/)の講義内容を手を動かしながら理解するために作成された個人用レポジトリです。

## 使用ツール

- プロジェクト作成＆Pythonパッケージマネージャー [uv](https://docs.astral.sh/uv/)
- タスクランナー [Invoke](http://www.pyinvoke.org/)
- コード整形など [Ruff](https://docs.astral.sh/ruff/)

## はじめての使い方

1. このリポジトリをクローンします。
2. VS Codeを開きます。
3. Remote-Containers拡張機能をインストールします。
4. 左下の「><」をクリックして、コマンドパレットを開きます。
5. `Remote-Containers: Reopen in Container`を選択します。
6. コンテナの起動と同時に新しいウィンドウが開き、画面左下に「開発コンテナ: python @ desktop-linux」と表示されているのを確認します。
7. ターミナルを開いて、`(workspace) root@9dd39b93510f:/workspace#`のように表示されていることを確認します。
8. `python --version`を実行してPythonのバージョンが`Python 3.12.8`と表示されることを確認します。
9. `uv add invoke`を実行して、Invokeをインストールします。
10. `invoke lecture01.my-task`を実行して、`Hello, world!`と表示されれば成功です。やったね！

## その他の使い方

### Pythonパッケージのインストール

```bash
uv add <package-name>
```

### Pythonパッケージのアンインストール

```bash
uv remove <package-name>
```

### Invokeタスクの列挙

```bash
invoke --list
```

### Invokeタスクの追加

`tasks.py`や`scripts`以下にタスクを追加します。

## このリポジトリをどのように作成したか

1. `qa4u3-lectures`という名前でプロジェクトを作成

    ```bash
    uv init qa4u3-lectures  # 今回はアプリ形式（flat layout）を採用
    # uv init qa4u3-lectures --lib # ライブラリ形式（src layout）にしたければこちら

    # プロジェクトディレクトリの中に移動
    cd qa4u3-lectures
    ```

2. `.devcontainer`の中身を他のリポジトリからコピーしてきて使いやすいように変更

3. `tasks.py`を作成してDONE!
