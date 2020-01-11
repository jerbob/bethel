var app = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  data: {
    book: 0,
    chapter: 1,
    verse: 0,
    presentable: [],
    socket: io.connect('http://' + document.domain + ':' + location.port + '/socket')
  }
})

app.socket.on('update', function(msg) {
  app.presentable = JSON.parse(msg);
});
