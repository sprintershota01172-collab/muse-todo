# MUSE GANTT — MUSE（秘書）向けの手引き

このリポジトリは iPhone 用のガントチャート型タスク・工程管理アプリ「MUSE GANTT」です。
本人はタスクの追加・変更・完了などの**操作や更新を MUSE（このリポジトリを扱う Claude）に指示して行います**。
データの更新はこの手引きのとおりに行い、アプリのコード（`app.html`）はデータ更新のために書き換えないでください。

## アプリは2つあり、データの置き場所が違う

| アプリ | URL | データ | MUSE の更新方法 |
|---|---|---|---|
| claude.ai 版（推奨・端末間同期） | https://claude.ai/artifact/7b8ctLAEMyqEsmPmCcGZDp | アーティファクトのデータベース | `ArtifactData` ツールで直接読み書き（下記 A） |
| GitHub Pages 版（PWA） | https://sprintershota01172-collab.github.io/muse-todo/ | `muse-data.json`（端末にも保存） | `muse-data.json` を編集 → `python3 build.py` → push（下記 B） |

どちらに反映するか指示がなければ、本人に聞かずに**両方**へ同じ内容を反映します。

## A. claude.ai 版（ArtifactData）

- 対象の URL：`https://claude.ai/artifact/7b8ctLAEMyqEsmPmCcGZDp`
- コレクション `tasks`、ドキュメント ID ＝ タスクの `id`
- 追加・変更は `set`（丸ごと）か `update`（一部だけ）。複数件は `batch`
- 削除はドキュメントを `delete`（ほかのタスクの `deps` からも外す）
- 変更するときは `updatedAt` に現在時刻（ミリ秒）を入れ、`rev` を1つ増やし、`history` の末尾に
  `{"at":<ミリ秒>,"by":"muse","action":"<何をしたか>","reason":"<本人の指示など>"}` を足す。
  アプリは `by:"muse"` の変更を「MUSEが〜を更新しました」と通知し、履歴に「MUSE」と表示します
- 勤務条件 `meta/settings`、出退勤 `attendance/YYYY-MM`（`{days:{"YYYY-MM-DD":{in,out}}}`）
- アプリを開いていればその場で反映されます

## B. GitHub Pages 版（muse-data.json）

1. `muse-data.json` の `tasks` を編集する（1行1タスク）。休み・休日出勤は `days`、出退勤は `attendance`
2. `version` を **1つ上げる**（上げないと端末に反映されません）。`updatedAt` も今日にする
3. 変えたタスクの `updatedAt` を現在時刻にする（端末で本人が後から変えた項目より新しくなり、MUSE の内容が反映される）
4. `python3 build.py` で `index.html` を作り直す（JSON の誤りや id の重複はここでエラーになります）
5. commit して `main` に push（GitHub Actions が Pages に公開）

反映のしかた：端末で本人が後から変えた・追加した項目は残ります。MUSE が `updatedAt` を新しくした項目は MUSE の内容になります。
`tasks` から消した項目は端末からも消えます（端末で新しく追加した項目は消えません）。

## タスクの書き方

```json
{"id":"695-proto-build","name":"695試作品作製","project":"695","kind":"desk","scale":"time",
 "start":"2026-11-17 08:30","end":"2026-11-17 17:30","deadline":"2026-11-17",
 "status":"todo","important":false,"priority":"mid","milestone":false,"deps":[],"memo":"","assignee":""}
```

| 項目 | 内容 |
|---|---|
| `id` | 英数字とハイフン。一度決めたら変えない |
| `name` / `project` | 名前（80字まで）/ 車種・プロジェクト名（左の列でグループになる） |
| `scale` | `"time"`＝日・週に出る普通のタスク、`"week"`＝**大日程**（月単位。`"大日程"` `"month"` でも可） |
| `start` / `end` | 時刻は `"2026-11-09 08:30"`、ISO（`"2026-11-09T08:30:00+09:00"`）、ミリ秒のどれでも可。日付だけ（`"2026-11-09"`）なら勤務時間（8:30–17:30）いっぱい |
| 大日程の `start` / `end` | `"2027-05"` のように**月**で書く。`end` はその月を**含む**（`"2027-05"`〜`"2027-09"` は5か月の帯） |
| `milestone` | `true` で◆。大日程の◆は `start` の月の真ん中に出る（`end` 不要） |
| `kind` | `desk` 通常業務 / `line` 工程調整・改造 / `stop` 設備停止 / `witness` 工程立ち会い / `holiday` 休日作業 / `private` プライベート（日本語の名前でも可） |
| `status` | `todo` / `doing` / `paused` / `done`（`未着手` `作業中` `中断` `完了` でも可）。`done` はチャートから消えて一覧の「完了」へ |
| `priority` / `important` | `high` `mid` `low`（`高` `中` `低`）/ `true` で重要（真鍮色） |
| `deadline` | 期限。日付だけなら終業時刻（17:30） |
| `deps` | 前工程のタスク `id` の配列 |
| `segs` | 実績 `[{"s":開始,"e":終了}]`（任意） |

決まりごと：
- 工程の調整・改造（`line`）と設備停止（`stop`）は、製造部門の休憩（10:15–11:00）か休日にだけ置く
- 大日程（`scale:"week"`）には日々のタスクを入れない。車種・プロジェクトごとの節目（号試・図面発行・SOP など）だけ
- 日時がはっきりしないときは本人に確認するか、`memo` に「仮」と書いておく
- 進捗率（％）は使わない

## コードを直すとき（本人がアプリの改良を頼んだとき）

- 本体は `app.html`（claude.ai 版として公開しているもの）。直したら `python3 build.py` で `index.html` を作り直す
- iPhone SE／15／15 Pro Max の幅で、ページ全体がスクロールしないこと・入力画面が動かないことを確認する
- claude.ai 版は `Artifact` ツールで上記 URL に同じ `app.html` を公開し直す（データベースの権限設定はそのまま）
- 返答の最後には毎回、claude.ai 版・リポジトリ・GitHub Pages の URL を載せる
