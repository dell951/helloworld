// ==UserScript==
// @name         NFOMaker
// @namespace    http://tampermonkey.net/
// @include      https://*vixen.com/*
// @include      https://*tushy.com/*
// @include      https://*blacked.com/*
// @include      https://*x-art.com/*
// @include      https://*nubilefilms.com/*
// @include      https://*letsdoeit.com/watch/*
// @include      https://*sexart.com/*
// @include      https://*metart.com/*
// @include      https://*newsensations.com/*
// @include      https://*sweetsinner.com/*
// @include      https://javdb*.com/v/*
// @include      https://*wowgirlsblog.com/*
// @include      https://*18onlygirlsblog.com/*
// @include      https://*passion-hd.com/*
// @include      https://*tiny4k.com/*
// @include      https://*21naturals.com/*
// @include      https://*eroticax.com/*
// @version      0.2
// @description  NFO Maker
// @author       You
// @require      http://ajax.aspnetcdn.com/ajax/jQuery/jquery-3.5.1.min.js
// @grant        GM_xmlhttpRequest
// @grant        GM_addStyle
// @grant        GM_getValue
// @grant        GM_setValue
// @grant        GM_setClipboard
// @grant        GM_getResourceURL
// ==/UserScript==

var pickUpSite = function(body){
    var site = window.location.hostname.replace("www.", "").replace(".com","").replace(".xxx","");
    console.log("current site: " + site);
    if (site === "x-art")
        xArtNFOGenerator(body);
    else if (site === "nubilefilms")
        nubilefilmsNFOGenerator(body);
    else if (site === "letsdoeit")
        setTimeout(function() {letsdoeitNFOGenerator(body);}, 5000);
    else if (site === "sexart")
        setTimeout(function() {sexartNFOGenerator(body);}, 5000);
    else if (site === "metart")
        setTimeout(function() {metartNFOGenerator(body);}, 5000);
    else if (site === "newsensations")
        newsensationsNFOGenerator(body);
    else if (site === "passion-hd" || site === "tiny4k")
        passionHdNFOGenerator(body, site);
    else if (site === "21naturals")
        TwentyOnenaturalsNFOGenerator(body);
    else if (site === "eroticax")
        eroticaxNFOGenerator(body);
    else if (site === "wowgirlsblog" || site === "18onlygirlsblog")
        setTimeout(function() {wowgirlsNFOGenerator(body);}, 5000);
    else if (site === "vixen" || site === "tushy" || site === "blacked")
        vtbNFOGenerator(body, site);
    else if (site === "sweetsinner")
        setTimeout(function() {sweetsinnerNFOGenerator(body);}, 5000);
    else if (site.startsWith('javdb'))
        javDbNFOGenerator(body);
    else console.log("Not Supported");
}

var javDbNFOGenerator = function(body) {
    var movieFile = "";
    if (document.querySelector("nav.movie-panel-info span.value"))
        movieFile = document.querySelector("nav.movie-panel-info span.value").textContent;
    var movieTitle = document.querySelector("h2.title strong").textContent.replace(movieFile, "").trim();
    var movieDate = document.querySelectorAll("nav.movie-panel-info div.panel-block")[1].querySelector("span").textContent;
    var movieDesc = movieTitle;
    var starsList = [];
    if (document.querySelectorAll("nav.movie-panel-info div.panel-block")[8])
     starsList = document.querySelectorAll("nav.movie-panel-info div.panel-block")[8].querySelector("span").textContent.split(" ");
    var movieStars = [];
    starsList.forEach((star) => {
        if (!star.includes('♂')) {
            movieStars.push(star.replace('♀','').replace('♂','').trim());
            console.log(star.replace('♀','').replace('♂','').trim());
        }
    });
    var movieFanart = document.querySelector("img.video-cover").src;
    var moviePoster = movieFanart.replace("/covers/","/thumbs/");
    var $input = $('<input type="button" value="createNfo" id="btn_generate_nfo"/>');
    $(document).on('click', '#btn_generate_nfo', function(){
        outPutCommand(movieFile, movieTitle, '', movieDesc, movieDate, movieStars, movieFanart, moviePoster, true);
    });
    $input.appendTo($("body"));
}

var sweetsinnerNFOGenerator = function(body) {
    var movieFile = window.location.pathname.split("/")[3];
    console.log(movieFile);
    var movieTitle = document.querySelector("section h2").textContent;
    console.log(movieTitle);
    var dateStr = contains("div div span", "Release Date:")[0].textContent.replace("Release Date:","");
    var movieDate = new Date(dateStr).toLocaleDateString("en-CA");
    console.log(movieDate);
    var movieDesc = contains("div div span", "Description:")[0].textContent.replace("Description:","");
    console.log(movieDesc);
    var starsList = document.querySelectorAll("div.wxt7nk-5.cSAYFi a");
    var movieStars = [];
    starsList.forEach((star) => {
        movieStars.push(star.text);
        console.log(star.text);
    })
    var movieFanart = document.querySelector("div.tg5e7m-2.hQwXfp img").src;
    var moviePoster = movieFanart;
    outPutCommand(movieFile, movieTitle, 'sweetsinner', movieDesc, movieDate, movieStars, movieFanart, moviePoster, true);
}

// Google Posters 21Naturals
var TwentyOnenaturalsNFOGenerator = function(body) {
    var movieFile = window.location.pathname.split('/')[3]
    console.log(movieFile);
    var movieTitle = document.querySelector("div.titleBar h1.title").textContent;
    console.log(movieTitle);
    var movieDate = document.querySelector("div.updatedDate").textContent.trim();
    console.log(movieDate);
    var movieDesc = document.querySelector("div.sceneDesc").textContent.replace('Video Description:','').trim()
    console.log(movieDesc);
    var starsList = document.querySelectorAll("div.sceneCol.sceneColActors a")
    var movieStars = [];
    starsList.forEach((star) => {
        movieStars.push(star.text);
        console.log(star.text);
    })
    var movieFanart = document.querySelector("div.playerDiv div.vjs-poster").style.backgroundImage.replace('url("','').replace('")','');
    var moviePoster = movieFanart;
    outPutCommand(movieFile, movieTitle, '21naturals', movieDesc, movieDate, movieStars, movieFanart, moviePoster, true);
}

var eroticaxNFOGenerator = function(body) {
    var movieFile = window.location.pathname.split('/')[3]
    console.log(movieFile);
    var movieTitle = document.querySelector("div.titleBar h1.title").textContent;
    console.log(movieTitle);
    var dateStr = document.querySelector("div.updatedDate").textContent.trim();
    var movieDate = new Date(dateStr).toLocaleDateString("en-CA");
    console.log(movieDate);
    var movieDesc = "movieTitle";
    if (document.querySelector("div.sceneDesc"))
        document.querySelector("div.sceneDesc").textContent.replace('Video Description:','').trim();    console.log(movieDesc);
    var starsList = document.querySelectorAll("div.sceneCol.sceneColActors a")
    var movieStars = [];
    starsList.forEach((star) => {
        movieStars.push(star.text);
        console.log(star.text);
    })
    var movieFanart = document.querySelector("div.playerDiv div.vjs-poster").style.backgroundImage.replace('url("','').replace('")','');
    var moviePoster = movieFanart;
    outPutCommand(movieFile, movieTitle, 'eroticax', movieDesc, movieDate, movieStars, movieFanart, moviePoster, true);
}

// No Date found on page. search it from google.
var passionHdNFOGenerator = function(body, site) {
    var movieFile = window.location.pathname.split("/")[2];
    console.log(movieFile);
    var movieTitle = document.querySelector("h1").textContent;
    console.log(movieTitle);
    var movieDate = "";
    console.log(movieDate);
    var movieDesc = "";
    if (document.querySelector("div#t2019-side div#t2019-sinfo div"))
        movieDesc = document.querySelector("div#t2019-side div#t2019-sinfo div").textContent.trim();
    console.log(movieDesc);
    var starsList = [];
    if (document.querySelector("div#t2019-side div#t2019-sinfo div#t2019-models"))
        starsList = document.querySelector("div#t2019-side div#t2019-sinfo div#t2019-models").querySelectorAll("a");
    var movieStars = [];
    starsList.forEach((star) => {
        movieStars.push(star.text);
        console.log(star.text);
    })
    var movieFanart = "";
    if (document.querySelector("video.player"))
        movieFanart = document.querySelector("video.player").poster;
    var moviePoster = movieFanart;
    if (document.querySelector("div.t2019-thumbs a img"))
        moviePoster = document.querySelector("div.t2019-thumbs a img").src
    outPutCommand(movieFile, movieTitle, site, movieDesc, movieDate, movieStars, movieFanart, moviePoster, false);
}

// search the movie name and get the pictures and pick up poster
var wowgirlsNFOGenerator = function(body) {
    var movieFile = window.location.pathname.replaceAll("/","");
    console.log(movieFile);
    var movieTitle = document.querySelector("h1").textContent.split("-")[1].trim()
    var dateStr = document.querySelector("div.post_date").textContent;
    var movieDate = new Date(dateStr).toLocaleDateString("en-CA");
    var movieDesc = movieTitle;
    var descEl = document.querySelector("div.video-embed").querySelectorAll("p")[1];
    if (descEl)
        movieDesc = descEl.textContent;

    var starsList = document.querySelector("h1").textContent.split("-")[0].split(",");
    var movieStars = [];
    starsList.forEach((star) => {
        movieStars.push(star.trim());
        console.log(star.trim());
    });
    var movieFanart = "";
    if (document.querySelector("div.wpfp_custom_background"))
        movieFanart = document.querySelector("div.wpfp_custom_background").style.backgroundImage.replace('url("','').replace('")','')
    var moviePoster = movieFanart
    outPutCommand(movieFile, movieTitle, 'wowgirls', movieDesc, movieDate, movieStars, movieFanart, moviePoster, true);
}

var newsensationsNFOGenerator = function(body) {
    var movieFile = window.location.pathname.split("/")[3].replace(".html","");
    console.log(movieFile);
    var movieTitle = document.querySelector("div.sceneRight h2").textContent;
    console.log(movieTitle);
    var dateStr = document.querySelector("div.sceneRight div.sceneDateP").textContent.split(",")[0];
    var movieDate = new Date(dateStr).toLocaleDateString("en-CA");
    console.log(movieDate);
    var movieDesc = document.querySelector("div.description p").textContent.replace("Description: ","");
    console.log(movieDesc);
    var starsList = document.querySelectorAll("div.sceneRight span.tour_update_models a");
    var movieStars = [];
    starsList.forEach((star) => {
        movieStars.push(star.text);
        console.log(star.text);
    })
    var movieFanart = document.querySelector("div.indvideo.clear img").src;
    console.log(movieFanart);
    var moviePoster = movieFanart;
    console.log(moviePoster);
    outPutCommand(movieFile, movieTitle, 'newsensations', movieDesc, movieDate, movieStars, movieFanart, moviePoster, true);
}

var letsdoeitNFOGenerator = function(body) {
    var movieFile = window.location.pathname.split("/")[3].replace(".en.html","");
    console.log(movieFile);
    var movieTitle = document.querySelectorAll("div.module-video-details h1")[0].textContent;
    console.log(movieTitle);
    var dateStr = document.querySelectorAll("div.h5-published")[0].textContent.split("•")[1].trim();
    var movieDate = new Date(dateStr).toLocaleDateString("en-CA");
    console.log(movieDate);

    var movieDesc = document.querySelector("div.module-video-details").querySelector("span.toggle-text").textContent.trim();
    console.log(movieDesc);

    var starsList = document.querySelectorAll("div.module-video-details div.actors a.links strong");
    var movieStars = [];
    starsList.forEach((star) => {
        movieStars.push(star.textContent);
        console.log(star.textContent);
    })
    var movieFanart = document.querySelectorAll("div.video-cover-container picture.poster img")[0].src
    console.log(movieFanart);
    var moviePoster = movieFanart;
    console.log(moviePoster);
    outPutCommand(movieFile, movieTitle, 'letsdoeit', movieDesc, movieDate, movieStars, movieFanart, moviePoster, true);
};

var metartNFOGenerator = function(body) {
    var movieFile = window.location.pathname.split("/")[5].toLowerCase().replaceAll("_","-");
    console.log(movieFile);
    var movieTitle = document.querySelector("div.movie-image-panel div.info-container h3").textContent;
    console.log(movieTitle);
    var showMoreLink = document.querySelector("div.movie-image-panel div.info-container div.description a.clickable");
    if (showMoreLink) showMoreLink.click();

    var movieDesc = movieTitle;
    var descEl = document.querySelector("div.movie-image-panel div.info-container div.description p");
    if (descEl) movieDesc = descEl.textContent.trim().replaceAll('"',"'");
    console.log(movieDesc);

    var dateStr = document.querySelectorAll("div.movie-image-panel div.info-container div.movie-data ul li")[2].textContent.replace("Released:","");
    var movieDate = new Date(dateStr).toLocaleDateString("en-CA");
    console.log(movieDate);
    var starsList = document.querySelectorAll("div.movie-image-panel div.info-container div.movie-data ul li")[0].textContent.replace("Cast:","").split("&");
    var movieStars = [];
    starsList.forEach((star) => {
        movieStars.push(star.trim());
        console.log(star.trim());
    });
    var movieFanart = "";
    var fanartEl = document.querySelector("div.player img.cover-image");
    if (fanartEl)
        movieFanart = document.querySelector("div.player img.cover-image").src;
    else
        movieFanart = document.querySelector("div.player div.jw-preview").style.backgroundImage.replace('url("','').replace('")','');
    console.log(movieFanart);
    var moviePoster = document.querySelector("div.img-container img").src;
    console.log(moviePoster);
    outPutCommand(movieFile, movieTitle, 'metart', movieDesc, movieDate, movieStars, movieFanart, moviePoster, true);
}

var sexartNFOGenerator = function(body) {
    var movieFile = window.location.pathname.split("/")[5].toLowerCase().replaceAll("_","-");
    console.log(movieFile);
    var movieTitle = document.querySelector("div.movie-image-panel div.info-container h3").textContent;
    console.log(movieTitle);
    document.querySelector("div.movie-image-panel div.info-container div.description a.clickable").click();
    //var movieDesc = $("div.movie-image-panel div.info-container div.description p").textContent.trim().replaceAll('"',"'");
    var movieDesc = document.querySelector("div.movie-image-panel div.info-container div.description p").textContent.trim().replaceAll('"',"'");
    console.log(movieDesc);
    var dateStr = document.querySelectorAll("div.movie-image-panel div.info-container div.movie-data ul li")[2].textContent.replace("Released:","");
    var movieDate = new Date(dateStr).toLocaleDateString("en-CA");
    console.log(movieDate);
    var starsList = document.querySelectorAll("div.movie-image-panel div.info-container div.movie-data ul li")[0].textContent.replace("Cast:","").split("&");
    var movieStars = [];
    starsList.forEach((star) => {
        movieStars.push(star.trim());
        console.log(star.trim());
    });
    var movieFanart = "";
    if (document.querySelector("div.player div.jw-preview"))
        movieFanart = document.querySelector("div.player div.jw-preview").style.backgroundImage.replace('url("','').replace('")','');
    else
        movieFanart = document.querySelector("div.player img").src;
    console.log(movieFanart);
    var moviePoster = document.querySelector("div.movie-image-panel div.img-container img").src;
    console.log(moviePoster);
    outPutCommand(movieFile, movieTitle, 'sexart', movieDesc, movieDate, movieStars, movieFanart, moviePoster, true);
}

var nubilefilmsNFOGenerator = function(body) {
    var movieFile = window.location.pathname.split("/")[4];
    console.log(movieFile);
    var movieTitle = $("div.content-pane-container div.content-pane-title h2").toArray()[0].textContent;
    console.log(movieTitle);

    var movieDesc = movieTitle;
    var descs = $("div.content-pane-container div.content-pane-column div.collapse").toArray()[0];
    if(descs !== undefined){
        movieDesc = descs.textContent.trim().replaceAll('"',"'");
    }
    console.log(movieDesc);
    var dateStr = $("div.content-pane-container span.date").toArray()[0].textContent.trim();
    var movieDate = new Date(dateStr).toLocaleDateString("en-CA");
    console.log(movieDate);
    var starsList = $("div.content-pane-performers a.model").toArray();
    var movieStars = [];
    starsList.forEach((star) => {
        movieStars.push(star.textContent);
        console.log(star.textContent)
    })

    var fanartDiv = $("div.watch-page-video-container video").toArray()[0];
    var movieFanart = fanartDiv.poster;
    console.log(movieFanart);
    var moviePoster = movieFanart.replace("cover1280.jpg", "cover614.jpg");
    console.log(moviePoster);
    outPutCommand(movieFile, movieTitle, 'nubilefilms', movieDesc, movieDate, movieStars, movieFanart, moviePoster, true);
};

var xArtNFOGenerator = function(body) {
    var movieFile = window.location.pathname.replace("/videos", "").replaceAll("/","").replaceAll("_","-").replaceAll("%20","-");
    console.log(movieFile);
    var movieTitle = $("div.row div.columns h1").toArray()[0].textContent;
    console.log(movieTitle);

    var movieDesc = movieTitle;
    var descs = $("div.row div.info p").toArray()[1];
    if(descs !== undefined){
        movieDesc = descs.textContent.trim().replaceAll('"',"'");
    }
    console.log(movieDesc);
    var dateStr = $("div.row div.info h2").toArray()[2].textContent.trim();
    var movieDate = new Date(dateStr).toLocaleDateString("en-CA");
    console.log(movieDate);
    var movieStars = $("div.row div.info h2").toArray()[3].textContent.replace("featuring", "").split("|");
    movieStars.forEach(star => console.log(star.trim()))

    var movieFanart = $("div.widescreen img").toArray()[1].src;
    var moviePoster = movieFanart.replace("1-lrg", "2");
    outPutCommand(movieFile, movieTitle, 'x-art', movieDesc, movieDate, movieStars, movieFanart, moviePoster, true);
};

// get poster manually
var vtbNFOGenerator = function(body, site) {
   console.log("NFOGenerator for VTB:");
   var movieFile = window.location.pathname.replace("/videos/","");
   console.log(movieFile);
   var movieTitle = document.querySelectorAll("h1[data-test-component=VideoTitle]")[0].textContent;
   console.log(movieTitle);
   var movieDesc = document.querySelectorAll("div[data-test-component=VideoDescription]")[0].textContent;
   console.log(movieDesc);
   var dateStr = document.querySelectorAll("span[data-test-component=ReleaseDateFormatted]")[0].textContent;
   var movieDate = new Date(dateStr).toLocaleDateString("en-CA");
   console.log(movieDate);
   var starList = document.querySelectorAll("div[data-test-component=VideoModels]")[0].querySelectorAll("a");
   var movieStars = [];
   starList.forEach((star)=> {
       console.log(star.text);
       movieStars.push(star.text);
   });

   //var movieFanart = document.querySelectorAll("div[data-test-component=ProgressiveImage]")[0].querySelectorAll("picture")[0].querySelector("source").src;
   var movieFanart = document.querySelector("div[data-test-component=VideoCoverWrapper]").querySelectorAll("div[data-test-component=ProgressiveImage]")[0].querySelector("picture img").src;
    var moviePoster = movieFanart;
   outPutCommand(movieFile, movieTitle, site, movieDesc, movieDate, movieStars, movieFanart, moviePoster, true);
};

var outPutCommand = function(file, title, studio, desc, date, stars, fanart, poster, runme) {
   var output = './nfomaker.py -i /volume5/Downloaded/' + file + '.mp4 -m "' + title + '" -s "' + studio + '" -r "' + date + '" -d "' + desc + '"' + ' -f "' + fanart + '"' + ' -p "' + poster + '"';
   stars.forEach((star) => {
      if (star.trim() != "") output = output + ' -a "' + star.trim() + '"';
   });
   console.log(output);
   if (runme)
       postNfo("/volume5/Downloaded/"+file+".mp4", title, studio, desc, date, stars, fanart, poster);
}

var postNfo = function(file, title, studio, desc, date, stars, fanart, poster) {
   var xhr = new XMLHttpRequest();
   var url = 'https://192.168.1.150:5556/postnfo'
   xhr.open("POST", url, true);
   xhr.setRequestHeader("Content-Type", "application/json");
   xhr.onreadystatechange = function () {
      if (xhr.readyState === 4 && xhr.status === 200) {
          var json = JSON.parse(xhr.responseText);
      }
   };
   var data = JSON.stringify({"file": file, "title": title, "studio": studio, "desc": desc, "date": date, "fanart": fanart, "poster": poster, "stars": stars});
   var resp = xhr.send(data);
   console.log(resp);
}

function contains(selector, text) {
  var elements = document.querySelectorAll(selector);
  return Array.prototype.filter.call(elements, function(element){
    return RegExp(text).test(element.textContent);
  });
}

$(document).ready(
     pickUpSite(document.body)
);