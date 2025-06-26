from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import names, random, string, time

# Настройки
PROXY = "socks5://96.126.96.163:9090"  # Обязательно для ротации IP
NUM_ACCOUNTS = 100  # Количество аккаунтов для создания

def generate_fake_data():
    """Генерация фейковых данных"""
    first_name = names.get_first_name()
    last_name = names.get_last_name()
    username = f"{first_name.lower()}{last_name.lower()}{random.randint(100,999)}"
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    recovery_email = f"{username}@outlook.com"  # Фейковая почта
    return first_name, last_name, username, password, recovery_email

def create_gmail_account(driver):
    """Процесс создания аккаунта"""
    first_name, last_name, username, password, recovery_email = generate_fake_data()
    
    try:
        driver.get("https://accounts.google.com/signup")
        
        # Шаг 1: Основная информация
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "firstName"))).send_keys(first_name)
        driver.find_element(By.ID, "lastName").send_keys(last_name)
        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.NAME, "Passwd").send_keys(password)
        driver.find_element(By.NAME, "ConfirmPasswd").send_keys(password)
        driver.find_element(By.ID, "accountDetailsNext").click()
        
        # Шаг 2: Телефон (пропускаем)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Пропустить']"))).click()
        
        # Шаг 3: Резервная почта
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "recoveryEmailId"))).send_keys(recovery_email)
        driver.find_element(By.XPATH, "//span[text()='Далее']").click()
        
        # Шаг 4: День рождения и пол
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "day"))).send_keys(str(random.randint(1,28)))
        driver.find_element(By.ID, "year").send_keys(str(random.randint(1980,2000)))
        driver.find_element(By.ID, "month").click()
        driver.find_element(By.XPATH, f"//option[@value='{random.randint(1,12)}']").click()
        driver.find_element(By.ID, "gender").click()
        driver.find_element(By.XPATH, "//option[@value='{random.randint(1,3)}']").click()
        driver.find_element(By.XPATH, "//span[text()='Далее']").click()
        
        # Шаг 5: Пропуск верификации номера
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Пропустить']"))).click()
        
        # Шаг 6: Принятие условий
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Принимаю']"))).click()
        
        print(f"[SUCCESS] Создан аккаунт: {username}@gmail.com | Пароль: {password}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Ошибка создания: {str(e)}")
        return False

def main():
    # Настройка Chrome с прокси
    chrome_options = Options()
    chrome_options.add_argument(f'--proxy-server={PROXY}')
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    # Для обхода детекта автоматизации
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    service = Service(ChromeDriverManager().install())
    
    success_count = 0
    for i in range(NUM_ACCOUNTS):
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Случайный User-Agent
        user_agent = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(90,110)}.0.{random.randint(1000,9999)}.0 Safari/537.{random.randint(10,99)}"
        driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": user_agent})
        
        if create_gmail_account(driver):
            success_count += 1
        
        driver.quit()
        time.sleep(random.uniform(5, 15))  # Рандомная пауза
        
        print(f"Прогресс: {i+1}/{NUM_ACCOUNTS} | Успешно: {success_count}")
    
    print(f"Создано аккаунтов: {success_count}/{NUM_ACCOUNTS}")

if __name__ == "__main__":
    main()
