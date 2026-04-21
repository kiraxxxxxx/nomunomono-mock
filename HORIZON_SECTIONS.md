# Horizon Theme Section 設計書 ─ のむのもの

**Date**: 2026-04-21
**Target**: Shopify Horizon Theme
**Purpose**: 簡易モック（HTML/CSS）を Horizon の section.liquid 構造に落とし込む際の対応表・骨格設計。

---

## 前提

- Horizon は Shopify の最新公式テーマ（2024.5リリース）
- Section + Block の柔軟な構造・AI機能・メガメニュー対応
- `sections/` 配下に個別の `.liquid` ファイルを作成し、`templates/index.json` に配置する
- Horizon は **Liquid + JSON schema** ベース、CSS は `assets/base.css` に追加

---

## 📦 ファイル構造（Horizon ベース）

```
theme/
├── config/
│   └── settings_schema.json       # ブランド色・フォント定義
├── sections/
│   ├── hero.liquid                # 01 HERO
│   ├── intro.liquid               # 02 INTRO
│   ├── bestsellers.liquid         # 03 BESTSELLERS (Horizon標準の featured-collection 拡張)
│   ├── categories.liquid          # 04 CATEGORIES (multicolumn 拡張)
│   ├── engimono-stories.liquid    # 05 ENGIMONO STORIES (カスタム)
│   ├── collaboration.liquid       # 06 COLLABORATION (カスタム)
│   ├── factory.liquid             # 07 FACTORY (image-with-text 拡張)
│   ├── journal.liquid             # 08 JOURNAL (featured-blog 拡張)
│   ├── oem-banner.liquid          # 09 OEM BANNER (カスタム・call-to-action 拡張)
│   ├── instagram-grid.liquid      # 10 INSTAGRAM (カスタム)
│   └── footer.liquid              # 11 FOOTER (Horizon標準footer拡張)
├── templates/
│   └── index.json                 # TOP構成定義
├── assets/
│   └── nomunomono.css             # カスタムCSS
└── locales/
    ├── ja.default.json            # 日本語テキスト
    └── en.json                    # 英語テキスト
```

---

## 🎨 config/settings_schema.json 追加項目

```json
{
  "name": "Brand",
  "settings": [
    { "type": "color", "id": "color_paper", "label": "和紙白", "default": "#f6f1e8" },
    { "type": "color", "id": "color_ink", "label": "墨", "default": "#1a1614" },
    { "type": "color", "id": "color_aka", "label": "朱（だるま赤）", "default": "#c8362d" },
    { "type": "color", "id": "color_kin", "label": "金（縁起アクセント）", "default": "#b48a3e" },
    { "type": "color", "id": "color_ai", "label": "藍（富士山系）", "default": "#5b8aa6" },
    { "type": "font_picker", "id": "font_heading_jp", "label": "日本語見出し", "default": "shippori_mincho_b1_n5" },
    { "type": "font_picker", "id": "font_body_jp", "label": "日本語本文", "default": "noto_serif_jp_n4" }
  ]
}
```

---

## 🧩 各セクション対応表

### 01. HERO — `sections/hero.liquid`

**用途**: TOPのファーストビュー
**Horizon標準**: `hero.liquid` 相当（拡張）
**Schema**:
```liquid
{% schema %}
{
  "name": "Hero",
  "settings": [
    { "type": "text", "id": "issue", "label": "Issue No.", "default": "VOL.001 ─ EST.1923" },
    { "type": "richtext", "id": "title", "label": "Title",
      "default": "<p>革に、<br>願いを<em>縫いつけて</em>。</p>" },
    { "type": "text", "id": "title_en", "label": "Title (EN)",
      "default": "Where wishes are stitched into leather." },
    { "type": "richtext", "id": "lead", "label": "Lead Copy" },
    { "type": "image_picker", "id": "hero_image", "label": "Hero Image" },
    { "type": "url", "id": "cta_primary_url", "label": "CTA 1 URL" },
    { "type": "text", "id": "cta_primary_text", "label": "CTA 1 Text", "default": "PRODUCTS →" },
    { "type": "url", "id": "cta_secondary_url", "label": "CTA 2 URL" },
    { "type": "text", "id": "cta_secondary_text", "label": "CTA 2 Text", "default": "のむのもの とは" }
  ],
  "presets": [{ "name": "Hero" }]
}
{% endschema %}
```

**注意**:
- HEROは1ブロックのみ（複数スライドは今回不要）
- `{{ section.settings.hero_image | image_url: width: 1200 }}` で最適化画像
- Horizon の AI 機能でコピー改変する際、`title` フィールドは日本語で固定＋英語は別フィールド

---

### 02. INTRO — `sections/intro.liquid`

**用途**: ブランド紹介の短文＋CTA
**Horizon標準**: `rich-text.liquid` ベース
**Schema (簡略)**:
```liquid
{
  "name": "Intro",
  "settings": [
    { "type": "richtext", "id": "title", "default": "<p>革工場がつくる、<br>日本の革みやげ。</p>" },
    { "type": "richtext", "id": "lead" },
    { "type": "url", "id": "cta_url" },
    { "type": "text", "id": "cta_text" }
  ]
}
```

---

### 03. BESTSELLERS — `sections/bestsellers.liquid`

**用途**: 人気商品4グリッド
**Horizon標準**: `featured-collection.liquid` を流用（拡張）
**実装**:
```liquid
{% assign collection = collections[section.settings.collection] %}
<div class="bestsellers-grid">
  {% for product in collection.products limit: section.settings.product_limit %}
    <a href="{{ product.url }}" class="product-card">
      <div class="product-img">
        <span class="product-rank">No.{{ forloop.index }}</span>
        {{ product.featured_image | image_url: width: 600 | image_tag: alt: product.title }}
      </div>
      <p class="product-name">{{ product.title }}</p>
      <p class="product-colors">{{ product.metafields.custom.colors }}</p>
      <p class="product-price">{{ product.price | money }}</p>
    </a>
  {% endfor %}
</div>
```

**必要な設定**:
- Shopify Admin で `bestsellers` コレクションを作成（手動でランキング順に商品追加）
- 商品メタフィールド `custom.colors` を用意（カラー表記用）

---

### 04. CATEGORIES — `sections/categories.liquid`

**用途**: カテゴリー4カード
**Horizon標準**: `multicolumn.liquid` + `collection-list.liquid` のハイブリッド
**Block構造**:
```liquid
{% schema %}
{
  "name": "Categories",
  "max_blocks": 6,
  "blocks": [
    {
      "type": "category",
      "name": "Category",
      "settings": [
        { "type": "collection", "id": "collection", "label": "Collection" },
        { "type": "image_picker", "id": "image", "label": "Image" },
        { "type": "text", "id": "tag", "label": "Tag", "default": "CAT 01" },
        { "type": "text", "id": "name", "label": "Name" },
        { "type": "text", "id": "desc", "label": "Description" },
        { "type": "checkbox", "id": "is_dark", "label": "Dark variant" }
      ]
    }
  ]
}
{% endschema %}
```

---

### 05. ENGIMONO STORIES — `sections/engimono-stories.liquid`

**用途**: 色の意味を読み解く特設ゾーン
**Horizon標準**: `image-with-text.liquid` + `gallery.liquid` のハイブリッド（カスタム）
**Block構造**: meaning × 4（赤/金/白/限定）

**重要**: このセクションはブランドの独自性が最も出る場所。Horizon の AI 機能で翻訳させる際、「魔除け」「財運」などの縁起用語は **手動で英訳** を入れる（AI任せだと"Evil warding"などの直訳になる → "Protection" など意訳で）

---

### 06. COLLABORATION — `sections/collaboration.liquid`

**用途**: コラボ実績＋featured case
**Horizon標準**: 新規カスタムセクション
**Block構造**:
```json
{
  "blocks": [
    { "type": "logo", "settings": [{"type":"text","id":"name"}, {"type":"image_picker","id":"image"}] },
    { "type": "featured_case", "limit": 1, "settings": [
      { "type":"image_picker","id":"image" },
      { "type":"text","id":"subtitle" },
      { "type":"text","id":"title" },
      { "type":"richtext","id":"body" },
      { "type":"url","id":"cta_cases_url" },
      { "type":"url","id":"cta_collab_url" }
    ]}
  ]
}
```

---

### 07. FACTORY — `sections/factory.liquid`

**用途**: 工房紹介（墨背景反転）
**Horizon標準**: `image-with-text.liquid` を拡張
**特徴**:
- `color_scheme: "inverse"` を使用（Horizonの color_scheme 機能）
- 画像は `filter:brightness(0.85) contrast(1.05)` を CSS で
- CTAボタン 2つ（工房を見る・OEM相談）

```liquid
<section class="factory color-scheme-inverse">
  <div class="factory-grid">
    <div class="factory-visual">
      {{ section.settings.image | image_url: width: 1000 | image_tag }}
    </div>
    <div class="factory-text">
      <p class="sec-num">{{ section.settings.since_label }}</p>
      <h2>{{ section.settings.title }}</h2>
      <p>{{ section.settings.body }}</p>
      <div class="factory-actions">
        <a href="{{ section.settings.cta1_url }}" class="btn ghost-light">{{ section.settings.cta1_text }}</a>
        <a href="{{ section.settings.cta2_url }}" class="btn kin">{{ section.settings.cta2_text }}</a>
      </div>
    </div>
  </div>
</section>
```

---

### 08. JOURNAL — `sections/journal.liquid`

**用途**: ブログ記事3件
**Horizon標準**: `featured-blog.liquid`
**実装**: 標準の featured-blog をほぼそのまま使用・スタイルのみカスタム

```liquid
{% assign blog = blogs[section.settings.blog] %}
<div class="journal-grid">
  {% for article in blog.articles limit: 3 %}
    <a href="{{ article.url }}" class="journal-card">
      <div class="journal-img">
        {{ article.image | image_url: width: 800 | image_tag }}
      </div>
      <p class="journal-meta">{{ article.tags | first | upcase }} ・ {{ article.published_at | date: "%Y.%m.%d" }}</p>
      <h3 class="journal-title">{{ article.title }}</h3>
    </a>
  {% endfor %}
</div>
```

**必要な設定**: Shopify Admin で `journal` ブログを作成、タグ運用（MEDIA / ENGIMONO / NEWS）

---

### 09. OEM BANNER — `sections/oem-banner.liquid`

**用途**: toB問い合わせCTA（茶墨背景）
**Horizon標準**: `call-to-action.liquid` カスタム
**特徴**: 背景 `#2a241f`・CTA 2つ（コラボ相談＝金／OEM相談＝ゴーストライト）

---

### 10. INSTAGRAM — `sections/instagram-grid.liquid`

**用途**: Instagram 6枚グリッド
**実装**:
- **Phase 1**: 手動で画像アップロード（6 image_picker block）
- **Phase 2**: Instagram API または Shopify App（例: Instafeed）連携

---

### 11. FOOTER — `sections/footer.liquid`

**用途**: 4カラム（Brand / SHOP / FOR BUSINESS / SUPPORT）
**Horizon標準**: `footer.liquid` を拡張
**Block構造**: `menu_block` × 4（それぞれ Shopify のメニュー or 手動リンク）

**注意**:
- Shopify の Menu 機能と併用（Admin > オンラインストア > メニュー）
- `footer-menu-shop` / `footer-menu-business` / `footer-menu-support` の 3 メニュー作成

---

## 📋 templates/index.json 構成

```json
{
  "sections": {
    "hero": { "type": "hero" },
    "intro": { "type": "intro" },
    "bestsellers": { "type": "bestsellers" },
    "categories": { "type": "categories" },
    "engimono-stories": { "type": "engimono-stories" },
    "collaboration": { "type": "collaboration" },
    "factory": { "type": "factory" },
    "journal": { "type": "journal" },
    "oem-banner": { "type": "oem-banner" },
    "instagram-grid": { "type": "instagram-grid" }
  },
  "order": [
    "hero", "intro", "bestsellers", "categories",
    "engimono-stories", "collaboration", "factory",
    "journal", "oem-banner", "instagram-grid"
  ]
}
```

---

## 🌐 多言語化（Shopify Translate & Adapt）

**方針**:
- サイトの**ベース言語は日本語**（Shopify Admin で設定）
- **追加言語は英語**（Settings > Languages > Add English）
- **Translate & Adapt アプリ**（無料）を導入

**翻訳ルール**:
| 要素 | ベース（日本語） | 英語訳 |
|---|---|---|
| HEROタイトル | 革に、願いを縫いつけて。 | Where wishes are stitched into leather. |
| HERO Lead | 大正12年、東東京の革工房から… | Since 1923, from a leather atelier in east Tokyo… |
| INTRO | 革工場がつくる、日本の革みやげ。 | Leather souvenirs of Japan, made by a Tokyo leather factory. |
| ENGIMONO 見出し | 色にも、形にも、意味がある。 | Every color, every shape carries meaning. |
| FACTORY 見出し | 大正12年から、東東京の革工房。 | Crafted in east Tokyo since 1923. |
| OEM BANNER | オリジナルを、一緒につくりませんか。 | Let's create something original, together. |

**ナビラベル**:
- Admin > Menu で各リンクを編集
- Horizon の言語スイッチャー（ヘッダー右端）を有効化
- 英語モード時は `/en/` プレフィックス付きURL（Shopify 標準）

---

## 🚀 実装フェーズ

### Phase 1（4/25まで・Shopifyで簡易サイト公開）
- [x] モック HTML 完成（このセッション）
- [ ] Horizon テーマを Shopify ストアにインストール
- [ ] `hero.liquid` / `intro.liquid` / `factory.liquid` の3セクションだけ実装
- [ ] 商品は `bestsellers` コレクションに4〜6商品登録のみ
- [ ] 英語翻訳は Translate & Adapt で主要コピーだけ

### Phase 2（5〜7月・本格EC）
- [ ] 全11セクションを Horizon で実装
- [ ] 商品詳細ページ・/engimono LP・/collaboration LP 作成
- [ ] Translate & Adapt で全コンテンツ英語化
- [ ] Geolocation 設定（海外訪問者に英語自動表示）
- [ ] Instagram API 連携

### Phase 3（8〜10月・拡張）
- [ ] `/tokyo-leather-souvenir` SEO LP 作成
- [ ] 干支シリーズ年替わり運用
- [ ] メルマガ・CRM 連携（Shopify Email または Klaviyo）

---

## 💡 Horizon ならではの活用ポイント

1. **AI画像生成**: 縁起物コラムの挿絵を Horizon の AI 機能で生成可能
2. **Metaobjects**: 縁起物の「意味」を Metaobject として管理（赤→魔除け、金→財運…）
3. **Color Schemes**: `default` / `inverse`（墨背景）/ `accent`（茶墨）の3スキームを定義し、各セクションに適用
4. **Block の柔軟性**: BESTSELLERS / CATEGORIES / COLLABORATION はすべて block 配列で追加削除自由
5. **Mega Menu**: PRODUCTS ナビから商品カテゴリ＋限定コーナーをメガメニュー表示

---

## ⚠️ 注意点

- HEROの `em` タグ（"縫いつけて"の朱色）は Rich Text editor で装飾必要（Admin から編集する際の手順を野村さんに説明）
- カートアイコンは Horizon 標準で対応済み
- モバイルナビは Horizon 標準のハンバーガーに依存（モックは `display:none` で非表示にしている）
- フォントは Google Fonts 経由で `theme.liquid` に `<link>` 追加するか、Horizon の font_picker で指定

---

## 📎 参考

- Horizon Documentation: https://shopify.dev/docs/storefronts/themes/tools/horizon
- Dawn (過去の標準テーマ) との差分: https://shopify.dev/docs/storefronts/themes/trending/horizon-vs-dawn
- Translate & Adapt: https://apps.shopify.com/translate-and-adapt
