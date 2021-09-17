# 미니 프로젝트 : 재판하는 존경장님
[**재판하는 존경장님**](http://starandnight.shop/)
### 설명
//설명 추가

**데모영상 유튜브 링크 (녹음/설명 없이 둘러보는 용도로 녹화해주세요)**



**데모영상 썸네일 이미지 (280*160 사이즈를 권장합니다)**


[**github 주소 (public)**](https://github.com/jeangho293/_week1)

### 페이지 설계

- 메인 페이지
  1. 전체 재판 목록 확인
     - 최근에 저장된 재판 순으로 전체 재판 목록 확인
     - 목록의 오른쪽 끝에서 해당 재판의 공감 수를 확인
     - 클릭하면 해당 재판의 상세 페이지로 이동
     - 한 페이지에 7개 씩 출력
  2. 재판 저장
     - 로그인하지 않았으면 얼럿 띄우기
  3. 오늘의 TOP3 / 이번 주 TOP3
     - 오늘 또는 한 주간의 재판 중 공감 수가 높은 순으로 각 3개 확인
- 재판 상세 페이지
  1. 재판 상세 내용 확인
     - 재판의 제목, 내용, 작성자, 작성 시간, 조회 수, 공감 수, 비공감 수, 댓글, 댓글 수를 확인
  2. 재판 수정과 삭제
     - 재판의 작성자가 아니면 얼럿 띄우기
  3. 공감과 비공감
     - 공감 또는 비공감 중복 선택 불가
     - 두번 이상 선택 불가
  4. 댓글
     - 댓글을 작성하고 목록을 확인
     - 댓글 목록에는 댓글의 내용, 작성자, 작성 시간을 확인할 수 있음
     - 댓글의 작성자만 댓글을 삭제할 수 있음
- 재판 수정 페이지
  1. 재판의 제목 또는 내용을 수정
- 마이 페이지
  1. 내가 작성한 재판 및 댓글 목록 확인
     - 최근에 저장된 글 순으로 목록 확인
     - 작성한 재판 목록의 오른쪽 끝에서 해당 재판의 공감 수를 확인
     - 작성한 댓글 내용과 어떤 제목의 재판에 달렸는 지 확인
     - 클릭하면 해당 재판의 상세 페이지로 이동
     - 한 페이지에 10개 씩 출력
- 로그인 페이지
  1. 로그인 또는 회원가입
    
- 에러 페이지
  1. 잘못된 URL로 접근 시 404 페이지
  2. 토큰 시간이 만료되거나 토큰 정보가 잘못되어 있으면 401 페이지

    
### API
기능 | URL | Method | Request | Response
---- | ---- | ---- | --------| ---------|
로그인 | POST | /login | 뚝배기깹니다
회원가입 | POST | /register | <pre>{<br>   user_id: user_name,<br>   pw: password<br>}</pre>
회원가입 중복 확인 | POST | /register/check_dup | <pre>{<br>   username_give: username<br>}</pre>
게시글 목록 리뷰 | GET | /posts |  | 전체 게시글 목록 
게시글 상세 내용 | GET | /post | | 해당 게시글 Objectid, 게시글 DB
게시글 작성 | POST | /post | <pre>{<br>   title: title,<br>   content: comment,<br>   image: ''<br>}</pre>
조회수 증가 | POST | /view | <pre>{<br>   post_id: id<br>}</pre>
댓글 작성 | POST |  | <pre>{<br>   post_id: button_value,<br>   comment: reply,<br>   create_date: Today<br>}</pre>
게시글 삭제 | DELETE | /post | <pre>{<br>   post_id: PostID<br>}</pre>
공감 비공감 이벤트 | POST | /like | <pre>{<br>   post_id: button_id,<br>   action: button_action<br>}</pre>
댓글 제거 | DELETE | /comment | <pre>{<br>   post_id: PostID,<br>   comment_id: CommentID<br>}</pre>
게시판 수정 | PUT | /post | <pre>{<br>   post_id: PostID,<br>   title: PostTitle,<br>   content: PostContent,<br>   image: PostImage<br>}</pre>

