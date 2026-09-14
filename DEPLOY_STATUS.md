# TRIPSA — حالة النشر والتشخيص (مرجع داخلي)

## المشكلة الحالية (401 Unauthorized)
التطبيق المنشور يقرأ توكناً بصمته `token_sha=4280648c12` (token_len=348) — وهذا
لا يطابق أي توكن صالح لدينا:

| التوكن | SHA-256 (أول 10) | الحالة |
|---|---|---|
| الموثق الجديد (يعمل، status 200) | `89746b5475` | صالح — المطلوب |
| الأول (قديم) | `fd9ee27898` | منتهي |
| التالف (auth role not found) | `6b706d2366` | تالف |
| توكن طوكيو الأصلي | `21c388e1b6` | قاعدة قديمة |
| **ما يقرأه التطبيق فعلياً** | `4280648c12` | **غير معروف — خطأ اللصق** |

## التشخيص
محرر Secrets في Streamlit Cloud (CodeMirror) يكسر سطر `TURSO_TOKEN =` بصرياً عند
اللصق، فيلتقط التطبيق قيمة ناقصة/مشوهة (401). عند تحديد الكل (Ctrl+A) وحذفه يعود
المحرر لنص المثال placeholder — أي أن الحذف عبر التحديد لا يمس القيمة الفعلية.

## الحل المطلوب (خطوات دقيقة في واجهة Secrets)
1. فتح: share.streamlit.io → tripsa-streamlit → ⋮ → Settings → Secrets
2. النقر داخل المحرر، ثم تحديد الكل Ctrl+A، ثم Delete (وليس Backspace على التحديد)
   حتى يصبح المحرر فارغاً تماماً (بدون نص المثال DB_USERNAME).
3. لصق السطرين فقط (كل قيمة في سطر واحد، بدون كسر):
   TURSO_URL = "libsql://tripsa-us-naalthmari-droid.aws-us-east-1.turso.io"
   TURSO_TOKEN = "<التوكن الموثق sha=89746b5475 — محفوظ في /home/ubuntu/.tripsa_us_token_fresh>"
4. Save changes → انتظار ~دقيقة → Reboot.
5. التحقق: يجب أن تظهر في صفحة التطبيق بصمة `token_sha=89746b5475` (لا 4280648c12).

## المنجز حتى الآن
- نقل قاعدة Turso من طوكيو (aws-ap-northeast-1) إلى أمريكا (aws-us-east-1):
  مجموعة tripsa-us + قاعدة tripsa-us. رُحّلت كل البيانات وتطابقت الأعداد:
  trips=21, members=40, votes=26, item_votes=177, comments=9, rec_ratings=0, notifications=28.
- تحسين الأداء في db.py: جلسة HTTPS واحدة keep-alive (بارد ~4.9s → دافئ ~1.1s).
- إضافة إعادة محاولة تلقائية (×4 مع تراجع أسّي) لأخطاء 401/403/404/429/5xx العابرة.
- نظام حسابات المؤسسين مكتمل ومختبر محلياً وسحابياً:
  جدول founders + عمود trips.founder_id + تسجيل/دخول PBKDF2 (100k) + صفحة My Trips
  + حماية صفحة الإنشاء + عزل المدعوين (لا يحتاجون حساباً) + claim_legacy_trips.
- تشخيص آمن في app.py يعرض host + token_len + token_sha (بصمة فقط، بلا توكن) عند فشل DB.
- كل الكود مدفوع إلى GitHub (naalthmari-droid/tripsa-streamlit, main): آخر commit 727d0a8.

## الروابط
- التطبيق: https://tripsa-app-hyjsp9bnu4fvx2k5vad88g.streamlit.app/
- المستودع: https://github.com/naalthmari-droid/tripsa-streamlit (main)
- قاعدة Turso الجديدة: libsql://tripsa-us-naalthmari-droid.aws-us-east-1.turso.io

## ملاحظة أمنية
يجب تدوير كل التوكنات التي ظهرت نصاً في المحادثة (Turso platform token + db tokens)
بعد استقرار النشر، لأنها أصبحت مكشوفة.

## حالة العمل الجارية (2026-09-14) — دمج بيانات المسافرون العرب
- مصدر البيانات: https://www.almosaferoon.com/ksa/ (ملف: /home/ubuntu/tripsa_streamlit/saudi_tourism_data.json)
  يحوي 20 وجهة، ~70 معلماً، مدة إقامة موصى بها، أفضل أشهر زيارة، وقواعد تخطيط (مكة/المدينة للمسلمين فقط، دمج المنطقة الشرقية...).
- وحدة الدمج: saudi_extra.py (خرائط الأسماء العربية→ids، تصنيف الفئات العربية→interest keys، 5 وجهات جديدة: umluj, kaec, jazan, farasan, tanomah).
- data.py: دمج تلقائي عند الاستيراد (DESTINATIONS=20، ATTRACTIONS مدموجة، rec_days/best_months/min_nights محدثة).
- airports: أضيفت umluj→EJH, kaec→JED, tanomah→AHB (farasan عبّارة فقط).
- engine.py: أُضيفت فنادق kaec وjazan داخل HOTELS قبل قوس الإغلاق مباشرة (تحقق من الموقع).
- ملاحظة: قسم app.py الذي كان يعرض "15 DESTINATIONS" ربما لم يُحدَّث لديناميكي؛ تحقق من الرقم في الصفحة الرئيسية.
- الميزة السابقة المكتملة: custom_items (فعاليات مقترحة من الأعضاء، تصويت، إدراج في Final Plan عند avg>=2.5، حذف من المقترح فقط).
- آخر commit مدفوع قبل الدمج: c0174fb (todo). الدمج الحالي لم يُختبر بعد ولم يُدفع.
- التطبيق: https://tripsa-app-hyjsp9bnu4fvx2k5vad88g.streamlit.app/ — قاعدة Turso: tripsa-us (aws-us-east-1)، التوكن المدوّر sha=2f8618415a في Streamlit Secrets (لا تعرضه).
- التوكنات المحلية: /home/ubuntu/.tripsa_us_token_rotated (الصالح)، platform token القديم أُبطل.

## تحديث: اكتمال تدوير الأسرار (بتاريخ الجلسة)
- ✅ أُبطل منصة Token القديم المكشوف (jti PUA8-LAiEfG0Gx4QqgdJSg) عبر Platform API — status 200.
- ✅ أُصدر توكن قاعدة بيانات جديد آمن (kid jLv3EwCR, sha 2f8618415a) — تحقق 200.
- ✅ حُدّثت Streamlit Secrets بالتوكن المدوّر — التطبيق يعمل بدون خطأ.
- ✅ كل الأسرار المكشوفة في المحادثة أصبحت الآن غير صالحة/مُبطلة.
