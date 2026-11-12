import os,json,urllib.request as U
V=[0,100,320,330,500,975,0]
PS=['MMMMMMMMffffffffRRW\\\\WRROORYYROOMMMWWMMMOKHMMHKOORRCCRROMMMMMMMM','49>>>>949CMMMMC9>MRUURM>>OUWWUO>>MUWWUM>>ORUURO>9CMOOMC949>>>>94','M'*64,'M'*64,'M'*64,'M'*64]
T=[[(ord(c)-77)*2 for c in s]for s in PS]
KN=[-33,-31,-18,-14,14,18,31,33];BD=[-17,-15,15,17];RD=[-16,-1,1,16];QD=BD+RD
D=[(KN,0),(BD,1),(RD,1),(QD,1),(QD,0)]
CR={112:13,119:14,0:7,7:11,116:12,4:3}
CT=((1,116,118,(117,118),(116,117,118)),(2,116,114,(113,114,115),(114,115,116)),(4,4,6,(5,6),(4,5,6)),(8,4,2,(1,2,3),(2,3,4)))
INF=10**9;CAP=20000;ND=[0];X=TimeoutError
def att(B,s,c):
 for ds,v,sl in(((15*c,17*c),1,0),(KN,2,0),(QD,6,0),(BD,3,1),(BD,5,1),(RD,4,1),(RD,5,1)):
  for d in ds:
   t=s+d
   while not t&0x88:
    p=B[t]
    if p:
     if p==v*c:return 1
     break
    if not sl:break
    t+=d
def gen(S):
 B,tn,ca,ep=S;ms=[]
 for sq in range(128):
  p=B[sq]
  if p*tn<=0:continue
  a=abs(p)
  if a==1:
   d=-16*tn;rw=sq>>4;pr=rw==(1 if tn>0 else 6);tg=[]
   if not B[sq+d]:tg.append(sq+d)
   for dd in(d-1,d+1):
    t=sq+dd
    if not t&0x88 and(B[t]and B[t]*tn<0 or t==ep):tg.append(t)
   for t in tg:ms+=[sq|t<<7|x<<14 for x in(5,4,3,2)]if pr else[sq|t<<7]
   if rw==(6 if tn>0 else 1)and not B[sq+d]and not B[sq+2*d]:ms.append(sq|(sq+2*d)<<7)
  else:
   ds,sl=D[a-2]
   for d in ds:
    t=sq+d
    while not t&0x88:
     q=B[t]
     if q:
      if q*tn<0:ms.append(sq|t<<7)
      break
     ms.append(sq|t<<7)
     if not sl:break
     t+=d
 for bt,kf,kt,em,sf in CT:
  if ca&bt and(bt<3)==(tn>0)and all(not B[x]for x in em)and all(not att(B,x,-tn)for x in sf):ms.append(kf|kt<<7)
 return ms
def mk(S,m):
 B,tn,ca,ep=S;B=B[:];f=m&127;t=(m>>7)&127;p=B[f];a=abs(p);B[f]=0
 if a==1 and t==ep and not B[t]:B[t+16*tn]=0
 B[t]=(m>>14)*tn if m>>14 else p
 if a==6 and abs(t-f)==2:rf,rt=(t+1,t-1)if t>f else(t-2,t+1);B[rt]=B[rf];B[rf]=0
 return B,-tn,ca&CR.get(f,15)&CR.get(t,15),(f+t)//2 if a==1 and abs(t-f)==32 else-1
def lm(S):
 return[m for m in gen(S)if not att((Z:=mk(S,m))[0],Z[0].index(-6*Z[1]),Z[1])]
def ev(S):
 B=S[0];s=0
 for sq in range(128):
  p=B[sq]
  if p:a=abs(p);s+=(V[a]+T[a-1][sq-(sq>>4)*8 if p>0 else(7-(sq>>4))*8+(sq&7)])*(p//a)
 return s
def qs(S,a,b,pl):
 ND[0]+=1
 if ND[0]>CAP:raise X
 st=ev(S)*S[1]
 if st>=b:return st
 a=max(a,st);bs=a;ms=[m for m in lm(S)if S[0][(t:=(m>>7)&127)]or t==S[3]]
 ms.sort(key=lambda m:-msc(S,m))
 for m in ms:
  s=-qs(mk(S,m),-b,-a,pl+1)
  bs=max(bs,s);a=max(a,s)
  if a>=b:break
 return bs
def msc(S,m):
 B=S[0];t=(m>>7)&127;pr=(m>>14)&7;c=B[t]
 if c:return 1000000+V[abs(c)]*16-V[abs(B[m&127])]//16
 if pr:return 900000+V[pr]
 return 0
def sr(S,d,a,b,pl):
 ND[0]+=1
 if ND[0]>CAP:raise X
 if d==0:return qs(S,a,b,pl)
 ms=lm(S)
 if not ms:return-INF+pl if att(S[0],S[0].index(6*S[1]),-S[1])else 0
 ms.sort(key=lambda m:-msc(S,m));bs=-INF
 for m in ms:
  s=-sr(mk(S,m),d-1,-b,-a,pl+1)
  bs=max(bs,s);a=max(a,s)
  if a>=b:break
 return bs
def best(S):
 ND[0]=0;ms=lm(S)
 if not ms:return None
 bm=ms[0]
 for d in 3,9:
  ms.sort(key=lambda m:-msc(S,m));a=-INF
  try:
   for m in ms:
    s=-sr(mk(S,m),d-1,-INF,-a,1)
    if s>a:a=s;bm=m
  except X:break
 return bm
def fen(s):
 ps=s.split();B=[0]*128;sq=0
 for ch in ps[0]:
  if ch=='/':sq+=8
  elif ch.isdigit():sq+=int(ch)
  else:B[sq]=('pnbrqk'.index(ch.lower())+1)*(1,-1)[ch.islower()];sq+=1
 ca=sum(1<<i for i,ch in enumerate('KQkq')if ch in ps[2])
 ep=(8-int(ps[3][1]))*16+ord(ps[3][0])-97 if len(ps)>3 and ps[3]!='-'else-1
 return B,(1,-1)[ps[1]=='b'],ca,ep
def uci(m):
 return''.join(chr(97+(s&7))+chr(56-(s>>4))for s in(m&127,(m>>7)&127))+('  nbrq'[m>>14]if m>>14 else'')
URL=os.getenv('MAKEFUN_ENV_URL','')
def post(p,o):
 with U.urlopen(U.Request(URL+p,data=json.dumps(o).encode()),timeout=30)as r:return json.loads(r.read()or b'{}')
def play():
 for _ in range(64):
  g=post('/game',{})
  if not g.get('game'):return
  S=fen(g['fen']);me=S[1]
  while S[1]==me:
   m=best(S)
   if m is None:break
   r=post('/move',{'game':g['game'],'move':uci(m)})
   S=fen(r['fen'])if r.get('fen')else mk(S,m)
if __name__=='__main__'and URL:play()
