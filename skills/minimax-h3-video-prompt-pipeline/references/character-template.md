# 《深渊赌局》统一角色模板（MiniMax H3）

批量生成分镜提示词时，每个片段文件只复制该片段出现的角色定义行。角色定义保持逐字一致，否则连续生成会变脸。

## 通用场景风格句（detailed_description 开头，所有片段复用）

```
High-quality Japanese anime style, clean 2D hand-drawn animation with crisp ink lines, soft cel shading and subtle motion smear: moody amber lighting from an unsteady crystal chandelier, dark marble floor with faint engraved patterns, drifting dust, deep shadows swallowing a vintage casino hall, stacks of hexagonal chips on the green-felt table.
```

## 角色定义（subject_definitions 行）

**S1 男主（唯一人类）**：
```
<Subject 1> is the protagonist: a young Asian man in his late twenties with sharp pale features, slicked-back black hair, cold dark eyes, and a faint serpentine tattoo curling at his neck, wearing a black vintage three-piece suit with a dark silk tie; he is the only full human among the beastmen.
```

**S2 猪人（贪婪蛮横兽人）**：
```
<Subject 2> is an anthropomorphic pig beastman with a massive bulky frame, coarse dark bristles, a prominent snout, and small greedy eyes, wearing a gold chain and a rolled-sleeve waistcoat that reveals swirling coin tattoos on his arms; his manner is brash and smug.
```

**S3 狐狸（韩国御姐半兽，参考图驱动：银灰发+黑狐耳+银灰尾+酒红漆皮裙）**：
```
<Subject 3> is an exceptionally beautiful mature Korean woman with a cold, seductive older-sister aura: porcelain pale skin, sharp elegant Korean facial features, large golden-yellow eyes framed by long thick lashes with a smoky shadow, vivid crimson lips, voluminous layered silver-gray hair with warm reddish edge highlights, tall pointed black fox ears with pinkish inner fur, and a huge fluffy silver-gray fox tail. She wears a glossy burgundy patent-leather dress with a deep plunging neckline, high side slits rising to her upper thighs, and a low open back bound by thin red straps, black fishnet mesh sleeves and matching thigh-high fishnet stockings, a wide black choker with a hanging pendant, a layered silver necklace with an ornate medallion, and long black gloves with pointed fingertips; she is a half-beast, human-faced with fox ears and tail, and her manner is glamorous, composed and dangerously sly.
```

**S4 乌龟（怯懦自卑兽人）**：
```
<Subject 4> is an anthropomorphic turtle beastman, hunched and timid, with a dark cracked shell on his back, grey-green skin, and frightened wide eyes, wearing a loose old coat.
```

**S5 猫头鹰（理智审判兽人）**：
```
<Subject 5> is an anthropomorphic owl beastman with grey-white feathers, round piercing cold eyes, and white shoulder feathers, dressed in a dark formal coat; his manner is stern and judging.
```

**S6 兔子（脆弱悲悯兽人）**：
```
<Subject 6> is a small timid anthropomorphic rabbit beastman with soft white-grey fur, long drooping ears, and red-rimmed teary eyes, wearing a tattered oversized shirt and clutching a worn cloth doll with cracked stitching; his manner is fragile and sorrowful.
```

## 备注
- 参考图源：`<project-assets>/character-reference.png`（狐狸三视图设定图）
- 已交付 9 段示例素材均存于 `<project-assets>/video-clips/`，实际项目请替换为自己的资产目录
