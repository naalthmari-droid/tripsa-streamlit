"""TRIPSA — Elegant theme + animations (custom CSS injected into Streamlit)."""

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

:root{
  --sand:#f6f1e7; --ink:#1c2b21; --olive:#2f5233; --olive2:#3e6b44;
  --gold:#c9a24b; --gold2:#e3c878; --card:#ffffff; --muted:#6b7560;
}
html,body,[class*="css"]{font-family:'Poppins',sans-serif !important;}
.stApp{background:linear-gradient(160deg,#f8f4ea 0%,#f2ecdd 50%,#eef0e6 100%);color:var(--ink);}
#MainMenu,footer,header{visibility:hidden;}

/* ---------- Hero ---------- */
.hero{
  position:relative;padding:64px 40px;border-radius:28px;overflow:hidden;
  background:linear-gradient(120deg,#22402a 0%,#2f5233 45%,#3e6b44 100%);
  color:#f4efe2;box-shadow:0 24px 60px -18px rgba(34,64,42,.45);
  animation:fadeUp .8s cubic-bezier(.22,1,.36,1) both;
}
.hero::before{
  content:"";position:absolute;inset:0;
  background:radial-gradient(circle at 85% 20%,rgba(227,200,120,.28),transparent 45%),
             radial-gradient(circle at 10% 90%,rgba(227,200,120,.14),transparent 40%);
}
.hero h1{font-size:52px;font-weight:800;line-height:1.05;margin:0;letter-spacing:-1px;
  background:linear-gradient(90deg,#fff,#e3c878);-webkit-background-clip:text;background-clip:text;color:transparent;}
.hero p{font-size:18px;color:#e9e4d2;max-width:560px;margin-top:16px;font-weight:300;}
.brand{display:inline-flex;align-items:center;gap:10px;font-weight:700;letter-spacing:3px;
  font-size:15px;color:var(--gold2);text-transform:uppercase;}
.brand .dot{width:10px;height:10px;border-radius:50%;background:var(--gold2);
  box-shadow:0 0 0 0 rgba(227,200,120,.6);animation:pulse 2s infinite;}

/* ---------- Cards ---------- */
.card{
  background:var(--card);border-radius:20px;padding:24px;border:1px solid #ece5d2;
  box-shadow:0 10px 30px -12px rgba(28,43,33,.12);
  transition:transform .3s cubic-bezier(.22,1,.36,1),box-shadow .3s;
  animation:fadeUp .7s cubic-bezier(.22,1,.36,1) both;
}
.card:hover{transform:translateY(-6px);box-shadow:0 22px 44px -14px rgba(47,82,51,.28);}
.card h3{margin:0 0 6px;font-size:20px;font-weight:700;color:var(--olive);}
.card .sub{color:var(--muted);font-size:14px;font-weight:300;}

/* metric chips */
.metric{background:linear-gradient(135deg,#fff,#f7f2e4);border:1px solid #eee4c9;
  border-radius:16px;padding:16px;text-align:center;animation:fadeUp .8s both;}
.metric .v{font-size:26px;font-weight:800;color:var(--olive);}
.metric .l{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:1px;}

/* stop timeline */
.stop{display:flex;gap:16px;position:relative;padding:18px 0;animation:fadeUp .6s both;}
.stop .num{flex:0 0 40px;height:40px;border-radius:50%;background:var(--olive);color:#fff;
  display:flex;align-items:center;justify-content:center;font-weight:700;
  box-shadow:0 6px 14px -4px rgba(47,82,51,.5);}
.stop .body{flex:1;background:var(--card);border:1px solid #ece5d2;border-radius:16px;padding:16px 18px;}
.stop .body h4{margin:0;color:var(--olive);font-size:18px;}
.tag{display:inline-block;background:#f1ead6;color:var(--olive);border-radius:999px;
  padding:3px 12px;font-size:12px;margin:3px 6px 0 0;font-weight:500;}

/* invite code */
.invite{font-family:'Poppins',monospace;font-size:30px;font-weight:800;letter-spacing:4px;
  color:var(--olive);background:linear-gradient(135deg,#f3edda,#e9f0e6);
  border:2px dashed var(--gold);border-radius:16px;padding:18px;text-align:center;
  animation:glow 2.4s ease-in-out infinite;}

/* schedule rows */
.act{display:flex;align-items:center;gap:12px;padding:10px 14px;border-radius:12px;
  background:#fbf9f2;border:1px solid #f0e9d6;margin-bottom:8px;animation:slideIn .5s both;}
.act .t{font-family:monospace;font-weight:700;color:var(--olive);min-width:110px;font-size:13px;}
.act .dotm{width:9px;height:9px;border-radius:50%;background:var(--gold);}
.act.meal{background:#f3efe2;}
.act .star{color:var(--gold);font-weight:700;font-size:12px;}

/* buttons */
.stButton>button{
  background:linear-gradient(135deg,var(--olive),var(--olive2));color:#fff;border:none;
  border-radius:14px;padding:12px 28px;font-weight:600;font-size:16px;letter-spacing:.3px;
  transition:transform .18s cubic-bezier(.22,1,.36,1),box-shadow .2s;
  box-shadow:0 10px 24px -8px rgba(47,82,51,.5);}
.stButton>button:hover{transform:translateY(-2px) scale(1.02);box-shadow:0 16px 32px -8px rgba(47,82,51,.6);}
.stButton>button:active{transform:scale(.97);}

/* section title */
.sec{font-size:26px;font-weight:800;color:var(--ink);margin:34px 0 14px;
  display:flex;align-items:center;gap:12px;animation:fadeUp .6s both;}
.sec::before{content:"";width:6px;height:28px;border-radius:4px;
  background:linear-gradient(180deg,var(--gold),var(--olive));}

/* animations */
@keyframes fadeUp{from{opacity:0;transform:translateY(24px)}to{opacity:1;transform:translateY(0)}}
@keyframes slideIn{from{opacity:0;transform:translateX(-18px)}to{opacity:1;transform:translateX(0)}}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(227,200,120,.55)}70%{box-shadow:0 0 0 14px rgba(227,200,120,0)}100%{box-shadow:0 0 0 0 rgba(227,200,120,0)}}
@keyframes glow{0%,100%{box-shadow:0 0 0 0 rgba(201,162,75,.0)}50%{box-shadow:0 0 26px 2px rgba(201,162,75,.35)}}

/* stagger children */
.stagger>*{animation:fadeUp .6s both;}
.stagger>*:nth-child(1){animation-delay:.05s}.stagger>*:nth-child(2){animation-delay:.12s}
.stagger>*:nth-child(3){animation-delay:.19s}.stagger>*:nth-child(4){animation-delay:.26s}
.stagger>*:nth-child(5){animation-delay:.33s}.stagger>*:nth-child(6){animation-delay:.40s}

/* ---------- Extra polish ---------- */
/* animated progress bars */
.stProgress > div > div > div{background:linear-gradient(90deg,var(--olive),var(--gold));
  border-radius:8px;transition:width .8s cubic-bezier(.22,1,.36,1);}

/* inputs */
.stTextInput input,.stNumberInput input,.stSelectbox div[data-baseweb]{
  border-radius:12px !important;border:1px solid #e3dcc6 !important;
  transition:border-color .2s,box-shadow .2s;}
.stTextInput input:focus,.stNumberInput input:focus{
  border-color:var(--olive) !important;box-shadow:0 0 0 3px rgba(47,82,51,.15) !important;}

/* sliders */
.stSlider [role="slider"]{background:var(--olive) !important;box-shadow:0 4px 10px -2px rgba(47,82,51,.5);}

/* tabs / radio */
.stRadio label{font-weight:500;}

/* expander */
.streamlit-expanderHeader{font-weight:600;color:var(--olive);border-radius:12px;
  transition:background .2s;}
.streamlit-expanderHeader:hover{background:#f3efe0;}

/* floating back-to-top feel for headers */
.sec{position:relative;}

/* shimmer on hero */
.hero::after{content:"";position:absolute;top:0;left:-60%;width:40%;height:100%;
  background:linear-gradient(100deg,transparent,rgba(255,255,255,.12),transparent);
  animation:shimmer 3.5s infinite;}
@keyframes shimmer{0%{left:-60%}100%{left:130%}}

/* consensus ring */
.ring{position:relative;width:120px;height:120px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;margin:auto;
  background:conic-gradient(var(--olive) calc(var(--p)*1%),#eee4c9 0);
  animation:fadeUp .7s both;}
.ring::before{content:"";position:absolute;inset:10px;border-radius:50%;background:#fff;}
.ring .rv{position:relative;font-size:28px;font-weight:800;color:var(--olive);}

/* toast-like badges */
.pill{display:inline-flex;align-items:center;gap:6px;background:#eef3ea;color:var(--olive);
  border:1px solid #d7e2cf;border-radius:999px;padding:5px 14px;font-size:13px;font-weight:600;
  animation:slideIn .5s both;}

/* map card */
.mapwrap{border-radius:20px;overflow:hidden;border:1px solid #ece5d2;
  box-shadow:0 14px 34px -14px rgba(28,43,33,.2);animation:fadeUp .8s both;}
</style>
"""

# Lottie animation URLs (free, from lottiefiles)
LOTTIE = {
    "travel": "https://assets9.lottiefiles.com/packages/lf20_zw0djhar.json",
    "map": "https://assets2.lottiefiles.com/packages/lf20_06a6pf9i.json",
    "compass": "https://assets5.lottiefiles.com/packages/lf20_49dzk0.json",
    "group": "https://assets8.lottiefiles.com/packages/lf20_t24tpvcu.json",
    "success": "https://assets1.lottiefiles.com/packages/lf20_jbrw3hcz.json",
}
