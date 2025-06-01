# # user_inp = int(input("Enter a number: "))
#
# # s = 0
# # for i in range(1,user_inp):
# #     if user_inp % i == 0:
# #         s += 1
# # if s == 2:
# #     print('ПРостое число')
# # else:
# #     print('Не простое')
#
# n = int(input("Введите число: "))
# is_negative = n < 0
# n = abs(n)
# reversed_num =, 0
#
# while n > 0:
#     digit = n % 10
#     reversed_num = reversed_num * 10 + digit
#     n = n // 10
#
# if is_negative:
#     reversed_num = -reversed_num
#
# print("Перевёрнутое число:", reversed_num)
#
# # son = int(input("Enter a number: "))
#
# #
# # son1 = int(input("dfjpjfwi"))
# # son2 = int(input("dwwewrer"))
# #
# # if (son1<=son2):
# #     bir = son1
# #     ikki = son2
# # for j in range(bir,ikki+1):
# #     s = 0
# #     for i in range(1,j+1):
# #         if j%i==0:
# #             s+=1
# #     if s==2:
# #         print(j)
#
#
# #
# # for i in range(1,user_inp):
# #     if user_inp / 2:
# #         print('Простое число')
# #     elif user_inp % 2:
# #         print("usk")
# #     else:
# #         print('Не простое')
# #
# # for i in range(1 ,user_inp+1):
# #     if user_inp % 2 == 0:
# #         print(f"Простое число")
# #     else:
# #         print("непростое")
# #
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics.texture import Texture

import matplotlib.pyplot as plt
import io
from PIL import Image as PILImage


class ChartApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        self.image_widget = Image()
        btn = Button(text="Показать график")
        btn.bind(on_press=self.show_chart)

        layout.add_widget(self.image_widget)
        layout.add_widget(btn)

        return layout

    def show_chart(self, instance):
        # Построение графика через matplotlib
        plt.figure(figsize=(4, 3))
        plt.plot([1, 2, 3, 4], [10, 20, 25, 30], marker='o')
        plt.title("Пример графика")
        plt.tight_layout()

        # Сохраняем график во временный буфер
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        # Загружаем изображение через Pillow
        pil_image = PILImage.open(buf)
        pil_image = pil_image.convert('RGBA')

        # Преобразуем изображение в текстуру Kivy
        tex = Texture.create(size=pil_image.size, colorfmt='rgba')
        tex.blit_buffer(pil_image.tobytes(), colorfmt='rgba', bufferfmt='ubyte')
        tex.flip_vertical()

        # Отображаем текстуру
        self.image_widget.texture = tex


if __name__ == '__main__':
    ChartApp().run()
    