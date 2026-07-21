// ============================================================
//  تحليل الأخبار المدخلة يدوياً
// ============================================================

function analyzeManualNews() {
    const input = document.getElementById('manualNews');
    const result = document.getElementById('manualResult');
    const resultText = document.getElementById('manualResultText');

    const text = input.value.trim();
    if (!text) {
        alert('⚠️ الرجاء إدخال نص الخبر');
        return;
    }

    let impact = 0;
    let direction = 'محايد (Neutral)';
    let color = '#f1c40f';
    let reason = 'تأثير محدود على الذهب';

    const lowerText = text.toLowerCase();

    // ====== كلمات مفتاحية ======
    const bullishKeywords = ['ارتفاع', 'زيادة', 'صاعد', 'bullish', 'up', 'rise', 'high', 'إيجابي', 'تضخم', 'inflation', 'cpi'];
    const bearishKeywords = ['انخفاض', 'نقص', 'هابط', 'bearish', 'down', 'fall', 'low', 'سلبي', 'فائدة', 'interest rate', 'رفع الفائدة'];
    const highImpact = ['فيد', 'الاحتياطي', 'البنك المركزي', 'تضخم', 'CPI', 'interest rate', 'سعر الفائدة'];

    // ====== حساب التأثير ======
    let score = 0;

    for (const word of highImpact) {
        if (lowerText.includes(word.toLowerCase())) {
            score += 2;
        }
    }

    for (const word of bullishKeywords) {
        if (lowerText.includes(word.toLowerCase())) {
            score += 1;
        }
    }

    for (const word of bearishKeywords) {
        if (lowerText.includes(word.toLowerCase())) {
            score -= 1;
        }
    }

    // ====== تحديد النتيجة ======
    if (score > 2) {
        impact = Math.min(5 + score, 15);
        direction = 'صاعد (Bullish) 🟢';
        color = '#2ecc71';
        reason = 'الخبر يدعم ارتفاع الذهب';
    } else if (score < -2) {
        impact = Math.min(5 + Math.abs(score), 15);
        direction = 'هابط (Bearish) 🔴';
        color = '#e74c3c';
        reason = 'الخبر يضعف الذهب';
    } else {
        impact = Math.min(1 + Math.abs(score), 5);
        direction = 'محايد (Neutral) 🟡';
        color = '#f1c40f';
        reason = 'تأثير محدود على الذهب';
    }

    // ====== عرض النتيجة ======
    result.classList.add('show');
    resultText.innerHTML = `
        <strong>💡 تحليل الخبر:</strong><br>
        📝 النص المدخل: "${text}"<br>
        📊 التأثير المتوقع على الذهب: <strong style="color:${color};">${impact.toFixed(1)}%</strong><br>
        🎯 الاتجاه المتوقع: <strong style="color:${color};">${direction}</strong><br>
        📌 السبب: ${reason}
    `;
}

// ====== عند الضغط على Enter ======
document.addEventListener('DOMContentLoaded', function() {
    const manualInput = document.getElementById('manualNews');
    if (manualInput) {
        manualInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                analyzeManualNews();
            }
        });
    }
});

console.log('📰 Gold AI - News page loaded successfully!');