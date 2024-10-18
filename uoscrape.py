from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import ast

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def scrape_proj_urls():
    for page in range(1, 129):
        current_page = "https://makerepo.com/explore?page=" + str(page)
        print(current_page)
        try:
            driver.get(current_page)

            WebDriverWait(driver, 5).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            projects = driver.find_elements(By.CSS_SELECTOR, "a.link")
            #next_page = driver.find_element(By.CSS_SELECTOR, '[rel="next"]').get_attribute("href")

            for project in projects:
                project_data = project.get_attribute("href")
                print(project_data)
                with open('hst.txt', 'a') as fd:
                    fd.write(f'\n{project_data}')
        except:
            print("couldn't get page")
    driver.quit()

def scrape_projs():
    page_table = []
    with open('makerepo-com-projects.txt') as projects:
        for project in projects:
            page_data = []
            page_data.append(project)
            try:
                driver.get(project)
                WebDriverWait(driver, 10).until(
                    lambda driver: driver.execute_script("return document.readyState") == "complete"
                )

                # project_data = driver.find_element(By.CSS_SELECTOR, "section#show-repository").get_attribute('innerHTML')

                title = driver.find_element(By.CSS_SELECTOR, "div#repo-title").text
                page_data.append(title)

                date = driver.find_element(By.CSS_SELECTOR, "div.date").text
                page_data.append(date)

                try:
                    desc = driver.find_element(By.CSS_SELECTOR, "div.description").get_attribute('innerHTML')
                    page_data.append(desc)
                except:
                    desc = "No desc"
                    page_data.append(desc)

                try:
                    #imgs = []
                    imgs_divs = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '[alt="Repository Main image"]')))
                    #for imgs_html in imgs_divs:
                    main_img = imgs_divs[0].get_attribute('src')
                    print(main_img)
                    #imgs.append(imgs_divs[0].get_attribute('src'))
                    page_data.append(main_img)
                except: 
                    imgs = "No imgs"

                try:
                    tags = []
                    tags_spans = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "tags")))
                    for tags_html in tags_spans:
                        tags.append(tags_html.get_attribute('innerText'))
                    page_data.append(tags)
                except: 
                    tags = "No tags"
                
                print(page_data)
                page_table.append(page_data)
                #with open('hst.txt', 'a') as fd:
                #   fd.write(f'{project_data}\n')
                #print(title.text) #.get_attribute('innerHTML'))
                #project_data = project.get_attribute("href")
                #print(project_data)
            except:
                print("couldn't get project")
                break
    data = pd.DataFrame(page_table, columns = ['Url', 'Title', 'Date', 'Desc', 'img', 'tags']) 
    data.to_csv('makerepo-pages-data.csv')
    driver.quit()

#scrape_projs()

def unique_tags_list(df):
    tags_list = []
    for index, row in df.loc[:, ['tags']].iterrows():
        if type(row['tags']) == str:
            tags_list.extend(ast.literal_eval(row['tags']))
    u_tags = set(tags_list)
    print(u_tags)
    return list(u_tags)

def clean_data():
    proj_list = pd.read_csv('makerepo-pages-data.csv')
    proj_list['Candidate'] = False
    proj_list['unique_tags'] = pd.Series(unique_tags_list(proj_list))
    proj_list = proj_list[proj_list.columns.intersection(["Url", "Candidate", "Title", "Desc", "img", "tags", "unique_tags"])]
    proj_list.to_csv('makerepo-pages-data.csv')

clean_data()

def test():
    with open('makerepo-com-projects.txt') as projects:
        count = 0
        for project in projects:
            count += 1
            driver.get(project)
            print(project)
            try:
                img = []
                img_divs = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div#show-photo")))
                for img_html in img_divs:
                    img.append(img_html.get_attribute('innerHTML'))
            except: 
                img = "No img"

            print(img)

            try:
                tags = []
                tags_spans = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "tags")))
                for tags_html in tags_spans:
                    tags.append(tags_html.get_attribute('innerHTML'))
            except: 
                tags = "No tags"

            print(tags)

            if count == 5:
                break

        driver.quit()

#test()
#scrape_projs()