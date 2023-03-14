BeakjoonDownload
---

python으로 작성한 백준 문제 다운로더입니다.

selenium과 clipboard 모듈이 필요합니다.

    pip install selenium
    pip install clipboard

크롬 웹 드라이버도 필요합니다!

[웹 드라이버 링크](https://chromedriver.chromium.org/downloads)




saveid 함수내의 

    userId.send_keys("##")
    userPsw.send_keys("##")

    userPsw.send_keys(Keys.RETURN)

    print("저장된 아이디로 로그인 합니다")
    now_acting.config(text="저장된 아이디로 로그인합니다.")

'#' 으로 된 부분에 본인 아이디를 치면, '사용자' 버튼만 눌러도 로그인이 가능합니다 .
