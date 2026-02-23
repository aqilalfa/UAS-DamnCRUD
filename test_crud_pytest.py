import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://localhost:8000/DamnCRUD"

@pytest.fixture
def driver():
    """Setup WebDriver: Runs headless untuk keperluan CI/CD (GitHub Actions)"""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    
    # ---------------------------------------------------------
    # PRASYARAT: Login untuk setiap Test Function
    # ---------------------------------------------------------
    driver.get(f"{BASE_URL}/login.php")
    driver.find_element(By.ID, "inputUsername").send_keys("admin")
    driver.find_element(By.ID, "inputPassword").send_keys("nimda666!")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    # Tunggu secara eksplisit (Maximum 10 detik) hingga Browser mengalihkan halaman menuju ID "employee" (Dashboard)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'employee')))
    
    yield driver
    
    # Teardown WebDriver setelah tiap test case selesai
    driver.quit()


def test_tc04_read_dashboard(driver):
    """
    Test Case 04: Memastikan tabel data dashboard termuat (Read)
    """
    table = driver.find_element(By.ID, "employee")
    assert table.is_displayed(), "Tabel Data Kontak tidak dimuat dengan benar di Dashboard!"


def test_tc05_create_contact(driver):
    """
    Test Case 05: Menambahkan kontak baru ke dalam sistem
    """
    driver.get(f"{BASE_URL}/create.php")
    
    driver.find_element(By.ID, "name").send_keys("Pytest Worker")
    driver.find_element(By.ID, "email").send_keys("worker@pytest.dev")
    driver.find_element(By.ID, "phone").send_keys("08122334455")
    driver.find_element(By.ID, "title").send_keys("Automated Tester")
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
    
    # Menunggu Dashboard (element tbody) ter-render kembali
    wait = WebDriverWait(driver, 5)
    wait.until(EC.presence_of_element_located((By.ID, "employee")))
    
    # Gunakan Searchbar agar data yang bersembunyi di Page 2 ditarik ke Page 1
    search_box = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='search']")))
    search_box.clear()
    search_box.send_keys("Pytest Worker")
    time.sleep(1) # Tunggu transisi DataTables
    
    assert "Pytest Worker" in driver.page_source, "Kontak yang dijabarkan gagal disimpan/tampil"


def test_tc07_update_contact(driver):
    """
    Test Case 07: Mengedit title kontak (Update)
    """
    # Mengambil tombol klik edit pertama di barisan (index 0)
    edit_buttons = driver.find_elements(By.XPATH, "//a[contains(text(), 'edit')]")
    if len(edit_buttons) == 0:
        pytest.skip("Data kosong, tidak bisa menguji fitur edit!")
        
    edit_buttons[0].click()
    
    title_field = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "title")))
    title_field.clear() 
    title_field.send_keys("Direktur Utama")
    
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
    
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "employee")))
    assert "Direktur Utama" in driver.page_source, "Pengubahan Title kontak menjadi Direktur Utama gagal tersimpan"


def test_tc09_delete_contact(driver):
    """
    Test Case 09: Menghapus sebuah kontak (Delete)
    """
    # Mengambil elemen *terakhir* dari list kotak tombol delete (untuk menghindari menghapus kontak yang sedang dites oleh thread TC07 yang berjalan paralel)
    delete_buttons = driver.find_elements(By.XPATH, "//a[contains(text(), 'delete')]")
    if len(delete_buttons) == 0:
        pytest.skip("Data kosong, tidak bisa menguji fitur delete!")
        
    delete_buttons[-1].click()
    
    # Menerima Confirm Alert javascript
    Alert(driver).accept() 
    
    # Jeda menunggu transisi page submit form di CI/CD
    time.sleep(1) 
    
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "employee")))
    assert "Howdy, damn admin!" in driver.page_source


def test_tc14_search_filter_datatables(driver):
    """
    Test Case 14: Menguji bar search dari jQuery DataTables
    """
    wait = WebDriverWait(driver, 10)
    search_box = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='search']")))
    search_box.clear()

    # Search query yang tidak pernah ada
    search_box.send_keys("ZZZZX")
    
    # Beri jeda jQuery transition search
    time.sleep(1) 

    tbody_rows = driver.find_elements(By.XPATH, "//table[@id='employee']/tbody/tr")
    
    # 1 Baris berarti tulisan peringatan pencarian kosong dari datatables ("No matching record found")
    assert len(tbody_rows) <= 1, "DataTables Filter tidak bekerja dengan semestinya"
