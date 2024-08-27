document.addEventListener("DOMContentLoaded", function () {
    const textareas = document.querySelectorAll(".custom-textarea");

    function adjustHeight(textarea) {
        textarea.style.height = "40px"; // Сначала устанавливаем минимальную высоту
        textarea.style.height = `${Math.max(40, textarea.scrollHeight)}px`;
    }

    textareas.forEach(textarea => {
        // Устанавливаем начальную высоту
        adjustHeight(textarea);

        textarea.addEventListener("input", function () {
            adjustHeight(textarea);
        });
    });
});