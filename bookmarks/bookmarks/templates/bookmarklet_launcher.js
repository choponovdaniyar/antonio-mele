document.body.innerHTML +=  `<inhead>${document.head.outerHTML}</inhead>`;
if(window.myBookmarklet !== undefined){
    myBookmarklet();
}else{
    var src_ = `https://14a5-193-106-51-180.eu.ngrok.io/static/js/bookmarklet.js?r=${Math.floor(Math.random()*99999999999999999999)}`;
    var script = `<br><script src='${src_}'></script>`;
    document.body.innerHTML += script;
}



