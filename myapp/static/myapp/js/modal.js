$(document).ready(function () {
    // Функция для получения CSRF-токена из куки
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Проверяем, начинается ли строка с имени токена
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    // Функция, которая проверяет, требует ли метод CSRF-токен
    function csrfSafeMethod(method) {
        // методы, не требующие CSRF-токена
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    // Настройка jQuery AJAX для добавления CSRF-токена в заголовки
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // Открытие модального окна
    $(".openModal").click(function () {
        $("#consultationModal").fadeIn();
    });

    // Закрытие модального окна при клике на крестик
    $(".close").click(function () {
        $("#consultationModal").fadeOut();
    });

    // Закрытие модального окна при клике вне его области
    $(window).click(function (event) {
        if (event.target == $("#consultationModal")[0]) {
            $("#consultationModal").fadeOut();
        }
    });

    // Обработка отправки формы
    $("#consultationForm").submit(function (event) {
        event.preventDefault();

        const url = $(this).data('url'); // Получаем URL из data-url атрибута

        $.ajax({
            type: "POST",
            url: url, // Используем URL из data-url
            data: $(this).serialize(),
            success: function (response) {
                $("#consultationForm").html('<p>Спасибо, что оставили заявку, я свяжусь с вами в ближайшее время!</p>');
                setTimeout(function () {
                    $("#consultationModal").fadeOut();
                }, 3000);
            },
            error: function () {
                alert("Ошибка при отправке заявки.");
            }
        });
    });
});
