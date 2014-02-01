var Quantify = {};

Quantify.getData = function(http, hostname) {
    var url = 'http://' + hostname + ':8080';
    return http.get(url)
}
