from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome

def initial_click(driver):
    """
    Click to the top left corner to remove the help window
    (https://stackoverflow.com/questions/16807258/selenium-click-at-certain-position)
    """
    gmodel = driver.execute_script("return document.querySelector('body')")
    action = webdriver.common.action_chains.ActionChains(driver)
    action.move_to_element_with_offset(gmodel, 5, 5)
    action.click()
    action.perform()

def get_key_buttons(driver):
    # Find the divs in which the keyboard elements are
    # (Inspired by https://stackoverflow.com/questions/65044870/
    #               how-to-extract-info-within-a-shadow-root-open-using-selenium-python)
    gk = driver.execute_script("return document.querySelector('game-app')" 
                                + ".shadowRoot"
                                + ".querySelector('game-theme-manager div game-keyboard')" 
                                + ".shadowRoot"
                                + ".querySelector('div')" 
    )
    rows = gk.find_elements(By.TAG_NAME, 'div')

    # Collect the button elements of the keyboard
    keys = [['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
            [],
            [],
            ['enter', 'z', 'x', 'c', 'v', 'b', 'n', 'm', 'backspace']]

    buttons = {}
    for i in range(5):
        but = rows[i].find_elements(By.TAG_NAME, 'button')
        for j, key in enumerate(keys[i]):
            buttons[key] = but[j]

    return buttons

def get_results(driver, line_no):
    """
    """
    #Find the elements in which the results are displayed
    gtm = driver.execute_script("return document.querySelector('game-app')" 
                                + ".shadowRoot"
                                + ".querySelector('game-theme-manager div div div')" 
                                + ".querySelector('game-row:nth-of-type(" + str(line_no) + ")')"
                                + ".shadowRoot"
                                + ".querySelector('div')"
    )
    tiles = gtm.find_elements(By.TAG_NAME, 'game-tile')

    # Read off the values and convert to the format used by the bot
    to_gyx = {'correct': 'g', 'present': 'y', 'absent': 'x'}
    res = ''
    for t in tiles:
        res += to_gyx[t.get_attribute('evaluation')]

    return res
