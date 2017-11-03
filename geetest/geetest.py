from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from time import sleep
from PIL import Image
from io import BytesIO


class crakegeetest():
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.wait = WebDriverWait(self.driver, 20)
        self.url = 'http://www.gsxt.gov.cn/index.html'
        self.serach = '蛟龙出海'

    def get_image(self):
        self.driver.get(self.url)

        element = self.wait.until(
            EC.presence_of_element_located((By.ID, 'keyword'))
        )
        element.clear()
        element.send_keys(self.serach)
        click = self.wait.until(EC.element_to_be_clickable((By.ID, 'btn_query')))
        return click

    def get_position(self):
        image = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, 'gt_box'))
        )
        sleep(1)
        location = image.location
        size = image.size
        top, botom, left, right = location['y'], location['y']+size['height'], location['x'], location['x']+size['width']
        return (top, botom, left, right)

    def get_screenshot(self):
        """
        获取网页截图
        :return: 截图对象
        """
        screenshot = self.driver.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_captcha(self, name='captcha.png'):
        top, bottom, left, right = self.get_position()
        sreenshot = self.get_screenshot()
        captcha = sreenshot.crop((left, top, right, bottom))
        captcha.save(name)
        return captcha

    def get_slider(self):
        """
        获取滑块
        :return: 滑块对象
        """
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'gt_slider_knob')))
        return slider

    def get_slider_distance(self, image1, image2):
        value = 60
        left = 60 #滑块的宽度
        for w in range(left, image1.size[0]):
            for h in range(image1.size[1]):
                pixel1 = image1.getpixel((w, h))
                pixel2 = image2.getpixel((w, h))
                if not abs(pixel1[0] - pixel2[0]) < value and abs(pixel1[1] - pixel2[1]) < value and abs(pixel1[2] - pixel2[2]) < value:
                    left = w
                    print(left)
                    return left
        #print(left)
        return left

    def get_track(self, distance):
        """
        根据偏移量获取移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 5 / 7
        # 计算间隔
        t = 0.2
        # 初速度
        v = 0

        while current < distance:
            if current < mid:
                # 加速度为正2
                a = 3
            else:
                # 加速度为负3
                a = -2
            # 初速度v0
            v0 = v
            # 当前速度v = v0 + at
            v = v0 + a * t
            # 移动距离x = v0t + 1/2 * a * t^2
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))
        return track

    def move_to_gap(self, slider, track):
        """
        拖动滑块到缺口处
        :param slider: 滑块
        :param track: 轨迹
        :return:
        """
        ActionChains(self.driver).click_and_hold(slider).perform()
        for x in track:
            ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=0).perform()
        sleep(0.5)
        ActionChains(self.driver).release().perform()

    def crack(self):
        click = self.get_image()
        click.click()
        image1 = self.get_captcha(name='image1.png')
        click = self.get_slider()
        click.click()
        sleep(2)
        image2 = self.get_captcha(name='image2.png')
        distance = self.get_slider_distance(image1, image2)
        distance -= 10
        track = self.get_track(distance)
        self.move_to_gap(click, track)
        fail = self.wait.until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, 'gt_info_type'), '验证失败'))
        print(fail)
        sleep(1)
        if fail:
            self.crack()
        else:
            print(fail)

if __name__ == '__main__':
    crack = crakegeetest()
    crack.crack()
