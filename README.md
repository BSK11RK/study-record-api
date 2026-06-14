# Study Record SNS API

FastAPIで作成した学習記録SNS APIです。

## 使用技術

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* Alembic
* JWT Authentication
* Docker
* Pytest

---

## 主な機能

### 認証

* ユーザー登録
* ログイン
* JWT認証

### 学習記録

* 学習記録作成
* 一覧取得
* 1件取得
* 更新(PATCH)
* 削除
* 科目検索
* 日付範囲検索

### 集計

* 総学習時間
* 科目別集計

### SNS機能

* タイムライン
* ページネーション
* フォロー
* フォロワー一覧
* フォロー中一覧
* フォロー中タイムライン
* ユーザープロフィール

---

## データベース

PostgreSQL

---

## 起動方法

### Docker

```bash
docker compose up --build
```

### Alembic

```bash
docker compose exec api alembic upgrade head
```

### Swagger

```text
http://localhost:8000/docs
```

---

## テスト

```bash
pytest
```

---

## 今後追加予定

* いいね機能
* コメント機能
* GitHub Actions
* CI/CD

```
```