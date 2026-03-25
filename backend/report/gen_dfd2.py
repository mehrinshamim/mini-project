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
C_SPECIAL  = '#E76F51'  # rate limit handler

def draw_proc(ax, x, y, w, h, label, color=C_PROCESS, fontsize=8.5,
              text_color='white', sublabel=None):
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle="round,pad=0.07,rounding_size=0.15",
                         facecolor=color, edgecolor='#333333', linewidth=1.4, zorder=3)
    ax.add_patch(box)
    if sublabel:
        ax.text(x + w/2, y + h/2 + 0.14, label,
                ha='center', va='center', fontsize=fontsize,
                fontweight='bold', color=text_color, zorder=4, multialignment='center')
        ax.text(x + w/2, y + h/2 - 0.17, sublabel,
                ha='center', va='center', fontsize=7,
                color=text_color, zorder=4, style='italic', multialignment='center')
    else:
        ax.text(x + w/2, y + h/2, label,
                ha='center', va='center', fontsize=fontsize,
                fontweight='bold', color=text_color, zorder=4, multialignment='center')

def draw_ext(ax, x, y, w, h, label, sublabel=None):
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle="round,pad=0.07,rounding_size=0.15",
                         facecolor=C_EXTERNAL, edgecolor='#333333', linewidth=1.4, zorder=3)
    ax.add_patch(box)
    if sublabel:
        ax.text(x + w/2, y + h/2 + 0.14, label,
                ha='center', va='center', fontsize=8.5,
                fontweight='bold', color='white', zorder=4, multialignment='center')
        ax.text(x + w/2, y + h/2 - 0.17, sublabel,
                ha='center', va='center', fontsize=7,
                color='white', zorder=4, style='italic', multialignment='center')
    else:
        ax.text(x + w/2, y + h/2, label,
                ha='center', va='center', fontsize=8.5,
                fontweight='bold', color='white', zorder=4, multialignment='center')

def draw_store(ax, x, y, w, h, label, sublabel=None):
    rect = FancyBboxPatch((x, y), w, h,
                          boxstyle="square,pad=0",
                          facecolor=C_STORAGE, edgecolor='none', zorder=2)
    ax.add_patch(rect)
    ax.plot([x, x+w], [y+h, y+h], color='#333333', lw=1.4, zorder=3)
    ax.plot([x, x+w], [y, y], color='#333333', lw=1.4, zorder=3)
    ax.plot([x, x], [y, y+h], color='#333333', lw=1.4, zorder=3)
    if sublabel:
        ax.text(x + w/2, y + h/2 + 0.12, label,
                ha='center', va='center', fontsize=8.5,
                fontweight='bold', color='#333333', zorder=4)
        ax.text(x + w/2, y + h/2 - 0.15, sublabel,
                ha='center', va='center', fontsize=7,
                color='#555555', zorder=4, style='italic')
    else:
        ax.text(x + w/2, y + h/2, label,
                ha='center', va='center', fontsize=8.5,
                fontweight='bold', color='#333333', zorder=4)

def arrow(ax, x1, y1, x2, y2, label='', color='#333333', lw=1.4, loff=(0,0),
          rad=0.0, bidirectional=False):
    style = '->' if not bidirectional else '<->'
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw,
                                connectionstyle=f'arc3,rad={rad}'), zorder=5)
    if label:
        mx = (x1+x2)/2 + loff[0]
        my = (y1+y2)/2 + loff[1]
        ax.text(mx, my, label, ha='center', va='center', fontsize=7.5,
                color='#111111', zorder=6,
                bbox=dict(boxstyle='round,pad=0.12', facecolor='white',
                          edgecolor='#BBBBBB', alpha=0.88))

# Title
ax.text(6, 8.65, 'Data Flow Diagram — Level 2',
        ha='center', fontsize=14, fontweight='bold', color='#222222')
ax.text(6, 8.25, 'P3: Job Scoring Process — Detailed Sub-processes',
        ha='center', fontsize=9.5, color='#555555')

# ---- External Entities ----
draw_ext(ax, 0.1, 4.2, 1.7, 0.85, 'Job Store\nTrigger',
         sublabel='(score batch API)')
draw_ext(ax, 10.2, 5.5, 1.7, 0.85, 'Groq API',
         sublabel='Llama 3.1-8b-instant')

# ---- Data Stores ----
draw_store(ax, 0.1, 1.2, 2.5, 0.7, 'D2: Job Store',
           sublabel='status, title, company, JD')
draw_store(ax, 0.1, 0.2, 2.5, 0.7, 'D1: Resume Store',
           sublabel='markdown_content')

# ---- Sub-processes ----
# P3.1: Fetch Pending Jobs
draw_proc(ax, 2.8, 7.2, 2.6, 0.85,
          'P3.1: Fetch\nPending Jobs',
          sublabel='status="pending" query')
# P3.2: Fetch Resume Markdown
draw_proc(ax, 2.8, 5.7, 2.6, 0.85,
          'P3.2: Fetch\nResume Markdown',
          sublabel='JOIN on user_id')
# P3.3: Truncate Inputs
draw_proc(ax, 2.8, 4.2, 2.6, 0.85,
          'P3.3: Truncate\nInputs',
          sublabel='resume[:6000], JD[:4000]')
# P3.4: Call Groq API
draw_proc(ax, 5.8, 5.7, 2.6, 0.85,
          'P3.4: Call\nGroq API',
          sublabel='chat.completions.create()')
# P3.5: Parse & Validate Response
draw_proc(ax, 5.8, 4.2, 2.6, 0.85,
          'P3.5: Parse &\nValidate Response',
          sublabel='Pydantic ScoringResult\n{score: int, reasoning: str}')
# P3.6: Update Job Record
draw_proc(ax, 5.8, 2.7, 2.6, 0.85,
          'P3.6: Update\nJob Record',
          sublabel='score, fit_reasoning\nstatus="scored"')
# P3.7: Rate Limit Handler
draw_proc(ax, 8.8, 4.2, 2.6, 0.85,
          'P3.7: Rate Limit\nHandler',
          color=C_SPECIAL,
          sublabel='_parse_retry_after()\nmax_retries=10')

# ---- Arrows ----

# Trigger → P3.1
arrow(ax, 1.8, 4.65, 2.8, 7.5, 'score_batch request\n(user_id)', color='#2E86AB',
      loff=(-0.7, 0.1))

# D2 → P3.1 (pending jobs)
arrow(ax, 2.6, 1.55, 3.3, 7.2, 'pending jobs\n(query DB)', color='#B8860B',
      loff=(-0.8, 0))

# D1 → P3.2 (resume markdown)
arrow(ax, 2.6, 0.55, 3.3, 5.7, 'markdown_content\n(user_id lookup)', color='#B8860B',
      loff=(-0.8, 0))

# P3.1 → P3.3 (job list)
arrow(ax, 4.1, 7.2, 4.1, 5.05, 'job list\n(id, title, JD)', color='#2E86AB',
      loff=(0.55, 0))

# P3.2 → P3.3 (resume_md)
arrow(ax, 4.1, 5.7, 4.1, 5.05, '', color='#2E86AB')

# P3.3 → P3.4 (truncated inputs)
arrow(ax, 5.4, 4.65, 5.8, 6.1, 'truncated_resume\n+ truncated_JD', color='#9B59B6',
      loff=(0.0, 0.22))

# P3.4 → Groq (request)
arrow(ax, 8.4, 6.1, 10.2, 6.0, 'chat completion\nrequest (JSON)', color='#9B59B6',
      loff=(0, 0.22))
# Groq → P3.4 (response)
arrow(ax, 10.2, 5.8, 8.4, 5.9, 'raw JSON\nresponse', color='#9B59B6',
      loff=(0, -0.22))

# P3.4 → P3.5 (raw response)
arrow(ax, 7.1, 5.7, 7.1, 5.05, 'raw LLM\noutput', color='#555555',
      loff=(0.5, 0))

# P3.5 → P3.6 (valid result)
arrow(ax, 7.1, 4.2, 7.1, 3.55, 'ScoringResult\n(score, reasoning)', color='#555555',
      loff=(0.6, 0))

# P3.5 → P3.7 (rate limit error)
arrow(ax, 8.4, 4.65, 8.8, 4.65, 'RateLimitError\n(exception)', color='#E76F51',
      loff=(0, 0.22))

# P3.7 → P3.4 (retry)
arrow(ax, 9.3, 5.05, 8.1, 5.55, 'retry after\nwait_seconds', color='#E76F51',
      rad=-0.3, loff=(0.4, 0.2))

# P3.6 → D2 (update)
arrow(ax, 6.4, 2.7, 2.6, 1.7, 'UPDATE job\n(score, status)', color='#B8860B',
      loff=(0, 0.22))

# P3.1 also returns count label
ax.text(3.0, 7.6, 'score_jobs_task\n(Celery Worker)',
        ha='center', fontsize=7.5, color='#666666',
        bbox=dict(boxstyle='round,pad=0.1', facecolor='#F0F0F0',
                  edgecolor='#CCCCCC', alpha=0.9))

# Legend
legend_elements = [
    mpatches.Patch(facecolor=C_PROCESS,  edgecolor='#333', label='Sub-process'),
    mpatches.Patch(facecolor=C_SPECIAL,  edgecolor='#333', label='Error Handler'),
    mpatches.Patch(facecolor=C_EXTERNAL, edgecolor='#333', label='External Entity'),
    mpatches.Patch(facecolor=C_STORAGE,  edgecolor='#333', label='Data Store'),
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=8.5,
          framealpha=0.9, bbox_to_anchor=(11.9, 0.0), ncol=2)

plt.tight_layout()
plt.savefig('/home/mehrin/repo/mini-project/backend/report/dfd2.png',
            dpi=100, bbox_inches='tight', facecolor='white')
print("dfd2.png saved")
