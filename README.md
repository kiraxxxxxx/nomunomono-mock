# のむのもの Mock Site

野村製作所のオリジナルブランド「のむのもの / NOM NO MONO」のTOPページモック。

## デザイン方針
- **HEROコピー**：革に、願いを縫いつけて。（Where wishes are stitched into leather.）
- 商品が主役・サイトは引き算
- 和紙白×墨を基調、朱（だるま赤）をアクセント、金はtoB領域のみ
- 英語ナビ＋ヘッダー右端に言語スイッチ（Shopify Translate & Adapt前提）

## 確認方法
```bash
open index.html
```

## セクション構成（TOP・全11）
1. NAV（ロゴ＋6項目＋JA/EN＋カート）
2. HERO（だるまコインケース赤＋新HEROコピー）
3. INTRO（革工場がつくる、日本の革みやげ）
4. BESTSELLERS（だるま・富士山・まねきねこ・おにぎり）
5. CATEGORIES（4カード）
6. ENGIMONO STORIES（赤/金/白/限定の4意味）
7. COLLABORATION（6ロゴ＋featured case）
8. FACTORY（墨背景反転・toB第二の入口）
9. JOURNAL（メディア/コラム/新作 3記事）
10. OEM BANNER（茶墨・念押し）
11. INSTAGRAM（6枚グリッド）
12. FOOTER（4カラム・toB導線含む）

## 使用アセット
- `images/logo.png` ─ ロゴ（本日2026-04-21取得）
- `images/darma_*.jpg` ─ だるま赤/白/金/ラベンダー
- `images/fuji_*.jpg` ─ 富士山青/赤富士
- `images/manekineko.jpg` ─ まねきねこポーチ
- `images/onigiri.jpg` ─ おにぎりポーチ
- `images/whale_pen.jpg` ─ くじらペンケース
- `images/eto_uma.jpg` ─ 午干支シリーズ
- `images/factory_*.jpg` ─ 工房写真

## 未対応（Phase 2以降）
- 商品詳細ページ
- 縁起物コーナー（/engimono）のランディングページ実装
- コラボ実績ページ（ケーススタディ個別）
- FACTORY詳細ページ
- JOURNAL一覧・個別記事ページ
- CONTACT フォーム
- Shopify Translate & Adapt 導入（日英切替）

## デプロイ
`mock-url-publish` スキルで GitHub Pages へ。
```
bash publish.sh <作業Dir> nomunomono-mock "<commit msg>" "<description>"
```
