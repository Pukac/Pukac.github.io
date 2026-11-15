"""Create the two client profiles from the website's current SK/EN content.

Run with Python and reportlab installed. Outputs contain public portfolio text only.
"""
import json
import re
from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / 'index.html').read_text(encoding='utf-8')
MATCH = re.search(r'const CONTENT = (.*?);\s*function restoreLanguage', SOURCE, re.S)
if MATCH is None:
    raise ValueError('Cannot locate portfolio content')
CONTENT = json.loads(MATCH.group(1))
OUT = ROOT / 'output' / 'pdf'
OUT.mkdir(parents=True, exist_ok=True)
FONT_DIR = Path('C:/Windows/Fonts')
for name, file in [('Body', 'arial.ttf'), ('BodyBold', 'arialbd.ttf'), ('Display', 'georgia.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(FONT_DIR / file)))
OLIVE = colors.HexColor('#4c5844')
INK = colors.HexColor('#302f25')
MUTED = colors.HexColor('#626251')
PAPER = colors.HexColor('#f5f2e9')
styles = {
    'body': ParagraphStyle('body', fontName='Body', fontSize=10.2, leading=15, textColor=INK, spaceAfter=10),
    'title': ParagraphStyle('title', fontName='Display', fontSize=34, leading=39, textColor=INK, spaceAfter=9),
    'kicker': ParagraphStyle('kicker', fontName='Body', fontSize=8.5, leading=12, textColor=OLIVE, spaceAfter=15),
    'heading': ParagraphStyle('heading', fontName='Display', fontSize=18, leading=23, textColor=OLIVE, spaceBefore=13, spaceAfter=9, keepWithNext=True),
    'offer': ParagraphStyle('offer', fontName='BodyBold', fontSize=11, leading=15, textColor=OLIVE, spaceAfter=8),
    'small': ParagraphStyle('small', fontName='Body', fontSize=9, leading=13, textColor=MUTED, spaceAfter=8),
}

def p(text, style='body'):
    return Paragraph(escape(text), styles[style])

def decorate(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    canvas.setFillColor(OLIVE)
    canvas.rect(0, A4[1]-10, A4[0], 10, fill=1, stroke=0)
    canvas.setStrokeColor(colors.HexColor('#c6cbb9'))
    canvas.line(43, 48, A4[0]-43, 48)
    canvas.setFont('Body', 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(43, 32, 'Ján Janda | Full remote B2B')
    canvas.restoreState()

for language, c in CONTENT.items():
    target = OUT / ('jan-janda-profile-' + language + '.pdf')
    doc = SimpleDocTemplate(str(target), pagesize=A4, leftMargin=43, rightMargin=43,
                            topMargin=40, bottomMargin=62, title='Ján Janda | '+c['profileTitle'], author='Ján Janda')
    flow = [p(c['profileTitle'].upper() + ' / FULL REMOTE B2B', 'kicker'), p('Ján Janda', 'title'),
            p(c['profileFooter'], 'small'), Spacer(1, 9), p(c['printIntro']), p(c['profileServices'], 'heading')]
    columns = [
        [p(c['softwareTitle'], 'offer'), p(c['profileOfferSoftware'])],
        [p(c['aiTitle'], 'offer'), p(c['profileOfferAi'])]
    ]
    offers = Table([columns], colWidths=[245, 245], hAlign='LEFT')
    offers.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),
                               ('RIGHTPADDING',(0,0),(-1,-1),16),('TOPPADDING',(0,0),(-1,-1),4),
                               ('BOTTOMPADDING',(0,0),(-1,-1),0)]))
    flow += [offers, p(c['profileExperience'], 'heading'), p(c['profileExperienceCopy']),
             p(c['processLabel'], 'heading'), p(c['profileMethod']),
             p(c['printSkills'], 'heading'), p('C# / .NET / WPF / Python / OpenCV / PyQt / SDK / GitLab CI'),
             p(c['profilePersonal'], 'small'), Spacer(1, 8)]
    label = 'LinkedIn: Ján Janda'
    link = '<link href="https://www.linkedin.com/in/j%C3%A1n-janda-0052a4221/" color="#4c5844"><u>'+label+'</u></link>'
    flow += [Paragraph(link, styles['body']), p(c['contactMeta'], 'small')]
    doc.build(flow, onFirstPage=decorate, onLaterPages=decorate)
    print(target)
