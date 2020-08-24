// form
let frm = document.forms["frm"];
// 버튼들
let addBtn = document.getElementById("submit-btn");
let resetBtn = document.getElementById("reset-btn");
// 북마크 리스트
let bookmarkList = document.getElementById("bookmark-list");
// form reset
function reset() {
    frm.elements.namedItem("id").value = ''
    frm.elements.namedItem("title").value = '';
    frm.elements.namedItem("url").value = '';
}
// 취소 버튼 핸들러 등록
resetBtn.addEventListener("click", reset);
// DOM에 새로운 bookmark 정보 추가
function addItem(bookmark) {
    let templ = `
    <a href="${bookmark.url}" class="bookmark-link">${bookmark.title}</a>
    [<a href="#" class="edit-btn">수정</a>]
    [<a href="#" class="delete-btn">삭제</a>]
    `;
    let el = document.createElement('li');
    el.dataset.itemId = bookmark.id;
    el.classList.add("list-item");
    el.innerHTML = templ;
    bookmarkList.appendChild(el);
}
// 초기 목록 얻기
axios.get("http://127.0.0.1:8000/api/bookmark")
    .then(res => {
        res.data.datas.forEach(item => addItem(item));
    }).catch(e => console.log(e));
// 폼 입력 확인
function check_frm() {
    let title = frm.elements.namedItem("title").value;
    if (!title) return alert("title을 입력하세요");
    let url = frm.elements.namedItem("url").value;
    if (!url) return alert("url을 입력하세요");
    return {
        title,
        url
    };
}
// 확인 버튼 핸들러 등록: itemId가 없으면 추가, 있으면 수정
addBtn.addEventListener("click", event => {
    let itemId = frm.elements.namedItem("id").value.trim();
    data = check_frm();
    if (!data) return;
    if (!itemId) { // 추가
        axios.post("http://127.0.0.1:8000/api/bookmark", data)
            .then(res => {
                addItem(res.data);
                reset();
            }).catch(e => console.log(e));
    } else { // 수정
        // 추후 구현
    }
});

// 수정 - 클릭핚 아이템을 수정 화면으로 설정
bookmarkList.on("click", ".edit-btn", function (e) {
    let el = this.closest(".list-item");
    let itemId = el.dataset.itemId;
    let bookmark = el.getElementsByClassName("bookmark-link")[0];
    let title = bookmark.innerHTML;
    let url = bookmark.href;
    frm.elements.namedItem("id").value = itemId
    frm.elements.namedItem("title").value = title;
    frm.elements.namedItem("url").value = url;
});

// 지정핚 bookmark id의 <a> 엘리턴트를 찾아 리턴
function findItem(id) {
    let items = bookmarkList.getElementsByClassName("bookmark-link");
    let length = items.length;
    for (let i = 0; i < length; i++) {
        if (items[i].parentNode.dataset.itemId == id)
            return items[i];
    }
}
// 수싞핚 수정된 bookmark 정보 갱싞
function updateItem(bookmark) {
    let el = findItem(bookmark.id);
    if (el) {
        el.href = bookmark.url;
        el.innerHTML = bookmark.title;
    }
}
// 확인 버튼 핸들러 등록: itemId가 없으면 추가, 있으면 수정
addBtn.addEventListener("click", event => {
    let itemId = frm.elements.namedItem("id").value.trim();
    data = check_frm();
    if (!data) return;
    if (!itemId) { // 추가
        axios.post("http://127.0.0.1:8000/api/bookmark", data)
            .then(res => {
                addItem(res.data);
                reset();
            }).catch(e => console.log(e));
    } else { // 수정
        axios.put(`http://127.0.0.1:8000/api/bookmark/${itemId}`, data)
            .then(res => {
                updateItem(res.data);
                reset();
            }).catch(e => console.log(e));
    }
});

// bookmark 삭제
bookmarkList.on("click", ".delete-btn", function (e) {
    if (!confirm("삭제하겠습니까?")) return;
    let el = this.closest(".list-item");
    let itemId = el.dataset.itemId;
    axios.delete(`http://127.0.0.1:8000/api/bookmark/${itemId}`)
        .then(res => el.remove())
        .catch(e => console.log(e));
});