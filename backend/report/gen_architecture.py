import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(12, 9))
ax.set_xlim(0, 12)
ax.set_ylim(0, 9)
ax.axis('off')
ax.set_facecolor('white')
fig.patch.set_facecolor('white')

# Color scheme
C_CLIENT   = '#4A90D9'   # blue
C_API      = '#2E86AB'   # teal
C_SERVICE  = '#F4A261'   # orange
C_WORKER   = '#E76F51'   # red-orange
C_DATA     = '#F6C90E'   # yellow
C_EXTERNAL = '#57CC99'   # green
C_LAYER_BG = '#F8F9FA'   # light gray layer bg

def draw_box(ax, x, y, w, h, label, color, fontsize=9, text_color='white', sublabel=None, radius=0.15):
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle=f"round,pad=0.05,rounding_size={radius}",
                         facecolor=color, edgecolor='#333333', linewidth=1.2, zorder=3)
    ax.add_patch(box)
    if sublabel:
        ax.text(x + w/2, y + h/2 + 0.12, label,
                ha='center', va='center', fontsize=fontsize,
                fontweight='bold', color=text_color, zorder=4)
        ax.text(x + w/2, y + h/2 - 0.15, sublabel,
                ha='center', va='center', fontsize=7,
                color=text_color, zorder=4, style='italic')
    else:
        ax.text(x + w/2, y + h/2, label,
                ha='center', va='center', fontsize=fontsize,
                fontweight='bold', color=text_color, zorder=4, wrap=True,
                multialignment='center')

def draw_layer_bg(ax, y, h, label):
    rect = FancyBboxPatch((0.15, y), 11.7, h,
                          boxstyle="round,pad=0.05,rounding_size=0.1",
                          facecolor=C_LAYER_BG, edgecolor='#CCCCCC',
                          linewidth=0.8, zorder=1, linestyle='--')
    ax.add_patch(rect)
    ax.text(0.28, y + h/2, label, ha='left', va='center',
            fontsize=7.5, color='#666666', fontweight='bold',
            rotation=90, zorder=2)

def arrow(ax, x1, y1, x2, y2, label='', color='#555555'):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.5), zorder=5)
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx + 0.05, my, label, fontsize=7, color=color, zorder=6)

# --- Layer backgrounds ---
draw_layer_bg(ax, 7.8, 0.9,  'CLIENT')
draw_layer_bg(ax, 6.3, 1.2,  'API')
draw_layer_bg(ax, 4.6, 1.4,  'SERVICE')
draw_layer_bg(ax, 3.1, 1.2,  'WORKER')
draw_layer_bg(ax, 1.5, 1.3,  'DATA')
draw_layer_bg(ax, 0.1, 1.1,  'EXTERNAL')

# --- Title ---
ax.text(6, 8.85, 'Job Autofiller — System Architecture',
        ha='center', va='center', fontsize=14, fontweight='bold', color='#222222')

# --- CLIENT LAYER (y=7.8) ---
draw_box(ax, 1.0, 7.9, 2.8, 0.65, 'Chrome Extension', C_CLIENT, fontsize=9,
         sublabel='(Browser Client)')
draw_box(ax, 4.5, 7.9, 2.8, 0.65, 'User / Frontend', C_CLIENT, fontsize=9,
         sublabel='(REST API calls)')
draw_box(ax, 8.2, 7.9, 2.8, 0.65, 'WebSocket Client', C_CLIENT, fontsize=9,
         sublabel='(Streaming answers)')

# --- API LAYER (y=6.3) ---
draw_box(ax, 0.5,  6.45, 2.2, 0.7, 'resumes.py', C_API, fontsize=8.5,
         sublabel='POST /resumes/upload')
draw_box(ax, 2.9,  6.45, 2.2, 0.7, 'jobs.py', C_API, fontsize=8.5,
         sublabel='POST /jobs/discover\nGET /jobs/')
draw_box(ax, 5.3,  6.45, 2.4, 0.7, 'extension_rest.py', C_API, fontsize=8.5,
         sublabel='POST /extension/answers')
draw_box(ax, 7.9,  6.45, 2.4, 0.7, 'extension_ws.py', C_API, fontsize=8.5,
         sublabel='WS /extension/ws/{id}')

# FastAPI label
ax.text(6, 6.25, 'FastAPI Application (app/main.py)',
        ha='center', va='center', fontsize=8, color='#2E86AB', fontweight='bold')

# --- SERVICE LAYER (y=4.6) ---
draw_box(ax, 0.4,  4.75, 2.3, 0.85, 'ParsingService', C_SERVICE, fontsize=8.5,
         sublabel='Docling\nPDF → Markdown')
draw_box(ax, 2.9,  4.75, 2.3, 0.85, 'DiscoveryService', C_SERVICE, fontsize=8.5,
         sublabel='Apify Actor\nLinkedIn scrape')
draw_box(ax, 5.4,  4.75, 2.5, 0.85, 'ReasoningService', C_SERVICE, fontsize=8.5,
         sublabel='Groq Llama 3.1-8b\nJob scoring 1-10')
draw_box(ax, 8.1,  4.75, 2.8, 0.85, 'ExtensionService', C_SERVICE, fontsize=8.5,
         sublabel='Groq Llama 3.3-70b\nAnswer generation')

# --- WORKER LAYER (y=3.1) ---
draw_box(ax, 0.4,  3.25, 2.5, 0.75, 'parse_resume_task', C_WORKER, fontsize=8.5,
         sublabel='Celery async')
draw_box(ax, 3.2,  3.25, 2.5, 0.75, 'discover_jobs_task', C_WORKER, fontsize=8.5,
         sublabel='Celery async')
draw_box(ax, 6.0,  3.25, 2.5, 0.75, 'score_jobs_task', C_WORKER, fontsize=8.5,
         sublabel='Celery, max_retries=10')
draw_box(ax, 8.7,  3.25, 2.4, 0.75, 'Celery App', C_WORKER, fontsize=8.5,
         sublabel='Redis broker/backend')

# --- DATA LAYER (y=1.5) ---
draw_box(ax, 0.8,  1.65, 4.0, 0.85, 'PostgreSQL', C_DATA, fontsize=9,
         text_color='#333333',
         sublabel='User · Resume · Job · JobSearch · JobSearchResult')
draw_box(ax, 5.5,  1.65, 3.5, 0.85, 'Redis', C_DATA, fontsize=9,
         text_color='#333333',
         sublabel='Celery broker & result backend')

# --- EXTERNAL LAYER (y=0.1) ---
draw_box(ax, 0.5,  0.22, 3.0, 0.7, 'Groq API', C_EXTERNAL, fontsize=9,
         sublabel='Llama 3.1-8b + Llama 3.3-70b')
draw_box(ax, 5.0,  0.22, 3.2, 0.7, 'Apify / LinkedIn', C_EXTERNAL, fontsize=9,
         sublabel='curious_coder/linkedin-jobs-scraper')
draw_box(ax, 8.5,  0.22, 2.8, 0.7, 'Docling', C_EXTERNAL, fontsize=9,
         sublabel='PDF → Markdown OCR')

# --- ARROWS (representative flows) ---
# Client -> API
arrow(ax, 2.4, 7.9, 1.6, 7.15, color='#2E86AB')
arrow(ax, 5.9, 7.9, 4.0, 7.15, color='#2E86AB')
arrow(ax, 9.6, 7.9, 8.9, 7.15, color='#2E86AB')

# API -> Services
arrow(ax, 1.6, 6.45, 1.5, 5.6, color='#F4A261')
arrow(ax, 4.0, 6.45, 4.0, 5.6, color='#F4A261')
arrow(ax, 6.5, 6.45, 6.65, 5.6, color='#F4A261')
arrow(ax, 9.1, 6.45, 9.5, 5.6, color='#F4A261')

# Services -> Workers
arrow(ax, 1.5, 4.75, 1.65, 4.0, color='#E76F51')
arrow(ax, 4.0, 4.75, 4.45, 4.0, color='#E76F51')
arrow(ax, 6.65, 4.75, 7.25, 4.0, color='#E76F51')

# Workers -> Data
arrow(ax, 1.65, 3.25, 2.0, 2.5, color='#999900')
arrow(ax, 4.45, 3.25, 3.5, 2.5, color='#999900')
arrow(ax, 7.25, 3.25, 4.5, 2.5, color='#999900')
arrow(ax, 9.9, 3.25, 7.0, 2.5, color='#999900')

# Services -> External
arrow(ax, 6.65, 4.75, 2.0, 0.92, color='#57CC99')
arrow(ax, 4.0,  4.75, 6.3, 0.92, color='#57CC99')
arrow(ax, 1.5,  4.75, 9.9, 0.92, color='#57CC99')

# Legend
legend_elements = [
    mpatches.Patch(facecolor=C_CLIENT,   edgecolor='#333', label='Client'),
    mpatches.Patch(facecolor=C_API,      edgecolor='#333', label='API Router'),
    mpatches.Patch(facecolor=C_SERVICE,  edgecolor='#333', label='Service'),
    mpatches.Patch(facecolor=C_WORKER,   edgecolor='#333', label='Celery Task'),
    mpatches.Patch(facecolor=C_DATA,     edgecolor='#333', label='Data Store'),
    mpatches.Patch(facecolor=C_EXTERNAL, edgecolor='#333', label='External'),
]
ax.legend(handles=legend_elements, loc='lower right',
          fontsize=8, framealpha=0.9, ncol=3,
          bbox_to_anchor=(11.9, 0.0))

plt.tight_layout()
plt.savefig('/home/mehrin/repo/mini-project/backend/report/architecture.png',
            dpi=100, bbox_inches='tight', facecolor='white')
print("architecture.png saved")
