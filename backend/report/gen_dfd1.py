import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(12, 9))
ax.set_xlim(0, 12)
ax.set_ylim(0, 9)
ax.axis('off')
ax.set_facecolor('white')
fig.patch.set_facecolor('white')

C_PROCESS  = '#2E86AB'
C_EXTERNAL = '#57CC99'
C_STORAGE  = '#F6C90E'

def draw_rect(ax, x, y, w, h, label, color, fontsize=9.5, text_color='white',
              sublabel=None, radius=0.15):
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle=f"round,pad=0.05,rounding_size={radius}",
                         facecolor=color, edgecolor='#333333', linewidth=1.4, zorder=3)
    ax.add_patch(box)
    if sublabel:
        ax.text(x + w/2, y + h/2 + 0.15, label,
                ha='center', va='center', fontsize=fontsize,
                fontweight='bold', color=text_color, zorder=4, multialignment='center')
        ax.text(x + w/2, y + h/2 - 0.18, sublabel,
                ha='center', va='center', fontsize=7.5,
                color=text_color, zorder=4, style='italic', multialignment='center')
    else:
        ax.text(x + w/2, y + h/2, label,
                ha='center', va='center', fontsize=fontsize,
                fontweight='bold', color=text_color, zorder=4, multialignment='center')

def draw_datastore(ax, x, y, w, h, label, sublabel=None):
    # Open-ended rectangle (data store notation)
    ax.plot([x, x+w], [y+h, y+h], color='#333333', lw=1.4, zorder=3)
    ax.plot([x, x+w], [y, y], color='#333333', lw=1.4, zorder=3)
    ax.plot([x, x], [y, y+h], color='#333333', lw=1.4, zorder=3)
    rect = FancyBboxPatch((x, y), w, h,
                          boxstyle="square,pad=0",
                          facecolor=C_STORAGE, edgecolor='none', zorder=2)
    ax.add_patch(rect)
    if sublabel:
        ax.text(x + w/2, y + h/2 + 0.12, label,
                ha='center', va='center', fontsize=9,
                fontweight='bold', color='#333333', zorder=4)
        ax.text(x + w/2, y + h/2 - 0.15, sublabel,
                ha='center', va='center', fontsize=7.5,
                color='#555555', zorder=4, style='italic')
    else:
        ax.text(x + w/2, y + h/2, label,
                ha='center', va='center', fontsize=9,
                fontweight='bold', color='#333333', zorder=4)

def arrow(ax, x1, y1, x2, y2, label='', color='#333333', rad=0.0, lw=1.4,
          loff=(0, 0)):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw,
                                connectionstyle=f'arc3,rad={rad}'), zorder=5)
    if label:
        mx = (x1+x2)/2 + loff[0]
        my = (y1+y2)/2 + loff[1]
        ax.text(mx, my, label, ha='center', va='center', fontsize=7.5,
                color='#222222', zorder=6,
                bbox=dict(boxstyle='round,pad=0.12', facecolor='white',
                          edgecolor='#CCCCCC', alpha=0.85))

# Title
ax.text(6, 8.65, 'Data Flow Diagram — Level 1 (Main Processes)',
        ha='center', fontsize=14, fontweight='bold', color='#222222')
ax.text(6, 8.25, 'Job Autofiller System — Expanded into 4 processes',
        ha='center', fontsize=9, color='#555555')

# --- External Entities ---
draw_rect(ax, 0.1, 6.5, 1.8, 1.0, 'User', C_EXTERNAL, fontsize=10)
draw_rect(ax, 0.1, 3.8, 1.8, 1.0, 'Chrome\nExtension', C_EXTERNAL, fontsize=9)
draw_rect(ax, 0.1, 1.5, 1.8, 1.0, 'Apify\nLinkedIn', C_EXTERNAL, fontsize=9)
draw_rect(ax, 10.0, 4.5, 1.8, 1.0, 'Groq API', C_EXTERNAL, fontsize=9)

# --- Processes ---
# P1: Resume Processing
draw_rect(ax, 3.0, 6.5, 2.8, 1.0, 'P1: Resume\nProcessing',
          C_PROCESS, fontsize=9, sublabel='Docling PDF→Markdown')
# P2: Job Discovery
draw_rect(ax, 3.0, 3.8, 2.8, 1.0, 'P2: Job\nDiscovery',
          C_PROCESS, fontsize=9, sublabel='Apify LinkedIn scraper')
# P3: Job Scoring
draw_rect(ax, 7.0, 6.5, 2.8, 1.0, 'P3: Job\nScoring',
          C_PROCESS, fontsize=9, sublabel='Groq Llama 3.1-8b-instant')
# P4: Answer Generation
draw_rect(ax, 7.0, 3.8, 2.8, 1.0, 'P4: Answer\nGeneration',
          C_PROCESS, fontsize=9, sublabel='Groq Llama 3.3-70b-versatile')

# --- Data Stores ---
draw_datastore(ax, 3.8, 1.5, 2.2, 0.7, 'D1: Resume Store',
               sublabel='resume.markdown_content')
draw_datastore(ax, 6.6, 1.5, 2.2, 0.7, 'D2: Job Store',
               sublabel='jobs, scores, status')

# --- Flows ---

# User → P1 (PDF upload)
arrow(ax, 1.9, 7.1, 3.0, 7.1, 'PDF bytes\n(resume upload)', color='#2E86AB',
      loff=(0, 0.22))
# P1 → D1 (store markdown)
arrow(ax, 4.4, 6.5, 4.5, 2.2, 'Markdown content', color='#F4A261',
      loff=(-0.7, 0))
# User → P3 (trigger scoring)
arrow(ax, 1.9, 6.9, 7.0, 7.0, 'Job IDs\n(score batch request)', color='#2E86AB',
      loff=(0, 0.25))
# P3 → User (ranked jobs)
arrow(ax, 7.0, 6.8, 1.9, 6.8, 'Scored jobs\n(ranked list)', color='#57CC99',
      loff=(0, -0.28))
# D1 → P3 (resume for scoring)
arrow(ax, 4.8, 2.15, 8.4, 6.5, 'resume_markdown\n(for scoring)', color='#B8860B',
      loff=(0.7, 0))
# D2 → P3 (pending jobs)
arrow(ax, 7.2, 2.2, 7.6, 6.5, 'pending jobs\n(title, JD)', color='#B8860B',
      loff=(1.0, 0))
# P3 → Groq (scoring request)
arrow(ax, 9.8, 7.0, 10.0, 5.0, 'resume + JD\n(truncated)', color='#9B59B6',
      loff=(0.6, 0))
# Groq → P3 (scoring result)
arrow(ax, 10.0, 4.8, 9.8, 6.8, 'score 1-10\n+ fit_reasoning', color='#9B59B6',
      loff=(-0.6, 0))
# P3 → D2 (save scores)
arrow(ax, 8.4, 6.5, 8.0, 2.2, 'score, reasoning\nstatus=scored', color='#F4A261',
      loff=(0.8, 0))

# User → P2 (job search trigger)
arrow(ax, 1.9, 4.3, 3.0, 4.3, 'title, location\n(search params)', color='#2E86AB',
      loff=(0, 0.22))
# Apify → P2 (job listings)
arrow(ax, 1.9, 2.0, 3.0, 4.0, 'Job listings\n(raw JSON)', color='#1A7A4A',
      loff=(-0.4, 0))
# P2 → Apify (scrape request)
arrow(ax, 3.0, 3.9, 1.9, 2.1, 'Actor run\n(title, location)', color='#1A7A4A',
      loff=(0.5, 0))
# P2 → D2 (save jobs)
arrow(ax, 5.8, 4.3, 6.6, 2.0, 'Job records\n(title, company, JD)', color='#F4A261',
      loff=(0.7, 0))

# Chrome Extension → P4 (questions)
arrow(ax, 1.9, 4.1, 7.0, 4.1, 'Scraped questions\n+ job context', color='#E76F51',
      loff=(0, 0.25))
# D1 → P4 (resume for answers)
arrow(ax, 4.5, 1.8, 7.5, 3.8, 'resume_markdown\n(full, no truncation)', color='#B8860B',
      loff=(0, -0.25))
# P4 → Groq (answer request)
arrow(ax, 9.8, 4.3, 10.0, 4.9, 'question + resume\n+ JD', color='#9B59B6',
      loff=(0.65, 0))
# Groq → P4 (answer)
arrow(ax, 10.0, 5.1, 9.8, 4.5, 'Generated answer\n(text)', color='#9B59B6',
      loff=(-0.65, 0))
# P4 → Chrome Extension (stream)
arrow(ax, 7.0, 4.0, 1.9, 4.0, 'Answers streamed\n(WebSocket)', color='#E76F51',
      loff=(0, -0.25))

# Legend
legend_elements = [
    mpatches.Patch(facecolor=C_PROCESS,  edgecolor='#333', label='Process'),
    mpatches.Patch(facecolor=C_EXTERNAL, edgecolor='#333', label='External Entity'),
    mpatches.Patch(facecolor=C_STORAGE,  edgecolor='#333', label='Data Store'),
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=9,
          framealpha=0.9, bbox_to_anchor=(11.9, 0.0))

plt.tight_layout()
plt.savefig('/home/mehrin/repo/mini-project/backend/report/dfd1.png',
            dpi=100, bbox_inches='tight', facecolor='white')
print("dfd1.png saved")
