function logout() {
    // Очищаем access_token из куки
    document.cookie = 'access_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';

    // Перенаправляем на страницу авторизации
    window.location.href = '/auth';
}

function getAccessToken() {
    // Получаем все cookies в виде строки
    const allCookies = document.cookie;

    // Разбиваем строку cookies на массив отдельных cookies
    const cookiesArray = allCookies.split('; ');

    // Ищем cookie с именем 'access_token'
    for (const cookie of cookiesArray) {
        const [name, value] = cookie.split('=');
        if (name === 'access_token') {
            return value;
        }
    }

    // Если 'access_token' не найден, возвращаем null или нужное вам значение по умолчанию
    return null;
}

async function fetchBalance() {
    // Показываем индикатор загрузки
    document.getElementById("balanceLoader").style.visibility = "visible";

    // Здесь делаете асинхронный запрос к серверу для получения баланса
    const response = await fetch('/api/auth/get-balance');
    const balance = await response.json();

    console.log(balance)

    // Скрываем индикатор загрузки
    document.getElementById("balanceLoader").style.visibility = "hidden";

    // Обновляем баланс на странице
    document.getElementById("userBalance").innerText = "Баланс: " + balance;
}

// Функция для отправки POST-запроса
async function sendRequest() {
    // Определяем, какая вкладка активна
    const isFromDatabase = document.getElementById('tab-btn-1').checked;
    let apiURL;
    let requestData;
    let contentType;
    
    // Собираем данные для запроса

    if (isFromDatabase) {
        requestData = {};
        const start_datetime = document.getElementById('startDate').value + ' ' + document.getElementById('startTime').value
        const end_datetime = document.getElementById('endDate').value + ' ' + document.getElementById('endTime').value
        apiURL = ('/api/predictions/by-date/' 
                        + document.getElementById('carModel').value + '?'
                        + 'start_datetime=' + start_datetime + '&'
                        + 'end_datetime=' + end_datetime);
    } else {
        const fileInput = document.getElementById('csvFile');
        const file = fileInput.files[0];

        requestData = new FormData();
        requestData.append('file', file);

        apiURL = 'api/predictions/from-file/' + document.getElementById('carModel').value;
            }

    try {
        // Отправляем POST-запрос
        const response = await fetch(apiURL, {
            method: 'POST',
            headers: {
                "Authorization": "Bearer " + getAccessToken(),
            },
            body: requestData,
        });

        // Проверяем успешность запроса
        if (response.ok) {
            // Если успешно, показываем всплывающее окно
            document.getElementById('notification-popup').classList.add('active');
            setTimeout(() => {
                document.getElementById('notification-popup').classList.remove('active');
            }, 3000);
            fetchBalance();
            refreshTable()
        } else {
            // Обрабатываем ошибку, если не успешно
            console.error('Ошибка при отправке запроса:', response.statusText);
        }
    } catch (error) {
        console.error('Произошла ошибка:', error);
    }
}

document.addEventListener('DOMContentLoaded', async function () {
    // Используйте функцию для первичной загрузки данных и отображения таблицы
    await refreshTable();

    // Навешиваем обработчик события на кнопку для обновления таблицы
    const refreshButton = document.getElementById('refreshButton');
    refreshButton.addEventListener('click', refreshTable);
});

async function refreshTable() {
    // Получаем результаты прогнозов из API
    const predictions = await fetchPredictions();

    // Отображаем результаты в таблице
    displayPredictions(predictions);
}

async function fetchPredictions() {
    try {
        // Замените этот URL на ваш реальный эндпоинт API
        const response = await fetch('/api/predictions', {
            headers: {
                "Authorization": "Bearer " + getAccessToken(),
            },
        });
        if (response.ok) {
            const predictions = await response.json();
            return predictions;
        } else {
            console.error('Ошибка при получении результатов прогнозов:', response.statusText);
            return [];
        }
    } catch (error) {
        console.error('Произошла ошибка:', error);
        return [];
    }
}

function displayPredictions(predictions) {
    const tableBody = document.querySelector('#predictionsTable tbody');

    // Очищаем предыдущие данные в таблице
    tableBody.innerHTML = '';

    predictions.reverse();

    // Заполняем таблицу новыми данными
    predictions.forEach(prediction => {
        const row = tableBody.insertRow();

        // Добавляем ячейки с данными
        const idCell = row.insertCell();
        idCell.textContent = prediction.prediction_id;

        const modelIdCell = row.insertCell();
        modelIdCell.textContent = 'model_' + prediction.prediction_model_id;

        const createdAtCell = row.insertCell();
        createdAtCell.textContent = prediction.created_at;

        const resultsCell = row.insertCell();
        if (prediction.error_info) {
            resultsCell.textContent = prediction.error_info;
        } else {
            resultsCell.textContent = JSON.stringify(prediction.prediction_results);
        }
    });
}

function displayPredictions(predictions) {
    const tableBody = document.querySelector('#predictionsTable tbody');

    // Очищаем предыдущие данные в таблице
    tableBody.innerHTML = '';

    predictions.reverse();

    // Заполняем таблицу новыми данными
    predictions.forEach(prediction => {
        const row = tableBody.insertRow();

        // Добавляем ячейки с данными
        const predictionIdCell = row.insertCell();
        predictionIdCell.textContent = prediction.prediction_id;

        const modelIdCell = row.insertCell();
        modelIdCell.textContent = 'model_' + prediction.prediction_model_id;

        const createdAtCell = row.insertCell();
        createdAtCell.textContent = prediction.created_at;

        const resultsCell = row.insertCell();
        if (prediction.error_info) {
            resultsCell.textContent = prediction.error_info;
        } else {
            // Создаем вложенную таблицу для отображения результатов прогнозов
            const nestedTable = document.createElement('table');
            const nestedTableBody = document.createElement('tbody');

            // Заполняем вложенную таблицу данными из поля results
            prediction.prediction_results.forEach(result => {
                const nestedRow = nestedTableBody.insertRow();
                const datetimeCell = nestedRow.insertCell();
                datetimeCell.textContent = result.datetime;

                const isAnomalyCell = nestedRow.insertCell();
                isAnomalyCell.textContent = result.is_anomaly ? 'Да' : 'Нет';

                const probabilityCell = nestedRow.insertCell();
                probabilityCell.textContent = result.anomaly_probability.toFixed(2);
            });

            nestedTable.appendChild(nestedTableBody);
            resultsCell.appendChild(nestedTable);
        }
    });
}