BeakjoonDownload
---

python으로 작성한 백준 문제 다운로더입니다.

풀었던 문제들을 저장 할 수 있습니다.

selenium과 clipboard 모듈이 필요합니다.

    pip install selenium
    pip install clipboard

크롬 웹 드라이버도 필요합니다!

[웹 드라이버 링크](https://chromedriver.chromium.org/downloads)


해당 부분을 삭제해야 전체가 다운로드 됩니다.


    # 테스트 시범 10개 다운로드
    cnt += 1
    if cnt == 10: 
        print("10개 다운")
        break



savedid 함수내의 

    userId.send_keys("##")
    userPsw.send_keys("##")

    userPsw.send_keys(Keys.RETURN)

    print("저장된 아이디로 로그인 합니다")
    now_acting.config(text="저장된 아이디로 로그인합니다.")

'#' 으로 된 부분에 본인 아이디와 비밀번호를 넣으면, '사용자' 버튼만 눌러도 로그인이 가능합니다 .
