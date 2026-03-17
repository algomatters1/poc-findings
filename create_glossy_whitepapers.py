#!/usr/bin/env python3
"""
Create glossy, narrative-style whitepaper PDFs with diagrams and professional layout.
Uses reportlab for PDF generation with custom styling.
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
    PageBreak, Image, KeepTogether, ListFlowable, ListItem,
    Flowable, HRFlowable
)
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Circle, Polygon
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color
import os
import re
from datetime import datetime

# Color schemes for each whitepaper
COLORS = {
    'gitnexus': {
        'primary': HexColor('#1a73e8'),
        'secondary': HexColor('#4285f4'),
        'accent': HexColor('#34a853'),
        'dark': HexColor('#0d47a1'),
        'light': HexColor('#e8f0fe'),
        'gradient_start': HexColor('#1a73e8'),
        'gradient_end': HexColor('#0d47a1'),
    },
    'gstack': {
        'primary': HexColor('#34a853'),
        'secondary': HexColor('#4caf50'),
        'accent': HexColor('#ff9800'),
        'dark': HexColor('#1b5e20'),
        'light': HexColor('#e8f5e9'),
        'gradient_start': HexColor('#34a853'),
        'gradient_end': HexColor('#1b5e20'),
    },
    'paperclip': {
        'primary': HexColor('#9c27b0'),
        'secondary': HexColor('#ab47bc'),
        'accent': HexColor('#ff5722'),
        'dark': HexColor('#4a148c'),
        'light': HexColor('#f3e5f5'),
        'gradient_start': HexColor('#9c27b0'),
        'gradient_end': HexColor('#4a148c'),
    },
    'executive': {
        'primary': HexColor('#37474f'),
        'secondary': HexColor('#546e7a'),
        'accent': HexColor('#2196f3'),
        'dark': HexColor('#263238'),
        'light': HexColor('#eceff1'),
        'gradient_start': HexColor('#37474f'),
        'gradient_end': HexColor('#263238'),
    }
}


class GradientRect(Flowable):
    """A flowable that draws a gradient rectangle."""
    def __init__(self, width, height, start_color, end_color, text="", text_color=colors.white):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.start_color = start_color
        self.end_color = end_color
        self.text = text
        self.text_color = text_color
    
    def draw(self):
        steps = 50
        for i in range(steps):
            ratio = i / steps
            r = self.start_color.red + (self.end_color.red - self.start_color.red) * ratio
            g = self.start_color.green + (self.end_color.green - self.start_color.green) * ratio
            b = self.start_color.blue + (self.end_color.blue - self.start_color.blue) * ratio
            self.canv.setFillColor(Color(r, g, b))
            y = self.height * (1 - i/steps)
            h = self.height / steps + 1
            self.canv.rect(0, y, self.width, h, fill=True, stroke=False)
        
        if self.text:
            self.canv.setFillColor(self.text_color)
            self.canv.setFont("Helvetica-Bold", 20)
            self.canv.drawCentredString(self.width/2, self.height/2 - 10, self.text)


class KnowledgeGraphDiagram(Flowable):
    """Draw a knowledge graph diagram."""
    def __init__(self, width=450, height=200, colorscheme='gitnexus'):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.colorscheme = colorscheme
        self.c = COLORS[colorscheme]
    
    def draw(self):
        self.canv.setFillColor(self.c['light'])
        self.canv.roundRect(0, 0, self.width, self.height, 10, fill=True, stroke=False)
        
        nodes = [
            (50, 150, "Function\nlogin()"),
            (150, 170, "Function\nverify()"),
            (150, 100, "Class\nUser"),
            (250, 140, "Database\nusers"),
            (250, 60, "Function\ngetToken()"),
            (350, 100, "Module\nauth"),
            (400, 160, "API\n/login"),
        ]
        
        edges = [
            (50, 145, 150, 165),
            (150, 165, 250, 145),
            (150, 105, 250, 75),
            (250, 75, 350, 105),
            (350, 105, 400, 155),
            (50, 145, 150, 105),
        ]
        
        self.canv.setStrokeColor(self.c['secondary'])
        self.canv.setLineWidth(2)
        for x1, y1, x2, y2 in edges:
            self.canv.line(x1, y1, x2, y2)
        
        for x, y, label in nodes:
            self.canv.setFillColor(self.c['primary'])
            self.canv.circle(x, y, 25, fill=True, stroke=False)
            self.canv.setFillColor(colors.white)
            self.canv.setFont("Helvetica", 6)
            lines = label.split('\n')
            for i, line in enumerate(lines):
                self.canv.drawCentredString(x, y + 5 - i*8, line)
        
        self.canv.setFillColor(self.c['dark'])
        self.canv.setFont("Helvetica-Bold", 10)
        self.canv.drawString(10, self.height - 15, "Knowledge Graph: Authentication Flow")


class WorkflowDiagram(Flowable):
    """Draw a workflow pipeline diagram."""
    def __init__(self, width=450, height=120, colorscheme='gstack'):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.colorscheme = colorscheme
        self.c = COLORS[colorscheme]
    
    def draw(self):
        self.canv.setFillColor(self.c['light'])
        self.canv.roundRect(0, 0, self.width, self.height, 10, fill=True, stroke=False)
        
        stages = [
            ("CEO\nReview", self.c['primary']),
            ("CTO\nReview", self.c['secondary']),
            ("Design\nReview", self.c['accent']),
            ("Eng\nReview", self.c['primary']),
            ("QA", self.c['secondary']),
            ("Ship", self.c['accent']),
        ]
        
        x = 30
        y = self.height / 2
        box_width = 55
        box_height = 50
        spacing = 70
        
        for i, (label, color) in enumerate(stages):
            self.canv.setFillColor(color)
            self.canv.roundRect(x, y - box_height/2, box_width, box_height, 8, fill=True, stroke=False)
            self.canv.setFillColor(colors.white)
            self.canv.setFont("Helvetica-Bold", 8)
            lines = label.split('\n')
            for j, line in enumerate(lines):
                self.canv.drawCentredString(x + box_width/2, y - 5 - j*10, line)
            
            if i < len(stages) - 1:
                self.canv.setFillColor(self.c['dark'])
                self.canv.setFont("Helvetica-Bold", 14)
                self.canv.drawString(x + box_width + 8, y - 5, "→")
            
            x += spacing
        
        self.canv.setFillColor(self.c['dark'])
        self.canv.setFont("Helvetica-Bold", 10)
        self.canv.drawString(10, self.height - 15, "gstack Workflow: From Idea to Production")


class OrgChartDiagram(Flowable):
    """Draw an org chart diagram."""
    def __init__(self, width=450, height=180, colorscheme='paperclip'):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.colorscheme = colorscheme
        self.c = COLORS[colorscheme]
    
    def draw(self):
        self.canv.setFillColor(self.c['light'])
        self.canv.roundRect(0, 0, self.width, self.height, 10, fill=True, stroke=False)
        
        # CEO at top
        self.canv.setFillColor(self.c['primary'])
        self.canv.roundRect(175, 140, 100, 30, 5, fill=True, stroke=False)
        self.canv.setFillColor(colors.white)
        self.canv.setFont("Helvetica-Bold", 9)
        self.canv.drawCentredString(225, 152, "CEO Agent")
        
        reports = [("CTO", 50), ("CFO", 150), ("COO", 250), ("CPO", 350)]
        
        self.canv.setStrokeColor(self.c['secondary'])
        self.canv.setLineWidth(2)
        for _, x in reports:
            self.canv.line(225, 140, x + 35, 105)
        
        for label, x in reports:
            self.canv.setFillColor(self.c['secondary'])
            self.canv.roundRect(x, 75, 70, 30, 5, fill=True, stroke=False)
            self.canv.setFillColor(colors.white)
            self.canv.setFont("Helvetica-Bold", 8)
            self.canv.drawCentredString(x + 35, 87, label)
        
        teams = [
            ("Eng-1", 20), ("Eng-2", 80), ("Fin", 140),
            ("Ops", 240), ("Product", 320),
        ]
        
        for team, x in teams:
            self.canv.setFillColor(self.c['accent'])
            self.canv.roundRect(x, 10, 60, 25, 3, fill=True, stroke=False)
            self.canv.setFillColor(colors.white)
            self.canv.setFont("Helvetica", 7)
            self.canv.drawCentredString(x + 30, 20, team)
        
        self.canv.setFillColor(self.c['dark'])
        self.canv.setFont("Helvetica-Bold", 10)
        self.canv.drawString(10, self.height - 15, "Paperclip: Autonomous AI Org Structure")


class StackDiagram(Flowable):
    """Draw a technology stack diagram."""
    def __init__(self, width=450, height=150, colorscheme='executive'):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.colorscheme = colorscheme
        self.c = COLORS[colorscheme]
    
    def draw(self):
        self.canv.setFillColor(self.c['light'])
        self.canv.roundRect(0, 0, self.width, self.height, 10, fill=True, stroke=False)
        
        layers = [
            ("Infrastructure Layer", COLORS['gitnexus']['primary'], "GitNexus: Code Intelligence"),
            ("Workflow Layer", COLORS['gstack']['primary'], "gstack: Process Skills"),
            ("Orchestration Layer", COLORS['paperclip']['primary'], "Paperclip: Organization"),
            ("AI Agents", self.c['accent'], "Claude, OpenClaw, etc."),
        ]
        
        y = 20
        box_height = 28
        spacing = 32
        
        for label, color, desc in reversed(layers):
            self.canv.setFillColor(color)
            self.canv.roundRect(30, y, self.width - 60, box_height, 5, fill=True, stroke=False)
            self.canv.setFillColor(colors.white)
            self.canv.setFont("Helvetica-Bold", 9)
            self.canv.drawString(40, y + 9, label)
            self.canv.setFont("Helvetica", 7)
            self.canv.drawRightString(self.width - 40, y + 9, desc)
            y += spacing
        
        self.canv.setFillColor(self.c['dark'])
        self.canv.setFont("Helvetica-Bold", 10)
        self.canv.drawString(10, self.height - 15, "The Autonomous AI Development Stack")


def create_styles(colorscheme='gitnexus'):
    """Create custom paragraph styles for the whitepaper."""
    c = COLORS[colorscheme]
    styles = getSampleStyleSheet()
    
    styles.add(ParagraphStyle(
        name='WP_Title',
        parent=styles['Heading1'],
        fontSize=28,
        leading=34,
        textColor=c['dark'],
        spaceAfter=30,
        alignment=TA_LEFT,
        fontName='Helvetica-Bold',
    ))
    
    styles.add(ParagraphStyle(
        name='WP_Subtitle',
        parent=styles['Normal'],
        fontSize=14,
        leading=18,
        textColor=c['secondary'],
        spaceAfter=20,
        fontName='Helvetica-Oblique',
    ))
    
    styles.add(ParagraphStyle(
        name='WP_Section',
        parent=styles['Heading2'],
        fontSize=18,
        leading=22,
        textColor=c['primary'],
        spaceBefore=20,
        spaceAfter=12,
        fontName='Helvetica-Bold',
    ))
    
    styles.add(ParagraphStyle(
        name='WP_Subsection',
        parent=styles['Heading3'],
        fontSize=14,
        leading=18,
        textColor=c['dark'],
        spaceBefore=15,
        spaceAfter=8,
        fontName='Helvetica-Bold',
    ))
    
    styles.add(ParagraphStyle(
        name='WP_Body',
        parent=styles['Normal'],
        fontSize=11,
        leading=16,
        textColor=colors.black,
        spaceAfter=12,
        alignment=TA_JUSTIFY,
        fontName='Helvetica',
    ))
    
    styles.add(ParagraphStyle(
        name='WP_Code',
        parent=styles['Code'],
        fontSize=9,
        leading=12,
        textColor=c['dark'],
        backColor=HexColor('#f5f5f5'),
        leftIndent=10,
        rightIndent=10,
        fontName='Courier',
    ))
    
    return styles


def parse_markdown_to_story(md_content, colorscheme='gitnexus'):
    """Parse markdown content and convert to reportlab story."""
    styles = create_styles(colorscheme)
    story = []
    lines = md_content.split('\n')
    c = COLORS[colorscheme]
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if not line:
            i += 1
            continue
        
        if line.startswith('# '):
            title = line[2:].strip()
            story.append(Paragraph(title, styles['WP_Title']))
            i += 1
            continue
        
        if line.startswith('## '):
            heading = line[3:].strip()
            story.append(Paragraph(heading, styles['WP_Section']))
            i += 1
            continue
        
        if line.startswith('### '):
            heading = line[4:].strip()
            story.append(Paragraph(heading, styles['WP_Subsection']))
            i += 1
            continue
        
        if line.startswith('####'):
            i += 1
            continue
        
        if line.startswith('---'):
            story.append(HRFlowable(width="100%", thickness=1, color=c['primary']))
            story.append(Spacer(1, 10))
            i += 1
            continue
        
        if line.startswith('```'):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            code_text = '\n'.join(code_lines)
            story.append(Paragraph(f'<font face="Courier" size="9">{code_text}</font>', styles['WP_Code']))
            i += 1
            continue
        
        if line.startswith('|'):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                table_lines.append(lines[i])
                i += 1
            
            if len(table_lines) >= 2:
                rows = []
                for tline in table_lines:
                    if '---' in tline:
                        continue
                    cells = [c.strip() for c in tline.split('|')[1:-1]]
                    rows.append(cells)
                
                if rows:
                    t = Table(rows)
                    t.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), c['primary']),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                        ('BACKGROUND', (0, 1), (-1, -1), c['light']),
                        ('FONTSIZE', (0, 1), (-1, -1), 9),
                        ('GRID', (0, 0), (-1, -1), 0.5, c['secondary']),
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                        ('LEFTPADDING', (0, 0), (-1, -1), 6),
                        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                    ]))
                    story.append(t)
                    story.append(Spacer(1, 10))
            continue
        
        if line.startswith('- ') or line.startswith('* '):
            bullet_text = line[2:].strip()
            bullet_text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', bullet_text)
            bullet_text = re.sub(r'`(.+?)`', r'<font face="Courier" size="9">\1</font>', bullet_text)
            story.append(Paragraph(f'• {bullet_text}', styles['WP_Body']))
            i += 1
            continue
        
        if re.match(r'^\d+\. ', line):
            match = re.match(r'^(\d+)\. (.+)', line)
            if match:
                num, text = match.groups()
                text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
                text = re.sub(r'`(.+?)`', r'<font face="Courier" size="9">\1</font>', text)
                story.append(Paragraph(f'{num}. {text}', styles['WP_Body']))
            i += 1
            continue
        
        para_text = line
        i += 1
        
        while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith(('#', '-', '*', '|', '`', '---')):
            para_text += ' ' + lines[i].strip()
            i += 1
        
        para_text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', para_text)
        para_text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', para_text)
        para_text = re.sub(r'`(.+?)`', r'<font face="Courier" size="9">\1</font>', para_text)
        para_text = re.sub(r'\[(.+?)\]\((.+?)\)', r'\1', para_text)
        
        story.append(Paragraph(para_text, styles['WP_Body']))
    
    return story


def create_whitepaper_pdf(input_file, output_file, colorscheme='gitnexus', title=None, subtitle=None, diagram=None):
    """Create a glossy whitepaper PDF from markdown."""
    with open(input_file, 'r') as f:
        md_content = f.read()
    
    doc = SimpleDocTemplate(
        output_file,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=60,
        bottomMargin=60,
    )
    
    c = COLORS[colorscheme]
    styles = create_styles(colorscheme)
    story = []
    
    # Cover page
    story.append(Spacer(1, 100))
    story.append(GradientRect(450, 80, c['gradient_start'], c['gradient_end'], 
                              title or "Whitepaper", colors.white))
    story.append(Spacer(1, 20))
    
    if subtitle:
        story.append(Paragraph(subtitle, styles['WP_Subtitle']))
    
    story.append(Spacer(1, 30))
    
    if diagram == 'knowledge_graph':
        story.append(KnowledgeGraphDiagram(450, 180, colorscheme))
    elif diagram == 'workflow':
        story.append(WorkflowDiagram(450, 120, colorscheme))
    elif diagram == 'org_chart':
        story.append(OrgChartDiagram(450, 180, colorscheme))
    elif diagram == 'stack':
        story.append(StackDiagram(450, 150, colorscheme))
    
    story.append(Spacer(1, 20))
    story.append(Paragraph(f"<b>POC Date:</b> March 17, 2026", styles['WP_Body']))
    story.append(Paragraph(f"<b>Classification:</b> Strategic Intelligence Report", styles['WP_Body']))
    story.append(Paragraph(f"<b>Version:</b> 2.0 (Glossy Edition)", styles['WP_Body']))
    story.append(PageBreak())
    
    story.extend(parse_markdown_to_story(md_content, colorscheme))
    
    doc.build(story)
    print(f"Created: {output_file}")
    return output_file


def main():
    """Create all whitepaper PDFs."""
    base_path = "/Users/rr/projects/poc-findings"
    
    # GitNexus Whitepaper
    create_whitepaper_pdf(
        input_file=f"{base_path}/WHITEPAPER_GitNexus.md",
        output_file=f"{base_path}/WHITEPAPER_GitNexus_Glossy.pdf",
        colorscheme='gitnexus',
        title="GitNexus",
        subtitle="Knowledge Graph-Powered Code Intelligence for AI Agents",
        diagram='knowledge_graph',
    )
    
    # gstack Whitepaper
    create_whitepaper_pdf(
        input_file=f"{base_path}/WHITEPAPER_gstack.md",
        output_file=f"{base_path}/WHITEPAPER_gstack_Glossy.pdf",
        colorscheme='gstack',
        title="gstack",
        subtitle="Workflow Skills for Autonomous AI Development",
        diagram='workflow',
    )
    
    # Paperclip Whitepaper
    create_whitepaper_pdf(
        input_file=f"{base_path}/WHITEPAPER_Paperclip.md",
        output_file=f"{base_path}/WHITEPAPER_Paperclip_Glossy.pdf",
        colorscheme='paperclip',
        title="Paperclip",
        subtitle="Orchestration Platform for Autonomous AI Companies",
        diagram='org_chart',
    )
    
    # Executive Summary
    create_whitepaper_pdf(
        input_file=f"{base_path}/EXECUTIVE_SUMMARY.md",
        output_file=f"{base_path}/EXECUTIVE_SUMMARY_Glossy.pdf",
        colorscheme='executive',
        title="Executive Summary",
        subtitle="The Autonomous AI Development Stack",
        diagram='stack',
    )
    
    print("\n✅ All glossy whitepapers created!")
    print("Files created:")
    print(f"  - {base_path}/WHITEPAPER_GitNexus_Glossy.pdf")
    print(f"  - {base_path}/WHITEPAPER_gstack_Glossy.pdf")
    print(f"  - {base_path}/WHITEPAPER_Paperclip_Glossy.pdf")
    print(f"  - {base_path}/EXECUTIVE_SUMMARY_Glossy.pdf")


if __name__ == "__main__":
    main()