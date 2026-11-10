import numpy as np, subprocess, os
SR=44100; rng=np.random.default_rng(11)
def lp(x,fc):  # jednobiegunowy dolnoprzepustowy (wielokrotnie = łagodniejszy)
    a=np.exp(-2*np.pi*fc/SR); y=np.empty_like(x); s=0.0
    from scipy.signal import lfilter
    return lfilter([1-a],[1,-a],x)
from scipy.signal import butter, sosfilt, sosfiltfilt
def bp(x,lo,hi,o=2): return sosfilt(butter(o,[lo,hi],'band',fs=SR,output='sos'),x)
def lpf(x,fc,o=2): return sosfilt(butter(o,fc,'low',fs=SR,output='sos'),x)
def hpf(x,fc,o=2): return sosfilt(butter(o,fc,'high',fs=SR,output='sos'),x)
def env_noise(n,fc): return lpf(rng.standard_normal(n),fc,1)
def norm(x,peak=0.9): return x/np.max(np.abs(x))*peak

def ambience(dur=125, xf=5):
    n=int(dur*SR); t=np.arange(n)/SR; ch=[]
    gust=0.65+0.35*np.clip(lpf(rng.standard_normal(n),0.08,1)*40,-1,1)   # wolne porywy
    for c in range(2):
        rain=lpf(bp(rng.standard_normal(n),250,3800,2),2600,1)*0.30*gust
        rain+=hpf(rng.standard_normal(n),5000,2)*0.012*gust
        drops=np.zeros(n); k=rng.poisson(45*dur); pos=rng.integers(0,n-800,k)
        amp=rng.pareto(3,k)*0.05; L=np.exp(-np.arange(400)/45)
        for p_,a_ in zip(pos,amp): drops[p_:p_+400]+=a_*L*rng.standard_normal(400)
        drops=bp(drops,1200,6000,2)
        wind=bp(rng.standard_normal(n),180,900,2)*0.10*(0.5+0.5*np.sin(2*np.pi*t/23+c))*gust
        ch.append(rain+drops+wind)
    # wspólne: pomruk domu, dron, grzmoty, tykanie zegara
    room=lpf(np.cumsum(rng.standard_normal(n))*0.002,120,2); room-=lpf(room,8,1)
    drone=(0.020*np.sin(2*np.pi*55*t)+0.012*np.sin(2*np.pi*82.41*t+1)+0.008*np.sin(2*np.pi*65.41*t+2))*(0.6+0.4*np.sin(2*np.pi*t/31))
    thunder=np.zeros(n)
    for start in [14, 52, 93]:
        s=int(start*SR); L=int(9*SR); tt=np.arange(L)/SR
        e=(1-np.exp(-tt/0.35))*np.exp(-tt/2.6)
        rum=lpf(np.cumsum(rng.standard_normal(L))*0.01,160,2); rum=rum-lpf(rum,15,1)
        crack=hpf(rng.standard_normal(L),900,2)*np.exp(-tt/0.25)*0.15
        thunder[s:s+L]+=norm(rum*e,0.55)+crack*(tt<1.2)
    clock=np.zeros(n)
    for i,tk in enumerate(np.arange(0.5,dur,1.0)):
        s=int(tk*SR); L=900; ttk=np.arange(L)/SR
        clock[s:s+L]+=np.sin(2*np.pi*(2600 if i%2 else 2200)*ttk)*np.exp(-ttk/0.004)*0.035
    common=room*0.8+drone+thunder*0.55+clock
    st=np.stack([ch[0]+common, ch[1]+common*0.97],1)
    # pętla bez szwu: ogon przenikany w początek (równa moc)
    X=int(xf*SR); fade=np.sin(np.linspace(0,np.pi/2,X))[:,None]
    head=st[:X]*fade + st[-X:]*np.cos(np.linspace(0,np.pi/2,X))[:,None]
    loop=np.concatenate([head, st[X:-X]],0)
    return norm(loop,0.8)


def train_ambience(dur=125, xf=5):
    n=int(dur*SR); t=np.arange(n)/SR
    rumble=lpf(np.cumsum(rng.standard_normal(n))*0.004,140,2); rumble-=lpf(rumble,10,1)
    rumble*=0.9+0.1*np.sin(2*np.pi*t/7.3)
    body=bp(rng.standard_normal(n),60,400,2)*0.18
    hiss=bp(rng.standard_normal(n),800,3500,2)*0.05
    # stukot na złączach szyn: para uderzeń (wózek przedni i tylny) co 1,5 s
    clack=np.zeros(n)
    def hit(at,a):
        s0=int(at*SR); L=int(0.12*SR); tt=np.arange(L)/SR
        if s0+L>=n: return
        w=(np.sin(2*np.pi*95*tt)*0.7+bp(rng.standard_normal(L),300,2500,2)*0.6)*np.exp(-tt/0.03)
        clack[s0:s0+L]+=w*a
    for k,at in enumerate(np.arange(0.3,dur,1.5)):
        j=rng.uniform(-0.01,0.01)
        hit(at+j,0.55); hit(at+0.11+j,0.45); hit(at+0.62+j,0.5); hit(at+0.73+j,0.4)
    rain=lpf(bp(rng.standard_normal(n),400,5000,2),3000,1)*0.07*(0.7+0.3*np.sin(2*np.pi*t/19))
    horn=np.zeros(n)
    for at in [37, 96]:
        s0=int(at*SR); L=int(2.6*SR); tt=np.arange(L)/SR
        e=np.clip(tt/0.25,0,1)*np.clip((2.6-tt)/0.8,0,1)
        h=(np.sin(2*np.pi*311*tt)+0.6*np.sin(2*np.pi*370*tt)+0.3*np.sin(2*np.pi*622*tt))*e*0.10
        horn[s0:s0+L]+=lpf(h,1200,2)
    mono=rumble*1.1+body+hiss+clack*0.5+horn
    st=np.stack([mono+rain, mono*0.98+np.roll(rain,4410)],1)
    X=int(xf*SR); fade=np.sin(np.linspace(0,np.pi/2,X))[:,None]
    head=st[:X]*fade+st[-X:]*np.cos(np.linspace(0,np.pi/2,X))[:,None]
    return norm(np.concatenate([head,st[X:-X]],0),0.8)

def sfx_paper():
    L=int(0.55*SR); t=np.arange(L)/SR; x=np.zeros(L)
    for s0,d in [(0,.18),(.12,.22),(.3,.2)]:
        s=int(s0*SR); m=int(d*SR); tt=np.arange(m)/SR
        e=np.sin(np.pi*tt/d)**2 * (0.6+0.4*np.abs(lpf(rng.standard_normal(m),40,1))*30).clip(0,1.5)
        x[s:s+m]+=bp(rng.standard_normal(m),900,6500,2)*e
    return norm(x,0.7)
def sfx_stamp():
    L=int(0.45*SR); t=np.arange(L)/SR
    f=110*np.exp(-t*9)+45; ph=2*np.pi*np.cumsum(f)/SR
    thump=np.sin(ph)*np.exp(-t/0.07)
    slap=bp(rng.standard_normal(L),300,3500,2)*np.exp(-t/0.018)*0.8
    wood=np.sin(2*np.pi*230*t)*np.exp(-t/0.05)*0.25
    return norm(thump+slap+wood,0.85)
def sfx_unlock():
    L=int(0.7*SR); t=np.arange(L)/SR; x=np.zeros(L)
    for s0,f,a in [(0.0,3100,.5),(0.07,2600,.45),(0.18,1900,.35),(0.32,0,1)]:
        s=int(s0*SR); m=int(0.25*SR); tt=np.arange(m)/SR
        if f: x[s:s+m]+=(np.sin(2*np.pi*f*tt)*np.exp(-tt/0.012)+hpf(rng.standard_normal(m),3000,2)*np.exp(-tt/0.004))*a
        else: x[s:s+m]+=(np.sin(2*np.pi*95*tt)*np.exp(-tt/0.05)+bp(rng.standard_normal(m),200,1500,2)*np.exp(-tt/0.02)*0.5)*a
    return norm(x,0.8)
def sfx_wrong():
    L=int(0.6*SR); t=np.arange(L)/SR
    x=np.sin(2*np.pi*98*t)*np.exp(-t/0.12)*(t<0.3) + np.sin(2*np.pi*87.3*t)*np.exp(-(t-0.18).clip(0)/0.2)*(t>=0.18)*0.9
    x+=bp(rng.standard_normal(L),150,800,2)*np.exp(-t/0.03)*0.3
    return norm(x,0.6)
def sfx_reveal():  # przełom w przesłuchaniu: niski akcent + ciche „szszsz”
    L=int(1.6*SR); t=np.arange(L)/SR
    x=(np.sin(2*np.pi*73.4*t)+0.5*np.sin(2*np.pi*110*t)+0.3*np.sin(2*np.pi*146.8*t))*np.exp(-t/0.6)*(1-np.exp(-t/0.01))
    x+=bp(rng.standard_normal(L),2000,8000,2)*np.exp(-t/0.25)*0.25
    return norm(x,0.75)

def write(name,x,stereo=False,lufs=-20,br='96k'):
    import tempfile; wav=os.path.join(tempfile.gettempdir(), f'{name}.wav')
    import wave
    data=(np.clip(x,-1,1)*32767).astype('<i2')
    with wave.open(wav,'wb') as w:
        w.setnchannels(2 if stereo else 1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(data.tobytes())
    out=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','assets','audio',f'{name}.mp3')
    subprocess.run(['ffmpeg','-v','error','-y','-i',wav,'-af',f'loudnorm=I={lufs}:TP=-2:LRA=11','-ar','44100','-b:a',br,out],check=True)
    print(name, os.path.getsize(out)//1024,'KB')
import sys
which=sys.argv[1] if len(sys.argv)>1 else 'all'
if which in ('all','001'): write('case-001', ambience(), stereo=True, lufs=-24, br='112k')
if which in ('all','002'): write('case-002', train_ambience(), stereo=True, lufs=-24, br='112k')
if which in ('all','sfx'):
    for n,f in [('sfx-paper',sfx_paper),('sfx-stamp',sfx_stamp),('sfx-unlock',sfx_unlock),('sfx-wrong',sfx_wrong),('sfx-break',sfx_reveal)]:
        write(n,f(),lufs=-19,br='96k')
