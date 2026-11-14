# Montaż nagrania łączności 007 (e08) z dźwięków Groka: wiatr, piec, głos, pies, „Mam.”, sygnał cofania, filtr radiowy.
# Wejście: katalog S z plikami SLAD007-0[3-6]-*.mp3; wyjście /tmp/call007.wav → ffmpeg loudnorm I=-20 → assets/audio/007-call.mp3
import numpy as np, subprocess, scipy.signal as sg
from scipy.io import wavfile
SR=48000
S='/mnt/user-data/uploads/Downloads/SLAD-007/dzwieki/'
def load(p):
    subprocess.run(['ffmpeg','-v','error','-y','-i',p,'-ac','1','-ar',str(SR),'/tmp/_l.wav'],check=True)
    r,a=wavfile.read('/tmp/_l.wav'); a=a.astype(np.float32)/32768; return a
def rms(a): return float(np.sqrt(np.mean(a**2))+1e-9)
T=21.5; N=int(T*SR); mix=np.zeros(N,np.float32)
def put(sig,t,g):
    i=int(t*SR); j=min(N,i+len(sig)); mix[i:j]+=sig[:j-i]*g
# wind bed with gusts
wind=load(S+'SLAD007-05-sfx-wind.mp3'); wind=wind/rms(wind)
w=wind[:N] if len(wind)>=N else np.pad(wind,(0,N-len(wind)))
t=np.arange(N)/SR
env=0.05+0.10*np.exp(-((t-1.8)/0.6)**2)+0.12*np.exp(-((t-16.5)/0.8)**2)
mix+=w*env
# stove (clip) from 0.5 to 13.0, quiet; ensure pops near 1.2-2.4 and 9.8
st=load(S+'SLAD007-06-sfx-stove.mp3'); st=st/rms(st)
e=np.abs(st); hop=SR//100; fr=np.array([e[k:k+hop].max() for k in range(0,len(e)-hop,hop)])
pk=np.argsort(fr)[::-1]; pops=[]
for p in pk:
    if all(abs(p-q)>60 for q in pops): pops.append(p)
    if len(pops)>=6: break
pops=sorted(pops); print('stove pops (s):',[p/100 for p in pops])
# choose offset so a pop lands at ~1.8
off=pops[0]/100-1.8+0.5  # stove placed starting at 0.5s, source offset
src0=max(0.0,pops[0]/100-(1.8-0.5))
clip_len=12.5
seg=st[int(src0*SR):int((src0+clip_len)*SR)]
fade=np.ones(len(seg)); fl=int(0.05*SR); fade[:fl]=np.linspace(0,1,fl); fade[-fl:]=np.linspace(1,0,fl)
put(np.clip(seg*fade,-6,6),0.5,0.02)
# extra pop at 9.8: take loudest pop window not already used and place at 9.8
p2=pops[-1]/100; pw=st[int((p2-0.05)*SR):int((p2+0.25)*SR)]
put(np.clip(pw,-8,8),9.75,0.035)
# voice
v=load(S+'SLAD007-03-krystian-call.mp3'); v=v/ (np.abs(v).max()+1e-9)
put(v,3.0,0.55)
# dog
d=load(S+'SLAD007-04-sfx-dog.mp3'); d=d/(np.abs(d).max()+1e-9)
put(d,6.0,0.45)
# Igor "Mam."
m=load('/home/claude/slad/assets/voice/007/mam.mp3'); m=m/(np.abs(m).max()+1e-9)
put(m,14.0,0.25)
# beeps: 8 x 0.25s at 1150 Hz every 0.5s from 15.5
for k in range(8):
    bt=np.arange(int(0.25*SR))/SR; b=np.sin(2*np.pi*1150*bt)*np.minimum(1,np.minimum(bt,0.25-bt)/0.01)
    put(b.astype(np.float32),15.5+0.5*k,0.12)
# radio filter
sos=sg.butter(4,[300,3400],btype='band',fs=SR,output='sos'); y=sg.sosfilt(sos,mix)
y=np.tanh(y*2.2)/np.tanh(2.2)  # light saturation/compression
# hiss + clicks
rng=np.random.default_rng(7); hiss=sg.sosfilt(sos,rng.standard_normal(N))*0.012; y=y+hiss
def click(t0,dur=0.3):
    n=int(dur*SR); c=rng.standard_normal(n)*np.exp(-np.arange(n)/(0.05*SR)); i=int(t0*SR); y[i:i+n]+=c[:len(y[i:i+n])]*0.35
click(0.0); click(20.5)
y[int(20.55*SR):]*=1  # noise continues
y=y/np.abs(y).max()*0.7
wavfile.write('/tmp/call007.wav',SR,(y*32767).astype(np.int16))
