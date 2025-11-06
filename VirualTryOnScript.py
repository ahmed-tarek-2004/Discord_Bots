from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import requests

image1_path = r"E:\\VSC_ Codes\\python\\ME.jpg"
image2_path = r"E:\\VSC_ Codes\\python\\ahmed.jpg"

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")  
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)
driver.get("https://huggingface.co/spaces/Kwai-Kolors/Kolors-Virtual-Try-On")


wait = WebDriverWait(driver, 180)
print(" Waiting for page to load...")


iframes = driver.find_elements(By.TAG_NAME, "iframe")
if iframes:
    driver.switch_to.frame(iframes[0])
    print(" Switched into iframe")


print(" Uploading first image...")
file_inputs = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='file']")))
file_inputs[0].send_keys(image1_path)
print(" Uploaded person image")

for i in range(10,1,-1):
    print("wait "+str(i)+" s")
    time.sleep(1)


print(" Uploading second image...")
if len(file_inputs) > 1:
    file_inputs[1].send_keys(image2_path)
    print(" Uploaded cloth image")
else:
    print(" Couldn't find second input!")

for i in range(10,1,-1):
    print("wait "+str(i)+" s")
    time.sleep(1)



print(" Running model...")
run_button = wait.until(EC.element_to_be_clickable((By.ID, "button")))
run_button.click()

print(" Waiting for result image...")
result_img = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "img.svelte-1pijsyv"))
)
print("Result appeared!")


print(" Waiting for garment image to appear...")

garment_img = wait.until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.image-frame img[loading='lazy'].svelte-1pijsyv"))
)[-1]

wait.until(lambda d: garment_img.get_attribute("src") and "tmp" in garment_img.get_attribute("src"))
print("Garment image loaded")



# for i in range(60,1,-1):
#     print("wait "+str(i)+" s")
#     time.sleep(1)


# # --- Screenshot ---
# screenshot_path = os.path.join(os.getcwd(), "result.png")
# driver.save_screenshot(screenshot_path)
# print(f" Screenshot saved as {screenshot_path}")

img_url = garment_img.get_attribute("src")
print(" Image URL:", img_url)

response = requests.get(img_url)
output_path = os.path.join(os.getcwd(), "result.webp")
with open(output_path, "wb") as f:
    f.write(response.content)

print(f" Saved result image as {output_path}")

driver.quit()


