# 미니 프로젝트 : 재판하는 존경장님

## 웹 사이트 URL : [**재판하는 존경장님**](http://starandnight.shop/) 

<hr>

설명
###KBS 토크쇼 '안녕하세요' 프로그램을 오마주하여 만든 프로젝트로 각자의 사연을 게시하고 **다른 회원들도 공감되는 사연인지를 공유**하는 웹 사이트입니다.  

<hr>

## Youtube URL : [**재판하는 존경장님**](https://www.youtube.com/watch?v=ssS0QL75v0g)

<img width="140" alt="썸네일" src="https://user-images.githubusercontent.com/84619866/133743855-03d1d3cd-b89c-409a-92fe-9aeb455c75a5.png">

<hr>

## Github URL : [**github 주소 (public)**](https://github.com/jeangho293/_week1)


## 페이지 설계

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
   
<hr>

## API
기능 | URL | Method | Request | Response
---- | ---- | ---- | --------| ---------|
로그인 | POST | /login | <pre>{<br>   user_id:username,<br>   pw:password<br>}</pre>
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

<hr>
<pre>
<h2>JWT vs 세션/쿠키</h2>
공통점 : 둘다 애플리케이션에서 인증을 하기위해 사용되며 HTTP 헤더에 세션ID나 토큰을 실어서 서버로 보내준다는 것은 동일하다.
차이점 : 세션/쿠키 방식은 사용자의 정보를 저장하는 세션 저장소를 필요로 하는 반면 JWT는 세션 저장소 없이 토큰 안에 유저의 정보들이 넣는다.
즉, 인증을 위해 정보를 암호화 하냐(JWT) 별도의 저장소를 이용하냐(세션/쿠키)의 차이가 있다.

###JWT의 장점
JWT는 발급한 후 검증만 하면 되기 때문에 추가 저장소가 필요 없다.
토큰을 기반으로 하는 다른 인증 시스템에 접근이 가능하기 때문에 확장성이 뛰어나다. (ex) Facebook 로그인, Google 로그인

###JWT의 단점
이미 발급된 JWT에 대해서는 돌이킬 수 없다. 세션/쿠키 방식의 경우에는 만일 쿠키가 악의적으로 이용된다면, 해당하는 세션을 저장소에서 지워버리면 되지만 JWT는 한 번 발급되면 유효기간이 만료될 때 까지는 사용이 가능하다.
이 문제를 해결하기 위해서는 기존의 Access Token의 유효기간을 짧게 가져가고 Refresh Token이라는 새로운 토큰을 발급한다. 이러면 Access Token을 탈취당하더라도 상대적으로 피해를 줄일 수 있다.
유저의 중요한 정보들은 Payload에 넣을 수 없기 때문에 (Payload는 탈취당하면 충분히 복호화될 수 있다.) Payload 정보가 제한적이다.
토큰은 세션/쿠키 방식에 비해 크기가 크다.
</pre>
