# Continuity Validation V1.2

## Required State
Character: pose/state, gaze, screen position, movement direction, costume/accessory.
Scene: layout, time, weather, lighting.
Camera: axis, screen direction, lens/shot size where relevant.
Props: state and ownership.

## Checks
- `continuity_out(S_n)` must be compatible with `continuity_in(S_n+1)`.
- Screen direction changes require reason or transition.
- Axis breaks must be explicitly intentional.
- Asset version changes require a change event.
- Lighting/time/weather jumps require a state event.
- Character count changes require story justification.

## Failure Codes
`CONTINUITY_BREAK`, `CAMERA_DRIFT`, `BACKGROUND_DRIFT`, `CHARACTER_DRIFT`.

## Repair
Prefer adding a transition shot, correcting the affected state field, or restoring the previous locked asset. Do not rewrite unrelated prompts.
