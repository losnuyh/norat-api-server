1. 학교 검색
    [GET] `/school/search?keyword=안양`
```
[
    {
        "id": "34583458",
        "name": "안양초등학교",
        "address": "도로명 주소"
    },
    {
        "name": "안양중학교",
        "address": "도로명 주소"
    }
]
```

2. 휴대폰 인증 번호 발송
    [GET] `authentication/phone`
   * 휴대폰 인증 번호 발송

3. 휴대폰 인증 코드 전송,
   4. 미가입시 핸드폰 인증 토큰 발행 (유효시간 1시간)
   5. 기존 가입시 에러
4. 아이디 중복 체크
5. 회원가입
   6. 아이디, 패스워드, 생년월일
   7. 리턴, 토큰값
8. 로그인
   9. 아이디 패스워드
   10. 리턴: 토큰

--------- 2023-12-25 ---------


7. 내 정보 상태
   8. 가입정보
   9. 학교 정보
   9. 약관동의 상태
   10. 본인 얼굴인증여부
   10. 본인 또는 부모인증상태
7. 약관 동의 업데이트
8. [???] 본인 또는 부모인증 관련 api
9. 아이디 찾기 (require phone token)
10. 패스워드 변경하기 (require phone token or access token)
11. 학교 선택하기
13. 영상 업로드 pre signed url + key 받기
14. 학교 인증 요청하기
15. 학교 게시판 상태보기 (오픈 여부, 인증한 학생 수)
16. 비공개 상태인 내가 쓴글 확인
    17. 심사중인 내가 작성한 글 목록을 확인할 수 있음
    18. 시간순
    19. 게시 수락된 글은 보이지 않음
19. 비공개 상태인 내가 쓴글 삭제하기
20. 글쓰기
    21. 제목
    22. 내용 (최대 200글자?)
21. 게시판 글목록
    22. 페이지네이션
    23. 제목, 본문, 작성자 닉네임 (랜덤), + 내가 쓴 글 여부
22. 글 지우기
24. 탈퇴하기
