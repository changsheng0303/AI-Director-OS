# Official H3 comparison — 2026-08-24

## Upstream

- Repository: `https://github.com/MiniMax-AI/MiniMax-H3`
- Commit: `d21241f0a4b3acbb34c97dae47fa417b7065e438`
- Commit date: `2026-08-15T16:31:16+08:00`
- Installed read-only skill: `<codex-skills>/h3-prompt-writing`
- Audited upstream source snapshot: `G:/codex-AI测试/_upstream-snapshots/MiniMax-H3-d21241f`

Installed raw SHA-256 values:

- `SKILL.md`: `A7000443588CA3F145E3B3FD8900F14E0325DC460BD811268FAC89A9DC8E56D0`
- `references/base-en.txt`: `2CFEBC096A6E08370F288D468D90B60F7F9BCB938F94BF090816E910E48E75FC`
- `references/ref-en.txt`: `1E574F356716AD55612247FFB7BBCCBCDB484AD96599D63C7DCA1AF186B1FAB7`

The installer normalized line endings relative to the Git checkout. `git diff --no-index --ignore-space-at-eol` reports no content difference.

## Material differences from the prior local workflow

1. Official Base modes T2VA/I2VA/FL2VA/L2VA use three core fields: `integrated_multimodal_description`, `overall_soundscape`, `non_diegetic_music`.
2. Only full-reference Ref2VA uses the six-section rewrite structure.
3. Official duration guidance is 4–15 seconds.
4. I2VA, FL2VA, and L2VA use explicit frame-alignment instructions before the core fields.
5. FL2VA generally favors one continuous shot unless multiple shots are explicitly required.
6. The prior local workflow incorrectly forced pure T2VA into Ref2VA six-section syntax with synthetic subjects and retention rows.

## Overlay policy

The official skill owns format, mode semantics, field names, section order, timing notation, reference-label semantics, and examples. Local skills may add upstream/downstream artifacts—Canon, Narrative IR, assets, Shot IR, continuity manifests, audio timelines, batch validation, and repair workflows—but must compile those constraints into an official output field without changing the official schema.

Never edit the installed official directory. When upstream changes, reinstall to a versioned staging location, compare, then replace the official directory only through the skill installer/update procedure. Keep local behavior in `minimax-h3-video-prompt-pipeline` and related overlay references/scripts.
