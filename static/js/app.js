document.addEventListener('DOMContentLoaded', function() {
    const dropZone = document.getElementById('dropZone');
    const chartInput = document.getElementById('chartInput');
    const preview = document.getElementById('preview');
    const analyseBtn = document.getElementById('analyseBtn');
    const form = document.getElementById('analyseForm');
    const loading = document.getElementById('loading');
    const result = document.getElementById('result');

    if (dropZone) {
        dropZone.addEventListener('click', () => chartInput.click());

        chartInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    preview.src = e.target.result;
                    preview.style.display = 'block';
                    analyseBtn.style.display = 'block';
                }
                reader.readAsDataURL(file);
            }
        });
    }

    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(form);
            
            analyseBtn.style.display = 'none';
            loading.style.display = 'block';
            result.style.display = 'none';

            try {
                const response = await fetch('/ai-analyse', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                
                loading.style.display = 'none';
                analyseBtn.style.display = 'block';
                
                if (data.analysis) {
                    result.innerText = data.analysis;
                    result.style.display = 'block';
                } else {
                    result.innerText = "خطأ: " + (data.error || "وقع مشكل ف السيرفر");
                    result.style.display = 'block';
                }
            } catch (err) {
                loading.style.display = 'none';
                analyseBtn.style.display = 'block';
                result.innerText = "مشكل ف الاتصال بالسيرفر";
                result.style.display = 'block';
            }
        });
    }
});