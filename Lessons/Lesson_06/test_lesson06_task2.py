from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_session_storage_auth():
    driver = webdriver.Chrome()


    # 1. Откройте страницу https://gitflic.ru/.
    driver.get("https://www.gitflic.ru/")
    # 2. Установите cookie пользователя 1.
   
    user1 = driver.add_cookie({
        "name": "SESSION",
        "value": "OGRmMzRiODUtMzBkYS00MTgwLWEwNWQtYTdlMTI5MzhmZTZl",
        "domain": "www.gitflic.ru"
    })

    driver.add_cookie({
        "name": "cookiesAccepted",
        "value": "true",
        "domain": "www.gitflic.ru"
    })
    # 3. Обновите страницу.
    driver.refresh()
    # 4. Перейдите на страницу пользователя 1.
    driver.get("https://gitflic.ru/user/user1_test")
    # 5. Сохраните текущий URL.
    url_user1 = driver.current_url
    # 6. Разлогиньтесь (очистите куки).
    driver.delete_all_cookies()
    driver.refresh()
    # 7. Установите cookie пользователя 2.
    
    user2 = driver.add_cookie({
        "name": "SESSION",
        "value": "NGU1ZTU3NmMtZDgxMi00Njc4LThlZGMtYjEwZGYzZTdlMmM4",
        "domain": "www.gitflic.ru"
    })

    driver.add_cookie({
        "name": "cookiesAccepted",
        "value": "true",
        "domain": "www.gitflic.ru"
    })
    # 8. Обновите страницу.
    driver.refresh()
    # 9. Перейдите на страницу пользователя 2.
    driver.get("https://gitflic.ru/user/user2_test")
    # 10. Сохраните текущий URL.
    url_user2 = driver.current_url
    # 11. Проверьте, что URL для пользователя 1 и пользователя 2 различаются.
    assert url_user1 != url_user2

    driver.quit()
