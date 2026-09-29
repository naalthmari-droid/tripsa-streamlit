"""TRIPSA — premium responsive design system for Streamlit."""

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

:root{
  --canvas:#F4F6F3;
  --canvas-2:#ECF2ED;
  --surface:#FFFFFF;
  --surface-soft:#F8FAF8;
  --ink:#10231F;
  --muted:#66766F;
  --pine:#073B33;
  --pine-2:#0C574A;
  --mint:#17C3B2;
  --mint-soft:#DDF8F3;
  --purple:#3A145B;
  --purple-2:#5A2778;
  --gold:#C9A33B;
  --line:rgba(7,59,51,.10);
  --shadow-sm:0 8px 24px rgba(16,35,31,.08);
  --shadow-md:0 18px 48px rgba(16,35,31,.13);
  --shadow-lg:0 30px 80px rgba(7,59,51,.20);
  --ease-out:cubic-bezier(.23,1,.32,1);
}

html,body,[class*="css"]{
  font-family:'Manrope',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif !important;
}
html{scroll-behavior:smooth;}
body{background:var(--canvas);}
.stApp{
  color:var(--ink);
  background:
    radial-gradient(circle at 92% 4%,rgba(23,195,178,.16),transparent 29rem),
    radial-gradient(circle at 7% 20%,rgba(58,20,91,.08),transparent 25rem),
    linear-gradient(180deg,#F9FBF8 0%,var(--canvas) 52%,#EEF3EF 100%);
}
#MainMenu,footer,header{visibility:hidden;}
[data-testid="stAppViewContainer"]>.main .block-container{
  max-width:1240px;padding-top:1.25rem;padding-bottom:4rem;
}

/* ---------- Premium hero ---------- */
.hero{
  position:relative;isolation:isolate;overflow:hidden;
  display:grid;grid-template-columns:minmax(0,1.15fr) minmax(310px,.85fr);gap:34px;
  min-height:470px;padding:54px;border-radius:34px;color:#fff;
  background:
    radial-gradient(circle at 88% 16%,rgba(23,195,178,.42),transparent 25%),
    radial-gradient(circle at 72% 105%,rgba(201,163,59,.22),transparent 30%),
    linear-gradient(135deg,#052F2A 0%,#073B33 42%,#32134F 100%);
  box-shadow:var(--shadow-lg);
  animation:heroIn .7s var(--ease-out) both;
}
.hero::before{
  content:"";position:absolute;inset:0;z-index:-1;opacity:.36;
  background-image:linear-gradient(rgba(255,255,255,.045) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.045) 1px,transparent 1px);
  background-size:42px 42px;mask-image:linear-gradient(90deg,transparent,#000);
}
.hero-copy{position:relative;z-index:2;display:flex;flex-direction:column;justify-content:center;}
.hero-logo-wrap{display:inline-flex;align-items:center;justify-content:center;width:205px;height:72px;padding:7px 15px;margin-bottom:28px;border-radius:19px;background:rgba(255,255,255,.96);box-shadow:0 15px 34px rgba(0,0,0,.18);}
.hero-logo{width:178px;height:56px;object-fit:contain;}
.hero-kicker{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:20px;}
.hero-kicker span{
  display:inline-flex;align-items:center;padding:7px 12px;border-radius:999px;
  border:1px solid rgba(255,255,255,.18);background:rgba(255,255,255,.09);
  color:#EAFDF9;font-size:12px;font-weight:700;letter-spacing:.2px;backdrop-filter:blur(10px);
}
.hero h1{margin:0;max-width:720px;font-size:clamp(42px,5vw,67px);line-height:.99;letter-spacing:-2.5px;font-weight:800;color:#fff;}
.hero h1 .accent{color:var(--mint);}
.hero p{margin:22px 0 0;max-width:670px;font-size:18px;line-height:1.65;color:rgba(255,255,255,.79);font-weight:500;}
.hero-proof{display:flex;gap:22px;flex-wrap:wrap;margin-top:28px;color:#fff;font-size:13px;font-weight:700;}
.hero-proof span{display:flex;align-items:center;gap:7px;}
.hero-proof i{display:block;width:7px;height:7px;border-radius:50%;background:var(--mint);box-shadow:0 0 0 5px rgba(23,195,178,.13);}

.hero-visual{position:relative;display:flex;align-items:center;justify-content:center;min-height:360px;}
.phone-card{
  position:relative;width:100%;max-width:390px;padding:18px;border-radius:30px;
  background:rgba(255,255,255,.95);border:1px solid rgba(255,255,255,.68);
  box-shadow:0 30px 70px rgba(0,0,0,.30);transform:rotate(1.2deg);
  transition:transform .28s var(--ease-out),box-shadow .28s var(--ease-out);
}
.phone-card:hover{transform:rotate(0) translateY(-5px);box-shadow:0 38px 80px rgba(0,0,0,.36);}
.phone-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;color:var(--muted);font-size:11px;font-weight:700;}
.phone-title{font-size:20px;line-height:1.2;color:var(--pine);font-weight:800;margin-bottom:5px;}
.phone-sub{font-size:12px;color:var(--muted);margin-bottom:14px;}
.route-strip{display:flex;align-items:center;gap:7px;padding:11px 12px;border-radius:14px;background:var(--mint-soft);font-size:11px;color:var(--pine);font-weight:800;}
.route-strip b{display:inline-flex;width:22px;height:22px;border-radius:50%;align-items:center;justify-content:center;background:var(--pine);color:#fff;}
.route-strip em{height:2px;flex:1;background:linear-gradient(90deg,var(--mint),var(--gold));}
.mini-day{margin-top:14px;padding:14px;border-radius:18px;background:#F7F8F6;border:1px solid var(--line);}
.mini-day-head{display:flex;justify-content:space-between;color:var(--pine);font-size:12px;font-weight:800;margin-bottom:8px;}
.mini-row{display:grid;grid-template-columns:54px 8px 1fr;align-items:center;gap:8px;padding:9px 4px;border-top:1px solid rgba(7,59,51,.07);font-size:10px;color:var(--ink);}
.mini-row time{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--pine);font-weight:800;}
.mini-row i{width:7px;height:7px;border-radius:50%;background:var(--gold);}
.floating-chip{position:absolute;padding:10px 14px;border-radius:14px;background:#fff;color:var(--purple);font-size:12px;font-weight:800;box-shadow:var(--shadow-md);}
.floating-chip.one{right:-18px;top:34px;transform:rotate(3deg);}
.floating-chip.two{left:-22px;bottom:28px;transform:rotate(-3deg);}

/* ---------- Home sections ---------- */
.home-stats{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:18px 0 8px;}
.home-stat{padding:17px 18px;border-radius:18px;background:rgba(255,255,255,.78);border:1px solid rgba(255,255,255,.9);box-shadow:var(--shadow-sm);backdrop-filter:blur(12px);}
.home-stat b{display:block;color:var(--pine);font-size:25px;line-height:1;font-weight:800;}
.home-stat span{display:block;margin-top:7px;color:var(--muted);font-size:12px;font-weight:700;}
.feature-card{position:relative;overflow:hidden;min-height:174px;padding:25px;border-radius:23px;background:#fff;border:1px solid var(--line);box-shadow:var(--shadow-sm);transition:transform .22s var(--ease-out),box-shadow .22s var(--ease-out),border-color .22s;}
.feature-card:hover{transform:translateY(-5px);box-shadow:var(--shadow-md);border-color:rgba(23,195,178,.38);}
.feature-card .f-icon{display:flex;align-items:center;justify-content:center;width:46px;height:46px;border-radius:14px;background:var(--mint-soft);font-size:22px;margin-bottom:18px;}
.feature-card h3{margin:0 0 9px;color:var(--pine);font-size:20px;font-weight:800;}
.feature-card p{margin:0;color:var(--muted);font-size:14px;line-height:1.55;}
.feature-card::after{content:"";position:absolute;width:96px;height:96px;border-radius:50%;right:-35px;top:-38px;background:rgba(23,195,178,.08);}

/* ---------- Core surfaces ---------- */
.card,.metric,.invite,.mapwrap,.stForm,[data-testid="stExpander"],[data-testid="stDataFrame"]{
  border:1px solid var(--line) !important;box-shadow:var(--shadow-sm);background:rgba(255,255,255,.92);backdrop-filter:blur(12px);
}
.card{border-radius:22px;padding:24px;transition:transform .24s var(--ease-out),box-shadow .24s var(--ease-out);animation:fadeUp .45s var(--ease-out) both;}
.card:hover{transform:translateY(-4px);box-shadow:var(--shadow-md);}
.card h3{margin:0 0 7px;color:var(--pine);font-size:20px;font-weight:800;}
.card .sub{color:var(--muted);font-size:14px;line-height:1.55;}
.metric{border-radius:20px;padding:18px;text-align:center;animation:fadeUp .45s var(--ease-out) both;}
.metric .v{font-size:28px;font-weight:800;color:var(--purple);letter-spacing:-.7px;}
.metric .l{margin-top:4px;font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:1.1px;font-weight:700;}
.invite{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:28px;font-weight:800;letter-spacing:4px;color:var(--purple);border:1.5px dashed rgba(201,163,59,.75) !important;border-radius:20px;padding:18px;text-align:center;background:linear-gradient(135deg,#FFFDF7,#F1FBF8);animation:softGlow 2.8s ease-in-out infinite;}
.mapwrap{border-radius:24px;overflow:hidden;animation:fadeUp .5s var(--ease-out) both;}
.stForm{padding:22px;border-radius:24px;}
[data-testid="stExpander"]{border-radius:18px !important;overflow:hidden;margin-bottom:10px;}

/* ---------- Route and itinerary ---------- */
.stop{display:flex;gap:16px;position:relative;padding:10px 0;animation:fadeUp .45s var(--ease-out) both;}
.stop .num{flex:0 0 42px;height:42px;border-radius:14px;background:linear-gradient(135deg,var(--pine),var(--mint));color:#fff;display:flex;align-items:center;justify-content:center;font-weight:800;box-shadow:0 9px 22px rgba(7,59,51,.24);transition:transform .2s var(--ease-out);}
.stop:hover .num{transform:translateY(-2px) rotate(-3deg);}
.stop .body{flex:1;background:rgba(255,255,255,.94);border:1px solid var(--line);border-radius:19px;padding:16px 18px;box-shadow:var(--shadow-sm);}
.stop .body h4{margin:0;color:var(--pine);font-size:18px;font-weight:800;}
.tag{display:inline-flex;align-items:center;background:#EFF6F1;color:var(--pine);border:1px solid rgba(7,59,51,.08);border-radius:999px;padding:5px 11px;font-size:11px;margin:6px 5px 0 0;font-weight:700;}
.act{display:flex;align-items:center;gap:12px;padding:12px 14px;border-radius:14px;background:rgba(255,255,255,.9);border:1px solid var(--line);margin-bottom:8px;box-shadow:0 5px 14px rgba(16,35,31,.045);animation:slideIn .35s var(--ease-out) both;transition:transform .18s var(--ease-out),border-color .18s,box-shadow .18s;}
.act:hover{transform:translateX(4px);border-color:rgba(23,195,178,.42);box-shadow:var(--shadow-sm);}
.act .t{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-weight:800;color:var(--pine);min-width:112px;font-size:12px;}
.act .dotm{width:8px;height:8px;border-radius:50%;background:var(--gold);box-shadow:0 0 0 4px rgba(201,163,59,.10);}
.act.meal{background:#FFFCF2;}
.act .star{color:#9E791B;font-weight:800;font-size:11px;}
.gmap-btn{transition:transform .16s var(--ease-out),filter .16s;}
.gmap-btn:hover{transform:translateY(-1px);filter:saturate(1.25);}

/* ---------- Controls ---------- */
.stButton>button,.stFormSubmitButton>button,.stDownloadButton>button{
  min-height:46px;border:none !important;border-radius:15px !important;padding:10px 22px !important;
  background:linear-gradient(135deg,var(--pine),var(--pine-2)) !important;color:#fff !important;
  font-weight:800 !important;font-size:14px !important;letter-spacing:.05px;
  box-shadow:0 11px 24px rgba(7,59,51,.20) !important;
  transition:transform .15s var(--ease-out),box-shadow .18s var(--ease-out),filter .18s !important;
}
.stButton>button:hover,.stFormSubmitButton>button:hover,.stDownloadButton>button:hover{transform:translateY(-2px);filter:saturate(1.15);box-shadow:0 16px 30px rgba(7,59,51,.28) !important;}
.stButton>button:active,.stFormSubmitButton>button:active,.stDownloadButton>button:active{transform:scale(.97);}
.stButton>button p,.stFormSubmitButton>button p,.stDownloadButton>button p{color:inherit !important;}
.stButton>button:not([kind="secondary"]) *,.stFormSubmitButton>button *,.stDownloadButton>button *{color:#fff !important;}
.stButton>button[kind="secondary"]{background:rgba(255,255,255,.88) !important;color:var(--pine) !important;border:1px solid rgba(7,59,51,.11) !important;box-shadow:0 6px 18px rgba(16,35,31,.07) !important;}
.stButton>button[kind="secondary"] *{color:var(--pine) !important;}
.stButton>button[kind="secondary"]:hover{background:#fff !important;border-color:rgba(23,195,178,.48) !important;}
.stButton>button[kind="primary"]{background:linear-gradient(135deg,var(--purple),var(--purple-2)) !important;box-shadow:0 11px 24px rgba(58,20,91,.22) !important;}

.stTextInput input,.stNumberInput input,.stTextArea textarea,
.stDateInput input,[data-baseweb="select"]>div{
  min-height:46px;border-radius:14px !important;border:1px solid rgba(7,59,51,.13) !important;
  background:rgba(255,255,255,.95) !important;color:var(--ink) !important;
  -webkit-text-fill-color:var(--ink) !important;box-shadow:0 4px 14px rgba(16,35,31,.04) !important;
  transition:border-color .18s,box-shadow .18s !important;
}
.stTextInput input:focus,.stNumberInput input:focus,.stTextArea textarea:focus,.stDateInput input:focus{
  border-color:var(--mint) !important;box-shadow:0 0 0 4px rgba(23,195,178,.14) !important;
}
input::placeholder,textarea::placeholder{color:#89948F !important;opacity:1;}
.stSlider,.stSlider *,.stSlider [data-baseweb]{direction:ltr !important;}
.stSlider [role="slider"]{background:var(--purple) !important;border:3px solid #fff;box-shadow:0 4px 12px rgba(58,20,91,.28);}
.stProgress>div>div>div{background:linear-gradient(90deg,var(--mint),var(--purple));border-radius:999px;transition:width .6s var(--ease-out);}
.stTabs [data-baseweb="tab-list"]{gap:8px;background:rgba(255,255,255,.76);padding:6px;border-radius:16px;border:1px solid var(--line);}
.stTabs [data-baseweb="tab"]{height:42px;border-radius:11px;padding:0 18px;font-weight:800;color:var(--muted);}
.stTabs [aria-selected="true"]{background:var(--pine) !important;color:#fff !important;}
.stTabs [aria-selected="true"] p{color:#fff !important;}
.stRadio [role="radiogroup"]{gap:8px;}
.stRadio label,.stCheckbox label{padding:4px 2px;}

/* ---------- Typography and messaging ---------- */
.sec{font-size:28px;font-weight:800;color:var(--pine);margin:34px 0 14px;display:flex;align-items:center;gap:11px;letter-spacing:-.5px;animation:fadeUp .4s var(--ease-out) both;}
.sec::before{content:"";width:6px;height:29px;border-radius:99px;background:linear-gradient(180deg,var(--mint),var(--purple));box-shadow:0 4px 10px rgba(23,195,178,.25);}
.stApp p,.stApp li,.stApp label{color:var(--ink);}
.stApp h1,.stApp h2,.stApp h3,.stApp h4,.stApp h5,.stApp h6{color:var(--pine);letter-spacing:-.35px;}
.stApp .hero h1{color:#fff;}
.stApp .hero h1 .accent{color:var(--mint);}
.stApp .hero p{color:rgba(255,255,255,.79);}
[data-testid="stMarkdownContainer"],[data-testid="stCaptionContainer"],[data-testid="stMarkdownContainer"] p{color:var(--ink);}
.stCaptionContainer,[data-testid="stCaptionContainer"]{color:var(--muted) !important;}
.stSlider label,.stSelectbox label,.stTextInput label,.stNumberInput label,.stDateInput label,.stTextArea label,.stRadio label,.stCheckbox label,[data-testid="stWidgetLabel"]{color:var(--ink) !important;font-weight:700 !important;}
[data-testid="stAlert"]{border-radius:17px;border:1px solid rgba(7,59,51,.09);box-shadow:var(--shadow-sm);}
[data-testid="stNotification"]{border-radius:17px;}

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"]{background:linear-gradient(180deg,#082F2A 0%,#0B473D 62%,#2F1348 100%);border-right:1px solid rgba(255,255,255,.06);}
[data-testid="stSidebar"] *{color:#F5FFFC !important;}
[data-testid="stSidebar"] [data-testid="stCaptionContainer"]{color:rgba(255,255,255,.62) !important;}
[data-testid="stSidebar"] .stButton>button{background:rgba(255,255,255,.10) !important;border:1px solid rgba(255,255,255,.14) !important;box-shadow:none !important;}
[data-testid="stSidebar"] .stButton>button:hover{background:rgba(255,255,255,.17) !important;}

/* App-like navigation bar generated by the first Streamlit columns row. */
div[data-testid="stHorizontalBlock"]:has(.st-key-nav_home){
  position:sticky;top:8px;z-index:999;gap:8px;padding:7px;margin-bottom:14px;
  border:1px solid rgba(255,255,255,.86);border-radius:19px;
  background:rgba(248,251,248,.84);box-shadow:0 12px 32px rgba(16,35,31,.09);
  backdrop-filter:blur(18px);
}
div[data-testid="stHorizontalBlock"]:has(.st-key-nav_home) .stButton>button{
  min-height:40px;padding:7px 8px !important;border-radius:12px !important;font-size:12px !important;
}

/* ---------- Supporting widgets ---------- */
.ring{position:relative;width:122px;height:122px;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:auto;background:conic-gradient(var(--mint) calc(var(--p)*1%),rgba(7,59,51,.08) 0);animation:fadeUp .45s both;box-shadow:var(--shadow-sm);}
.ring::before{content:"";position:absolute;inset:11px;border-radius:50%;background:#fff;}
.ring .rv{position:relative;font-size:28px;font-weight:800;color:var(--purple);}
.pill{display:inline-flex;align-items:center;gap:6px;background:var(--mint-soft);color:var(--pine);border:1px solid rgba(23,195,178,.22);border-radius:999px;padding:6px 13px;font-size:12px;font-weight:800;}
.hero-badge{background:#fff;border:1px solid var(--line);border-radius:24px;padding:22px;text-align:center;box-shadow:var(--shadow-md);}
.hero-badge .hb-num{font-size:30px;font-weight:800;color:var(--purple);}
.hero-badge .hb-lbl{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:1px;margin-top:2px;font-weight:700;}
.hero-badge .hb-div{height:1px;background:linear-gradient(90deg,transparent,rgba(7,59,51,.16),transparent);margin:12px 8px;}

/* ---------- Motion ---------- */
@keyframes heroIn{from{opacity:0;transform:translateY(14px) scale(.99)}to{opacity:1;transform:translateY(0) scale(1)}}
@keyframes fadeUp{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:translateY(0)}}
@keyframes slideIn{from{opacity:0;transform:translateX(-10px)}to{opacity:1;transform:translateX(0)}}
@keyframes softGlow{0%,100%{box-shadow:var(--shadow-sm)}50%{box-shadow:0 14px 35px rgba(201,163,59,.17)}}

/* ---------- Responsive ---------- */
@media(max-width:900px){
  [data-testid="stAppViewContainer"]>.main .block-container{padding:1rem 1rem 3rem;}
  .hero{grid-template-columns:1fr;padding:34px;min-height:auto;border-radius:28px;}
  .hero h1{font-size:48px;letter-spacing:-1.8px;}
  .hero-visual{min-height:330px;}
  .home-stats{grid-template-columns:repeat(2,1fr);}
}
@media(max-width:640px){
  [data-testid="stAppViewContainer"]>.main .block-container{padding:.7rem .75rem 4rem;}
  .hero{padding:27px 22px;border-radius:24px;gap:18px;}
  .hero-logo{width:145px;margin-bottom:20px;}
  .hero h1{font-size:38px;line-height:1.02;letter-spacing:-1.2px;}
  .hero p{font-size:15px;line-height:1.55;}
  .hero-proof{gap:12px;font-size:11px;}
  .hero-visual{min-height:300px;}
  .phone-card{max-width:330px;padding:14px;border-radius:24px;transform:none;}
  .floating-chip{font-size:10px;padding:8px 10px;}
  .floating-chip.one{right:-7px;top:23px}.floating-chip.two{left:-5px;bottom:20px;}
  .home-stats{grid-template-columns:repeat(2,1fr);gap:8px;}
  .home-stat{padding:14px}.home-stat b{font-size:21px;}
  .feature-card{min-height:0;padding:20px;}
  .sec{font-size:23px;margin-top:28px;}
  .invite{font-size:22px;letter-spacing:2px;}
  .act{align-items:flex-start;gap:8px}.act .t{min-width:92px;font-size:11px;}
  .stButton>button,.stFormSubmitButton>button,.stDownloadButton>button{min-height:44px;padding:9px 12px !important;font-size:13px !important;}
  div[data-testid="stHorizontalBlock"]:has(.st-key-nav_home){display:grid !important;grid-template-columns:repeat(4,minmax(0,1fr));gap:6px;top:5px;padding:6px;border-radius:17px;}
  div[data-testid="stHorizontalBlock"]:has(.st-key-nav_home)>div[data-testid="stColumn"]{width:auto !important;min-width:0 !important;flex:initial !important;}
  div[data-testid="stHorizontalBlock"]:has(.st-key-nav_home) .stButton>button{min-height:39px;padding:5px 3px !important;font-size:10px !important;white-space:nowrap;}
}
@media(prefers-reduced-motion:reduce){
  *,*::before,*::after{animation-duration:.01ms !important;animation-iteration-count:1 !important;transition-duration:.01ms !important;scroll-behavior:auto !important;}
}
</style>
"""

LOTTIE = {
    "travel": "assets/travel.json",
    "group": "assets/group.json",
    "success": "assets/success.json",
}
