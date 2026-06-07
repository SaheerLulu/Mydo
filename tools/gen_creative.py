#!/usr/bin/env python3
"""Bespoke, content-specific diagrams per industry (light theme).

Each industry gets three diagrams of *different visual forms* so the blogs
stop looking templated. Shared palette/typography keeps the site cohesive.
"""
import os, math

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "img")
FONT = "Segoe UI, Roboto, Helvetica, Arial, sans-serif"

WHITE="#ffffff"; INK="#1a1a1a"; INK2="#374151"; MUTED="#6b7280"
LINE="#e3e8f0"; BOXF="#f5f8ff"; BOXS="#dbe4f3"; WASH="#f8fafc"
BLUE="#2563eb"; TEAL="#0ea5a4"; AMBER="#f59e0b"; PURPLE="#7c3aed"
GREEN="#16a34a"; RED="#e11d48"; CYAN="#0891b2"; GREENF="#f0fbf7"; GREENS="#bfe6d8"

def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def bell(cx,cy,c):
    return (f'<path d="M{cx:.0f},{cy-7} C{cx+6:.0f},{cy-7} {cx+6:.0f},{cy+2} {cx+8:.0f},{cy+4} '
            f'L{cx-8:.0f},{cy+4} C{cx-6:.0f},{cy+2} {cx-6:.0f},{cy-7} {cx:.0f},{cy-7} Z" '
            f'fill="none" stroke="{c}" stroke-width="2" stroke-linejoin="round"/>'
            f'<circle cx="{cx:.0f}" cy="{cy-9:.0f}" r="1.6" fill="{c}"/>'
            f'<circle cx="{cx:.0f}" cy="{cy+7:.0f}" r="1.8" fill="{c}"/>')
def t(x,y,s,size,fill,w=400,anchor="start"):
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
            f'fill="{fill}" font-weight="{w}" text-anchor="{anchor}">{esc(s)}</text>')
def box(x,y,w,h,fill,stroke,r=10,sw=1):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def adefs(color=BLUE,name="ar"):
    return (f'<marker id="{name}" markerWidth="11" markerHeight="11" refX="7" refY="4" '
            f'orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0 L8,4 L0,8 Z" fill="{color}"/></marker>')
def save(name,w,h,body,defs=""):
    svg=(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="{FONT}">\n'
         f'<defs>{defs}</defs>\n<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="18" '
         f'fill="{WHITE}" stroke="{LINE}"/>\n'+body+"\n</svg>\n")
    open(os.path.join(OUT,name),"w",encoding="utf-8").write(svg)

def head(b,title,sub=None):
    b.append(t(40,50,title,23,INK,800))
    if sub: b.append(t(40,76,sub,14.5,MUTED,400))

# ============================================================ PHARMACY
def pharmacy_forecast():
    b=[adefs(TEAL)]; head(b,"Demand forecasting keeps shelves stocked — not overstocked",
        "Medloop learns each product's demand and reorders before you run out.")
    x0,x1,yb,yt=96,980,360,120
    # axes
    b.append(f'<line x1="{x0}" y1="{yt}" x2="{x0}" y2="{yb}" stroke="{BOXS}" stroke-width="1.5"/>')
    b.append(f'<line x1="{x0}" y1="{yb}" x2="{x1}" y2="{yb}" stroke="{BOXS}" stroke-width="1.5"/>')
    for gy in (yt+30,yt+90,yt+150):
        b.append(f'<line x1="{x0}" y1="{gy}" x2="{x1}" y2="{gy}" stroke="{LINE}" stroke-width="1"/>')
    # reorder line
    ry=320
    b.append(f'<line x1="{x0}" y1="{ry}" x2="{x1}" y2="{ry}" stroke="{RED}" stroke-width="1.6" stroke-dasharray="6 5"/>')
    b.append(t(x1-6,ry-8,"Reorder point",12.5,RED,700,"end"))
    n=8; xs=[x0+30+i*((x1-30-x0-10)/(n-1)) for i in range(n)]
    act=[250,236,262,228,246]; fc=[246,224,238,214]
    # confidence band for forecast (points 4..7)
    fxs=xs[4:]; up=[v-20 for v in fc]; dn=[v+20 for v in fc]
    band="M"+" L".join(f"{fxs[i]:.0f},{up[i]:.0f}" for i in range(4))
    band+=" L"+" L".join(f"{fxs[3-i]:.0f},{dn[3-i]:.0f}" for i in range(4))+" Z"
    b.append(f'<path d="{band}" fill="{TEAL}" opacity="0.12"/>')
    # actual line (solid, wk1-5)
    ap="M"+" L".join(f"{xs[i]:.0f},{act[i]:.0f}" for i in range(5))
    b.append(f'<path d="{ap}" fill="none" stroke="{BLUE}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')
    for i in range(5): b.append(f'<circle cx="{xs[i]:.0f}" cy="{act[i]}" r="4.5" fill="{BLUE}"/>')
    # forecast line (dashed, wk5-8) starting from last actual
    fp=f"M{xs[4]:.0f},{act[4]} "+"L"+" L".join(f"{fxs[i]:.0f},{fc[i]:.0f}" for i in range(4))
    b.append(f'<path d="{fp}" fill="none" stroke="{TEAL}" stroke-width="3" stroke-dasharray="7 5" stroke-linecap="round" stroke-linejoin="round"/>')
    for i in range(4): b.append(f'<circle cx="{fxs[i]:.0f}" cy="{fc[i]}" r="4.5" fill="{WHITE}" stroke="{TEAL}" stroke-width="2.5"/>')
    # x labels
    for i in range(n): b.append(t(xs[i],yb+22,f"W{i+1}",12,MUTED,600,"middle"))
    # stockout-avoided annotation near W4 dip (still above reorder)
    b.append(f'<circle cx="{xs[3]:.0f}" cy="{act[3]}" r="9" fill="none" stroke="{GREEN}" stroke-width="2"/>')
    b.append(t(xs[3]+14,act[3]-12,"dip stays above reorder",12,GREEN,700))
    # legend
    lx=x0+8
    b.append(f'<line x1="{lx}" y1="100" x2="{lx+26}" y2="100" stroke="{BLUE}" stroke-width="3"/>'); b.append(t(lx+34,104,"Actual demand",12.5,INK2,600))
    b.append(f'<line x1="{lx+170}" y1="100" x2="{lx+196}" y2="100" stroke="{TEAL}" stroke-width="3" stroke-dasharray="7 5"/>'); b.append(t(lx+204,104,"Medloop forecast",12.5,INK2,600))
    save("pharmacy-forecast.svg",1040,410,"".join(b))

def pharmacy_expiry():
    b=[adefs(AMBER,"aa")]; head(b,"Medloop sees expiry coming — and acts in time",
        "Every batch tracked by expiry date, flagged weeks ahead, moved where it sells.")
    ax=96; axr=980; ay=300
    b.append(f'<line x1="{ax}" y1="{ay}" x2="{axr}" y2="{ay}" stroke="{BOXS}" stroke-width="2"/>')
    for d in range(0,91,15):
        gx=ax+(axr-ax)*d/90
        b.append(f'<line x1="{gx:.0f}" y1="{ay-5}" x2="{gx:.0f}" y2="{ay+5}" stroke="{MUTED}" stroke-width="1.5"/>')
        b.append(t(gx,ay+24,("Today" if d==0 else f"+{d}d"),11.5,MUTED,600,"middle"))
    # alert window 0..45
    awx=ax; aww=(axr-ax)*45/90
    b.append(f'<rect x="{awx:.0f}" y="118" width="{aww:.0f}" height="160" rx="10" fill="{AMBER}" opacity="0.09"/>')
    b.append(t(awx+12,138,"Medloop alert window — 45 days out",12.5,"#9a6a06",700))
    # batch chips: (days_to_expiry, label, lane_y, color)
    chips=[(8,"Batch A123",150,RED),(22,"Batch B77",205,AMBER),(38,"Batch C40",165,AMBER),
           (64,"Batch D12",210,TEAL),(82,"Batch E05",150,GREEN)]
    for d,lab,y,c in chips:
        cx=ax+(axr-ax)*d/90
        b.append(box(cx-52,y,104,34,WHITE,c,9,2))
        b.append(f'<circle cx="{cx-36:.0f}" cy="{y+17}" r="5" fill="{c}"/>')
        b.append(t(cx-24,y+22,lab,12,INK2,600))
        b.append(f'<line x1="{cx:.0f}" y1="{y+34}" x2="{cx:.0f}" y2="{ay}" stroke="{c}" stroke-width="1.4" stroke-dasharray="3 3"/>')
    # transfer arrow from Batch B77 (amber) to high-demand branch node
    b.append(f'<path d="M{ax+(axr-ax)*22/90:.0f},239 C 470,360 700,360 {axr-150},332" fill="none" stroke="{TEAL}" stroke-width="2.5" stroke-dasharray="2 0" marker-end="url(#aa)"/>')
    b.append(box(axr-150,316,150,40,GREENF,GREENS,10)); b.append(t(axr-75,341,"High-demand branch",12,"#0f5132",700,"middle"))
    b.append(t(ax+(axr-ax)*22/90+8,250,"transfer → sells at full margin",11.5,TEAL,700))
    # legend
    for i,(c,lab) in enumerate([(RED,"Imminent"),(AMBER,"At risk"),(TEAL,"Watch"),(GREEN,"Healthy")]):
        lx=96+i*150; b.append(f'<circle cx="{lx}" cy="100" r="6" fill="{c}"/>'); b.append(t(lx+12,104,lab,12,INK2,600))
    save("pharmacy-expiry.svg",1040,390,"".join(b))

def pharmacy_audit():
    b=[]; head(b,"An audit-ready trail, written automatically",
        "Every controlled-substance movement logged, time-stamped and traceable.")
    lx=150; y0=120; dy=58
    events=[("Goods received","GRN #4821 · supplier verified",GREEN),
            ("Dispensed","Rx #99213 · pharmacist signed",BLUE),
            ("Controlled-substance log","Schedule entry auto-posted",PURPLE),
            ("Cold-chain check","2–8°C confirmed via IoT",TEAL),
            ("Recall trace","Batch + patients in seconds",AMBER)]
    b.append(f'<line x1="{lx}" y1="{y0}" x2="{lx}" y2="{y0+dy*(len(events)-1)}" stroke="{BOXS}" stroke-width="2"/>')
    for i,(ti,me,c) in enumerate(events):
        y=y0+i*dy
        b.append(f'<circle cx="{lx}" cy="{y}" r="11" fill="{WHITE}" stroke="{c}" stroke-width="3"/>')
        b.append(f'<path d="M{lx-4},{y} l3,4 l6,-8" fill="none" stroke="{c}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')
        b.append(t(lx+26,y-2,ti,15.5,INK,700)); b.append(t(lx+26,y+16,me,12.5,MUTED,500))
    # report card on right
    rx=720
    b.append(box(rx,150,260,150,WASH,LINE,14))
    b.append(t(rx+20,184,"Regulator-ready report",14,INK,800))
    for i,lab in enumerate(["Immutable & time-stamped","Filter by drug, batch, date","Exported on demand"]):
        yy=210+i*26; b.append(f'<circle cx="{rx+26}" cy="{yy-4}" r="3.5" fill="{BLUE}"/>'); b.append(t(rx+38,yy,lab,12.5,INK2,500))
    save("pharmacy-audit.svg",1040,400,"".join(b))

# ============================================================ ACCOUNTING
def accounting_extract():
    b=[adefs(PURPLE,"ap")]; head(b,"Document AI reads every invoice into clean data",
        "Biloop extracts, validates against the PO, and only asks when unsure.")
    # invoice card
    ix,iy,iw,ih=60,110,330,260
    b.append(box(ix,iy,iw,ih,WHITE,BOXS,12))
    b.append(t(ix+20,iy+34,"INVOICE",15,INK,800)); b.append(t(ix+iw-20,iy+34,"#INV-7741",12,MUTED,600,"end"))
    # faux text lines + highlighted fields
    def fld(yy,lab,val,c):
        b.append(f'<rect x="{ix+16}" y="{yy-16}" width="{iw-32}" height="26" rx="6" fill="{c}" opacity="0.10"/>')
        b.append(t(ix+24,yy,lab,11.5,c,700)); b.append(t(ix+iw-24,yy,val,12,INK2,600,"end"))
    fld(iy+78,"Vendor","Atlas Supplies",BLUE)
    fld(iy+114,"Invoice date","02 Jun 2026",TEAL)
    fld(iy+150,"Tax (5%)","QAR 312",AMBER)
    fld(iy+186,"Total","QAR 6,552",PURPLE)
    for k in range(3):
        b.append(f'<line x1="{ix+20}" y1="{iy+212+k*14}" x2="{ix+iw-40}" y2="{iy+212+k*14}" stroke="{LINE}" stroke-width="6" stroke-linecap="round"/>')
    # arrows to structured table
    tx,ty,tw=470,120,500
    rows=[("Vendor","Atlas Supplies",GREEN,"99%"),("Date","2026-06-02",GREEN,"99%"),
          ("Tax","QAR 312",GREEN,"98%"),("Total","QAR 6,552",GREEN,"99%"),
          ("PO match","PO-3120 ✓",GREEN,"matched"),("GL code","5100 · review",AMBER,"check")]
    b.append(box(tx,ty,tw,250,WASH,LINE,14))
    b.append(t(tx+20,ty+30,"Structured · validated",14,INK,800))
    for i,(k,v,c,conf) in enumerate(rows):
        yy=ty+58+i*32
        b.append(t(tx+22,yy,k,12.5,MUTED,600)); b.append(t(tx+150,yy,v,12.5,INK2,700))
        b.append(f'<circle cx="{tx+tw-86}" cy="{yy-4}" r="6" fill="{c}" opacity="0.18"/>')
        b.append(f'<circle cx="{tx+tw-86}" cy="{yy-4}" r="2.6" fill="{c}"/>')
        b.append(t(tx+tw-72,yy,conf,11.5,c,700))
    b.append(f'<path d="M{ix+iw},240 C 430,240 440,240 {tx},240" fill="none" stroke="{PURPLE}" stroke-width="2.5" marker-end="url(#ap)"/>')
    b.append(t((ix+iw+tx)/2,228,"AI extract",11.5,PURPLE,700,"middle"))
    save("accounting-extract.svg",1040,400,"".join(b))

def accounting_close():
    b=[]; head(b,"From a multi-day close to a continuous one",
        "Reconciliation runs every day, so the books are always close-ready.")
    x0,x1=210,980; days=8
    def dx(d): return x0+(x1-x0)*(d/days)
    for d in range(0,days+1):
        b.append(f'<line x1="{dx(d):.0f}" y1="120" x2="{dx(d):.0f}" y2="300" stroke="{LINE}" stroke-width="1"/>')
        b.append(t(dx(d),316,f"D{d}",11,MUTED,600,"middle"))
    # traditional row
    b.append(t(40,160,"Traditional",13,INK,800)); b.append(t(40,178,"close",13,INK,800))
    segs=[("Collect",0,2,"#cbd5e1"),("Reconcile",2,5,"#94a3b8"),("Adjust",5,7,"#64748b"),("Review",7,8,"#475569")]
    for lab,a,c,col in segs:
        b.append(box(dx(a),140,dx(c)-dx(a),40,col,col,8));
        b.append(t((dx(a)+dx(c))/2,165,lab,11.5,WHITE,700,"middle"))
    # biloop row
    b.append(t(40,240,"With Biloop",13,BLUE,800))
    for d in range(0,days):
        cxx=dx(d)+(dx(d+1)-dx(d))/2
        b.append(f'<circle cx="{cxx:.0f}" cy="240" r="7" fill="{GREEN}" opacity="0.18"/>')
        b.append(f'<path d="M{cxx-3:.0f},240 l2,3 l5,-6" fill="none" stroke="{GREEN}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
    b.append(box(x0,224,x1-x0,2,GREEN,GREEN,1))
    b.append(box(x1-176,256,176,34,GREENF,GREENS,9)); b.append(t(x1-88,278,"always close-ready",12,"#0f5132",700,"middle"))
    save("accounting-close.svg",1040,350,"".join(b))

def accounting_reconcile():
    b=[adefs(GREEN,"ag")]; head(b,"Reconciliation that matches itself",
        "Bank lines auto-match to the ledger — only true exceptions reach a person.")
    lx,rx,y0,dy=120,640,130,52
    bank=[("Bank · 02 Jun","QAR 6,552"),("Bank · 03 Jun","QAR 1,200"),("Bank · 04 Jun","QAR 980"),
          ("Bank · 05 Jun","QAR 3,410"),("Bank · 06 Jun","QAR 540")]
    led=[("INV-7741","QAR 6,552"),("INV-7742","QAR 1,200"),("Receipt 88","QAR 980"),
         ("INV-7745","QAR 3,410"),("—","unmatched")]
    b.append(t(lx,108,"Bank statement",13,INK,800)); b.append(t(rx,108,"Ledger",13,INK,800))
    for i in range(5):
        y=y0+i*dy
        b.append(box(lx,y,300,40,WHITE,BOXS,9)); b.append(t(lx+16,y+25,bank[i][0],12.5,INK2,600)); b.append(t(lx+284,y+25,bank[i][1],12.5,INK,700,"end"))
        b.append(box(rx,y,300,40,WHITE,BOXS,9)); b.append(t(rx+16,y+25,led[i][0],12.5,INK2,600)); b.append(t(rx+284,y+25,led[i][1],12.5,INK,700,"end"))
        if i<4:
            b.append(f'<line x1="{lx+300}" y1="{y+20}" x2="{rx}" y2="{y+20}" stroke="{GREEN}" stroke-width="2.4" marker-end="url(#ag)"/>')
        else:
            b.append(f'<line x1="{lx+300}" y1="{y+20}" x2="{rx}" y2="{y+20}" stroke="{AMBER}" stroke-width="2.4" stroke-dasharray="5 4"/>')
            b.append(t((lx+300+rx)/2,y+12,"exception → review",11,AMBER,700,"middle"))
    b.append(box(lx,y0+5*dy+6,820,34,GREENF,GREENS,9)); b.append(t(lx+410,y0+5*dy+28,"≈ 98% auto-matched · exceptions flagged the moment they appear",12.5,"#0f5132",700,"middle"))
    save("accounting-reconcile.svg",1040,470,"".join(b))

# ============================================================ REAL ESTATE
def realestate_funnel():
    b=[]; head(b,"More of every lead reaches a signed lease",
        "Instant response and scoring lift conversion at every stage.")
    stages=[("Leads",100,BLUE),("Responded <60s",96,BLUE),("Qualified",61,TEAL),("Viewing booked",38,TEAL),("Lease signed",14,GREEN)]
    cx=520; y0=110; h=46; gap=14; maxw=760
    for i,(lab,val,c) in enumerate(stages):
        w=maxw*val/100; y=y0+i*(h+gap)
        b.append(box(cx-w/2,y,w,h,c,c,10));
        b.append(t(cx,y+29,f"{lab}",14,WHITE,700,"middle"))
        b.append(t(cx+maxw/2+16,y+29,f"{val}",15,INK,800,"start"))
        b.append(t(cx+maxw/2+52,y+29,"of 100",11.5,MUTED,500,"start"))
    b.append(t(cx-maxw/2-16,y0+29,"before",11.5,MUTED,600,"end"))
    b.append(box(cx-150,y0+5*(h+gap)+10,300,34,GREENF,GREENS,9)); b.append(t(cx,y0+5*(h+gap)+32,"20–40% more qualified viewings",12.5,"#0f5132",700,"middle"))
    save("real-estate-funnel.svg",1040,480,"".join(b))

def realestate_speed():
    b=[]; head(b,"Speed is the deal","Replying first, every time — day or night.")
    # stopwatch
    cx,cy,r=190,250,84
    b.append(f'<line x1="{cx-10}" y1="{cy-r-22}" x2="{cx+10}" y2="{cy-r-22}" stroke="{INK2}" stroke-width="6" stroke-linecap="round"/>')
    b.append(f'<line x1="{cx}" y1="{cy-r-26}" x2="{cx}" y2="{cy-r-10}" stroke="{INK2}" stroke-width="6" stroke-linecap="round"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{WHITE}" stroke="{TEAL}" stroke-width="6"/>')
    for k in range(12):
        a=math.radians(k*30); x1=cx+(r-10)*math.sin(a); y1=cy-(r-10)*math.cos(a); x2=cx+r*math.sin(a); y2=cy-r*math.cos(a)
        b.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{BOXS}" stroke-width="2"/>')
    # hand pointing just past 12 (a few seconds)
    a=math.radians(38); b.append(f'<line x1="{cx}" y1="{cy}" x2="{cx+(r-22)*math.sin(a):.0f}" y2="{cy-(r-22)*math.cos(a):.0f}" stroke="{RED}" stroke-width="4" stroke-linecap="round"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="6" fill="{INK}"/>')
    b.append(t(cx,cy+r+34,"under 60 seconds",14,TEAL,800,"middle"))
    # comparison bars
    bx=360; b.append(t(bx,150,"Time to first response",13,INK,800))
    b.append(box(bx,170,90,30,TEAL,TEAL,8)); b.append(t(bx+45,191,"Biloop",12,WHITE,700,"middle")); b.append(t(bx+102,191,"< 1 min",12.5,INK2,700))
    b.append(box(bx,212,520,30,"#fde2e4","#f6b9c2",8)); b.append(t(bx+14,233,"Manual follow-up",12,RED,700)); b.append(t(bx+360,233,"hours → next day",12.5,RED,700))
    b.append(box(bx,266,540,90,WASH,LINE,12))
    b.append(t(bx+18,292,"Why it matters",13,INK,800))
    b.append(t(bx+18,316,"Leads contacted in the first minute are far more likely to",12.5,INK2,500))
    b.append(t(bx+18,336,"convert. Biloop makes “first” the default — without extra headcount.",12.5,INK2,500))
    save("real-estate-speed.svg",1040,400,"".join(b))

def realestate_portfolio():
    b=[]; head(b,"One live view of the whole portfolio",
        "Occupancy, yield and arrears for every asset — ask in plain language.")
    cols=6; rows=3; cw=86; ch=70; gx=58; gy=110; gap=12
    import random; random.seed(7)
    pal=[GREEN,TEAL,AMBER,RED]
    vals=[GREEN,GREEN,TEAL,GREEN,AMBER,TEAL, TEAL,GREEN,GREEN,AMBER,GREEN,RED, GREEN,TEAL,AMBER,GREEN,TEAL,GREEN]
    for i in range(cols*rows):
        r=i//cols; c=i%cols; x=gx+c*(cw+gap); y=gy+r*(ch+gap); col=vals[i]
        b.append(box(x,y,cw,ch,WHITE,BOXS,10))
        b.append(f'<rect x="{x}" y="{y}" width="{cw}" height="8" rx="4" fill="{col}"/>')
        # tiny building glyph
        bx=x+cw/2
        b.append(f'<rect x="{bx-13}" y="{y+24}" width="26" height="34" rx="3" fill="none" stroke="{col}" stroke-width="2"/>')
        for wy in (y+30,y+40,y+50):
            for wx in (bx-7,bx,bx+7):
                b.append(f'<rect x="{wx-2}" y="{wy}" width="4" height="4" fill="{col}"/>')
    # legend + query callout
    ly=gy+rows*(ch+gap)+8
    for i,(c,lab) in enumerate([(GREEN,"Strong"),(TEAL,"Steady"),(AMBER,"Watch"),(RED,"Underperforming")]):
        lx=58+i*150; b.append(f'<rect x="{lx}" y="{ly-10}" width="14" height="14" rx="3" fill="{c}"/>'); b.append(t(lx+20,ly+2,lab,12,INK2,600))
    b.append(box(700,108,280,150,WASH,LINE,12))
    b.append(t(716,136,"Just ask",13,INK,800))
    for i,q in enumerate(["“Highest arrears this quarter?”","“Net yield by building?”","“Vacancies over 30 days?”"]):
        b.append(t(716,162+i*26,q,12.5,BLUE,500))
    save("real-estate-portfolio.svg",1040,400,"".join(b))

# ============================================================ AMC
def amc_dispatch():
    b=[adefs(AMBER,"am")]; head(b,"The right tech, right parts, shortest route",
        "Biloop assigns by skill, location, parts and SLA — minimising drive time.")
    # map backdrop
    mx,my,mw,mh=60,100,920,250
    b.append(box(mx,my,mw,mh,WASH,LINE,14))
    for gx in range(mx+40,mx+mw,70): b.append(f'<line x1="{gx}" y1="{my}" x2="{gx}" y2="{my+mh}" stroke="{LINE}" stroke-width="1"/>')
    for gy in range(my+40,my+mh,70): b.append(f'<line x1="{mx}" y1="{gy}" x2="{mx+mw}" y2="{gy}" stroke="{LINE}" stroke-width="1"/>')
    depot=(140,300); jobs=[(330,180,"HVAC"),(540,250,"Lift"),(720,150,"Genset"),(880,260,"Chiller")]
    order=[depot]+[(j[0],j[1]) for j in jobs]
    path="M"+" L".join(f"{x},{y}" for x,y in order)
    b.append(f'<path d="{path}" fill="none" stroke="{AMBER}" stroke-width="3" stroke-dasharray="2 0" marker-end="url(#am)"/>')
    # depot
    b.append(f'<rect x="{depot[0]-22}" y="{depot[1]-22}" width="44" height="44" rx="8" fill="{BLUE}"/>')
    b.append(t(depot[0],depot[1]+5,"⌂",20,WHITE,800,"middle")); b.append(t(depot[0],depot[1]+38,"Depot",12,INK2,700,"middle"))
    for i,(x,y,lab) in enumerate(jobs):
        b.append(f'<circle cx="{x}" cy="{y}" r="16" fill="{WHITE}" stroke="{AMBER}" stroke-width="3"/>')
        b.append(t(x,y+5,str(i+1),13,AMBER,800,"middle"))
        b.append(box(x-44,y-46,88,24,WHITE,BOXS,7)); b.append(t(x,y-29,lab,11.5,INK2,700,"middle"))
    b.append(box(mx+mw-210,my+mh-44,200,32,GREENF,GREENS,8)); b.append(t(mx+mw-110,my+mh-23,"drive time minimised",12,"#0f5132",700,"middle"))
    save("amc-dispatch.svg",1040,380,"".join(b))

def amc_sla():
    b=[adefs(GREEN,"as")]; head(b,"Every job measured against its SLA",
        "Response and resolution tracked live against the contract.")
    x0,x1,y=110,980,200; deadline=8.0
    def dx(h): return x0+(x1-x0)*h/deadline
    b.append(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{BOXS}" stroke-width="3"/>')
    # progress (resolved at 7h, within 8h SLA)
    b.append(f'<line x1="{x0}" y1="{y}" x2="{dx(7):.0f}" y2="{y}" stroke="{GREEN}" stroke-width="6" stroke-linecap="round"/>')
    pts=[(0,"Logged"),(2,"Responded"),(5,"On-site"),(7,"Resolved")]
    for h,lab in pts:
        b.append(f'<circle cx="{dx(h):.0f}" cy="{y}" r="9" fill="{WHITE}" stroke="{GREEN}" stroke-width="3"/>')
        b.append(t(dx(h),y-22,lab,12.5,INK,700,"middle")); b.append(t(dx(h),y+30,f"{h}h",11.5,MUTED,600,"middle"))
    # deadline marker
    b.append(f'<line x1="{dx(8):.0f}" y1="{y-40}" x2="{dx(8):.0f}" y2="{y+40}" stroke="{RED}" stroke-width="2.5" stroke-dasharray="5 4"/>')
    b.append(t(dx(8),y-50,"SLA deadline 8h",12,RED,700,"middle"))
    b.append(box(x0,y+70,300,40,GREENF,GREENS,10)); b.append(t(x0+150,y+95,"Resolved with 1h to spare",13,"#0f5132",800,"middle"))
    b.append(box(x0+330,y+70,260,40,WASH,LINE,10)); b.append(t(x0+460,y+95,"Disputes settled with data",12.5,INK2,700,"middle"))
    save("amc-sla.svg",1040,340,"".join(b))

def amc_renewals():
    b=[adefs(BLUE,"an")]; head(b,"No renewal ever slips",
        "Biloop surfaces every contract months ahead and drafts the uplift.")
    x0,x1,y0,dy=150,980,130,56
    months=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    def mx(m): return x0+(x1-x0)*m/11
    for i,m in enumerate(months):
        b.append(t(mx(i),112,m,11,MUTED,600,"middle"))
        b.append(f'<line x1="{mx(i):.0f}" y1="120" x2="{mx(i):.0f}" y2="{y0+4*dy-20}" stroke="{LINE}" stroke-width="1"/>')
    # contracts: (label, end_month)
    cons=[("Tower A · HVAC",4),("Mall · Lifts",7),("Plant · Gensets",9),("Clinic · Chillers",11)]
    for i,(lab,em) in enumerate(cons):
        y=y0+i*dy
        b.append(box(x0,y,mx(em)-x0,32,BOXF,BOXS,8)); b.append(t(x0+12,y+21,lab,12.5,INK2,700))
        # nudge ~2 months before end
        nx=mx(max(em-2,0))
        b.append(f'<circle cx="{nx:.0f}" cy="{y+16}" r="12" fill="{WHITE}" stroke="{BLUE}" stroke-width="2.5"/>')
        b.append(bell(nx,y+15,BLUE))
        b.append(f'<circle cx="{mx(em):.0f}" cy="{y+16}" r="6" fill="{GREEN}"/>')
    ly=y0+4*dy+6
    b.append(bell(x0+8,ly-4,BLUE)); b.append(t(x0+24,ly,"Biloop nudge (≈60 days out)",12,MUTED,600))
    b.append(f'<circle cx="{x0+268}" cy="{ly-4}" r="5" fill="{GREEN}"/>'); b.append(t(x0+280,ly,"renewal secured",12,MUTED,600))
    save("amc-renewals.svg",1040,400,"".join(b))

# ============================================================ OIL & GAS
def og_predict():
    b=[adefs(RED,"or")]; head(b,"Biloop hears failure coming",
        "Rising vibration is detected weeks before the breakdown — so the fix is planned.")
    x0,x1,mid=70,980,230;
    # normal band
    b.append(f'<rect x="{x0}" y="{mid-26}" width="{x1-x0}" height="52" rx="8" fill="{TEAL}" opacity="0.07"/>')
    b.append(t(x0+8,mid-32,"normal band",11.5,TEAL,700))
    # signal: amplitude grows toward right
    pts=[]
    N=120
    for i in range(N+1):
        x=x0+(x1-x0)*i/N
        frac=i/N
        amp=10+ frac*frac*70
        y=mid - amp*math.sin(i*0.6)
        pts.append((x,y))
    d="M"+" L".join(f"{x:.1f},{y:.1f}" for x,y in pts)
    b.append(f'<path d="{d}" fill="none" stroke="{BLUE}" stroke-width="2.2"/>')
    # anomaly marker
    ax=x0+(x1-x0)*0.62
    b.append(f'<line x1="{ax:.0f}" y1="120" x2="{ax:.0f}" y2="340" stroke="{AMBER}" stroke-width="2" stroke-dasharray="5 4"/>')
    b.append(f'<circle cx="{ax:.0f}" cy="{mid-46}" r="7" fill="{AMBER}"/>'); b.append(t(ax-8,112,"anomaly detected",12,"#9a6a06",700,"end"))
    # failure zone
    fz=x1-90
    b.append(f'<rect x="{fz}" y="120" width="{x1-fz}" height="220" rx="8" fill="{RED}" opacity="0.10"/>')
    b.append(t((fz+x1)/2,112,"failure",12,RED,700,"middle"))
    # lead-time window
    b.append(f'<path d="M{ax:.0f},330 L{fz},330" fill="none" stroke="{GREEN}" stroke-width="2" marker-end="url(#or)"/>')
    b.append(t((ax+fz)/2,350,"lead time to plan the fix — weeks of warning",12,GREEN,700,"middle"))
    save("oil-and-gas-predict.svg",1040,380,"".join(b))

def og_schematic():
    b=[adefs(BLUE,"os")]; head(b,"Live asset health, wellhead to refinery",
        "Sensors on every asset stream into one operations view.")
    y=190; nodes=[("Wellhead",GREEN),("Separator",GREEN),("Compressor",AMBER),("Pipeline",GREEN),("Refinery",GREEN)]
    n=len(nodes); x0,x1=110,930;
    xs=[x0+(x1-x0)*i/(n-1) for i in range(n)]
    # pipe
    b.append(f'<line x1="{xs[0]}" y1="{y}" x2="{xs[-1]}" y2="{y}" stroke="{BOXS}" stroke-width="8" stroke-linecap="round"/>')
    for i,(lab,c) in enumerate(nodes):
        x=xs[i]
        b.append(f'<circle cx="{x:.0f}" cy="{y}" r="26" fill="{WHITE}" stroke="{c}" stroke-width="4"/>')
        b.append(f'<circle cx="{x:.0f}" cy="{y}" r="8" fill="{c}"/>')
        b.append(t(x,y-40,lab,12.5,INK,700,"middle"))
        # sensor dot
        b.append(t(x,y+48,"sensor",10.5,MUTED,500,"middle"))
        # data line down to engine bar
        b.append(f'<line x1="{x:.0f}" y1="{y+26}" x2="{x:.0f}" y2="300" stroke="{c}" stroke-width="1.6" stroke-dasharray="3 3"/>')
    # compressor alert
    cxw=xs[2]
    b.append(f'<path d="M{cxw:.0f},{y-76} l-9,16 h18 z" fill="{AMBER}"/>'); b.append(t(cxw,y-80,"watch",10.5,"#9a6a06",700,"middle"))
    # engine bar
    b.append(box(110,300,820,46,"#eef3ff","#c7d6f5",12)); b.append(t(520,328,"Biloop · unified operations view",13.5,BLUE,800,"middle"))
    # legend
    for i,(c,lab) in enumerate([(GREEN,"Healthy"),(AMBER,"Watch"),(RED,"Alert")]):
        lx=110+i*150; b.append(f'<circle cx="{lx}" cy="100" r="6" fill="{c}"/>'); b.append(t(lx+12,104,lab,12,INK2,600))
    save("oil-and-gas-schematic.svg",1040,380,"".join(b))

def og_downtime():
    b=[]; head(b,"Unplanned is the expensive path",
        "Catching it early turns a costly shutdown into a planned, cheap fix.")
    x0=300
    b.append(t(60,178,"Unplanned",13,RED,800)); b.append(t(60,196,"failure",13,RED,800))
    b.append(box(x0,160,600,46,"#fde2e4","#f6b9c2",10)); b.append(t(x0+20,189,"halted production · emergency crew · collateral damage",12.5,RED,700))
    b.append(t(920,189,"$$$",18,RED,800,"end"))
    b.append(t(60,258,"Planned fix",13,GREEN,800)); b.append(t(60,276,"(predicted)",13,GREEN,800))
    b.append(box(x0,240,150,46,GREENF,GREENS,10)); b.append(t(x0+75,269,"scheduled",12.5,"#0f5132",700,"middle"))
    b.append(t(x0+170,269,"during planned downtime",12.5,INK2,600))
    b.append(t(920,269,"$",18,GREEN,800,"end"))
    b.append(box(60,320,890,46,WASH,LINE,12)); b.append(t(505,348,"Predictive maintenance can cut the cost of a failure by an order of magnitude (illustrative).",12.5,INK2,600,"middle"))
    save("oil-and-gas-downtime.svg",1040,400,"".join(b))

def main():
    pharmacy_forecast(); pharmacy_expiry(); pharmacy_audit()
    accounting_extract(); accounting_close(); accounting_reconcile()
    realestate_funnel(); realestate_speed(); realestate_portfolio()
    amc_dispatch(); amc_sla(); amc_renewals()
    og_predict(); og_schematic(); og_downtime()
    print("generated 15 bespoke diagrams in", os.path.normpath(OUT))

if __name__=="__main__":
    main()
