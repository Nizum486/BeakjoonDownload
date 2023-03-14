from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from tkinter import*

import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
from tkinter import filedialog
import clipboard
import sys, os
import glob

info = """ 백준 문제 다운로더 입니다.

        1. 먼저 로그인을 합니다.
            => 로그인시, 타일을 찾게할 수 도 있습니다.
            => 수동으로 부탁드립니다..!

        2. 문제 리스트 받아오기를 합니다.

        3. 문제를 어떤 형식으로 다운받을지 선택합니다.
            => 선택하지 않아도 기본형식은 .txt 를 사용합니다.

        4. 저장공간을 선택합니다.

        5. 문제 다운로드를 눌러 다운로드를 진행합니다
            => 다운로드 진행중에는 손을 떼시길 권장합니다.

"""


problemLst = []
exNameLSt = []

root = Tk()
root.title("백준 문제 다운로더")


options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

if getattr(sys, 'frozen', False):
    chromdriver_path = os.path.join(sys._MEIPASS, "chromedriver.exe")
    driver = webdriver.Chrome(options=options)
else: driver = webdriver.Chrome(options=options)


# 로그인 함수
def login():

    try:
        myId = idEntry.get()
        myPsw = pswEntry.get()

        if len(myId) == 0:
            msgbox.showwarning("경고", "아이디를 입력하세요")
            return
        
        if len(myPsw) == 0:
            msgbox.showwarning("경고", "비밀번호를 입력하세요")
            return

        driver.get("https://www.acmicpc.net/login?next=%2F")

        # 아이디 비밀번호 입력창 찾기
        userId = driver.find_element(By.NAME, "login_user_id")
        userPsw = driver.find_element(By.NAME, "login_password")

        # 아이디 비밀번호 입력
        userId.send_keys(myId)
        userPsw.send_keys(myPsw)

        userPsw.send_keys(Keys.RETURN)

        # GUI 화면 내 로그인 정보 삭제
        idEntry.delete(0, END)
        idEntry.insert(0, "")
        pswEntry.delete(0, END)
        pswEntry.insert(0, "")

    except Exception as err:
        msgbox.showerror("에러", err)


    print(myId + "로 로그인되었습니다")
    now_acting.config(text= myId + "로 로그인되었습니다.")

# 로그아웃
def logout():

    global problemLst, exNameLSt

    logoutBtn = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/div/ul/li[5]/a")
    logoutBtn.click()

    # 로그아웃시, 문제 리스트도 초기화
    problemLst = []
    exNameLSt = []
    now_acting.config(text="로그아웃 되었습니다.")

# 미리 저장된 아이디로 로그인
def savedId():

    driver.get("https://www.acmicpc.net/login?next=%2F")

    # 아이디 비밀번호 입력창 찾기
    userId = driver.find_element(By.NAME, "login_user_id")
    userPsw = driver.find_element(By.NAME, "login_password")

    # 아이디 비밀번호 입력
    userId.send_keys("##")
    userPsw.send_keys("##")

    userPsw.send_keys(Keys.RETURN)

    print("저장된 아이디로 로그인 합니다")
    now_acting.config(text="저장된 아이디로 로그인합니다.")

# 문제 리스트 받아오기
def getProblems():

    now_acting.config(text="문제 리스트를 받아옵니다.")

    try:
        user = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/div/ul/li[1]/a")
        user.click()

        problems = driver.find_elements(By.CLASS_NAME, "result-ac")
        for idx, problem in enumerate(problems):
            problemNumber = problem.text
            problemLst.append(problemNumber)
            problemLstBox.insert(END, problemNumber)

            progress = (idx + 1) / len(problems) * 100
            p_var.set(progress)
            progress_bar.update()

        print(problemLst)
        print("푼 문제 수 : " + str(len(problemLst)))
    except:
        msgbox.showwarning("경고", "로그인을 먼저 해주세요.")
        
# 문제 다운로드 하기
def downloadProblem():

    # 문제 리스트를 받지 않았을 때
    if len(problemLst) == 0:
        msgbox.showwarning("경고", "먼저 문제 리스트를 받아와주세요.")
        return

    # 저장 경로를 선택하지 않았을 때
    if len(txt_dest_path.get()) == 0:
        msgbox.showwarning("경고", "저장경로를 선택하세요.")
        return

    # 테스트를 위한 cnt
    cnt = 0

    now_acting.config(text="문제 다운로드를 시작합니다.")

    for problem in problemLst:
        try:
            # 각 문제의 페이지로 이동
            driver.get("https://www.acmicpc.net/status?from_mine=1&problem_id="+problem+"&user_id=gbs102505")

            problemLanguage = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[3]/div[6]/div/table/tbody/tr/td[7]/a[1]")
            
            
            Language = problemLanguage.text
            exNameLSt.append(Language)

            problemLanguage.click()

            formatOption = 0
            fileFormat = cmb_format.get()
            if fileFormat == "txt파일": formatOption = 0
            else: formatOption = 1


            
            # 복사 버튼 클릭 -> 클립보드에 저장
            # 복사 버튼이 다른 위치에 있는 경우도 있어서, try-except문으로 잡기
            # 현재까지는 이 두개로 다 잡았지만, 추후에 더 추가될 수 도 있음.
            try:
                copyBtn = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[3]/div[5]/div/button")
                
            except:
                copyBtn = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[3]/div[7]/div/button")
            
            # else: pass

            copyBtn.click()

            path = txt_dest_path.get()

            # 클립보드에 저장된 정보를 myCode에 저장한 후,  txt파일에 paste한다
            # 지정된 경로에 저장하기 위해 경로를 txt_dest_path로 받음
            f = open(path + "/" + problem + ".txt", 'w')
            myCode = clipboard.paste()
            f.write(myCode)
            f.close()

            print(problem + "문제가 저장 되었습니다.")
            
            # 테스트 시범 10개 다운로드
            cnt += 1
            if cnt == 10: 
                print("10개 다운")
                break
        
        except:
            print("오류가 발생했습니다. 다음으로 넘어갑니다.")
            pass
    
    print("다운이 완료되었습니다.")
    now_acting.config(text="다운로드가 완료되었습니다.")
    

    if formatOption == 1:
        print("파일 형식 변환을 시작합니다.")
        changeExName()

# 닫기
def close():
    driver.close()
    quit()

# 저장 경로 (폴더)
def browse_dest_path():
    folder_selected = filedialog.askdirectory()
    if folder_selected == '':
        return
    txt_dest_path.delete(0, END)
    txt_dest_path.insert(0, folder_selected)

def changeExName():
    
    for j, i in enumerate(exNameLSt):
        if i == "C99": exNameLSt[j] = ".c"
        elif i == "C++17": exNameLSt[j] = ".cpp"
        elif i == "Python 3" or "PyPy3": exNameLSt[j] = ".py"
        else: exNameLSt[j] = ".txt"

    print(exNameLSt)
    c_cnt = exNameLSt.count(".c")
    cpp_cnt = exNameLSt.count(".cpp")
    py_cnt = exNameLSt.count(".py")

    # 터미널에 각 언어당 몇문제 풀었는지 표시
    print("C : %d" % c_cnt)
    print("C++ : %d" % cpp_cnt)
    print("python : %d" % py_cnt)


    path = txt_dest_path.get()
    files = glob.glob(path + "/*.txt")

    for i, name in enumerate(files):
        if not os.path.isdir(name): # 디렉터리 포함X
            src = os.path.splitext(name) # 확장자, 파일명 구분
            os.rename(name,src[0]+ exNameLSt[i]) # 확장자를 없에고 exNameLst의 확장자명

    print("변환이 완료 되었습니다.")
    now_acting.config(text="파일 형식 변환이 완료되었습니다.")


def howItWork():
    msgbox.showinfo("도움말", info)

# 도움말 메뉴
menu = Menu(root)
menu_info = Menu(menu, tearoff=0)
menu_info.add_command(label="도움말", command=howItWork)
menu.add_cascade(label="도움말", menu = menu_info)

root.config(menu=menu)


# 1. 로고 프레임
logoFrame = Frame(root)
logoFrame.pack(padx = 5, pady = 5)

logo = PhotoImage(file="./img/beakjoonlogo.png")
imglabel = Label(logoFrame, image=logo)
imglabel.pack()


# 2. 로그인프레임 => loginEntry프레임, 로그인 버튼 프레임
loginFrame = Frame(root)
loginFrame.pack()

# id, psw 프레임
loginEntryFrame = LabelFrame(loginFrame, text="아이디 비밀번호를 입력하세요", labelanchor='n')
loginEntryFrame.pack(side="left", padx = 5, pady = 5)

# 아이디
idLabel = Label(loginEntryFrame, text="Id")
idLabel.pack(padx = 5)
idEntry = Entry(loginEntryFrame, width=30)
idEntry.pack(padx = 5, pady = 5)

# 패스워드
pswLabel = Label(loginEntryFrame, text="Password")
pswLabel.pack(padx = 5)
pswEntry = Entry(loginEntryFrame, width=30, show="*")
pswEntry.pack(padx = 5, pady = 5)

# 로그인 버튼 프레임
loginButtonFrame = Frame(loginFrame)
loginButtonFrame.pack(side="right", padx = 5, pady = 5)

loginButton = Button(loginButtonFrame, text="로그인" ,command=login)
loginButton.pack(side="left", padx=5, pady=5, ipadx=10, ipady=2)

logoutButton = Button(loginButtonFrame, text="로그아웃", command=logout)
logoutButton.pack(side="left", padx=5, pady=5, ipadx=10, ipady=2)

savedIdButton = Button(loginButtonFrame, text="사용자", command=savedId)
savedIdButton.pack(side="bottom", padx=5, pady=5, ipadx=10, ipady=2)


# 3. 리스트 프레임 => 확장자 옵션 프레임, 문제 리스트 프레임
lstFrame = Frame(root)
lstFrame.pack(padx = 5, pady = 5)

# 파일 확장자 옵션 프레임
FormatOptFrame = LabelFrame(lstFrame, text="파일 저장 형식")
FormatOptFrame.pack(side="right", padx = 5, pady = 5)

FormatOptionLst = ["txt파일", "제출한 코드의 형식"]
cmb_format = ttk.Combobox(FormatOptFrame, state="readonly", values=FormatOptionLst, width=20)
cmb_format.current(0)
cmb_format.pack(side="right", padx = 5, pady = 5)

# 문제 리스트 프레임
problemLstFrame = LabelFrame(lstFrame, text="문제 리스트", labelanchor='n')
problemLstFrame.pack(padx = 5, pady = 5)

scrollbar = Scrollbar(problemLstFrame)
scrollbar.pack(side="right", fill="y")

problemLstBox = Listbox(problemLstFrame, width=30, height=10, selectmode="extended", yscrollcommand=scrollbar.set)
problemLstBox.pack()

scrollbar.config(command=problemLstBox.yview)


# 4. 저장경로 프레임
pathFrame = LabelFrame(root, text="저장경로")
pathFrame.pack(fill="x", padx = 5, pady = 5, ipady=5)

txt_dest_path = Entry(pathFrame)
txt_dest_path.pack(side="left", fill="x", expand=True, padx = 5, pady = 5, ipady=4)

btn_dest_path = Button(pathFrame, text="찾아보기", width=10, command=browse_dest_path)
btn_dest_path.pack(side="right", padx = 5, pady = 5)


# 5. 버튼 프레임
buttonFrame = Frame(root)
buttonFrame.pack(fill = BOTH, padx = 5, pady = 5)

now = LabelFrame(buttonFrame, text="진행상황", labelanchor='n')
now.pack(padx=5, pady=5, ipady=2)

# 진행 상황 Progress Bar
frame_progress = LabelFrame(buttonFrame, text="진행 상황")
frame_progress.pack(fill=BOTH, padx = 5, pady = 5, ipady=5)

p_var = DoubleVar()
progress_bar = ttk.Progressbar(frame_progress, maximum=len(problemLst), variable=p_var)
progress_bar.pack(fill=BOTH, padx = 5, pady = 5)


now_acting = Label(now, text="현재 진행상황이 표시됩니다.")
now_acting.pack(padx = 5, pady=5)

getproblemsBtn = Button(buttonFrame, text="문제 리스트 받기", command=getProblems)
getproblemsBtn.pack(side="left", padx=5, pady=5, ipady=2)

downloadBtn = Button(buttonFrame, text="문제다운로드", command=downloadProblem)
downloadBtn.pack(side="left", padx=5, pady=5, ipady=2)

closeBtn = Button(buttonFrame, text="나가기", command=close)
closeBtn.pack(side="right", padx=5, pady=5, ipady=2)


root.resizable(False, False)
root.mainloop()