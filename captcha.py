# https://yanwei-liu.medium.com/python%E7%88%AC%E8%9F%B2%E5%AD%B8%E7%BF%92%E7%AD%86%E8%A8%98-%E4%B8%83-%E8%99%95%E7%90%86%E5%9C%96%E7%89%87%E9%A9%97%E8%AD%89%E7%A2%BC-962e1c008ce9

from PIL import Image
import cv2
import pytesseract
import numpy as np

class Captcha():
    MORPH_OPEN = 1
    MORPH_CLOSE = 2
    DILATE = 3
    ERODE = 4
    
    INTER_NEAREST = cv2.INTER_NEAREST
    INTER_LINEAR = cv2.INTER_LINEAR
    INTER_AREA = cv2.INTER_AREA
    INTER_CUBIC = cv2.INTER_CUBIC
    INTER_LANCZOS4 = cv2.INTER_LANCZOS4
    
    def __init__(self, image_path=None):
        self.image_array = None
        if image_path:
            set_image(image_path=image_path)
        pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract'
        
    def set_image(self, image_path=None, image_array=None):
        if image_path:
            self.image_array = cv2.imread(image_path)
            return self.image_array
        if not image_array is None:
            self.image_array = image_array
            return self.image_array
        raise Exception('need set image_path or image_array')
        
    def get_image(self):
        if not self.image_array is None:
            return Image.fromarray(self.image_array)
        else:
            return None
    
    def resize(self, image_array=None, magnification=2, mode=INTER_NEAREST):
        image_is_input = True
        if image_array is None:
            image_is_input = False
            image_array = self.image_array
            
        height = int(image_array.shape[0]*magnification)
        width = int(image_array.shape[1]*magnification)
        
        image_array = cv2.resize(image_array, (width, height), interpolation=cv2.INTER_AREA)
        if not image_is_input:
            self.set_image(image_array=image_array)
        return image_array
        
    def get_grayscale(self, image_array=None):
        image_is_input = True
        if image_array is None:
            image_is_input = False
            image_array = self.image_array
        image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
        if not image_is_input:
            self.set_image(image_array=image_array)
        return image_array
        
    def binarizing(self, image_array=None, threshold_number=127.5, inverse=False):
        image_is_input = True
        if image_array is None:
            image_is_input = False
            image_array = self.image_array
        if inverse:
            _, image_array = cv2.threshold(image_array, threshold_number, 255, cv2.THRESH_BINARY_INV)
        else:
            _, image_array = cv2.threshold(image_array, threshold_number, 255, cv2.THRESH_BINARY)
        if not image_is_input:
            self.set_image(image_array=image_array)
        return image_array
                
    def gray_to_rgb(self, image_array):
        temp = np.empty((image_array.shape[0], image_array.shape[1], 3), dtype=np.uint8)
        for i in range(3):
            temp[:, :, i] = image_array
        return temp
    
    def mean_shift_remove_noise(self, image_array=None, sp=50, sr=50):
        image_is_input = True
        if image_array is None:
            image_is_input = False
            image_array = self.image_array
        
        if len(image_array.shape) == 2:
            image_array = self.gray_to_rgb(image_array)
            
        image_array = cv2.pyrMeanShiftFiltering(image_array, sp=sp, sr=sr)
        
        if not image_is_input:
            self.set_image(image_array=image_array)
        return image_array
        
    def bilateral_remove_noise(self, image_array=None, kernel_size=5, sigma_color=50, sigma_space=50):
        image_is_input = True
        if image_array is None:
            image_is_input = False
            image_array = self.image_array
        
        if len(image_array.shape) == 2:
            image_array = self.gray_to_rgb(image_array)
            
        image_array = cv2.bilateralFilter(image_array, kernel_size, sigma_color, sigma_space)
        if not image_is_input:
            self.set_image(image_array=image_array)
        return image_array
        
    def median_blur_remove_noise(self, image_array=None, kernel_size=3):
        image_is_input = True
        if image_array is None:
            image_is_input = False
            image_array = self.image_array
            
        image_array = cv2.medianBlur(image_array, kernel_size)
        if not image_is_input:
            self.set_image(image_array=image_array)
        return image_array
        
    def gaussian_blur_remove_noise(self, image_array=None, kernel_size=3, sigma_color=0):
        image_is_input = True
        if image_array is None:
            image_is_input = False
            image_array = self.image_array
            
        image_array = cv2.GaussianBlur(image_array, (kernel_size, kernel_size), sigma_color)
        if not image_is_input:
            self.set_image(image_array=image_array)
        return image_array
        
    def morphologyEx(self, mode, image_array=None, kernel_size=2):
    
        kernel = np.ones((kernel_size, kernel_size), np.uint8)        
        image_is_input = True
        if image_array is None:
            image_is_input = False
            image_array = self.image_array
            
        if mode == self.MORPH_OPEN:
            image_array = cv2.morphologyEx(image_array, cv2.MORPH_OPEN, kernel)
        elif mode == self.MORPH_CLOSE:
            image_array = cv2.morphologyEx(image_array, cv2.MORPH_CLOSE, kernel)
        elif mode == self.DILATE:
            image_array = cv2.dilate(image_array, kernel, iterations = 1)
        elif mode == self.ERODE:
            image_array = cv2.erode(image_array, kernel, iterations = 1)        
        else:
            raise Exception('mode not match, mode: ' + mode)
            
        if not image_is_input:
            self.set_image(image_array=image_array)
        return image_array
        
    def edge_detection(self, image_array=None, threshold1=100, threshold2=200):
        image_is_input = True
        if image_array is None:
            image_is_input = False
            image_array = self.image_array
        image_array = cv2.Canny(image_array, threshold1, threshold2)
            
        if not image_is_input:
            self.set_image(image_array=image_array)
        return image_array
    
    # alpha ¡÷ Contrast control (1.0-3.0)
    # beta ¡÷ Brightness control (0-100)
    def contrast(self, image_array=None, alpha=1.5, beta=0):
        image_is_input = True
        if image_array is None:
            image_is_input = False
            image_array = self.image_array
            
        image_array = cv2.convertScaleAbs(image_array, alpha=alpha, beta=beta)
            
        if not image_is_input:
            self.set_image(image_array=image_array)
        return image_array
        
    def get_captcha(self, image_array=None):
        if image_array is None:
            image_array = self.image_array
        image = Image.fromarray(image_array)
        image.show()
        captcha = pytesseract.image_to_string(image, lang='eng', config='--psm 7 --oem 3')
        captcha = ''.join(filter(str.isalnum, captcha))
        return captcha