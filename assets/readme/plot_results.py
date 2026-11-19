"""Render the README figure with matplotlib: python assets/readme/plot_results.py."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Patch

ROOT = Path(__file__).resolve().parent
rows = json.loads((ROOT / 'results.json').read_text())
PAPER, INK, OLIVE = '#fcfaf1', '#343629', '#606f2e'
colors = ['#d6cbb3', '#aab99b', OLIVE]
labels = ['Base', 'Vanilla SFT', 'AutoMaster']
plt.rcParams.update({'font.family':'DejaVu Sans', 'svg.fonttype':'none'})
fig = plt.figure(figsize=(14.4, 6.0), facecolor=PAPER)
fig.text(.045,.91,'Same teacher. Better demonstrations.',
         fontfamily='DejaVu Serif', fontsize=24, color=INK)
fig.legend(handles=[Patch(facecolor=c,label=l) for c,l in zip(colors,labels)],
           loc='upper left',bbox_to_anchor=(.04,.86),ncol=3,frameon=False,
           fontsize=12,labelcolor=INK,handlelength=1.1,columnspacing=2)
for index, domain in enumerate(dict.fromkeys(r['domain'] for r in rows)):
    left=.035+index*.323
    card=FancyBboxPatch((left,.065),.307,.68,
                       boxstyle='round,pad=0.006,rounding_size=0.018',
                       transform=fig.transFigure,facecolor='#fffef9',
                       edgecolor='#dedfcf',linewidth=1,zorder=-1)
    fig.add_artist(card)
    fig.text(left+.018,.69,domain,fontfamily='DejaVu Serif',fontsize=17,color=INK)
    ax=fig.add_axes([left+.018,.10,.273,.53],facecolor='none')
    ax.set_xlim(0,74); ax.set_ylim(-.45,7.2); ax.axis('off')
    selected=[r for r in rows if r['domain']==domain]
    for i,row in enumerate(selected):
        top=6.65-i*3.75
        ax.text(0,top,row['student'],fontsize=12,weight='bold',color=INK)
        for j,label in enumerate(labels):
            y=top-.65-j*.70
            mean,sd=row[label]['mean'],row[label]['sd']
            ax.add_patch(FancyBboxPatch((0,y-.19),60,.38,
                         boxstyle='round,pad=0,rounding_size=.16',
                         facecolor='#f3f1e7',linewidth=0))
            ax.add_patch(FancyBboxPatch((0,y-.19),mean,.38,
                         boxstyle='round,pad=0,rounding_size=.16',
                         facecolor=colors[j],linewidth=0))
            ax.errorbar(mean,y,xerr=sd,fmt='none',ecolor='#555e40',
                        elinewidth=1,capsize=3,capthick=1)
            ax.text(73,y,f'{mean:.2f}',ha='right',va='center',fontsize=12,
                    color=OLIVE if j==2 else '#656651',
                    weight='bold' if j==2 else 'normal')
fig.savefig(ROOT/'results.svg',facecolor=PAPER)
svg = ROOT / 'results.svg'
svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines()) + '\n')
fig.savefig(ROOT/'results.png',facecolor=PAPER,dpi=180)
plt.close(fig)
