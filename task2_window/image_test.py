from tkinter import *

root = Tk()
root.title("Jong GUI")  # 타이틀명 지정
root.geometry("640x480")

label1 = Label(root, text="안녕하세요")
label1.pack()

photo = PhotoImage(file="D:\\python\\project\\tkinter\\image.png")
label2 = Label(root, image=photo)
label2.pack()


def change():
    label1.config(text="또 만나요")  # config 속성 값을 바꿔주고 싶을 때

    global photo2  # Garbage Collection : 불필요한 메모리 공간 해제
    # 전역변수로 만들어야 불필요한 메모리라고 인식이 안되기 때문에
    # 전역변수가 아니면 필요없는 것인지 알고 메모리 삭제해버림
    photo2 = PhotoImage(file="D:\\python\\project\\tkinter\\image2.png")
    label2.config(image=photo2)


btn = Button(root, text="클림", command=change)
btn.pack()


root.mainloop()  # 창이 닫히지 않게 해주는 것