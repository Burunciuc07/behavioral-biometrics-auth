"""
Eye Aspect Ratio (EAR) Diagram Generator
Generates a technical diagram showing the EAR calculation for blink detection
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch
import matplotlib.patches as mpatches

def draw_eye(ax, center_x, center_y, width, height, title, ear_value, is_closed=False):
    """
    Draw an eye with facial landmarks
    
    Parameters:
    - center_x, center_y: Center position of the eye
    - width, height: Dimensions of the eye
    - title: Title for this eye state
    - ear_value: EAR value to display
    - is_closed: Whether to draw a closed eye
    """
    
    if is_closed:
        # Closed eye (horizontal line)
        p1 = (center_x - width/2, center_y)
        p4 = (center_x + width/2, center_y)
        p2 = (center_x - width/4, center_y)
        p3 = (center_x + width/4, center_y)
        p5 = (center_x + width/4, center_y)
        p6 = (center_x - width/4, center_y)
        
        # Draw closed eye line
        ax.plot([p1[0], p4[0]], [p1[1], p4[1]], 'k-', linewidth=2)
    else:
        # Open eye (ellipse shape)
        p1 = (center_x - width/2, center_y)
        p4 = (center_x + width/2, center_y)
        p2 = (center_x - width/4, center_y + height/2)
        p3 = (center_x + width/4, center_y + height/2)
        p5 = (center_x + width/4, center_y - height/2)
        p6 = (center_x - width/4, center_y - height/2)
        
        # Draw eye outline
        theta = np.linspace(0, 2*np.pi, 100)
        x_ellipse = center_x + (width/2) * np.cos(theta)
        y_ellipse = center_y + (height/2) * np.sin(theta)
        ax.plot(x_ellipse, y_ellipse, 'k-', linewidth=2)
    
    # Plot landmark points
    points = {'p1': p1, 'p2': p2, 'p3': p3, 'p4': p4, 'p5': p5, 'p6': p6}
    colors = {'p1': 'red', 'p2': 'blue', 'p3': 'blue', 'p4': 'red', 'p5': 'blue', 'p6': 'blue'}
    
    for label, point in points.items():
        ax.plot(point[0], point[1], 'o', color=colors[label], markersize=10, zorder=5)
        # Add labels
        offset = 0.15
        if label in ['p1']:
            ax.text(point[0] - offset, point[1], label, fontsize=10, fontweight='bold', 
                   ha='right', va='center')
        elif label in ['p4']:
            ax.text(point[0] + offset, point[1], label, fontsize=10, fontweight='bold', 
                   ha='left', va='center')
        elif label in ['p2', 'p3']:
            ax.text(point[0], point[1] + offset, label, fontsize=10, fontweight='bold', 
                   ha='center', va='bottom')
        else:  # p5, p6
            ax.text(point[0], point[1] - offset, label, fontsize=10, fontweight='bold', 
                   ha='center', va='top')
    
    # Draw measurement lines
    if not is_closed:
        # Vertical distances
        ax.plot([p2[0], p6[0]], [p2[1], p6[1]], 'g--', linewidth=1.5, alpha=0.7)
        ax.plot([p3[0], p5[0]], [p3[1], p5[1]], 'g--', linewidth=1.5, alpha=0.7)
        
        # Add distance labels
        ax.text((p2[0] + p6[0])/2 - 0.2, (p2[1] + p6[1])/2, '||p2-p6||', 
               fontsize=8, color='green', rotation=90, va='center')
        ax.text((p3[0] + p5[0])/2 + 0.2, (p3[1] + p5[1])/2, '||p3-p5||', 
               fontsize=8, color='green', rotation=90, va='center')
    
    # Horizontal distance
    ax.plot([p1[0], p4[0]], [p1[1] - 0.8, p4[1] - 0.8], 'g--', linewidth=1.5, alpha=0.7)
    ax.text(center_x, center_y - 1.0, '||p1-p4||', fontsize=8, color='green', ha='center')
    
    # Add title and EAR value
    ax.text(center_x, center_y + height/2 + 0.8, title, fontsize=12, fontweight='bold', 
           ha='center')
    
    ear_color = 'red' if ear_value < 0.25 else 'green'
    ax.text(center_x, center_y - height/2 - 1.3, f'EAR ≈ {ear_value:.2f}', 
           fontsize=11, ha='center', color=ear_color, fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='white', edgecolor=ear_color, linewidth=2))

def create_ear_diagram():
    """
    Create the complete EAR diagram
    """
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Draw open eye
    draw_eye(ax, center_x=2, center_y=3, width=3, height=1.5, 
            title='Open Eye', ear_value=0.30, is_closed=False)
    
    # Draw closed eye
    draw_eye(ax, center_x=8, center_y=3, width=3, height=1.5, 
            title='Closed Eye - Blink Detected', ear_value=0.20, is_closed=True)
    
    # Add formula
    formula_text = r'$EAR = \frac{||p_2 - p_6|| + ||p_3 - p_5||}{2 \times ||p_1 - p_4||}$'
    ax.text(5, 6, 'Eye Aspect Ratio Formula:', fontsize=14, fontweight='bold', ha='center')
    ax.text(5, 5.3, formula_text, fontsize=16, ha='center', 
           bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='black', linewidth=2))
    
    # Add explanation box
    explanation = (
        'Blink Detection Logic:\n'
        '• Calculate EAR for both eyes\n'
        '• Average the values\n'
        '• Threshold: EAR < 0.25 indicates closed eye\n'
        '• Blink detected when eyes closed for 2-3 consecutive frames'
    )
    ax.text(5, 0.5, explanation, fontsize=10, ha='center', va='center',
           bbox=dict(boxstyle='round', facecolor='lightblue', edgecolor='darkblue', linewidth=2))
    
    # Add legend for landmark colors
    red_patch = mpatches.Patch(color='red', label='Horizontal landmarks (p1, p4)')
    blue_patch = mpatches.Patch(color='blue', label='Vertical landmarks (p2, p3, p5, p6)')
    green_patch = mpatches.Patch(color='green', label='Distance measurements')
    ax.legend(handles=[red_patch, blue_patch, green_patch], loc='upper right', fontsize=9)
    
    # Set axis properties
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-1, 7)
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.title('Eye Aspect Ratio (EAR) - Blink Detection Algorithm', 
             fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    return fig

# Generate and save the diagram
if __name__ == '__main__':
    fig = create_ear_diagram()
    
    # Save as high-resolution PNG
    plt.savefig('ear_diagram.png', dpi=300, bbox_inches='tight', facecolor='white')
    print(" Diagram saved as 'ear_diagram.png'")
    
    # Optionally save as SVG (vector format)
    plt.savefig('ear_diagram.svg', format='svg', bbox_inches='tight', facecolor='white')
    print(" Diagram saved as 'ear_diagram.svg'")
    
    plt.show()
