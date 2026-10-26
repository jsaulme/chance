import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="CHANCE | The Science of Unequal Outcomes", page_icon="🎲", layout="wide")

# Identidad de marca CHANCE
st.markdown("## CHANCE")
st.caption("The Science of Unequal Outcomes")


# Rango del peso de la suerte: lo usan el selector Y el barrido (una sola fuente de verdad)
LUCK_MAX = 100.0
GRID_PCT = [0, 1, 2, 5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 90, 100]

FONT = "'Segoe UI', -apple-system, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif"

# ------------------------------------------------------------------ idiomas
LANGS = {"es": "Español", "en": "English", "zh": "中文", "hi": "हिन्दी", "ar": "العربية"}

TR = {
    "es": dict(
        title="¿Cuánto importa la suerte en el éxito?",
        intro="**Modelo:** cada aplicante recibe una puntuación de *habilidad* y una de *suerte* (uniformes de 1 a 100). La puntuación final es `(1 − p)·habilidad + p·suerte` y las plazas se asignan a los mejores. El proceso se repite muchas veces y se compara con una selección basada **solo en habilidad**.",
        params="Parámetros", applicants="Aplicantes", seats="Plazas disponibles",
        luck_w="Peso de la suerte (%)", sims="Número de simulaciones", scoring="Puntuaciones",
        sc_cont="Continuas 1–100 (reproduce el ejercicio)", sc_int="Enteras 1–100",
        seed="Semilla aleatoria", dark="Modo oscuro", spinner="Simulando...",
        m_luck="Suerte promedio de los elegidos", m_luck_help="Un aplicante cualquiera tendría ~50.",
        m_coinc="Coinciden con selección por habilidad", m_other="Habrían sido otros", m_pct="% distinto",
        export="Exportar resultados", dl_summary="⬇️ Resumen (CSV)",
        dl_summary_help="Parámetros + métricas agregadas de este escenario (1 fila).",
        dl_sims="⬇️ Simulaciones (CSV)", dl_sims_help="Una fila por simulación.",
        save_scn="➕ Guardar escenario", save_help="Lo agrega a la tabla de comparación.",
        clear_scn="🗑️ Limpiar escenarios", saved_n="Escenarios guardados: {n}",
        dl_scn="⬇️ Escenarios guardados (CSV)",
        h_title="Suerte promedio de los elegidos (una observación por simulación)",
        h_x="Suerte promedio", h_vline="Promedio poblacional (50)",
        b_title="¿Cuántos elegidos lo habrían sido solo por habilidad?",
        b_x="Elegidos que coinciden con el top por habilidad", b_y="Simulaciones",
        d_title="Una selección en detalle", skill="Habilidad", luck="Suerte", group="Grupo",
        sel="Elegido", nsel="No elegido",
        sc_title="Los elegidos se concentran en habilidad alta Y suerte alta",
        sw_header="¿Y si la suerte pesara más (o menos)?",
        sw_check="Calcular barrido de peso de suerte", sw_spin="Calculando barrido...",
        sw_fig="% de elegidos distintos vs. selección solo por habilidad ({n} sims c/u)",
        dl_sweep="⬇️ Barrido (CSV)",
        concl="**Conclusión del modelo:** con competencia feroz (pocas plazas, muchísimos aplicantes), incluso un peso pequeño de suerte cambia a buena parte de los seleccionados. El resultado depende de supuestos: distribución uniforme, independencia entre habilidad y suerte, y si las puntuaciones son enteras o continuas (cambia los empates en el tope).",
    ),
    "en": dict(
        title="How much does luck matter for success?",
        intro="**Model:** each applicant gets a *skill* score and a *luck* score (uniform from 1 to 100). The final score is `(1 − p)·skill + p·luck`, and seats go to the top scorers. The process is repeated many times and compared with a selection based on **skill alone**.",
        params="Parameters", applicants="Applicants", seats="Available seats",
        luck_w="Luck weight (%)", sims="Number of simulations", scoring="Scores",
        sc_cont="Continuous 1–100 (reproduces the exercise)", sc_int="Integers 1–100",
        seed="Random seed", dark="Dark mode", spinner="Simulating...",
        m_luck="Average luck of those selected", m_luck_help="A random applicant would have ~50.",
        m_coinc="Match the skill-only selection", m_other="Would have been different", m_pct="% different",
        export="Export results", dl_summary="⬇️ Summary (CSV)",
        dl_summary_help="Parameters + aggregate metrics for this scenario (1 row).",
        dl_sims="⬇️ Simulations (CSV)", dl_sims_help="One row per simulation.",
        save_scn="➕ Save scenario", save_help="Adds it to the comparison table.",
        clear_scn="🗑️ Clear scenarios", saved_n="Saved scenarios: {n}",
        dl_scn="⬇️ Saved scenarios (CSV)",
        h_title="Average luck of those selected (one observation per simulation)",
        h_x="Average luck", h_vline="Population average (50)",
        b_title="How many of those selected would have made it on skill alone?",
        b_x="Selected who match the skill-only top", b_y="Simulations",
        d_title="One selection in detail", skill="Skill", luck="Luck", group="Group",
        sel="Selected", nsel="Not selected",
        sc_title="The selected cluster at high skill AND high luck",
        sw_header="What if luck weighed more (or less)?",
        sw_check="Run luck-weight sweep", sw_spin="Computing sweep...",
        sw_fig="% of selected who differ from skill-only selection ({n} sims each)",
        dl_sweep="⬇️ Sweep (CSV)",
        concl="**Model takeaway:** under fierce competition (few seats, very many applicants), even a small luck weight changes a large share of those selected. Results depend on assumptions: uniform distributions, independence between skill and luck, and whether scores are integers or continuous (which changes ties at the top).",
    ),
    "zh": dict(
        title="运气对成功有多重要？",
        intro="**模型：** 每位申请人获得一个*能力*分数和一个*运气*分数（1到100均匀分布）。最终得分为 `(1 − p)·能力 + p·运气`，名额授予得分最高者。该过程重复多次，并与**仅按能力**选拔的结果进行比较。",
        params="参数", applicants="申请人数", seats="可用名额",
        luck_w="运气权重 (%)", sims="模拟次数", scoring="分数类型",
        sc_cont="连续 1–100（复现原练习）", sc_int="整数 1–100",
        seed="随机种子", dark="深色模式", spinner="模拟中……",
        m_luck="入选者平均运气", m_luck_help="随机一名申请人约为 50。",
        m_coinc="与仅按能力选拔重合", m_other="本应是其他人", m_pct="不同比例 %",
        export="导出结果", dl_summary="⬇️ 汇总 (CSV)",
        dl_summary_help="本情景的参数与汇总指标（1 行）。",
        dl_sims="⬇️ 模拟明细 (CSV)", dl_sims_help="每次模拟一行。",
        save_scn="➕ 保存情景", save_help="加入对比表。",
        clear_scn="🗑️ 清空情景", saved_n="已保存情景：{n}",
        dl_scn="⬇️ 已保存情景 (CSV)",
        h_title="入选者平均运气（每次模拟一个观测值）",
        h_x="平均运气", h_vline="总体平均 (50)",
        b_title="仅凭能力，入选者中有多少人仍会入选？",
        b_x="与能力排名前列重合的入选者数", b_y="模拟次数",
        d_title="单次选拔详情", skill="能力", luck="运气", group="组别",
        sel="入选", nsel="未入选",
        sc_title="入选者集中在高能力且高运气区域",
        sw_header="如果运气权重更高（或更低）会怎样？",
        sw_check="计算运气权重扫描", sw_spin="正在计算扫描……",
        sw_fig="与仅按能力选拔不同的入选者占比（每点 {n} 次模拟）",
        dl_sweep="⬇️ 扫描 (CSV)",
        concl="**模型结论：** 在竞争激烈（名额少、申请人极多）的情况下，即使运气权重很小，也会改变相当大比例的入选者。结果取决于假设：均匀分布、能力与运气相互独立，以及分数是整数还是连续值（这会改变顶端的并列情况）。",
    ),
    "hi": dict(
        title="सफलता में भाग्य कितना मायने रखता है?",
        intro="**मॉडल:** हर आवेदक को एक *योग्यता* स्कोर और एक *भाग्य* स्कोर (1 से 100 तक समान वितरण) मिलता है। अंतिम स्कोर `(1 − p)·योग्यता + p·भाग्य` है और सीटें सबसे ऊँचे स्कोर वालों को मिलती हैं। प्रक्रिया को कई बार दोहराया जाता है और **केवल योग्यता** पर आधारित चयन से तुलना की जाती है।",
        params="पैरामीटर", applicants="आवेदकों की संख्या", seats="उपलब्ध सीटें",
        luck_w="भाग्य का भार (%)", sims="सिमुलेशन की संख्या", scoring="स्कोर का प्रकार",
        sc_cont="सतत 1–100 (मूल अभ्यास जैसा)", sc_int="पूर्णांक 1–100",
        seed="रैंडम सीड", dark="डार्क मोड", spinner="सिमुलेशन चल रहा है...",
        m_luck="चयनित लोगों का औसत भाग्य", m_luck_help="किसी भी आवेदक का औसत ~50 होगा।",
        m_coinc="केवल योग्यता वाले चयन से मेल", m_other="अलग होते", m_pct="% अलग",
        export="परिणाम निर्यात करें", dl_summary="⬇️ सारांश (CSV)",
        dl_summary_help="इस परिदृश्य के पैरामीटर और समेकित मेट्रिक्स (1 पंक्ति)।",
        dl_sims="⬇️ सिमुलेशन (CSV)", dl_sims_help="प्रति सिमुलेशन एक पंक्ति।",
        save_scn="➕ परिदृश्य सहेजें", save_help="तुलना तालिका में जोड़ता है।",
        clear_scn="🗑️ परिदृश्य हटाएँ", saved_n="सहेजे गए परिदृश्य: {n}",
        dl_scn="⬇️ सहेजे गए परिदृश्य (CSV)",
        h_title="चयनित लोगों का औसत भाग्य (प्रति सिमुलेशन एक अवलोकन)",
        h_x="औसत भाग्य", h_vline="जनसंख्या औसत (50)",
        b_title="केवल योग्यता से कितने चयनित लोग चुने जाते?",
        b_x="योग्यता-शीर्ष से मेल खाने वाले चयनित", b_y="सिमुलेशन",
        d_title="एक चयन का विवरण", skill="योग्यता", luck="भाग्य", group="समूह",
        sel="चयनित", nsel="अचयनित",
        sc_title="चयनित लोग उच्च योग्यता और उच्च भाग्य दोनों में केंद्रित हैं",
        sw_header="अगर भाग्य का भार ज़्यादा (या कम) होता तो?",
        sw_check="भाग्य-भार स्वीप चलाएँ", sw_spin="स्वीप की गणना हो रही है...",
        sw_fig="केवल-योग्यता चयन से भिन्न चयनितों का % (प्रत्येक बिंदु पर {n} सिमुलेशन)",
        dl_sweep="⬇️ स्वीप (CSV)",
        concl="**मॉडल का निष्कर्ष:** कड़ी प्रतिस्पर्धा (कम सीटें, बहुत अधिक आवेदक) में भाग्य का छोटा सा भार भी चयनित लोगों के बड़े हिस्से को बदल देता है। परिणाम मान्यताओं पर निर्भर हैं: समान वितरण, योग्यता और भाग्य की स्वतंत्रता, और स्कोर पूर्णांक हैं या सतत (इससे शीर्ष पर बराबरी बदलती है)।",
    ),
    "ar": dict(
        title="ما مدى أهمية الحظ في النجاح؟",
        intro="**النموذج:** يحصل كل متقدم على درجة *مهارة* ودرجة *حظ* (توزيع منتظم من 1 إلى 100). الدرجة النهائية هي `(1 − p)·المهارة + p·الحظ` وتُمنح المقاعد لأعلى الدرجات. تُكرَّر العملية مرات عديدة وتُقارَن بانتقاء يعتمد على **المهارة وحدها**.",
        params="المعلمات", applicants="عدد المتقدمين", seats="المقاعد المتاحة",
        luck_w="وزن الحظ (%)", sims="عدد عمليات المحاكاة", scoring="نوع الدرجات",
        sc_cont="مستمرة 1–100 (تعيد إنتاج التمرين)", sc_int="أعداد صحيحة 1–100",
        seed="البذرة العشوائية", dark="الوضع الداكن", spinner="جارٍ المحاكاة...",
        m_luck="متوسط حظ المختارين", m_luck_help="متوسط أي متقدم عشوائي نحو 50.",
        m_coinc="يتطابقون مع الانتقاء بالمهارة فقط", m_other="كانوا سيكونون مختلفين", m_pct="نسبة المختلفين %",
        export="تصدير النتائج", dl_summary="⬇️ ملخص (CSV)",
        dl_summary_help="معلمات ومقاييس مجمّعة لهذا السيناريو (صف واحد).",
        dl_sims="⬇️ المحاكاة (CSV)", dl_sims_help="صف لكل عملية محاكاة.",
        save_scn="➕ حفظ السيناريو", save_help="يضيفه إلى جدول المقارنة.",
        clear_scn="🗑️ مسح السيناريوهات", saved_n="السيناريوهات المحفوظة: {n}",
        dl_scn="⬇️ السيناريوهات المحفوظة (CSV)",
        h_title="متوسط حظ المختارين (ملاحظة واحدة لكل محاكاة)",
        h_x="متوسط الحظ", h_vline="متوسط المجتمع (50)",
        b_title="كم من المختارين كانوا سيُختارون بالمهارة وحدها؟",
        b_x="المختارون المتطابقون مع الأعلى مهارةً", b_y="عمليات المحاكاة",
        d_title="اختيار واحد بالتفصيل", skill="المهارة", luck="الحظ", group="المجموعة",
        sel="مختار", nsel="غير مختار",
        sc_title="المختارون يتركزون عند المهارة العالية والحظ العالي معًا",
        sw_header="ماذا لو كان وزن الحظ أكبر (أو أقل)؟",
        sw_check="حساب مسح وزن الحظ", sw_spin="جارٍ حساب المسح...",
        sw_fig="نسبة المختارين المختلفين عن الانتقاء بالمهارة فقط (كل نقطة {n} محاكاة)",
        dl_sweep="⬇️ المسح (CSV)",
        concl="**خلاصة النموذج:** في ظل منافسة شرسة (مقاعد قليلة ومتقدمون كثيرون جدًا)، يغيّر حتى وزن صغير للحظ نسبة كبيرة من المختارين. تعتمد النتائج على افتراضات: التوزيع المنتظم، واستقلال المهارة عن الحظ، وما إذا كانت الدرجات صحيحة أم مستمرة (وهذا يغيّر حالات التعادل في القمة).",
    ),
}


# Textos de los controles de realismo (distribución, ruido, correlación)
EXTRA = {
    "es": dict(
        dist="Habilidad con distribución normal",
        dist_help="Apagado: habilidad uniforme 1–100. Encendido: normal (media 50, desv. 15, sin truncar). Con normal, la suerte pesa relativamente más porque es más dispersa.",
        noise="Ruido de medición del selector (σ)",
        noise_help="El selector ve la habilidad con error aleatorio de esta desviación (en puntos). 0 = medición perfecta. La comparación sigue siendo contra la habilidad real.",
        rho="Correlación habilidad–suerte",
        rho_help="Correlación gaussiana entre ambas variables. 0 = independientes; positiva = quienes tienen más habilidad tienden a tener más suerte.",
    ),
    "en": dict(
        dist="Normally distributed skill",
        dist_help="Off: uniform skill 1–100. On: normal (mean 50, sd 15, untruncated). With normal skill, luck weighs relatively more because it is more spread out.",
        noise="Selector measurement noise (σ)",
        noise_help="The selector sees skill with random error of this standard deviation (in points). 0 = perfect measurement. The comparison is still against true skill.",
        rho="Skill–luck correlation",
        rho_help="Gaussian correlation between both variables. 0 = independent; positive = more skilled people tend to be luckier.",
    ),
    "zh": dict(
        dist="能力服从正态分布",
        dist_help="关闭：能力为 1–100 均匀分布。开启：正态分布（均值 50，标准差 15，不截断）。采用正态时，运气因离散度更大而相对权重更高。",
        noise="选拔者测量噪声 (σ)",
        noise_help="选拔者观察到的能力带有该标准差（以分数计）的随机误差。0 = 完美测量。比较对象仍是真实能力。",
        rho="能力与运气的相关性",
        rho_help="两者之间的高斯相关。0 = 相互独立；为正表示能力更强的人往往运气也更好。",
    ),
    "hi": dict(
        dist="योग्यता का सामान्य वितरण",
        dist_help="बंद: योग्यता 1–100 में समान वितरण। चालू: सामान्य वितरण (माध्य 50, मानक विचलन 15, बिना काटे)। सामान्य वितरण में भाग्य अधिक फैला होने के कारण अपेक्षाकृत ज़्यादा भार रखता है।",
        noise="चयनकर्ता का मापन शोर (σ)",
        noise_help="चयनकर्ता योग्यता को इस मानक विचलन (अंकों में) की यादृच्छिक त्रुटि के साथ देखता है। 0 = सटीक माप। तुलना अब भी वास्तविक योग्यता से होती है।",
        rho="योग्यता–भाग्य सहसंबंध",
        rho_help="दोनों चरों के बीच गाउसियन सहसंबंध। 0 = स्वतंत्र; धनात्मक = अधिक योग्य लोग प्रायः अधिक भाग्यशाली भी होते हैं।",
    ),
    "ar": dict(
        dist="المهارة بتوزيع طبيعي",
        dist_help="متوقف: مهارة منتظمة من 1 إلى 100. مفعّل: توزيع طبيعي (المتوسط 50، الانحراف 15، دون قطع). مع التوزيع الطبيعي يزداد وزن الحظ نسبيًا لأنه أكثر تشتتًا.",
        noise="ضجيج قياس المنتقي (σ)",
        noise_help="يرى المنتقي المهارة بخطأ عشوائي بهذا الانحراف المعياري (بالنقاط). 0 = قياس مثالي. تبقى المقارنة مع المهارة الحقيقية.",
        rho="الارتباط بين المهارة والحظ",
        rho_help="ارتباط غاوسي بين المتغيرين. 0 = مستقلان؛ القيمة الموجبة = الأكثر مهارة يميلون إلى حظ أفضل.",
    ),
}
for _k in TR:
    TR[_k].update(EXTRA[_k])


# Introducción ampliada, títulos de grupos y contexto del peso de la suerte
NUEVO = {
    "es": dict(
        intro="**¿Cómo funciona el modelo?** Cada aplicante tiene dos atributos: **habilidad** (esfuerzo, talento, experiencia) y **suerte** (circunstancias favorables que no dependen de él), ambos con una puntuación de 1 a 100. Entre los dos suman el **100%** del resultado final, así que al fijar el peso de la suerte en la barra lateral queda definido automáticamente el de la habilidad: con 5% de suerte, la habilidad pesa 95%. La puntuación final es `(1 − p)·habilidad + p·suerte`, donde *p* es el peso de la suerte, y las plazas se asignan a quienes obtienen el puntaje más alto. Este proceso se repite muchas veces y cada resultado se compara con una selección ideal basada **solo en habilidad**, para medir cuántos elegidos lo fueron gracias a la suerte. Por defecto ambos atributos son uniformes; en *Realismo del modelo* puedes cambiar la distribución de la habilidad, añadir ruido de medición o correlacionarlos.",
        g_pop="Población y plazas", g_weight="Habilidad vs. suerte", g_real="Realismo del modelo", g_sim="Simulación",
        luck_help="Habilidad y suerte suman 100%. Al fijar la suerte en 5%, la habilidad queda en 95%.",
    ),
    "en": dict(
        intro="**How does the model work?** Every applicant has two attributes: **skill** (effort, talent, experience) and **luck** (favorable circumstances outside their control), each scored from 1 to 100. Together they make up **100%** of the final result, so setting the luck weight in the sidebar automatically fixes the skill weight: with 5% luck, skill weighs 95%. The final score is `(1 − p)·skill + p·luck`, where *p* is the luck weight, and seats go to the highest scores. The process is repeated many times and each outcome is compared with an ideal selection based on **skill alone**, to measure how many of those selected got in thanks to luck. By default both attributes are uniform; under *Model realism* you can change the skill distribution, add measurement noise or correlate them.",
        g_pop="Population and seats", g_weight="Skill vs. luck", g_real="Model realism", g_sim="Simulation",
        luck_help="Skill and luck add up to 100%. Setting luck to 5% leaves skill at 95%.",
    ),
    "zh": dict(
        intro="**模型如何运作？** 每位申请人有两个属性：**能力**（努力、才华、经验）和**运气**（不受自己控制的有利环境），各以 1 到 100 分计。两者合计占最终结果的 **100%**，因此在侧边栏设定运气权重后，能力权重也就自动确定：运气占 5% 时，能力占 95%。最终得分为 `(1 − p)·能力 + p·运气`，其中 *p* 为运气权重，名额授予得分最高者。该过程会重复多次，并将每次结果与**仅按能力**的理想选拔进行比较，以衡量有多少入选者是靠运气入选的。默认情况下两个属性均为均匀分布；在*模型真实性*中可以更改能力的分布、加入测量噪声或设置两者的相关性。",
        g_pop="人群与名额", g_weight="能力与运气", g_real="模型真实性", g_sim="模拟",
        luck_help="能力与运气合计 100%。将运气设为 5%，能力即为 95%。",
    ),
    "hi": dict(
        intro="**मॉडल कैसे काम करता है?** हर आवेदक के दो गुण होते हैं: **योग्यता** (मेहनत, प्रतिभा, अनुभव) और **भाग्य** (अनुकूल परिस्थितियाँ जो उसके नियंत्रण में नहीं हैं), दोनों 1 से 100 के स्कोर में। दोनों मिलकर अंतिम परिणाम का **100%** बनाते हैं, इसलिए साइडबार में भाग्य का भार तय करते ही योग्यता का भार अपने-आप तय हो जाता है: 5% भाग्य पर योग्यता का भार 95% होता है। अंतिम स्कोर `(1 − p)·योग्यता + p·भाग्य` है, जहाँ *p* भाग्य का भार है, और सीटें सबसे ऊँचे स्कोर वालों को मिलती हैं। यह प्रक्रिया कई बार दोहराई जाती है और हर परिणाम की तुलना **केवल योग्यता** पर आधारित आदर्श चयन से की जाती है, ताकि पता चले कि कितने चयनित लोग भाग्य के कारण चुने गए। डिफ़ॉल्ट रूप से दोनों गुण समान वितरण में हैं; *मॉडल की यथार्थता* में आप योग्यता का वितरण बदल सकते हैं, मापन शोर जोड़ सकते हैं या दोनों में सहसंबंध रख सकते हैं।",
        g_pop="आबादी और सीटें", g_weight="योग्यता बनाम भाग्य", g_real="मॉडल की यथार्थता", g_sim="सिमुलेशन",
        luck_help="योग्यता और भाग्य का योग 100% है। भाग्य को 5% रखने पर योग्यता 95% रहती है।",
    ),
    "ar": dict(
        intro="**كيف يعمل النموذج؟** لكل متقدم سمتان: **المهارة** (الجهد والموهبة والخبرة) و**الحظ** (ظروف مواتية خارجة عن إرادته)، وكل منهما بدرجة من 1 إلى 100. يشكّلان معًا **100%** من النتيجة النهائية، لذا فعند تحديد وزن الحظ في الشريط الجانبي يتحدد وزن المهارة تلقائيًا: مع حظ بنسبة 5% يكون وزن المهارة 95%. الدرجة النهائية هي `(1 − p)·المهارة + p·الحظ` حيث *p* وزن الحظ، وتُمنح المقاعد لأعلى الدرجات. تُكرَّر العملية مرات عديدة وتُقارَن كل نتيجة بانتقاء مثالي يعتمد على **المهارة وحدها** لقياس عدد المختارين الذين دخلوا بفضل الحظ. افتراضيًا السمتان بتوزيع منتظم؛ ومن *واقعية النموذج* يمكنك تغيير توزيع المهارة أو إضافة ضجيج قياس أو ربطهما بارتباط.",
        g_pop="المتقدمون والمقاعد", g_weight="المهارة مقابل الحظ", g_real="واقعية النموذج", g_sim="المحاكاة",
        luck_help="المهارة والحظ مجموعهما 100%. عند ضبط الحظ على 5% تبقى المهارة 95%.",
    ),
}
for _k in TR:
    TR[_k].update(NUEVO[_k])


# Reinicio de valores, KPIs con contexto y explicación de lectura
NUEVO2 = {
    "es": dict(
        reset="↺ Restablecer valores iniciales",
        k_profile="Perfil de los elegidos · puntuaciones promedio, no porcentajes",
        k_impact="Impacto de la suerte en la selección",
        m_skill="Habilidad promedio de los elegidos", m_ideal="Habilidad promedio del top ideal",
        m_luck_help="Puntuación de suerte (1–100) promedio de los elegidos. Un aplicante cualquiera tendría ≈ 50. No es el peso de la suerte.",
        cap_luck="Puntuación de suerte · aplicante típico ≈ 50",
        cap_skill="Puntuación de habilidad · aplicante típico ≈ 50",
        cap_ideal="Si se eligiera solo por habilidad",
        cap_coinc="de {n} serían elegidos igual sin suerte",
        cap_other="de {n} cambian por el peso de la suerte",
        cap_pct="de los elegidos no lo serían solo por habilidad",
        how_title="¿Cómo leer estos indicadores?",
        how="**El {p}% es un *peso* dentro del puntaje final, no un porcentaje de lo que muestran los indicadores.** Cada aplicante recibe un puntaje final = {s}% × su habilidad + {p}% × su suerte (ambas de 1 a 100). Los indicadores de arriba, en cambio, son **puntuaciones promedio de 1 a 100** de las {k} personas elegidas; para un aplicante cualquiera ese promedio sería ≈ 50.\n\n**¿Por qué la suerte promedio de los elegidos es {luck} si la suerte solo pesa {p}%?** Compiten {n} aplicantes por {k} plazas, así que los finalistas tienen una habilidad altísima y muy parecida entre sí (los elegidos promedian {skill} y el top ideal por habilidad {ideal}: solo {gap} puntos de diferencia). Frente a una brecha tan pequeña, la suerte, que puede mover el puntaje final hasta {boost} puntos, decide quién entra, y entran quienes tuvieron una suerte muy alta. La suerte pesa poco en la fórmula, pero mucho en *quién queda seleccionado*.",
    ),
    "en": dict(
        reset="↺ Reset to initial values",
        k_profile="Profile of those selected · average scores, not percentages",
        k_impact="Impact of luck on the selection",
        m_skill="Average skill of those selected", m_ideal="Average skill of the ideal top",
        m_luck_help="Average luck score (1–100) of those selected. A typical applicant would be ≈ 50. This is not the luck weight.",
        cap_luck="Luck score · typical applicant ≈ 50",
        cap_skill="Skill score · typical applicant ≈ 50",
        cap_ideal="If selected on skill alone",
        cap_coinc="of {n} would be selected anyway without luck",
        cap_other="of {n} change because of the luck weight",
        cap_pct="of those selected would not be on skill alone",
        how_title="How to read these indicators",
        how="**The {p}% is a *weight* inside the final score, not a percentage of what the indicators show.** Each applicant's final score = {s}% × skill + {p}% × luck (both from 1 to 100). The indicators above, in contrast, are **average scores from 1 to 100** of the {k} people selected; for a typical applicant that average would be ≈ 50.\n\n**Why is the selected group's average luck {luck} if luck only weighs {p}%?** {n} applicants compete for {k} seats, so the finalists have very high and very similar skill (those selected average {skill} and the ideal skill-only top {ideal}: only {gap} points apart). Against such a small gap, luck, which can move the final score by up to {boost} points, decides who gets in, and those who get in are the ones who were very lucky. Luck weighs little in the formula but a lot in *who ends up selected*.",
    ),
    "zh": dict(
        reset="↺ 恢复初始值",
        k_profile="入选者概况 · 平均得分，而非百分比",
        k_impact="运气对选拔的影响",
        m_skill="入选者平均能力", m_ideal="理想名单平均能力",
        m_luck_help="入选者的平均运气得分（1–100）。普通申请人约为 50。这不是运气权重。",
        cap_luck="运气得分 · 普通申请人约为 50",
        cap_skill="能力得分 · 普通申请人约为 50",
        cap_ideal="若仅按能力选拔",
        cap_coinc="（共 {n} 个名额）即使没有运气也会入选",
        cap_other="（共 {n} 个名额）因运气权重而改变",
        cap_pct="的入选者仅凭能力不会入选",
        how_title="如何解读这些指标",
        how="**{p}% 是最终得分中的*权重*，不是指标所显示数值的百分比。** 每位申请人的最终得分 = {s}% × 能力 + {p}% × 运气（均为 1 到 100 分）。而上方的指标是这 {k} 位入选者的 **1 到 100 的平均得分**；对于任意一位申请人，该平均值约为 50。\n\n**为什么运气仅占 {p}%，入选者的平均运气却是 {luck}？** {n} 人竞争 {k} 个名额，进入最后阶段的人能力都极高且彼此非常接近（入选者平均 {skill}，仅按能力的理想名单为 {ideal}，相差只有 {gap} 分）。在这样微小的差距面前，运气最多可使最终得分变动 {boost} 分，因此由它来决定谁入选，入选的往往是运气极好的人。运气在公式中的权重不大，但对*谁被选中*影响很大。",
    ),
    "hi": dict(
        reset="↺ प्रारंभिक मान पुनर्स्थापित करें",
        k_profile="चयनित लोगों का प्रोफ़ाइल · औसत स्कोर, प्रतिशत नहीं",
        k_impact="चयन पर भाग्य का प्रभाव",
        m_skill="चयनित लोगों की औसत योग्यता", m_ideal="आदर्श शीर्ष की औसत योग्यता",
        m_luck_help="चयनित लोगों का औसत भाग्य स्कोर (1–100)। सामान्य आवेदक का औसत ≈ 50। यह भाग्य का भार नहीं है।",
        cap_luck="भाग्य स्कोर · सामान्य आवेदक ≈ 50",
        cap_skill="योग्यता स्कोर · सामान्य आवेदक ≈ 50",
        cap_ideal="यदि केवल योग्यता से चयन होता",
        cap_coinc="{n} में से बिना भाग्य के भी चुने जाते",
        cap_other="{n} में से भाग्य के भार से बदल जाते हैं",
        cap_pct="चयनित लोग केवल योग्यता से नहीं चुने जाते",
        how_title="इन संकेतकों को कैसे पढ़ें",
        how="**{p}% अंतिम स्कोर में एक *भार* है, संकेतकों में दिखने वाली संख्या का प्रतिशत नहीं।** हर आवेदक का अंतिम स्कोर = {s}% × योग्यता + {p}% × भाग्य (दोनों 1 से 100 में)। ऊपर के संकेतक चुने गए {k} लोगों के **1 से 100 के औसत स्कोर** हैं; किसी भी सामान्य आवेदक के लिए यह औसत ≈ 50 होगा।\n\n**भाग्य का भार केवल {p}% होने पर भी चयनित लोगों का औसत भाग्य {luck} क्यों है?** {k} सीटों के लिए {n} आवेदक प्रतिस्पर्धा करते हैं, इसलिए अंतिम दौर के लोगों की योग्यता बहुत ऊँची और एक-दूसरे के बहुत करीब होती है (चयनित लोगों का औसत {skill} और केवल-योग्यता वाले आदर्श शीर्ष का {ideal}: केवल {gap} अंक का अंतर)। इतने छोटे अंतर के सामने भाग्य, जो अंतिम स्कोर को अधिकतम {boost} अंक तक बदल सकता है, तय करता है कि कौन चुना जाएगा, और वही चुने जाते हैं जिनका भाग्य बहुत ऊँचा था। सूत्र में भाग्य का भार कम है, पर *कौन चुना जाएगा* इसमें उसका असर बड़ा है।",
    ),
    "ar": dict(
        reset="↺ استعادة القيم الأولية",
        k_profile="ملف المختارين · متوسطات درجات وليست نسبًا",
        k_impact="أثر الحظ في الانتقاء",
        m_skill="متوسط مهارة المختارين", m_ideal="متوسط مهارة الأفضل مثاليًا",
        m_luck_help="متوسط درجة حظ المختارين (1–100). المتقدم العادي ≈ 50. وهذا ليس وزن الحظ.",
        cap_luck="درجة الحظ · المتقدم العادي ≈ 50",
        cap_skill="درجة المهارة · المتقدم العادي ≈ 50",
        cap_ideal="لو تم الاختيار بالمهارة وحدها",
        cap_coinc="من {n} كانوا سيُختارون حتى دون حظ",
        cap_other="من {n} يتغيرون بسبب وزن الحظ",
        cap_pct="من المختارين لم يكونوا ليُختاروا بالمهارة وحدها",
        how_title="كيف تقرأ هذه المؤشرات",
        how="**الـ {p}% هو *وزن* داخل الدرجة النهائية، وليس نسبة مما تعرضه المؤشرات.** تحصل كل متقدم على درجة نهائية = {s}% × مهارته + {p}% × حظه (كلاهما من 1 إلى 100). أما المؤشرات أعلاه فهي **متوسطات درجات من 1 إلى 100** للأشخاص الـ {k} المختارين؛ ولأي متقدم عادي يكون هذا المتوسط ≈ 50.\n\n**لماذا متوسط حظ المختارين {luck} مع أن وزن الحظ {p}% فقط؟** يتنافس {n} متقدم على {k} مقعدًا، فيكون للمرشحين النهائيين مهارة عالية جدًا ومتقاربة (متوسط المختارين {skill} وأفضل انتقاء بالمهارة وحدها {ideal}: فرق {gap} نقطة فقط). أمام هذا الفرق الضئيل، يحسم الحظ، الذي قد يغيّر الدرجة النهائية حتى {boost} نقطة، من يدخل، ويدخل من كان حظه عاليًا جدًا. فالحظ قليل الوزن في المعادلة، لكن أثره كبير في *من يتم اختياره*.",
    ),
}
for _k in TR:
    TR[_k].update(NUEVO2[_k])


SW_NOW = {'es': 'Valor actual', 'en': 'Current value', 'zh': '当前值', 'hi': 'वर्तमान मान', 'ar': 'القيمة الحالية'}
for _k in TR:
    TR[_k]["sw_now"] = SW_NOW[_k]


NUEVO3 = {'es': {'sec_viz': 'Visualizaciones', 'sec_detail': 'Detalle y exportación', 'pf_title': 'Perfil de los elegidos: habilidad y suerte', 'pf_pop': 'Aplicante típico', 'pf_sel': 'Elegidos', 'pf_ideal': 'Top ideal (solo habilidad)', 'pf_y': 'Puntuación promedio', 'sw2_title': 'Habilidad y suerte de los elegidos según el peso de la suerte', 'hs_title': 'Habilidad promedio de los elegidos (una observación por simulación)', 'hs_x': 'Habilidad promedio', 'tbl_current': 'Escenario actual', 'tbl_param': 'Parámetro', 'tbl_value': 'Valor', 'tbl_sweep': 'Barrido del peso de la suerte'}, 'en': {'sec_viz': 'Visualizations', 'sec_detail': 'Detail and export', 'pf_title': 'Profile of those selected: skill and luck', 'pf_pop': 'Typical applicant', 'pf_sel': 'Selected', 'pf_ideal': 'Ideal top (skill only)', 'pf_y': 'Average score', 'sw2_title': 'Skill and luck of those selected by luck weight', 'hs_title': 'Average skill of those selected (one observation per simulation)', 'hs_x': 'Average skill', 'tbl_current': 'Current scenario', 'tbl_param': 'Parameter', 'tbl_value': 'Value', 'tbl_sweep': 'Luck-weight sweep'}, 'zh': {'sec_viz': '可视化', 'sec_detail': '明细与导出', 'pf_title': '入选者概况：能力与运气', 'pf_pop': '普通申请人', 'pf_sel': '入选者', 'pf_ideal': '理想名单（仅按能力）', 'pf_y': '平均得分', 'sw2_title': '入选者的能力与运气随运气权重的变化', 'hs_title': '入选者平均能力（每次模拟一个观测值）', 'hs_x': '平均能力', 'tbl_current': '当前情景', 'tbl_param': '参数', 'tbl_value': '数值', 'tbl_sweep': '运气权重扫描'}, 'hi': {'sec_viz': 'विज़ुअलाइज़ेशन', 'sec_detail': 'विवरण और निर्यात', 'pf_title': 'चयनित लोगों का प्रोफ़ाइल: योग्यता और भाग्य', 'pf_pop': 'सामान्य आवेदक', 'pf_sel': 'चयनित', 'pf_ideal': 'आदर्श शीर्ष (केवल योग्यता)', 'pf_y': 'औसत स्कोर', 'sw2_title': 'भाग्य के भार के अनुसार चयनित लोगों की योग्यता और भाग्य', 'hs_title': 'चयनित लोगों की औसत योग्यता (प्रति सिमुलेशन एक अवलोकन)', 'hs_x': 'औसत योग्यता', 'tbl_current': 'वर्तमान परिदृश्य', 'tbl_param': 'पैरामीटर', 'tbl_value': 'मान', 'tbl_sweep': 'भाग्य-भार स्वीप'}, 'ar': {'sec_viz': 'المرئيات', 'sec_detail': 'التفاصيل والتصدير', 'pf_title': 'ملف المختارين: المهارة والحظ', 'pf_pop': 'متقدم عادي', 'pf_sel': 'المختارون', 'pf_ideal': 'الأفضل مثاليًا (بالمهارة فقط)', 'pf_y': 'متوسط الدرجة', 'sw2_title': 'مهارة وحظ المختارين بحسب وزن الحظ', 'hs_title': 'متوسط مهارة المختارين (ملاحظة واحدة لكل محاكاة)', 'hs_x': 'متوسط المهارة', 'tbl_current': 'السيناريو الحالي', 'tbl_param': 'المعلمة', 'tbl_value': 'القيمة', 'tbl_sweep': 'مسح وزن الحظ'}}
for _k in TR:
    TR[_k].update(NUEVO3[_k])


DIST_T = {'es': 'Distribución de los elegidos: suerte y habilidad', 'en': 'Distribution of those selected: luck and skill', 'zh': '入选者分布：运气与能力', 'hi': 'चयनित लोगों का वितरण: भाग्य और योग्यता', 'ar': 'توزيع المختارين: الحظ والمهارة'}
for _k in TR:
    TR[_k]["dist_title"] = DIST_T[_k]


ZOOM_T = {'es': 'eje ampliado', 'en': 'zoomed axis', 'zh': '放大坐标轴', 'hi': 'ज़ूम किया हुआ अक्ष', 'ar': 'محور مكبّر'}
for _k in TR:
    TR[_k]["hs_zoom"] = ZOOM_T[_k]


HS_SHORT = {'es': 'Habilidad promedio de los elegidos', 'en': 'Average skill of those selected', 'zh': '入选者平均能力', 'hi': 'चयनित लोगों की औसत योग्यता', 'ar': 'متوسط مهارة المختارين'}
for _k in TR:
    TR[_k]["hs_title"] = HS_SHORT[_k]


NUEVO4 = {'es': {'dl_data': '⬇️ Datos del gráfico (CSV)', 'dl_data_help': 'Datos subyacentes de este gráfico.', 'sec_scn': 'Escenarios y exportación'}, 'en': {'dl_data': '⬇️ Chart data (CSV)', 'dl_data_help': 'Underlying data of this chart.', 'sec_scn': 'Scenarios and export'}, 'zh': {'dl_data': '⬇️ 图表数据 (CSV)', 'dl_data_help': '此图表的底层数据。', 'sec_scn': '情景与导出'}, 'hi': {'dl_data': '⬇️ चार्ट डेटा (CSV)', 'dl_data_help': 'इस चार्ट का अंतर्निहित डेटा।', 'sec_scn': 'परिदृश्य और निर्यात'}, 'ar': {'dl_data': '⬇️ بيانات الرسم (CSV)', 'dl_data_help': 'البيانات التي يعتمد عليها هذا الرسم.', 'sec_scn': 'السيناريوهات والتصدير'}}
for _k in TR:
    TR[_k].update(NUEVO4[_k])

# ------------------------------------------------------------------- tema
# Misma paleta en ambos modos: blanco, negro, azul y gris.
PALETAS = {
    False: dict(bg="#FFFFFF", text="#0B0B0B", accent="#0B5FFF", muted="#6B7280",
                line="#D1D5DB", panel="#F3F4F6"),
    True: dict(bg="#0B0B0B", text="#FFFFFF", accent="#3B82F6", muted="#9CA3AF",
               line="#3A3F47", panel="#161A20"),
}

CSS = """
<style>
:root{--bg:%(bg)s;--text:%(text)s;--accent:%(accent)s;--muted:%(muted)s;--line:%(line)s;--panel:%(panel)s;
  --glass:%(glass)s;--glass-line:%(glass_line)s;}
html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"]{
  background:var(--bg)!important;color:var(--text)!important;font-family:%(font)s;}
[data-testid="stSidebar"], [data-testid="stSidebar"] > div{
  background:var(--panel)!important;border-right:1px solid var(--line);}
.stApp h1,.stApp h2,.stApp h3{color:var(--text)!important;font-weight:700;letter-spacing:-0.01em;}
.stApp h1{border-bottom:3px solid var(--accent);padding-bottom:.4rem;}
.stApp h3{border-left:4px solid var(--accent);padding-left:.6rem;}
.stApp p,.stApp li,.stApp label,.stApp span,[data-testid="stWidgetLabel"] *{color:var(--text);}
[data-testid="stCaptionContainer"] *{color:var(--muted)!important;}
.stApp code{background:var(--panel);color:var(--accent);}
.stApp hr{border-color:var(--line);}
[data-testid="stMetric"]{background:var(--panel);border:1px solid var(--line);
  border-left:4px solid var(--accent);padding:.8rem 1rem;border-radius:4px;}
[data-testid="stMetricValue"],[data-testid="stMetricValue"] *{color:var(--accent)!important;}
[data-testid="stMetricLabel"],[data-testid="stMetricLabel"] *{color:var(--muted)!important;}
.stButton>button,.stDownloadButton>button,
[data-testid="stBaseButton-secondary"],[data-testid="stBaseButton-primary"]{
  background:var(--bg)!important;border:1px solid var(--accent)!important;border-radius:4px;}
.stButton>button *,.stDownloadButton>button *,
[data-testid="stBaseButton-secondary"] *,[data-testid="stBaseButton-primary"] *{color:var(--accent)!important;}
.stButton>button:hover,.stDownloadButton>button:hover,
[data-testid="stBaseButton-secondary"]:hover,[data-testid="stBaseButton-primary"]:hover{
  background:var(--accent)!important;}
.stButton>button:hover *,.stDownloadButton>button:hover *,
[data-testid="stBaseButton-secondary"]:hover *,[data-testid="stBaseButton-primary"]:hover *{
  color:var(--bg)!important;}
[data-testid="stTooltipIcon"] *,[data-testid="stTooltipHoverTarget"] *{color:var(--muted)!important;}
[data-testid="stTooltipIcon"] svg,[data-testid="stTooltipHoverTarget"] svg{color:var(--muted)!important;fill:var(--muted)!important;opacity:1!important;}
%(ctl)s
[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stSidebar"] [data-testid="stLayoutWrapper"] > [data-testid="stVerticalBlock"]{
  background:var(--glass)!important;border:1px solid var(--glass-line)!important;
  border-radius:14px!important;padding:.35rem .45rem .2rem;margin-bottom:.55rem;}
.stApp h4{color:var(--text)!important;font-weight:600;font-size:1.05rem;
  border-bottom:1px solid var(--line);padding-bottom:.3rem;margin-top:.9rem;}
.grp{font-size:.7rem;font-weight:700;letter-spacing:.09em;text-transform:uppercase;
  color:var(--accent)!important;margin:.1rem 0 .3rem;}
.splitbar{display:flex;height:8px;border-radius:6px;background:var(--muted);overflow:hidden;margin:.1rem 0 .3rem;}
.splitbar>span{display:block;height:100%%;background:var(--accent);}
.splittxt{font-size:.8rem;color:var(--muted)!important;margin-bottom:.6rem;}
.splittxt b{color:var(--text)!important;}
input,[data-baseweb="input"],[data-baseweb="base-input"]{
  background:var(--bg)!important;color:var(--text)!important;border-color:var(--line)!important;}
[data-testid="stNumberInputStepUp"],[data-testid="stNumberInputStepDown"]{
  background:var(--panel)!important;color:var(--text)!important;}
[data-baseweb="slider"] [role="slider"]{background:var(--accent)!important;}
[data-testid="stSliderThumbValue"],[data-testid="stSliderThumbValue"] *{color:var(--accent)!important;}
[data-testid="stSliderTickBarMin"],[data-testid="stSliderTickBarMax"]{color:var(--muted)!important;}
.stTable table{border-collapse:collapse;width:100%%;font-size:.85rem;}
.stTable th{background:var(--panel)!important;color:var(--text)!important;border:1px solid var(--line)!important;}
.stTable td{background:var(--bg)!important;color:var(--text)!important;border:1px solid var(--line)!important;}
.note{border:1px solid var(--line);border-left:4px solid var(--accent);background:var(--panel);
  padding:1rem 1.2rem;border-radius:4px;margin-top:1rem;margin-bottom:1.4rem;}
.note *{color:var(--text)!important;}
%(rtl)s
</style>
"""
CTL_CSS = """
[data-testid="stCheckbox"] label:has(input[role="switch"]) > div:nth-of-type(1){
  background:var(--line)!important;}
[data-testid="stCheckbox"] label[data-selected="true"]:has(input[role="switch"]) > div:nth-of-type(1){
  background:var(--accent)!important;}
[data-testid="stCheckbox"] label:has(input[role="switch"]) > div:nth-of-type(1) > div{
  background:var(--bg)!important;}
[data-testid="stCheckbox"] label:not(:has(input[role="switch"])) > div:nth-of-type(1){
  border:2px solid var(--muted)!important;background:var(--bg)!important;}
[data-testid="stCheckbox"] label[data-selected="true"]:not(:has(input[role="switch"])) > div:nth-of-type(1){
  border-color:var(--accent)!important;background:var(--accent)!important;}
label[data-testid="stRadioOption"] > div > div:first-child{
  background:var(--bg)!important;border:2px solid var(--muted)!important;}
label[data-testid="stRadioOption"][data-selected="true"] > div > div:first-child{
  border-color:var(--accent)!important;}
label[data-testid="stRadioOption"] > div > div:first-child > div{background:transparent!important;}
label[data-testid="stRadioOption"][data-selected="true"] > div > div:first-child > div{
  background:var(--accent)!important;}
"""
RTL_CSS = """[data-testid="stMarkdownContainer"],[data-testid="stHeading"],
[data-testid="stCaptionContainer"],.note{direction:rtl;text-align:right;}"""


def estilo_fig(fig, P, titulo):
    fig.update_layout(
        title=dict(text=titulo, font=dict(size=15, color=P["text"])),
        paper_bgcolor=P["bg"], plot_bgcolor=P["bg"],
        font=dict(color=P["text"], family=FONT),
        legend=dict(font=dict(color=P["text"])),
        margin=dict(l=40, r=20, t=60, b=40),
    )
    fig.update_xaxes(gridcolor=P["line"], linecolor=P["muted"], zerolinecolor=P["line"])
    fig.update_yaxes(gridcolor=P["line"], linecolor=P["muted"], zerolinecolor=P["line"])
    return fig


# ---------------------------------------------------------------- simulación
def top_k(values, k, rng):
    """Índices de los k valores más altos; empates resueltos al azar."""
    jitter = rng.random(values.shape[0]) * 1e-6
    return np.argpartition(-(values + jitter), k - 1)[:k]


def _phi(x):
    """CDF normal estándar (aproximación tanh, error < 1e-3)."""
    return 0.5 * (1 + np.tanh(0.7978845608 * (x + 0.044715 * x**3)))


def generar(rng, n, discreto, normal, rho):
    """Habilidad y suerte de n aplicantes.

    - Suerte: siempre uniforme 1–100.
    - Habilidad: uniforme 1–100, o normal (media 50, desv. 15, sin truncar).
    - rho: correlación gaussiana entre ambas (0 = independientes).
    Con uniforme + rho=0 se usa el camino original (mismos resultados que antes).
    """
    if rho == 0 and not normal:
        if discreto:
            return (rng.integers(1, 101, n).astype(float),
                    rng.integers(1, 101, n).astype(float))
        return rng.uniform(1, 100, n), rng.uniform(1, 100, n)
    z1 = rng.standard_normal(n)
    z2 = rho * z1 + np.sqrt(1 - rho**2) * rng.standard_normal(n)
    skill = 50 + 15 * z1 if normal else 1 + 99 * _phi(z1)
    luck = 1 + 99 * _phi(z2)
    if discreto:
        skill = np.clip(np.rint(skill), 1, 100)
        luck = np.rint(luck)
    return skill, luck


def puntuar(rng, skill, luck, peso_suerte, sigma):
    """Puntuación del selector: habilidad medida (con ruido) y suerte."""
    medida = skill + sigma * rng.standard_normal(skill.shape[0]) if sigma > 0 else skill
    return (1 - peso_suerte) * medida + peso_suerte * luck


@st.cache_data(show_spinner=False)
def simular(n_aplicantes, n_plazas, peso_suerte, n_sims, discreto, semilla,
            normal=False, rho=0.0, sigma=0.0):
    rng = np.random.default_rng(semilla)
    filas = []
    for _ in range(n_sims):
        skill, luck = generar(rng, n_aplicantes, discreto, normal, rho)
        score = puntuar(rng, skill, luck, peso_suerte, sigma)
        elegidos = top_k(score, n_plazas, rng)
        solo_skill = top_k(skill, n_plazas, rng)  # ideal: habilidad real

        filas.append(
            {
                "suerte_prom_elegidos": luck[elegidos].mean(),
                "skill_prom_elegidos": skill[elegidos].mean(),
                "skill_prom_top_skill": skill[solo_skill].mean(),
                "suerte_prom_top_skill": luck[solo_skill].mean(),
                "coinciden_con_solo_skill": np.intersect1d(elegidos, solo_skill).size,
            }
        )
    return pd.DataFrame(filas)


@st.cache_data(show_spinner=False)
def barrido_suerte(n_aplicantes, n_plazas, n_sims, discreto, semilla, pesos,
                   normal=False, rho=0.0, sigma=0.0):
    out = []
    for p in pesos:
        df = simular(n_aplicantes, n_plazas, p, n_sims, discreto, semilla, normal, rho, sigma)
        out.append(
            {
                "peso_suerte_%": p * 100,
                "suerte_prom_elegidos": df["suerte_prom_elegidos"].mean(),
                "skill_prom_elegidos": df["skill_prom_elegidos"].mean(),
                "coinciden": df["coinciden_con_solo_skill"].mean(),
                "pct_distintos": 100
                * (1 - df["coinciden_con_solo_skill"].mean() / n_plazas),
            }
        )
    return pd.DataFrame(out)


def tabla(df):
    """Tabla HTML (se adapta al tema claro/oscuro)."""
    st.table(df.style.hide(axis="index").format(
        lambda v: f"{v:g}" if isinstance(v, float) else v))


# ------------------------------------------------------------------- sidebar
def rgba(hex_color, alpha):
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r},{g},{b},{alpha})"


def titulo_grupo(texto):
    st.markdown(f'<div class="grp">{texto}</div>', unsafe_allow_html=True)


def bloque(texto):
    """Título de bloque de gráficos (más visible que las etiquetas pequeñas)."""
    st.markdown(f"#### {texto}")


with st.sidebar.container(border=True):
    titulo_grupo("Interface · Interfaz")
    lang = st.radio("🌐 Language / Idioma", list(LANGS), format_func=LANGS.get, key="lang")
    T = TR[lang]
    oscuro = st.toggle("🌙 " + T["dark"], value=True, key="oscuro")
P = PALETAS[oscuro]
st.markdown(
    CSS % dict(**P, font=FONT.replace("%", "%%"), rtl=RTL_CSS if lang == "ar" else "",
               ctl=CTL_CSS, glass=rgba(P["accent"], 0.07), glass_line=rgba(P["muted"], 0.45)),
    unsafe_allow_html=True,
)

st.sidebar.header(T["params"])

DEFAULTS = dict(n_aplicantes=18_300, n_plazas=11, peso_pct=5.0, n_sims=1_000,
                modo_punt="cont", normal=False, sigma=0.0, rho=0.0, semilla=42)


for _k, _v in DEFAULTS.items():
    st.session_state.setdefault(_k, _v)


def restablecer():
    for k, v in DEFAULTS.items():
        st.session_state[k] = v


st.sidebar.button(T["reset"], on_click=restablecer, width="stretch")

with st.sidebar.container(border=True):
    titulo_grupo(T["g_pop"])
    n_aplicantes = st.slider(T["applicants"], 100, 100_000, step=100, key="n_aplicantes")
    n_plazas = st.slider(T["seats"], 1, min(200, n_aplicantes - 1), key="n_plazas")

with st.sidebar.container(border=True):
    titulo_grupo(T["g_weight"])
    peso_suerte = st.slider(T["luck_w"], 0.0, LUCK_MAX, step=0.5, help=T["luck_help"], key="peso_pct") / 100
    _l, _h = peso_suerte * 100, 100 - peso_suerte * 100
    st.markdown(
        f'<div class="splitbar"><span style="width:{_h}%"></span></div>'
        f'<div class="splittxt">{T["luck"]} <b>{_l:g}%</b> + {T["skill"]} <b>{_h:g}%</b> = 100%</div>',
        unsafe_allow_html=True,
    )

with st.sidebar.container(border=True):
    titulo_grupo(T["g_real"])
    modo_punt = st.radio(
        T["scoring"], ["cont", "int"],
        format_func=lambda k: T["sc_cont"] if k == "cont" else T["sc_int"],
        key="modo_punt",
    )
    discreto = modo_punt == "int"
    normal = st.toggle(T["dist"], key="normal", help=T["dist_help"])
    sigma = st.slider(T["noise"], 0.0, 20.0, step=0.5, help=T["noise_help"], key="sigma")
    rho = st.slider(T["rho"], -0.5, 0.9, step=0.05, help=T["rho_help"], key="rho")

with st.sidebar.container(border=True):
    titulo_grupo(T["g_sim"])
    n_sims = st.slider(T["sims"], 100, 5_000, step=100, key="n_sims")
    semilla = st.number_input(T["seed"], 0, 10_000, key="semilla")

# ---------------------------------------------------------------------- main
st.title("🎲 " + T["title"])
st.markdown(T["intro"])

with st.spinner(T["spinner"]):
    df = simular(n_aplicantes, n_plazas, peso_suerte, n_sims, discreto, semilla,
                 normal, rho, sigma)

coinc = df["coinciden_con_solo_skill"].mean()
luck_sel = df["suerte_prom_elegidos"].mean()
skill_sel = df["skill_prom_elegidos"].mean()
skill_ideal = df["skill_prom_top_skill"].mean()
luck_ideal = df["suerte_prom_top_skill"].mean()
pct_dist = 100 * (1 - coinc / n_plazas)
pop_skill = 50.0 if normal else 50.5   # media poblacional de habilidad
pop_luck = 50.5                         # media poblacional de suerte

# =============================== 1) KPIs (arriba) ===============================
titulo_grupo(T["k_profile"])
a1, a2, a3 = st.columns(3)
a1.metric(T["m_luck"], f"{luck_sel:.1f}", help=T["m_luck_help"])
a1.caption(T["cap_luck"])
a2.metric(T["m_skill"], f"{skill_sel:.2f}")
a2.caption(T["cap_skill"])
a3.metric(T["m_ideal"], f"{skill_ideal:.2f}")
a3.caption(T["cap_ideal"])

titulo_grupo(T["k_impact"])
b1, b2, b3 = st.columns(3)
b1.metric(T["m_coinc"], f"{coinc:.2f} / {n_plazas}")
b1.caption(T["cap_coinc"].format(n=n_plazas))
b2.metric(T["m_other"], f"{n_plazas - coinc:.1f} / {n_plazas}")
b2.caption(T["cap_other"].format(n=n_plazas))
b3.metric(T["m_pct"], f"{pct_dist:.0f}%")
b3.caption(T["cap_pct"])

_how = T["how"].format(
    p=f"{peso_suerte * 100:g}", s=f"{100 - peso_suerte * 100:g}",
    n=f"{n_aplicantes:,}", k=n_plazas, luck=f"{luck_sel:.1f}",
    skill=f"{skill_sel:.2f}", ideal=f"{skill_ideal:.2f}",
    gap=f"{abs(skill_ideal - skill_sel):.2f}", boost=f"{99 * peso_suerte:.1f}",
)
st.markdown(f'<div class="note">\n\n**{T["how_title"]}**\n\n{_how}\n\n</div>',
            unsafe_allow_html=True)

modo = "enteras" if discreto else "continuas"
dist = "normal" if normal else "uniforme"
sufijo = f"a{n_aplicantes}_p{n_plazas}_s{peso_suerte * 100:g}_{modo}_{dist}_r{sigma:g}_c{rho:g}"


def dl(destino, datos, nombre, clave):
    """Botón para descargar los datos subyacentes de un gráfico."""
    destino.download_button(
        T["dl_data"], datos.to_csv(index=False).encode("utf-8"),
        file_name=f"{nombre}_{sufijo}.csv", mime="text/csv", key=clave, help=T["dl_data_help"],
    )


# ============================ 2) Visualizaciones (centro) ============================
st.subheader(T["sec_viz"])
y_max = max(105.0, skill_sel + 8, skill_ideal + 8)

# --- Fila A: perfil (habilidad y suerte) + coincidencias
gA1, gA2 = st.columns(2)
_grupos = [("aplicante_tipico", T["pf_pop"], pop_skill, pop_luck),
           ("elegidos", T["pf_sel"], skill_sel, luck_sel),
           ("top_ideal", T["pf_ideal"], skill_ideal, luck_ideal)]
perfil = pd.DataFrame(
    [
        {"grupo_cod": c, "grupo": g, "atributo_cod": ac, "atributo": at, "valor": v}
        for c, g, hab, sue in _grupos
        for ac, at, v in (("habilidad", T["skill"], hab), ("suerte", T["luck"], sue))
    ]
)
fig_p = px.bar(
    perfil, x="grupo", y="valor", color="atributo", barmode="group", text_auto=".1f",
    labels={"grupo": "", "valor": T["pf_y"], "atributo": ""},
    category_orders={"grupo": [g[1] for g in _grupos], "atributo": [T["skill"], T["luck"]]},
    color_discrete_map={T["skill"]: P["accent"], T["luck"]: P["muted"]},
)
fig_p.update_traces(textposition="outside", cliponaxis=False)
fig_p.update_layout(bargap=0.25, bargroupgap=0.06)
fig_p.update_yaxes(range=[0, y_max])
gA1.plotly_chart(estilo_fig(fig_p, P, T["pf_title"]), width="stretch", theme=None)
dl(gA1, perfil[["grupo_cod", "atributo_cod", "valor"]], "perfil_elegidos", "dl_perfil")

conteo = (df["coinciden_con_solo_skill"].value_counts()
          .reindex(range(0, n_plazas + 1), fill_value=0).rename_axis("coinciden")
          .reset_index())
conteo.columns = ["coinciden", "simulaciones"]
fig2 = px.bar(conteo, x="coinciden", y="simulaciones",
              labels={"coinciden": T["b_x"], "simulaciones": T["b_y"]})
fig2.update_traces(marker_color=P["accent"])
fig2.update_xaxes(range=[-0.6, n_plazas + 0.6])
gA2.plotly_chart(estilo_fig(fig2, P, T["b_title"]), width="stretch", theme=None)
dl(gA2, conteo, "coincidencias", "dl_coinc")

# --- Fila B: cómo cambia todo con el peso de la suerte (mismo rango que el selector)
bloque(T["sw_header"])
sw_on = st.checkbox(f'{T["sw_check"]} (0%–{LUCK_MAX:g}%)', value=True, key="sw_on")
sw = None
if sw_on:
    pesos = [g / 100 for g in GRID_PCT if g <= LUCK_MAX]
    n_b = int(max(30, min(200, n_sims, 5e7 / (len(pesos) * n_aplicantes))))
    with st.spinner(T["sw_spin"]):
        sw = barrido_suerte(n_aplicantes, n_plazas, n_b, discreto, semilla, tuple(pesos),
                            normal, rho, sigma)
    marca = dict(x=peso_suerte * 100, line_dash="dash", line_color=P["muted"],
                 annotation_text=f'{T["sw_now"]}: {peso_suerte * 100:g}%',
                 annotation_font_color=P["muted"])
    gB1, gB2 = st.columns(2)

    sw_long = sw.melt(id_vars="peso_suerte_%",
                      value_vars=["skill_prom_elegidos", "suerte_prom_elegidos"],
                      var_name="serie", value_name="valor")
    sw_long["serie"] = sw_long["serie"].map(
        {"skill_prom_elegidos": T["skill"], "suerte_prom_elegidos": T["luck"]})
    fig_s = px.line(sw_long, x="peso_suerte_%", y="valor", color="serie", markers=True,
                    labels={"peso_suerte_%": T["luck_w"], "valor": T["pf_y"], "serie": ""},
                    color_discrete_map={T["skill"]: P["accent"], T["luck"]: P["muted"]})
    fig_s.for_each_trace(lambda t: t.update(line=dict(dash="dot")) if t.name == T["luck"] else None)
    fig_s.add_vline(**marca)
    fig_s.add_hline(y=pop_luck, line_dash="longdash", line_color=P["line"],
                    annotation_text=T["pf_pop"], annotation_font_color=P["muted"],
                    annotation_position="bottom right")
    fig_s.update_xaxes(range=[0, LUCK_MAX])
    fig_s.update_yaxes(range=[max(0.0, float(min(sw_long["valor"].min(), pop_luck)) - 8),
                              float(sw_long["valor"].max()) + 5])
    gB1.plotly_chart(estilo_fig(fig_s, P, T["sw2_title"]), width="stretch", theme=None)
    dl(gB1, sw[["peso_suerte_%", "skill_prom_elegidos", "suerte_prom_elegidos"]], "barrido_habilidad_suerte", "dl_sw1")

    fig4 = px.line(sw, x="peso_suerte_%", y="pct_distintos", markers=True,
                   labels={"pct_distintos": T["m_pct"], "peso_suerte_%": T["luck_w"]})
    fig4.update_traces(line_color=P["accent"], marker_color=P["accent"])
    fig4.add_vline(**marca)
    fig4.update_xaxes(range=[0, LUCK_MAX])
    fig4.update_yaxes(range=[0, 100])
    gB2.plotly_chart(estilo_fig(fig4, P, T["sw_fig"].format(n=n_b)), width="stretch", theme=None)
    dl(gB2, sw[["peso_suerte_%", "coinciden", "pct_distintos"]], "barrido_pct_distintos", "dl_sw2")

# --- Fila C: distribuciones gemelas (suerte y habilidad de los elegidos)
bloque(T["dist_title"])
gC1, gC2 = st.columns(2)

fig1 = px.histogram(df, x="suerte_prom_elegidos", nbins=40, labels={"suerte_prom_elegidos": T["h_x"]})
fig1.update_traces(marker_color=P["accent"], marker_line_color=P["bg"], marker_line_width=1)
fig1.add_vline(x=pop_luck, line_dash="dash", line_color=P["muted"],
               annotation_text=T["h_vline"], annotation_font_color=P["muted"])
fig1.update_xaxes(range=[0, 100])
gC1.plotly_chart(estilo_fig(fig1, P, T["h_title"]), width="stretch", theme=None)
dl(gC1, df.rename_axis("sim").reset_index()[["sim", "suerte_prom_elegidos"]], "dist_suerte", "dl_hs")

fig_h = px.histogram(df, x="skill_prom_elegidos", nbins=40, labels={"skill_prom_elegidos": T["hs_x"]})
fig_h.update_traces(marker_color=P["accent"], marker_line_color=P["bg"], marker_line_width=1)
fig_h.add_vline(x=skill_ideal, line_dash="dash", line_color=P["muted"],
                annotation_text=T["pf_ideal"], annotation_font_color=P["muted"],
                annotation_position="top left")
_lo = float(min(df["skill_prom_elegidos"].min(), skill_ideal))
_hi = float(max(df["skill_prom_elegidos"].max(), skill_ideal))
_pad = max(0.05, 0.12 * (_hi - _lo))
fig_h.update_xaxes(range=[_lo - _pad, _hi + _pad])
gC2.plotly_chart(estilo_fig(fig_h, P, f'{T["hs_title"]} · {T["hs_zoom"]}'), width="stretch", theme=None)
dl(gC2, df.rename_axis("sim").reset_index()[["sim", "skill_prom_elegidos", "skill_prom_top_skill"]],
   "dist_habilidad", "dl_hh")

# --- Fila D: una selección en detalle
bloque(T["d_title"])
rng = np.random.default_rng(semilla + 1)
skill, luck = generar(rng, n_aplicantes, discreto, normal, rho)
score = puntuar(rng, skill, luck, peso_suerte, sigma)
sel = np.zeros(n_aplicantes, bool)
sel[top_k(score, n_plazas, rng)] = True
muestra = rng.choice(n_aplicantes, size=min(4000, n_aplicantes), replace=False)
idx = np.union1d(muestra, np.where(sel)[0])
dd = pd.DataFrame(
    {T["skill"]: skill[idx], T["luck"]: luck[idx],
     T["group"]: np.where(sel[idx], T["sel"], T["nsel"]), "_o": sel[idx]}
).sort_values("_o")
fig3 = px.scatter(
    dd, x=T["skill"], y=T["luck"], color=T["group"], opacity=0.75,
    color_discrete_map={T["sel"]: P["accent"], T["nsel"]: P["muted"]},
)
fig3.for_each_trace(lambda t: t.update(marker=dict(size=13 if t.name == T["sel"] else 5)))
fig3.update_yaxes(range=[0, 101])
st.plotly_chart(estilo_fig(fig3, P, T["sc_title"]), width="stretch", theme=None)
dl(st, pd.DataFrame({"habilidad": skill[idx], "suerte": luck[idx], "elegido": sel[idx]}),
   "seleccion_detalle", "dl_scatter")

st.markdown(f'<div class="note">\n\n{T["concl"]}\n\n</div>', unsafe_allow_html=True)

# ====================== 3) Escenarios y exportación (abajo) ======================
st.subheader(T["sec_scn"])

resumen = pd.DataFrame(
    [
        {
            "aplicantes": n_aplicantes,
            "plazas": n_plazas,
            "peso_suerte_pct": round(peso_suerte * 100, 2),
            "simulaciones": n_sims,
            "puntuaciones": modo,
            "distribucion_habilidad": dist,
            "ruido_medicion": sigma,
            "correlacion": rho,
            "semilla": semilla,
            "suerte_prom_elegidos": round(luck_sel, 3),
            "suerte_prom_elegidos_std": round(df["suerte_prom_elegidos"].std(), 3),
            "suerte_prom_elegidos_p5": round(df["suerte_prom_elegidos"].quantile(0.05), 3),
            "suerte_prom_elegidos_p95": round(df["suerte_prom_elegidos"].quantile(0.95), 3),
            "skill_prom_elegidos": round(skill_sel, 3),
            "skill_prom_top_skill": round(skill_ideal, 3),
            "suerte_prom_top_skill": round(luck_ideal, 3),
            "coinciden_prom": round(coinc, 3),
            "distintos_prom": round(n_plazas - coinc, 3),
            "pct_distintos": round(pct_dist, 2),
        }
    ]
)

if "escenarios" not in st.session_state:
    st.session_state["escenarios"] = []

e1, e2, e3, e4 = st.columns(4)
e1.download_button(
    T["dl_summary"], resumen.to_csv(index=False).encode("utf-8"),
    file_name=f"resumen_{sufijo}.csv", mime="text/csv", help=T["dl_summary_help"],
)
e2.download_button(
    T["dl_sims"], df.to_csv(index_label="sim").encode("utf-8"),
    file_name=f"simulaciones_{sufijo}.csv", mime="text/csv", help=T["dl_sims_help"],
)
if e3.button(T["save_scn"], help=T["save_help"]):
    st.session_state["escenarios"].append(resumen.iloc[0].to_dict())
if e4.button(T["clear_scn"]):
    st.session_state["escenarios"] = []

if st.session_state["escenarios"]:
    esc = pd.DataFrame(st.session_state["escenarios"])
    st.caption(T["saved_n"].format(n=len(esc)))
    tabla(esc)
    st.download_button(
        T["dl_scn"], esc.to_csv(index=False).encode("utf-8"),
        file_name="escenarios_comparados.csv", mime="text/csv",
    )
