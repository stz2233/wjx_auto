from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 单选题配置
single_choice_questions = {
    1: 4,
    3: 4,
    4: 5,
    5: 3,
    7: 2,
    8: 4,
    9: 4,
}

# 多选题配置
multiple_choice_questions = {
    2: 5,
}

# 新增矩阵题配置数组（格式：{题号: (子问题数量, 每个子问题选项数)}）
matrix_questions = {
    6: (3, 4)  # 题号6 → 3个子问题 → 每个子问题4个选项
}

def submit_form():
    WJX_URL = 'https://www.wjx.cn/vm/?.aspx'
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(WJX_URL)

    try:
         # -------------------- 处理新增矩阵题（关键修改） --------------------
        for qid, (sub_num, opts_per_sub) in matrix_questions.items():
            container_id = f"divRefTab{qid}"  # 容器ID规则（根据实际页面调整）
            
            question_div = driver.find_element(By.ID, container_id)

            
            # 遍历所有子问题（如q6_0, q6_1, q6_2）
            for sub_idx in range(sub_num):
                fid = f"q{qid}_{sub_idx}"  # 子问题fid规则（根据实际页面调整）
                sub_questions = question_div.find_elements(
                    By.XPATH, f".//tr[@fid='{fid}']"
                )
                score = random.randint(1, 4)
                # 使用相对XPath限定在当前评分组内
                option_xpath = f"./td/a[@dval='{score}']"
                target_element = sub_questions[0].find_element(By.XPATH, option_xpath)
                    
                    # 添加显式等待确保元素可点击
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(target_element))
                target_element.click()
                time.sleep(random.uniform(0.3, 0.7))
                
        # -------------------- 处理原单选题 --------------------
        for q, options in single_choice_questions.items():
            chosen = random.randint(1, options)
            selector = f'[for="q{q}_{chosen}"]'
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            ).click()
            time.sleep(random.uniform(0.3, 0.7))

        # -------------------- 处理原多选题 --------------------
        for q, options in multiple_choice_questions.items():
            selected = random.sample(range(1, options+1), random.randint(1, options))
            for opt in selected:
                selector = f'[for="q{q}_{opt}"]'
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                ).click()
            time.sleep(random.uniform(0.2, 0.5))

       

        # -------------------- 提交问卷 --------------------
        submit_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, 'ctlNext'))
        )
        ActionChains(driver).move_to_element(submit_btn).click().perform()
        time.sleep(3)  # 等待提交完成

    except Exception as e:
        print(f"❌ 执行异常：{str(e)}")
    finally:
        driver.quit()
        print("✅ 执行流程完成")

# 执行50次测试
for i in range(50):
    print(f"\n正在执行第 {i+1}/50 次提交...")
    submit_form()