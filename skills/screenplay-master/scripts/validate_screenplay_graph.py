#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

def unique(items, key, label, errors):
    out={}
    for i,item in enumerate(items,1):
        value=item.get(key) if isinstance(item,dict) else None
        if not value: errors.append(f"{label}[{i}] missing {key}")
        elif value in out: errors.append(f"duplicate {label} {value}")
        else: out[value]=item
    return out

def validate(data):
    errors=[]
    if not isinstance(data,dict): return ["root must be an object"]
    if data.get("schema_version")!="1.0": errors.append("schema_version must be 1.0")
    if not str(data.get("project_id","")).strip(): errors.append("project_id is required")
    if data.get("status") not in {"provisional","approved","locked"}: errors.append("status is invalid")
    contract=data.get("story_contract",{})
    for field in ("protagonist","want","opposition","stakes","ending_promise"):
        if not str(contract.get(field,"")).strip(): errors.append(f"story_contract missing {field}")
    characters=unique(data.get("characters",[]),"character_id","character",errors)
    names={c.get("name") for c in characters.values()}
    dialogue=unique(data.get("dialogue",[]),"dialogue_id","dialogue",errors)
    scenes=unique(data.get("scenes",[]),"scene_id","scene",errors)
    if not scenes: errors.append("at least one scene is required")
    for scene_id,scene in scenes.items():
        for field in ("heading","goal","resistance","turn","exit_state"):
            if not str(scene.get(field,"")).strip(): errors.append(f"scene {scene_id} missing {field}")
        for dialogue_id in scene.get("dialogue_ids",[]):
            if dialogue_id not in dialogue: errors.append(f"scene {scene_id} references unknown dialogue {dialogue_id}")
    for dialogue_id,line in dialogue.items():
        text=str(line.get("text","")).strip()
        if not text: errors.append(f"dialogue {dialogue_id} has empty text")
        if names and line.get("speaker") not in names: errors.append(f"dialogue {dialogue_id} speaker is not in characters")
        stress=line.get("logical_stress",[])
        if len(stress)>3: errors.append(f"dialogue {dialogue_id} has more than three logical stress spans")
        seen=[]
        for item in stress:
            span=str(item.get("span","")).strip()
            if not span or span not in text: errors.append(f"dialogue {dialogue_id} stress span not found in text: {span}")
            if span in seen: errors.append(f"dialogue {dialogue_id} has duplicate stress span {span}")
            seen.append(span)
            if item.get("strength") not in {"light","moderate","strong"}: errors.append(f"dialogue {dialogue_id} has invalid stress strength")
    return errors

def main():
    parser=argparse.ArgumentParser();parser.add_argument("path");args=parser.parse_args()
    data=json.loads(Path(args.path).read_text(encoding="utf-8-sig"));errors=validate(data)
    print("PASS" if not errors else "FAIL")
    for item in errors: print("ERROR:",item)
    return 1 if errors else 0
if __name__=="__main__": raise SystemExit(main())
