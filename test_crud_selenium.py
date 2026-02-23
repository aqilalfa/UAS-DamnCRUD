import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ==========================================
# KONFIGURASI DAN SETUP WEBDRIVER
# ==========================================
options = webdriver.ChromeOptions()
# options.add_argument('--headless') # Hapus komentar "#" ini jika ingin run tanpa buka GUI browser
driver = webdriver.Chrome(options=options)

base_url = "http://localhost:8000/DamnCRUD"

def print_result(tc_id, status):
    print(f"[{tc_id}] Result: {'✅ PASS' if status else '❌ FAIL'}")

try:
    # ---------------------------------------------------------
    # PRASYARAT (PRECONDITION): LOGIN SYSTEM
    # ---------------------------------------------------------
    print("Mempersiapkan Test... Melakukan Login...")
    driver.get(f"{base_url}/login.php")
    
    driver.find_element(By.ID, "inputUsername").send_keys("admin")
    driver.find_element(By.ID, "inputPassword").send_keys("nimda666!")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(1)

    # =========================================================
    # 04: Menampilkan Data Dashboard 
    # =========================================================
    try:
        table = driver.find_element(By.ID, "employee")
        print_result("04 - Read Dashboard Data", table.is_displayed())
    except Exception:
        print_result("04 - Read Dashboard Data", False)

    time.sleep(1)


    # =========================================================
    # 05: Menambahkan Data Baru (Create)
    # =========================================================
    try:
        driver.get(f"{base_url}/create.php")
        time.sleep(0.5)

        driver.find_element(By.ID, "name").send_keys("Selenium Bot")
        driver.find_element(By.ID, "email").send_keys("bot@selenium.dev")
        driver.find_element(By.ID, "phone").send_keys("08123456789")
        driver.find_element(By.ID, "title").send_keys("QA Engineer")
        driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        
        time.sleep(1)
        print_result("05 - Create New Contact", "Selenium Bot" in driver.page_source)
    except Exception:
        print_result("05 - Create New Contact", False)
        
    time.sleep(1)


    # =========================================================
    # 07: Mengubah Data Kontak (Update)
    # =========================================================
    try:
        driver.find_element(By.XPATH, "//a[contains(text(), 'edit')]").click()
        time.sleep(0.5)

        title_field = driver.find_element(By.ID, "title")
        title_field.clear() 
        title_field.send_keys("Direktur Utama")
        driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        
        time.sleep(1)
        print_result("07 - Update Contact Field", "Direktur Utama" in driver.page_source)
    except Exception as e:
        print_result("07 - Update Contact Field", False)

    time.sleep(1)


    # =========================================================
    # 09: Menghapus Data Kontak (Delete)
    # =========================================================
    try:
        driver.find_elements(By.XPATH, "//a[contains(text(), 'delete')]")[0].click()
        time.sleep(0.5)
        
        Alert(driver).accept() 
        time.sleep(1)

        print_result("09 - Delete Contact (Accept)", "Howdy, damn admin!" in driver.page_source)
    except Exception as e:
        print_result("09 - Delete Contact (Accept)", False)

    time.sleep(1)


    # =========================================================
    # 14: Menguji Fitur Filter/Search (DataTables)
    # =========================================================
    try:
        # Pindah kembali ke halaman dashboard utama (Refresh) agar state DataTables bersih
        driver.get(f"{base_url}/index.php")
        time.sleep(1)

        # [REVISI]: Gunakan Explicit Wait karena DataTables digenerate oleh jQuery AJAX asinkron
        wait = WebDriverWait(driver, 10)
        
        # Minta WebDriver menunggu hingga input kotak pencarian DataTables benar-benar bisa diklik
        search_box = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='search']")))
        search_box.clear()

        # Ketik kata kunci ngacak yang mustahil ditemui
        search_box.send_keys("ZZZZX")
        time.sleep(0.5) # Beri Jeda transisi sorting/filtering

        # Ambil daftar TR dari DOM yang sudah disegarkan jQuery
        tbody_rows = driver.find_elements(By.XPATH, "//table[@id='employee']/tbody/tr")
        
        # Cukup andalkan logika jumlah tbody rows kurang dari sama dengan 1 (pesan "No Results")
        status_tc14 = True if len(tbody_rows) <= 1 else False
        print_result("14 - Search/Filter DataTables", status_tc14)
    except Exception as e:
        # Debugging purposes
        # print("Error TC-14:", e) 
        print_result("14 - Search/Filter DataTables", False)


finally:
    print("\n[INFO] Skenario Test Selesai. Menutup Program/Browser dalam 3 detik...")
    time.sleep(3)
    driver.quit()
