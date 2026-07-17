from selenium import webdriver
from selenium.webdriver.common.by import By


def test_multiple_elements():
    driver = webdriver.Chrome()
    driver.get("https://httpbin.org/links/10")

    # Находим все ссылки на странице
    links = driver.find_elements(By.TAG_NAME, "a")
    
    # Проверяем, что количество ссылок
    assert len(links) == 10
    
    # Проверяем, что все ссылки отображаются на странице
    for link in links:
        assert link.is_displayed(), "Link is not displayed on the page"
    
    # Проверяем, что текст первой ссылки содержит "1"
    assert "1" in links[0].text, f"First link text does not contain '1'. Text: {links[0].text}"
    
    driver.quit()
