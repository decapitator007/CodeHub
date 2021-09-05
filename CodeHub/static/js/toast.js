var first=document.querySelector('#liveToast-1');
var second=document.querySelector('#liveToast-2');
if(first){
  new bootstrap.Toast(first).show();
}
if(second){
  new bootstrap.Toast(second).show();
}
