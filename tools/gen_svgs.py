#!/usr/bin/env python3
"""Generate the light-themed SVG visual system for the Biloop/Medloop site."""
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "img")
FONT = "Segoe UI, Roboto, Helvetica, Arial, sans-serif"

# palette
WHITE="#ffffff"; INK="#1a1a1a"; INK2="#374151"; MUTED="#6b7280"
LINE="#e3e8f0"; BOXF="#f5f8ff"; BOXS="#dbe4f3"
BLUE="#2563eb"; TEAL="#0ea5a4"; AMBER="#f59e0b"; PURPLE="#7c3aed"; GREEN="#16a34a"
AIF="#eef3ff"; AIS="#c7d6f5"; OUTF="#f0fbf7"; OUTS="#bfe6d8"; OUTT="#0f5132"

def esc(s):
    return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def t(x,y,s,size,fill,weight=400,anchor="start"):
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
            f'fill="{fill}" font-weight="{weight}" text-anchor="{anchor}">{esc(s)}</text>')

def box(x,y,w,h,fill,stroke,r=10,sw=1):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'

def arrow_defs(color=BLUE):
    return (f'<marker id="ar" markerWidth="12" markerHeight="12" refX="8" refY="4" '
            f'orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0 L9,4 L0,8 Z" fill="{color}"/></marker>')

def hline(x1,x2,y,color=BLUE):
    return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{color}" stroke-width="2.5" marker-end="url(#ar)"/>'

def frame(w,h):
    return f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="18" fill="{WHITE}" stroke="{LINE}"/>'

def save(name, vb_w, vb_h, body, defs=""):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vb_w} {vb_h}" '
           f'font-family="{FONT}">\n<defs>{defs}</defs>\n{frame(vb_w,vb_h)}\n{body}\n</svg>\n')
    with open(os.path.join(OUT,name),"w",encoding="utf-8") as f:
        f.write(svg)

DOTS=[BLUE,TEAL,AMBER,PURPLE]

# ---------------- 3-stage industry architecture ----------------
def arch(name, title, datain, ai, outcomes, users, product="Biloop"):
    b=[arrow_defs()]
    b.append(t(40,48,title,24,INK,800))
    b.append(t(40,92,"Data In",13,BLUE,700))
    b.append(t(400,92,f"{product} AI Engine",13,BLUE,700))
    b.append(t(760,92,"Outcomes",13,BLUE,700))
    ys=[108,180,252,324]
    for i,lab in enumerate(datain):
        b.append(box(40,ys[i],260,56,BOXF,BOXS)); b.append(t(62,ys[i]+34,lab,14.5,INK2,600))
    b.append(hline(308,386,240))
    b.append(box(392,100,276,296,AIF,AIS,16,1.5))
    cy=[120,186,252,318]
    for i,lab in enumerate(ai):
        b.append(box(410,cy[i],240,56,WHITE,BOXS))
        b.append(f'<circle cx="432" cy="{cy[i]+28}" r="6" fill="{DOTS[i]}"/>')
        b.append(t(448,cy[i]+33,lab,14.5,INK,700))
    b.append(hline(676,754,240))
    for i,lab in enumerate(outcomes):
        b.append(box(760,ys[i],240,56,OUTF,OUTS)); b.append(t(782,ys[i]+34,lab,14.5,OUTT,600))
    b.append(box(40,436,960,84,"#f8fafc",LINE,14))
    b.append(t(64,470,"Who uses it",13,BLUE,700))
    b.append(t(64,500,users,14,MUTED,600))
    save(f"{name}-architecture.svg",1040,560,"\n".join(b))

# ---------------- flow ----------------
def flow(name, title, steps, accent=BLUE):
    b=[arrow_defs(accent)]
    b.append(t(40,46,title,22,INK,800))
    x0=24; pitch=210; bw=176; y=92; h=132
    for i,(st,sub) in enumerate(steps):
        x=x0+i*pitch
        b.append(box(x,y,bw,h,BOXF,BOXS,14))
        b.append(f'<circle cx="{x+28}" cy="{y+30}" r="15" fill="{accent}"/>')
        b.append(t(x+28,y+35,str(i+1),15,WHITE,800,"middle"))
        b.append(t(x+16,y+74,st,15,INK,700))
        # subtitle up to 2 short lines split on '|'
        parts=sub.split("|")
        b.append(t(x+16,y+100,parts[0],12,MUTED,500))
        if len(parts)>1: b.append(t(x+16,y+118,parts[1],12,MUTED,500))
        if i<len(steps)-1:
            b.append(hline(x+bw,x+pitch-2,y+58,accent))
    save(f"{name}-flow.svg",1100,272,"\n".join(b))

# ---------------- impact infographic ----------------
def impact(name, title, stats, accent=BLUE):
    b=[]
    b.append(t(40,46,title,22,INK,800))
    tw=300; gap=32; x0=40; y=86; h=176
    cols=[accent,TEAL,AMBER]
    for i,(num,lab) in enumerate(stats):
        x=x0+i*(tw+gap); c=cols[i%len(cols)]; cx=x+tw/2
        b.append(box(x,y,tw,h,"#f7faff",BOXS,16))
        b.append(f'<rect x="{x}" y="{y}" width="{tw}" height="7" rx="3.5" fill="{c}"/>')
        b.append(f'<circle cx="{cx}" cy="{y+50}" r="20" fill="{c}" opacity="0.14"/>')
        b.append(f'<circle cx="{cx}" cy="{y+50}" r="7" fill="{c}"/>')
        b.append(t(cx,y+112,num,38,INK,800,"middle"))
        parts=lab.split("|")
        b.append(t(cx,y+142,parts[0],15,MUTED,600,"middle"))
        if len(parts)>1: b.append(t(cx,y+162,parts[1],15,MUTED,600,"middle"))
    save(f"{name}-impact.svg",1040,300,"\n".join(b))

# ---------------- banner (light, homepage thumbnails) ----------------
def banner(name, emoji, title, tag, accent=BLUE, product="Biloop"):
    defs=(f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
          f'<stop offset="0" stop-color="{accent}" stop-opacity="0.10"/>'
          f'<stop offset="1" stop-color="{accent}" stop-opacity="0.02"/></linearGradient>')
    b=[]
    b.append(f'<rect x="0" y="0" width="1200" height="240" fill="{WHITE}"/>')
    b.append(f'<rect x="0" y="0" width="1200" height="240" fill="url(#bg)"/>')
    b.append(f'<circle cx="980" cy="120" r="150" fill="{accent}" opacity="0.06"/>')
    b.append(f'<circle cx="980" cy="120" r="92" fill="{WHITE}" stroke="{accent}" stroke-width="3"/>')
    b.append(f'<text x="980" y="150" text-anchor="middle" font-size="84">{emoji}</text>')
    b.append(t(64,112,title,46,INK,800))
    b.append(t(64,150,tag,20,accent,700))
    sub = "Biloop · AI-powered transformation" if product=="Biloop" else f"{product} by Biloop · AI-powered transformation"
    b.append(t(64,194,sub,17,MUTED,600))
    save(f"{name}-banner.svg",1200,240,"\n".join(b),defs)

# ---------------- hero (light hub & spoke) ----------------
def hero():
    sats=[(190,96,"\U0001F48A"),(160,300,"\U0001F4CA"),(500,56,"\U0001F3E2"),
          (820,108,"\U0001F6E0️"),(840,320,"\U0001F6E2️"),
          (320,372,"\U0001F4C8"),(690,378,"\U0001F916")]
    b=[f'<rect x="0" y="0" width="1000" height="430" fill="{WHITE}"/>']
    for x,y,e in sats:
        b.append(f'<line x1="500" y1="215" x2="{x}" y2="{y}" stroke="#d6e0f5" stroke-width="2"/>')
    for x,y,e in sats:
        r=34 if y<360 else 26
        b.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{BOXF}" stroke="{BOXS}"/>')
        b.append(f'<text x="{x}" y="{y+8}" text-anchor="middle" font-size="{24 if r==34 else 19}">{e}</text>')
    b.append(f'<circle cx="500" cy="215" r="88" fill="{WHITE}" stroke="{BLUE}" stroke-width="3"/>')
    b.append(f'<circle cx="500" cy="215" r="62" fill="none" stroke="{BOXS}" stroke-width="1.5" stroke-dasharray="4 6"/>')
    b.append(t(500,208,"Biloop",28,INK,800,"middle"))
    b.append(t(500,234,"AI Engine",14,MUTED,600,"middle"))
    save("hero.svg",1000,430,"\n".join(b))

# ---------------- capabilities icon strip ----------------
def capabilities():
    cells=[
        ("Unify","Connect every source",BLUE,"unify"),
        ("Automate","Agents do the work",TEAL,"auto"),
        ("Predict","See problems early",AMBER,"pred"),
        ("Decide","Answers in plain language",PURPLE,"dec"),
    ]
    b=[]
    cw=244; gap=16; x0=24; y=24; ch=132
    for i,(name,sub,c,kind) in enumerate(cells):
        x=x0+i*(cw+gap); cx=x+cw/2
        b.append(box(x,y,cw,ch,BOXF,BOXS,16))
        # icon badge
        b.append(f'<circle cx="{cx}" cy="{y+40}" r="24" fill="{c}" opacity="0.12"/>')
        ix,iy=cx,y+40
        if kind=="unify":
            b.append(f'<circle cx="{ix-9}" cy="{iy-6}" r="5" fill="none" stroke="{c}" stroke-width="2.5"/>')
            b.append(f'<circle cx="{ix+9}" cy="{iy-6}" r="5" fill="none" stroke="{c}" stroke-width="2.5"/>')
            b.append(f'<path d="M{ix-9} {iy-1} L{ix} {iy+10} L{ix+9} {iy-1}" fill="none" stroke="{c}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>')
        elif kind=="auto":
            b.append(f'<rect x="{ix-11}" y="{iy-9}" width="22" height="18" rx="5" fill="none" stroke="{c}" stroke-width="2.5"/>')
            b.append(f'<line x1="{ix}" y1="{iy-9}" x2="{ix}" y2="{iy-15}" stroke="{c}" stroke-width="2.5"/>')
            b.append(f'<circle cx="{ix}" cy="{iy-17}" r="2.4" fill="{c}"/>')
            b.append(f'<circle cx="{ix-5}" cy="{iy-1}" r="2.4" fill="{c}"/><circle cx="{ix+5}" cy="{iy-1}" r="2.4" fill="{c}"/>')
        elif kind=="pred":
            b.append(f'<polyline points="{ix-12},{iy+9} {ix-3},{iy} {ix+3},{iy+5} {ix+12},{iy-10}" fill="none" stroke="{c}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>')
            b.append(f'<path d="M{ix+6} {iy-10} L{ix+12} {iy-10} L{ix+12} {iy-4}" fill="none" stroke="{c}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>')
        else:
            b.append(f'<rect x="{ix-12}" y="{iy-10}" width="24" height="17" rx="5" fill="none" stroke="{c}" stroke-width="2.5"/>')
            b.append(f'<path d="M{ix-4} {iy+7} L{ix-7} {iy+13} L{ix+1} {iy+7}" fill="none" stroke="{c}" stroke-width="2.5" stroke-linejoin="round"/>')
            for dx in (-5,0,5):
                b.append(f'<circle cx="{ix+dx}" cy="{iy-2}" r="1.8" fill="{c}"/>')
        b.append(t(cx,y+90,name,17,INK,800,"middle"))
        b.append(t(cx,y+112,sub,12.5,MUTED,500,"middle"))
    save("capabilities.svg",1040,180,"\n".join(b))

# ---------------- big platform architecture (light) ----------------
def platform():
    b=[arrow_defs()]
    b.append(t(40,50,"Biloop — Platform Architecture",28,INK,800))
    b.append(t(40,78,"Connect every source, automate the work, predict what matters, and put decisions in front of people.",15,MUTED))
    cols=[(40,"Data Sources"),(300,"Unify · Data Layer"),(560,"Biloop AI Engine"),(900,"Decide & Act")]
    for x,lab in cols: b.append(t(x,128,lab,14,BLUE,700))
    src=["ERP / Accounting","POS / Billing","Spreadsheets / Email","IoT / Sensors","Legacy Systems / Docs"]
    sy=[150,214,278,342,406]
    for i,s in enumerate(src):
        b.append(box(40,sy[i],200,50,BOXF,BOXS)); b.append(t(60,sy[i]+30,s,14,INK2,600))
    b.append(hline(248,292,303))
    b.append(box(300,150,200,306,"#f8fafc",LINE,14))
    uni=["Connectors / APIs","Normalize Data","Unified Data Lake","Data Governance"]
    uy=[172,240,308,376]
    for i,u in enumerate(uni):
        b.append(box(318,uy[i],164,56,WHITE,BOXS)); b.append(t(338,uy[i]+34,u,14,INK2,600))
    b.append(hline(508,552,303))
    b.append(box(558,148,284,310,AIF,AIS,16,1.5))
    caps=[("Automate","AI agents · workflows · RPA",BLUE),
          ("Predict","Forecasts · anomaly detection",TEAL),
          ("Document AI","Extract · classify · validate",AMBER),
          ("Decide","Conversational analytics",PURPLE)]
    cyy=[172,240,308,376]
    for i,(nm,ds,c) in enumerate(caps):
        b.append(box(578,cyy[i],244,58,WHITE,BOXS))
        b.append(f'<circle cx="600" cy="{cyy[i]+29}" r="6" fill="{c}"/>')
        b.append(t(616,cyy[i]+25,nm,15,INK,700)); b.append(t(616,cyy[i]+44,ds,12.5,MUTED))
    b.append(hline(850,894,303))
    dec=["Live Dashboards","Conversational Q&A","Alerts & Actions","Mobile & Portals","APIs & Integrations"]
    for i,d in enumerate(dec):
        b.append(box(900,sy[i],180,50,BOXF,BOXS)); b.append(t(920,sy[i]+30,d,14,INK2,600))
    b.append(box(40,500,1040,120,"#f8fafc",LINE,14))
    b.append(t(64,534,"Built-in across every layer",14,BLUE,700))
    foot=[("Security & Role-based Access",64,236),("Full Audit Trail",316,180),
          ("Human-in-the-loop Approvals",512,252),("Cloud · On-prem · Hybrid",780,300)]
    for lab,x,w in foot:
        b.append(box(x,556,w,44,WHITE,BOXS)); b.append(t(x+18,584,lab,13,INK2,600))
    save("mydo-architecture.svg",1120,660,"\n".join(b))

DATA={
 "pharmacy":{
   "title":"Pharmacy Retail — How Medloop Fits",
   "datain":["POS Sales","Purchases / Suppliers","Batch & Expiry Data","Prescriptions"],
   "ai":["Demand Forecasting","Expiry & FEFO Tracking","Compliance Automation","Margin Intelligence"],
   "out":["Fewer Stockouts","15–30% Less Expiry Loss","Audit-ready Reports","Inter-branch Transfers"],
   "users":"Pharmacists  ·  Branch Managers  ·  Procurement  ·  Owners",
   "accent":BLUE,
   "flow_title":"How a reorder decision happens",
   "flow":[("Ingest","POS + batch|data flow in"),("Forecast","per-SKU,|per-branch demand"),
           ("Flag","low stock &|near-expiry"),("Recommend","reorder or|transfer"),("Act","approve —|fully audited")],
   "impact_title":"What changes, in numbers",
   "impact":[("15–30%","less expiry|write-off"),("~98%","fast-mover|availability"),("Hrs → min","regulatory|reporting")],
 },
 "accounting":{
   "title":"Accounting — How Biloop Fits",
   "datain":["Invoices & Receipts","Bank Feeds","Purchase Orders","Contracts & Statements"],
   "ai":["Document AI Extraction","Continuous Reconciliation","Always-on Controls","Cash-flow Forecasting"],
   "out":["Close in 1–2 Days","~80% Less Keying","Fraud / Error Alerts","Real-time Reporting"],
   "users":"Accountants  ·  Controllers  ·  Audit  ·  CFO & Finance Leaders",
   "accent":PURPLE,
   "flow_title":"From document to ledger",
   "flow":[("Capture","invoice or|receipt arrives"),("Extract","AI reads|every field"),
           ("Validate","match PO &|contract"),("Reconcile","daily auto-|matching"),("Report","live, always|close-ready")],
   "impact_title":"What changes, in numbers",
   "impact":[("5–8d → 1–2d","month-end|close time"),("~80%","invoice data|auto-captured"),("100%","of transactions|controlled")],
 },
 "real-estate":{
   "title":"Real Estate — How Biloop Fits",
   "datain":["Leads (Portals/Web/Chat)","Leases & Title Docs","Maintenance Tickets","Rent & Payments"],
   "ai":["Lead-to-Lease Bot","Contract Intelligence","Predictive Maintenance","Portfolio Analytics"],
   "out":["<60s Lead Response","No Missed Renewals","Higher Asset Value","Live Portfolio View"],
   "users":"Agents  ·  Property Managers  ·  Developers  ·  Owners / Investors",
   "accent":TEAL,
   "flow_title":"From enquiry to booked viewing",
   "flow":[("Capture","lead from any|channel"),("Respond","in under|60 seconds"),
           ("Qualify","budget &|intent"),("Book","viewing in|agent calendar"),("Hand off","warm lead|to agent")],
   "impact_title":"What changes, in numbers",
   "impact":[("<60s","lead|response"),("20–40%","more qualified|viewings"),("Zero","missed lease|renewals")],
 },
 "amc":{
   "title":"AMC & Field Service — How Biloop Fits",
   "datain":["AMC Contracts","Asset Register","IoT Telemetry","Service Requests"],
   "ai":["Contract & SLA Intel","Smart Dispatch & Routing","Predictive Servicing","Parts Forecasting"],
   "out":["Zero Missed Renewals","+20–35% Jobs / Tech","Fewer Emergency Calls","Provable SLA Compliance"],
   "users":"Dispatchers  ·  Field Technicians  ·  Account Managers  ·  Customers",
   "accent":AMBER,
   "flow_title":"From service ticket to proven SLA",
   "flow":[("Logged","request or|sensor alert"),("Match SLA","priority &|deadline"),
           ("Dispatch","right tech +|right parts"),("Resolve","fix, full|history kept"),("Prove","SLA report|& renewal")],
   "impact_title":"What changes, in numbers",
   "impact":[("Zero","missed|renewals"),("+20–35%","jobs per|technician"),("100%","SLA|visibility")],
 },
 "oil-and-gas":{
   "title":"Oil & Gas — How Biloop Fits",
   "datain":["SCADA / Historian","Maintenance Records","HSE & Permits","P&IDs / Manuals"],
   "ai":["Predictive Maintenance","Digital HSE & Permits","Knowledge Search","Operations Intelligence"],
   "out":["Less Unplanned Downtime","Audit-ready Compliance","Retained Knowledge","Cost-per-Barrel View"],
   "users":"Reliability Engineers  ·  HSE Teams  ·  Operations & Plant Leaders",
   "accent":"#0891b2",
   "flow_title":"From sensor signal to prevented shutdown",
   "flow":[("Sense","millions of|readings/day"),("Detect","drift before|failure"),
           ("Alert","with days of|lead time"),("Plan","schedule the|intervention"),("Prevent","fix in planned|downtime")],
   "impact_title":"What changes, in numbers",
   "impact":[("↓ Downtime","fewer unplanned|failures"),("100%","permits &|incidents tracked"),("Weeks","of failure|lead time")],
 },
}

BANNERS={
 "pharmacy":("\U0001F48A","Pharmacy Retail","Smarter inventory · zero expiry surprises",BLUE),
 "accounting":("\U0001F4CA","Accounting","Continuous close · autonomous books",PURPLE),
 "real-estate":("\U0001F3E2","Real Estate","Lead-to-lease · portfolio intelligence",TEAL),
 "amc":("\U0001F6E0️","AMC & Field Service","Predictive service · zero lost renewals",AMBER),
 "oil-and-gas":("\U0001F6E2️","Oil & Gas","Predictive ops · airtight HSE","#0891b2"),
}

def product_for(k):
    # Pharmacy / healthcare is branded "Medloop"; everything else is "Biloop".
    return "Medloop" if k=="pharmacy" else "Biloop"

def main():
    for k,d in DATA.items():
        p=product_for(k)
        arch(k,d["title"],d["datain"],d["ai"],d["out"],d["users"],p)
        flow(k,d["flow_title"],d["flow"],d["accent"])
        impact(k,d["impact_title"],d["impact"],d["accent"])
    for k,(e,ti,tg,c) in BANNERS.items():
        banner(k,e,ti,tg,c,product_for(k))
    hero(); capabilities(); platform()
    print("generated all SVGs in", os.path.normpath(OUT))

if __name__=="__main__":
    main()
