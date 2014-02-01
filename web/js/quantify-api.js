var Quantify = {};

Quantify.getData = function(http) {
    return http.get('http://127.0.0.1:8080')
}

function asd() {
    return [
        {"city": "Frankfurt am Main", "country": "Germany", "ts": "2009-11-25 00:00:00", "type": "location", "transport": "air"},
        {"city": "Kiev", "country": "Ukraine", "ts": "2009-11-29 00:00:00", "type": "location", "transport": "air"},
        {"city": "Cologne", "country": "Germany", "ts": "2011-08-14 00:00:00", "type": "location", "transport": "air"},
        {"city": "Kiev", "country": "Ukraine", "ts": "2011-08-18 00:00:00", "type": "location", "transport": "air"},
        {"city": "Beijing", "country": "China", "ts": "2012-02-18 00:00:00", "type": "location", "transport": "air"},
        {"city": "Shenzhen", "country": "China", "ts": "2012-02-18 00:00:00", "type": "location", "transport": "air"},
        {"city": "Beijing", "country": "China", "ts": "2012-02-25 00:00:00", "type": "location", "transport": "air"},
        {"city": "Kiev", "country": "Ukraine", "ts": "2012-02-25 00:00:00", "type": "location", "transport": "air"},
        {"city": "Cologne", "country": "Germany", "ts": "2012-03-03 00:00:00", "type": "location", "transport": "air"},
        {"city": "Paris", "country": "France", "ts": "2012-03-03 00:00:00", "type": "location", "transport": "train"},
        {"city": "Nice", "country": "France", "ts": "2012-03-05 00:00:00", "type": "location", "transport": "air"},
        {"city": "Frankfurt am Main", "country": "Germany", "ts": "2012-03-11 00:00:00", "type": "location", "transport": "air"},
        {"city": "Kiev", "country": "Ukraine", "ts": "2012-03-11 00:00:00", "type": "location", "transport": "air"},
        {"city": "Moscow", "country": "Russia", "ts": "2012-05-18 00:00:00", "type": "location", "transport": "air"},
        {"city": "Kiev", "country": "Ukraine", "ts": "2012-05-20 00:00:00", "type": "location", "transport": "air"},
        {"city": "Frankfurt am Main", "country": "Germany", "ts": "2013-03-25 00:00:00", "type": "location", "transport": "air"},
        {"city": "Washington", "country": "USA", "ts": "2013-03-25 00:00:00", "type": "location", "transport": "air"},
        {"city": "San Francisco", "country": "USA", "ts": "2013-03-25 00:00:00", "type": "location", "transport": "air"},
        {"city": "Frankfurt am Main", "country": "Germany", "ts": "2013-03-31 00:00:00", "type": "location", "transport": "air"},
        {"city": "Kiev", "country": "Ukraine", "ts": "2013-03-31 00:00:00", "type": "location", "transport": "air"},
        {"city": "Memmingen", "country": "Germany", "ts": "2013-05-02 00:00:00", "type": "location", "transport": "air"},
        {"city": "Zurich", "country": "Switzerland", "ts": "2013-05-02 00:00:00", "type": "location", "transport": "train"},
        {"city": "Interlaken", "country": "Switzerland", "ts": "2013-05-04 00:00:00", "type": "location", "transport": "train"},
        {"city": "Geneva", "country": "Switzerland", "ts": "2013-05-07 00:00:00", "type": "location", "transport": "train"},
        {"city": "Milano", "country": "Italy", "ts": "2013-05-10 00:00:00", "type": "location", "transport": "train"},
        {"city": "Kiev", "country": "Ukraine", "ts": "2013-05-10 00:00:00", "type": "location", "transport": "air"},
        {"city": "Moscow", "country": "Russia", "ts": "2013-06-22 00:00:00", "type": "location", "transport": "air"},
        {"city": "Seoul", "country": "South Korea", "ts": "2013-06-23 00:00:00", "type": "location", "transport": "air"},
        {"city": "Moscow", "country": "Russia", "ts": "2013-07-06 00:00:00", "type": "location", "transport": "air"},
        {"city": "Kiev", "country": "Ukraine", "ts": "2013-07-06 00:00:00", "type": "location", "transport": "air"},
        {"city": "Prague", "country": "Czech Republic", "ts": "2013-07-21 00:00:00", "type": "location", "transport": "air"},
        {"city": "Seoul", "country": "South Korea", "ts": "2013-07-22 00:00:00", "type": "location", "transport": "air"},
        {"city": "Moscow", "country": "Russia", "ts": "2013-08-05 00:00:00", "type": "location", "transport": "air"},
        {"city": "Kiev", "country": "Ukraine", "ts": "2013-08-05 00:00:00", "type": "location", "transport": "air"},
        {"city": "Amsterdam", "country": "Netherlands", "ts": "2013-09-26 00:00:00", "type": "location", "transport": "air"},
        {"city": "Dublin", "country": "Ireland", "ts": "2013-09-26 00:00:00", "type": "location", "transport": "air"},
        {"city": "Amsterdam", "country": "Netherlands", "ts": "2013-09-28 00:00:00", "type": "location", "transport": "air"},
        {"city": "Kiev", "country": "Ukraine", "ts": "2013-09-28 00:00:00", "type": "location", "transport": "air"},
        {"city": "Kharkiv", "country": "Ukraine", "ts": "2013-11-29 00:00:00", "type": "location", "transport": "car"},
        {"city": "Melitopol", "country": "Ukraine", "ts": "2014-01-05 00:00:00", "type": "location", "transport": "train"},
        {"city": "Kharkiv", "country": "Ukraine", "ts": "2014-01-08 00:00:00", "type": "location", "transport": "train"},
        {"city": "Kiev", "country": "Ukraine", "ts": "2014-01-16 00:00:00", "type": "location", "transport": "train"},
        {"city": "Kharkiv", "country": "Ukraine", "ts": "2014-01-17 00:00:00", "type": "location", "transport": "train"}
    ];
}