# 미니 프로젝트 : 재판하는 존경장님

## 웹 사이트 URL : [**재판하는 존경장님**](http://starandnight.shop/)

<hr>

설명

### KBS 토크쇼 '안녕하세요' 프로그램을 오마주하여 만든 프로젝트로 각자의 사연을 게시하고 **다른 회원들도 공감되는 사연인지를 공유**하는 웹 사이트입니다.

<hr>

## Youtube URL : [**재판하는 존경장님**](https://www.youtube.com/watch?v=ssS0QL75v0g)

<img width="140" alt="썸네일" src="https://user-images.githubusercontent.com/84619866/133743855-03d1d3cd-b89c-409a-92fe-9aeb455c75a5.png">

<hr>

## Github URL : [**github 주소 (public)**](https://github.com/jeangho293/_week1)

## 페이지 설계

<img width="700" alt="재판실화면" src="https://user-images.githubusercontent.com/71538344/133754088-5d7c39ca-ccad-4601-babd-1a95402d7077.png">
<img width="700" alt="글작성화면" src="https://user-images.githubusercontent.com/71538344/133753789-51b1200c-75fd-454c-84c1-47e5de3b746a.png">

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

<img width="700" alt="상세페이지화면" src="https://user-images.githubusercontent.com/71538344/133754154-ffb00657-a9a1-4d4c-84e2-39fab9804e04.png">

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

<img width="700" alt="수정페이지화면" src="https://user-images.githubusercontent.com/71538344/133754262-0490a1ec-106f-4e7d-a952-7cae2d9b210a.png">

- 재판 수정 페이지
    1. 재판의 제목 또는 내용을 수정

<img width="700" alt="마이페이지화면" src="https://user-images.githubusercontent.com/71538344/133753717-05c20cf8-6432-4051-9e56-2ec1467b1cb2.png">

- 마이 페이지
    1. 내가 작성한 재판 및 댓글 목록 확인
        - 최근에 저장된 글 순으로 목록 확인
        - 작성한 재판 목록의 오른쪽 끝에서 해당 재판의 공감 수를 확인
        - 작성한 댓글 내용과 어떤 제목의 재판에 달렸는 지 확인
        - 클릭하면 해당 재판의 상세 페이지로 이동
        - 한 페이지에 10개 씩 출력

<img width="700" alt="로그인화면" src="https://user-images.githubusercontent.com/71538344/133760716-914d52c2-cdbd-46f1-aa31-ccc0088d2bb6.png">

- 로그인 페이지
    1. 로그인 또는 회원가입

- 에러 페이지
    1. 잘못된 URL로 접근 시 404 페이지
    2. 토큰 시간이 만료되거나 토큰 정보가 잘못되어 있으면 401 페이지

<hr>

## 모바일 페이지

<img width="200" alt="모바일화면" src="https://user-images.githubusercontent.com/71538344/133756747-4ac06d67-668a-4b6d-af8b-e640c1459297.gif" />

![카카오톡](https://user-images.githubusercontent.com/84619866/133869979-0165383a-fb43-4c17-a4ce-011252e181aa.png)


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

# CSR과 SSR

## - CSR과 SSR 비교

<pre>
<h2>CSR의 장점</h2>
첫 페이지 로딩을 제외하면 렌더링이 빠르고 데이터 비용도 아낄 수 있는 여지가 높다.
TTV와 TTI 사이의 공백이 없기때문에 페이지가 활성화되면 클릭과 같은 이벤트의 딜레이가 없다.

<h2>CSR의 단점</h2>
첫 페이지 로딩이 느릴 수 있으며 그에 따라 SEO에 취약하다.
그 이유는 CSR은 처음에 빈 페이지로 존재하기 때문에 검색엔진 로봇이 크롤링 할 때, 빈 페이지를 크롤링할 경우,
원하는 정보를 얻지 못 할 수 있다.

<h2>SSR의 장점</h2>
첫 페이지의 로딩이 빨라진다.
CSR에 비해서 SEO에 최적화 되어있다.

<h2>SSR의 단점</h2>
사용자가 많을수록 서버가 처리하는 데이터의 양이 많아지므로 과부하가 CSR에 비해 쉽다.
페이지는 띄어질수 있으나 JS와 같은 동적제어 소스코드를 전달받지 못한다면 클릭과 같은 이벤트를 수행할 수 없다.
즉, TTV와 TTI 사이에 공백이 있기 때문에 대기상태가 존재할 수 있다는 것이다.
</pre>

<hr>

# SSR과 쿠키/세션 설명

## - 쿠키/세션 대비 장점 설명

<pre>
<h2>JWT vs 세션/쿠키</h2>
공통점 : 둘 다 애플리케이션에서 인증을 하기위해 사용되며 HTTP 헤더에 세션ID나 토큰을 실어서 서버로 보내준다는 것은 동일하다.
차이점 : 세션/쿠키 방식은 사용자의 정보를 저장하는 세션 저장소를 필요로 하는 반면, JWT는 세션 저장소 없이 토큰 안에 유저의 정보들을 넣는다.
즉, 인증을 위해 정보를 암호화 하느냐(JWT) 별도의 저장소를 이용하느냐(세션/쿠키)의 차이가 있다.

<h2>JWT의 장점</h2>
JWT는 발급한 후 검증만 하면 되기 때문에 추가 저장소가 필요 없다.
토큰을 기반으로 하는 다른 인증 시스템에 접근이 가능하기 때문에 확장성이 뛰어나다. (ex) Facebook 로그인, Google 로그인

<h2>JWT의 단점</h2>
이미 발급된 JWT에 대해서는 돌이킬 수 없다. 세션/쿠키 방식의 경우에는 만일 쿠키가 악의적으로 이용된다면, 해당하는 세션을 저장소에서 지워버리면 그만이지만 JWT는 한 번 발급되면 유효기간이 만료될 때 까지는 사용이 가능하다.
이 문제를 해결하기 위해 기존의 Access Token의 유효기간을 짧게 가져가고 Refresh Token이라는 새로운 토큰을 발급할 수 있는데, 이러면 Access Token을 탈취당하더라도 상대적으로 피해를 줄일 수 있다.
유저의 중요한 정보들은 Payload에 넣을 수 없기 때문에 (Payload는 탈취당하면 충분히 복호화될 수 있다.) Payload 정보가 제한적이다.
토큰은 세션/쿠키 방식에 비해 크기가 크다.
</pre>

<hr>

# 직면한 문제와 해결 방안

<details>
<summary>댓글 작성 및 좋아요 이벤트 후 전체화면 새로고침할 경우, 사용자에게 보여지는 이벤트 결과에 딜레이 발생.</summary>
<div markdown="1">

    해결 방안
    전체 페이지에 대한 정보를 불러오기보단 수정된 영역 Refresh하여 데이터의 비용을 줄임으로써 딜레이 현상 최소화

    $('#ReplyDiv').load(window.location.href + " #ReplyDiv") // 특정 영역 부분 새로고침

</div>
</details>

<details>
<summary>게시글 작성과 댓글 작성 중 줄바꿈을 해도 실제 보이는 페이지는 한 줄로 게시되는 현상 발견.</summary>
<div markdown="1">
    
    원인
    
    해결방안
    게시글 작성 줄바꿈은 '\n'로 저장되기에 서버단에서 content.replace('\n', '<br>')로 필터링하여 DB 저장으로 해결.

</div>
</details>

<details>
<summary>jinja2를 사용하고 줄바꿈 동작을 구현하기위해 {{ content | safe }} 사용함에 따른 XSS의 취약점 발견.</summary>
<div markdown="1">

    해결방안
    서버에 데이터를 보내주기전에 미리 프론트에서 <>와 같은 태그의 속성을 나타내는 특수문자에 대해 필터링.

</div>
</details>

<details>
<summary>jinja2 반복문이 적용된 button의 value값을 정상적으로 불러오지 못하는 현상 발견.</summary>
<div markdown="1">

    해결방안
    onclick="function(this.value)" // 로 함수의 args를 설정하여 구현으로 해결함.

</div>
</details>

<details>
<summary>ajax에서 error로 빠지게 하려면 어떻게 해야 할까</summary>
<div markdown=“1”>

    해결방안
    render_template() 메서드 http status 변경하기
    `render_template(‘error/401.html’, msg=msg), 401`

</div>
</details>

<details>
<summary>매번 동일한 에러 처리를 작성하기 귀찮으면 어떻게 할 수 있을까</summary>
<div markdown=“1">

    해결방안
    http error 핸들러 작성하고 핸들러에 에러 처리를 위임하기
    `@app.errorhandler(500)
     def page_not_found(e):
         return render_template(‘error/500.html’), 500`
    `abort(404)`

</div>
</details>

<details>
<summary>ObjectId() is not JSON serializable 에러와 함께 jsonify에 db조회 값이 안들어가면? </summary>
<div markdown=“1”>

    해결방안
    mongoDB ObjectId를 jsonify에 넣기 전 문자열로 바꾸기
    `for post in posts:
         post[“_id”] = str(post[“_id”])`

</div>
</details>

<details>
<summary>문자열로 mongoDB의 ObjectId를 기준으로 조회하려면? </summary>
<div markdown=“1">

    해결방안
    ObjectId 생성자 사용하기
    `db.post.delete_one({‘_id’: ObjectId(post_id_receive)})`

</div>
</details>

<details>
<summary>JS에서 element를 생성하는 함수와 해당 element가 선택자인 Event Listener를 실행에 대한 에러 발생.</summary>
<div markdown=“1">

    원인
    element가 생성함수를 실행하기 전에 Event Listener가 선언되어 존재하지 않는 element를 참고하는 동작을 수행했기를 인지함.

    해결방안
    Event Listener가 element 생성 함수와 다른 스코프에 존재할 경우, element 생성 함수가 실행되고 난 후 Event Listener를 동작시킴.

</div>
</details>

<details>
<summary>글 목록 데이터 GET요청 시 글 목록 데이터가 undefined로 출력되는 현상 발생.</summary>
<div markdown=“1">

    원인
    글 데이터를 받은 GET요청은 비동기 처리이므로 요청된 데이터가 오기전에 글 목록 출력을 실행해서 생긴 현상임을 인지함.

    해결방안
    Ajax의 동작 후 글 출력 함수를 동작시키면 필요 데이터를 정상적으로 받고 수행하므로서 해결함. 

</div>
</details>
