import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Ellipse
import matplotlib.patheffects as pe

fig, ax = plt.subplots(figsize=(12, 9))
ax.set_xlim(0, 12)
ax.set_ylim(0, 9)
ax.axis('off')
ax.set_facecolor('white')
fig.patch.set_facecolor('white')

C_PROCESS  = '#2E86AB'
C_EXTERNAL = '#57CC99'
C_STORAGE  = '#F6C90E'

def draw_rect(ax, x, y, w, h, label, color, fontsize=10, text_color='white', sublabel=None):
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle="round,pad=0.1,rounding_size=0.2",
                         facecolor=color, edgecolor='#333333', linewidth=1.5, zorder=3)
    ax.add_patch(box)
    if sublabel:
        ax.text(x + w/2, y + h/2 + 0.18, label,
                ha='center', va='center', fontsize=fontsize,
                fontweight='bold', color=text_color, zorder=4)
        ax.text(x + w/2, y + h/2 - 0.22, sublabel,
                ha='center', va='center', fontsize=8,
                color=text_color, zorder=4, style='italic', multialignment='center')
    else:
        ax.text(x + w/2, y + h/2, label,
                ha='center', va='center', fontsize=fontsize,
                fontweight='bold', color=text_color, zorder=4, multialignment='center')

def draw_circle(ax, cx, cy, r, label, color, fontsize=10, text_color='white', sublabel=None):
    circle = plt.Circle((cx, cy), r, facecolor=color, edgecolor='#333333',
                         linewidth=2, zorder=3)
    ax.add_patch(circle)
    if sublabel:
        ax.text(cx, cy + 0.2, label, ha='center', va='center', fontsize=fontsize,
                fontweight='bold', color=text_color, zorder=4, multialignment='center')
        ax.text(cx, cy - 0.3, sublabel, ha='center', va='center', fontsize=8,
                color=text_color, zorder=4, style='italic', multialignment='center')
    else:
        ax.text(cx, cy, label, ha='center', va='center', fontsize=fontsize,
                fontweight='bold', color=text_color, zorder=4, multialignment='center')

def labeled_arrow(ax, x1, y1, x2, y2, label, color='#333333', lw=1.5, label_offset=(0,0)):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw,
                                connectionstyle='arc3,rad=0.0'), zorder=5)
    mx = (x1 + x2) / 2 + label_offset[0]
    my = (y1 + y2) / 2 + label_offset[1]
    ax.text(mx, my, label, ha='center', va='center', fontsize=8,
            color='#222222', zorder=6,
            bbox=dict(boxstyle='round,pad=0.15', facecolor='white',
                      edgecolor='#CCCCCC', alpha=0.85))

# Title
ax.text(6, 8.6, 'Data Flow Diagram — Level 0 (Context Diagram)',
        ha='center', va='center', fontsize=14, fontweight='bold', color='#222222')
ax.text(6, 8.2, 'Job Autofiller System',
        ha='center', va='center', fontsize=10, color='#555555')

# Central process
draw_circle(ax, 6.0, 4.5, 1.55, 'Job Autofiller\nSystem', C_PROCESS,
            fontsize=11, sublabel='(FastAPI + Celery\n+ Groq + Apify)')

# External entities
# User (left)
draw_rect(ax, 0.3, 3.9, 2.2, 1.2, 'User', C_EXTERNAL, fontsize=11,
          sublabel='(Job Seeker)')
# Chrome Extension (right)
draw_rect(ax, 9.5, 3.9, 2.2, 1.2, 'Chrome\nExtension', C_EXTERNAL, fontsize=10,
          sublabel='(Browser Client)')
# Groq API (top right)
draw_rect(ax, 8.2, 6.8, 2.8, 1.0, 'Groq API', C_EXTERNAL, fontsize=10,
          sublabel='Llama 3.1-8b + 3.3-70b')
# Apify / LinkedIn (top left)
draw_rect(ax, 0.9, 6.8, 2.8, 1.0, 'Apify / LinkedIn', C_EXTERNAL, fontsize=10,
          sublabel='Job listings source')
# PostgreSQL (bottom)
draw_rect(ax, 4.0, 0.4, 4.0, 1.0, 'PostgreSQL Database', C_STORAGE,
          fontsize=10, text_color='#333333',
          sublabel='Persistent data store')

# --- Arrows ---

# User -> System
labeled_arrow(ax, 2.5, 4.7, 4.45, 4.7, 'Resume PDF upload',
              color='#2E86AB', label_offset=(0, 0.22))
labeled_arrow(ax, 2.5, 4.3, 4.45, 4.3, 'Job search params',
              color='#2E86AB', label_offset=(0, -0.22))
# System -> User
labeled_arrow(ax, 4.45, 4.5, 2.5, 4.5, 'Ranked job list\n(scores + reasoning)',
              color='#57CC99', label_offset=(0, 0))

# Chrome Extension -> System
labeled_arrow(ax, 9.5, 4.7, 7.55, 4.7, 'Scraped questions\n+ Job context',
              color='#E76F51', label_offset=(0, 0.28))
# System -> Chrome Extension
labeled_arrow(ax, 7.55, 4.3, 9.5, 4.3, 'AI-generated answers\n(WebSocket stream)',
              color='#E76F51', label_offset=(0, -0.28))

# Groq API -> System
labeled_arrow(ax, 8.8, 6.8, 7.1, 5.85, 'Scoring result\n(score, reasoning)',
              color='#9B59B6', label_offset=(0.5, 0.1))
# System -> Groq API
labeled_arrow(ax, 7.1, 5.75, 8.8, 6.85, 'Resume + JD\n(truncated inputs)',
              color='#9B59B6', label_offset=(-0.5, -0.1))

# Apify -> System
labeled_arrow(ax, 3.3, 6.8, 5.0, 5.85, 'Job postings\n(title, company, JD)',
              color='#1A7A4A', label_offset=(-0.5, 0.1))
# System -> Apify
labeled_arrow(ax, 5.0, 5.75, 3.3, 6.85, 'Search query\n(title, location)',
              color='#1A7A4A', label_offset=(0.5, -0.1))

# PostgreSQL -> System
labeled_arrow(ax, 5.5, 1.4, 5.2, 2.95, 'Stored resume,\njobs, scores',
              color='#B8860B', label_offset=(-0.8, 0))
# System -> PostgreSQL
labeled_arrow(ax, 6.5, 2.95, 6.5, 1.4, 'Persist resume,\njobs, scores',
              color='#B8860B', label_offset=(0.8, 0))

# Legend
legend_elements = [
    mpatches.Patch(facecolor=C_PROCESS,  edgecolor='#333', label='Process'),
    mpatches.Patch(facecolor=C_EXTERNAL, edgecolor='#333', label='External Entity'),
    mpatches.Patch(facecolor=C_STORAGE,  edgecolor='#333', label='Data Store'),
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=9,
          framealpha=0.9, bbox_to_anchor=(11.9, 0.0))

plt.tight_layout()
plt.savefig('/home/mehrin/repo/mini-project/backend/report/dfd0.png',
            dpi=100, bbox_inches='tight', facecolor='white')
print("dfd0.png saved")
