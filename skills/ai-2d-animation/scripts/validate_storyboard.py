#!/usr/bin/env python3
"""AI 2D Animation Storyboard / Story / Adjacency Validator V1.6"""
import argparse,csv,json,re,sys
CSV_REQUIRED=["Shot","Version","Scene","Duration","Purpose","Beat","Story Info","Visual Question","Audience Knowledge","Character Knowledge","Information Withheld","Reveal Point","Emotional Landing","Camera Strategy","Camera Logic","Camera Necessity","Source","Coverage","Emotion In","Emotion Peak","Emotion Out","Acting","Action","Key Pose","Composition","Size/Angle","Screen Direction","Camera","Timing","Animation","Lighting","Audio","Transition","Continuity In","Continuity Out","Risk","Acceptance","Budget","Anime Treatment","Previous Shot","Adjacency Type","Start State","End State","Spatial Anchor","Subject Screen Position","Gaze Match","Action Match","Prop Match","Lighting Match","Bridge Reason","Ending Function","Exit State","Ending Reason"]
COV={"covered","intentional_repeat","omitted_with_reason","nonvisual_context"}; BUD={"L","M","H","HERO"}; ANIME={"REALISTIC-ANIME","SYMBOLIC","LIMITED","SAKUGA","COMEDY-SD","MOE"}; LOGIC={"ESTABLISH","OBSERVE","WITHHOLD","ALIGN","ESCALATE","REVEAL","MISDIRECT","RECONTEXTUALIZE","CONTRAST","RELEASE"}; NEC={"information","emotion","spatial_understanding","none"}; ADJ={"CONTINUE","REACT","REVEAL","CUTAWAY","BRIDGE","CONTRAST","SCENE_BREAK","TIME_JUMP"}; END={"ACTION_COMPLETE","REACTION_LANDING","REVEAL_LANDING","CHOICE_LANDING","CONSEQUENCE_LANDING","PROP_PAYOFF","RELATIONSHIP_LANDING","MOTION_CONTINUE","DIALOGUE_BUTTON","COMEDY_BUTTON","SUSPENSE_HOLD","TRANSITION_BRIDGE"}; CLICHE=re.compile(r"(fade to black|fade out|lights? dim|lamp.*dim|silhouette|pull back to wide|empty street|rain continues|walks? away|looks? into the distance|final piano note|灯.*暗|熄灯|淡黑|剪影|拉远|空镜|雨继续|背影|远方|最后.*音符)",re.I); VER=re.compile(r'^v\d{3}$')

def validate_csv(path,target_duration=None,sakuga_max_ratio=.25):
 issues=[]; warns=[]
 with open(path,encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
 if not rows:return ['No storyboard rows'],[]
 miss=[x for x in CSV_REQUIRED if x not in rows[0]]
 if miss:return ['Missing columns: '+', '.join(miss)],[]
 shots=set(); total=0; sak=0; prev_end=None; prev_scene=None; prev_shot=None; prev_anchor=None; prev_dir=None
 for i,r in enumerate(rows,1):
  shot=r['Shot'].strip(); scene=r['Scene'].strip()
  if shot in shots:issues.append(f'Row {i}: duplicate Shot {shot}')
  shots.add(shot)
  if not VER.match(r['Version'].strip()):issues.append(f'Row {i}: invalid Version')
  for k in CSV_REQUIRED:
   if k not in {'Shot','Version','Scene','Source','Coverage','Risk','Lighting','Audio','Transition','Spatial Anchor'} and not r.get(k,'').strip():issues.append(f'Row {i}: empty {k}')
  try:
   dur=float(r['Duration']); total+=dur
   if dur<=0:issues.append(f'Row {i}: Duration must be positive')
  except:issues.append(f'Row {i}: invalid Duration')
  if r['Coverage'].strip().lower() not in COV:issues.append(f'Row {i}: invalid Coverage')
  if r['Budget'].strip().upper() not in BUD:issues.append(f'Row {i}: invalid Budget')
  if r['Anime Treatment'].strip() not in ANIME:issues.append(f'Row {i}: invalid Anime Treatment')
  if r['Camera Logic'].strip().upper() not in LOGIC:issues.append(f'Row {i}: invalid Camera Logic')
  if r['Camera Necessity'].strip().lower() not in NEC:issues.append(f'Row {i}: invalid Camera Necessity')
  if r['Adjacency Type'].strip().upper() not in ADJ:issues.append(f'Row {i}: invalid Adjacency Type')
  if r['Ending Function'].strip().upper() not in END:issues.append(f'Row {i}: invalid Ending Function')
  if r['Ending Function'].strip().upper() in {'SCENE_BREAK','TIME_JUMP'}: pass
  ending_text=' '.join([r.get('Ending Function',''),r.get('End State',''),r.get('Ending Reason',''),r.get('Transition','')])
  if CLICHE.search(ending_text) and not r.get('Ending Reason','').strip(): issues.append(f'Row {i}: ENDING_CLICHE requires Ending Reason')
  if i==1:
   if r['Previous Shot'].strip() not in {'','NONE','N/A'}:warns.append('Row 1: Previous Shot should normally be NONE')
  else:
   if r['Previous Shot'].strip()!=prev_shot:issues.append(f'Row {i}: Previous Shot {r["Previous Shot"]} does not match prior Shot {prev_shot}')
   if scene==prev_scene and r['Adjacency Type'].strip().upper() in {'SCENE_BREAK','TIME_JUMP'}:warns.append(f'Row {i}: scene unchanged but break type={r["Adjacency Type"]}')
   if scene!=prev_scene and r['Adjacency Type'].strip().upper() not in {'SCENE_BREAK','TIME_JUMP'}:warns.append(f'Row {i}: new Scene without SCENE_BREAK/TIME_JUMP adjacency')
   if prev_end and r['Start State'].strip() and r['Start State'].strip()!=prev_end.strip():warns.append(f'Row {i}: Start State differs from prior End State; verify intentional state change')
   anchors=[x.strip() for x in r['Spatial Anchor'].split(';') if x.strip()]
   if scene==prev_scene and prev_anchor:
    shared=len(set(anchors)&set(prev_anchor))
    if shared<1:warns.append(f'Row {i}: no shared spatial anchor with previous shot')
   direction=re.sub(r'\s*\(intentional.*\)$','',r['Screen Direction'].strip(),flags=re.I)
   if prev_dir and direction and direction!=prev_dir and '(intentional' not in r['Screen Direction'].lower() and r['Adjacency Type'].strip().upper() not in {'SCENE_BREAK','TIME_JUMP','BRIDGE'}:
    warns.append(f'Row {i}: screen direction changed without bridge/intentional marker')
   if r['Adjacency Type'].strip().upper()=='CONTINUE' and r['Action Match'].strip().lower() in {'none','no',''}:issues.append(f'Row {i}: CONTINUE requires Action Match')
  if r['Camera Logic'].strip().upper() in {'WITHHOLD','MISDIRECT','RECONTEXTUALIZE'} and not r['Information Withheld'].strip():issues.append(f'Row {i}: {r["Camera Logic"]} requires Information Withheld')
  if r['Camera Logic'].strip().upper() in {'REVEAL','RECONTEXTUALIZE'} and not r['Reveal Point'].strip():issues.append(f'Row {i}: {r["Camera Logic"]} requires Reveal Point')
  if r['Camera Necessity'].strip().lower()=='none' and r['Camera'].strip().lower() not in {'static','locked static'}:warns.append(f'Row {i}: necessity none but camera not static')
  if r['Anime Treatment'].strip()=='SAKUGA':sak+=1
  prev_end=r['End State']; prev_scene=scene; prev_shot=shot; prev_anchor=[x.strip() for x in r['Spatial Anchor'].split(';') if x.strip()]; prev_dir=re.sub(r'\s*\(intentional.*\)$','',r['Screen Direction'].strip(),flags=re.I)
 if sak/len(rows)>sakuga_max_ratio:issues.append(f'SAKUGA ratio {sak/len(rows):.1%} exceeds {sakuga_max_ratio:.1%}')
 if target_duration is not None and abs(total-target_duration)>.5:issues.append(f'Duration {total:.1f}s differs from target {target_duration}s')
 return issues,warns

def main():
 p=argparse.ArgumentParser();p.add_argument('path');p.add_argument('--duration',type=float);p.add_argument('--sakuga-max-ratio',type=float,default=.25);a=p.parse_args()
 issues,warns=validate_csv(a.path,a.duration,a.sakuga_max_ratio) if not a.path.endswith('.json') else ([],[])
 print('PASS' if not issues else 'FAIL');[print('ERROR:',x) for x in issues];[print('WARN:',x) for x in warns];return 0 if not issues else 1
if __name__=='__main__':raise SystemExit(main())
