import re, glob, csv, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
R='results/corners'; IMG='images/corners'; import os; os.makedirs(IMG, exist_ok=True)
def parse(f):
    s=open(f).read(); g=lambda p: float(re.search(p,s).group(1))
    return dict(sndr=g(r'SNDR ([\d.]+)'), enob=g(r'ENOB ([\d.]+)'), sfdr=g(r'SFDR ([\d.]+)'), thd=g(r'THD (-?[\d.]+)'),
                tmax=g(r'conversion time max ([\d.]+)'), win=g(r'available ([\d.]+)'), power=g(r'= ([\d.]+) uW'),
                tvalid=(g(r'data valid max ([\d.]+)') if 'data valid' in s else float('nan')))
F=[('tt 27°C 1.8V','fft_tt_27_1.8'),('tt -40°C','fft_tt_-40_1.8'),('tt 125°C','fft_tt_125_1.8'),('fs 27°C','fft_fs_27_1.8'),
   ('sf 27°C','fft_sf_27_1.8'),('ff -40°C 1.98V','fft_ff_-40_1.98'),('ss 125°C 1.62V','ss25b')]
D=[(n,parse('%s/%s/result.txt'%(R,d)),d) for n,d in F]
rows=['| Corner | SNDR | ENOB | SFDR | THD | Worst conversion | Output bits valid | Power |','|---|---|---|---|---|---|---|---|']
for n,d,_ in D: rows.append('| %s | %.1f dB | %.2f | %.1f dB | %.1f dB | %.2f ns | %.2f ns | %.0f µW |'%(n,d['sndr'],d['enob'],d['sfdr'],d['thd'],d['tmax'],d['tvalid'],d['power']))
open('/tmp/fft_table.md','w').write('\n'.join(rows)+'\n')
x=np.arange(len(D)); fig,ax=plt.subplots(1,2,figsize=(13,4))
c=['#2b7bba' if d['enob']>=9 else '#d9534f' for _,d,_ in D]
ax[0].bar(x,[d['enob'] for _,d,_ in D],color=c); ax[0].axhline(9.0,ls='--',c='gray',lw=1); ax[0].set_ylim(7,10)
ax[0].set_ylabel('ENOB (bit)'); ax[0].set_title('ENOB per corner (red: below 9 bit)')
ax[1].bar(x,[d['sfdr'] for _,d,_ in D],color=c); ax[1].set_ylim(50,72); ax[1].set_ylabel('SFDR (dB)'); ax[1].set_title('SFDR per corner')
for a in ax: a.set_xticks(x); a.set_xticklabels([n for n,_,_ in D],rotation=30,ha='right',fontsize=9); a.grid(axis='y',alpha=.3)
fig.suptitle('v11a post-layout, 25 MS/s, fin 5.08 MHz, 64-point FFT'); fig.tight_layout(); fig.savefig(IMG+'/fft_enob_sfdr.png',dpi=110)
# spectra
fig,axs=plt.subplots(2,4,figsize=(16,6.5),sharey=True); axs=axs.ravel()
for a,(n,d,dd) in zip(axs,D):
    cd=np.loadtxt('%s/%s/codes.txt'%(R,dd))[:,0]; xx=cd-cd.mean(); X=np.abs(np.fft.rfft(xx))/(len(xx)/2)/512; X[0]=1e-12
    a.stem(np.arange(len(X))*25/64,20*np.log10(np.maximum(X,1e-7)),bottom=-120,basefmt=' ',markerfmt='.')
    a.set_ylim(-110,5); a.set_title('%s: ENOB %.2f, SFDR %.1f dB'%(n,d['enob'],d['sfdr']),fontsize=9); a.grid(alpha=.3)
axs[-1].axis('off'); [axs[i].set_xlabel('MHz') for i in range(4,7)]; axs[0].set_ylabel('dBFS'); axs[4].set_ylabel('dBFS')
fig.suptitle('v11a post-layout FFT spectra across corners (25 MS/s)'); fig.tight_layout(); fig.savefig(IMG+'/fft_spectra.png',dpi=100)
# PVT
P=[]
for f in sorted(glob.glob(R+'/pvt/result_*.csv')):
    t=open(f).read().strip().split(','); P.append(t)
order={'tt':0,'ss':1,'ff':2,'fs':3,'sf':4}
P.sort(key=lambda t:(order[t[0]],float(t[1]),float(t[2])))
lab=['%s %s°C %sV'%(t[0],t[1],t[2]) for t in P]; inl=np.array([float(t[4]) for t in P]); tc=np.array([float(t[6]) for t in P]); tv=np.array([float(t[7]) for t in P])
pw=np.array([float(t[8])+float(t[9]) for t in P]); miss=np.array([int(t[10]) for t in P])
rows=['| Corner | Worst nonlinearity | rms | Worst conversion | Output bits valid | Power | Unfinished |','|---|---|---|---|---|---|---|']
for t in P: rows.append('| %s %s °C %s V | %s LSB | %s LSB | %s ns | %s ns | %.0f µW | %s |'%(t[0],t[1],t[2],t[4] if int(t[10])==0 else '**%s (failed)**'%t[4],t[5],t[6],t[7],float(t[8])+float(t[9]),t[10] if int(t[10])==0 else '**%s of 8**'%t[10]))
open('/tmp/pvt_table.md','w').write('\n'.join(rows)+'\n')
x=np.arange(len(P)); fig,ax=plt.subplots(3,1,figsize=(13,9),sharex=True)
ok=miss==0
ax[0].bar(x[ok],inl[ok],color='#2b7bba'); ax[0].bar(x[~ok],np.minimum(inl[~ok],0.5),color='#d9534f'); ax[0].set_ylim(0,0.5); ax[0].set_ylabel('worst nonlinearity (LSB)')
for i in np.where(~ok)[0]: ax[0].text(i,0.42,'FAIL\n%d of 8\nunfinished'%miss[i],ha='center',fontsize=8,color='#d9534f')
ax[1].bar(x-0.2,tc,0.4,label='EOC (conversion done)'); ax[1].bar(x+0.2,tv,0.4,label='output bits valid'); ax[1].axhline(34,c='r',ls='--',lw=1,label='34 ns window (25 MS/s, 6 ns sampling)')
ax[1].set_ylabel('ns'); ax[1].legend(fontsize=8,loc='upper right')
ax[2].bar(x,pw,color='#5cb85c'); ax[2].set_ylabel('power (µW)')
ax[2].set_xticks(x); ax[2].set_xticklabels(lab,rotation=40,ha='right',fontsize=8)
for a in ax: a.grid(axis='y',alpha=.3)
fig.suptitle('v11a post-layout PVT sweep: 19 corners, 8 DC inputs each, 25 MS/s'); fig.tight_layout(); fig.savefig(IMG+'/pvt_sweep.png',dpi=100)
# static linearity
L=[l.split() for l in open(R+'/lin_tt/result.txt') if re.match(r'\s*-?\d+\.\d+\s+\d+\s',l)]
vd=np.array([float(l[0]) for l in L]); err=np.array([float(l[3]) for l in L])
fig,ax=plt.subplots(figsize=(8,3.6)); ax.plot(vd,err,'.-',lw=.8); ax.axhline(0,c='gray',lw=.6)
ax.set_xlabel('differential input (V)'); ax.set_ylabel('error (LSB)'); ax.set_ylim(-0.5,0.5); ax.grid(alpha=.3)
ax.set_title('Static nonlinearity, tt 25 MS/s, 120 DC inputs (quantisation removed): max %.2f LSB, rms %.2f LSB'%(abs(err).max(),err.std()),fontsize=9)
fig.tight_layout(); fig.savefig(IMG+'/static_nonlinearity.png',dpi=110)
# model INL/DNL from extracted CDAC weights
bw=[r for r in csv.reader(open('results/bitweights.csv')) if r and r[0].isdigit()]
err_k={int(r[0]):float(r[6])/100 for r in bw}
W=np.array([2.0**(10-k)*(1+err_k.get(k,0)) for k in range(1,10)]+[1.0])
codes=np.arange(1024); V=np.array([sum(W[k] for k in range(10) if (c>>(9-k))&1) for c in codes])
lsb=(V[-1]-V[0])/1023; dnl=np.diff(V)/lsb-1; pf=np.polyfit(codes,V,1); inl=(V-np.polyval(pf,codes))/pf[0]   # best-fit-line INL, comparable with the simulated sweep
fig,ax=plt.subplots(2,1,figsize=(10,5.5),sharex=True)
ax[0].plot(codes[1:],dnl,lw=.7); ax[0].set_ylabel('DNL (LSB)'); ax[0].set_title('Model DNL/INL from extracted CDAC bit weights (P side; excludes comparator offset and noise): DNL %.3f/+%.3f, best-fit INL ±%.3f LSB'%(dnl.min(),dnl.max(),abs(inl).max()),fontsize=9)
ax[1].plot(codes,inl,lw=.7); ax[1].set_ylabel('INL (LSB)'); ax[1].set_xlabel('code')
for a in ax: a.grid(alpha=.3)
fig.tight_layout(); fig.savefig(IMG+'/model_inl_dnl.png',dpi=110)
print('model DNL %.3f %.3f INL %.3f'%(dnl.min(),dnl.max(),abs(inl).max()))
print('lin points',len(vd))
