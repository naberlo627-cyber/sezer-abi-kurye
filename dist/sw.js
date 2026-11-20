/* Sezar Abi Kurye — çevrimdışı destek */
var CACHE = "sezar-v1";
var ASSETS = [
  "./",
  "./index.html",
  "./manifest.json",
  "./icons/icon-192.png",
  "./icons/icon-512.png",
  "./icons/maskable-512.png",
  "./icons/sc-gorev.png",
  "./icons/sc-kazanc.png",
  "./icons/sc-mesaj.png",
  "./icons/sc-yardim.png"
];

self.addEventListener("install", function(e){
  e.waitUntil(
    caches.open(CACHE).then(function(c){ return c.addAll(ASSETS); })
      .then(function(){ return self.skipWaiting(); })
  );
});

self.addEventListener("activate", function(e){
  e.waitUntil(
    caches.keys().then(function(adlar){
      return Promise.all(adlar.filter(function(a){ return a !== CACHE; })
        .map(function(a){ return caches.delete(a); }));
    }).then(function(){ return self.clients.claim(); })
  );
});

/* Sayfa: ağ öncelikli (düzenlemeler anında görünsün). Simgeler: önbellek öncelikli. */
self.addEventListener("fetch", function(e){
  var istek = e.request;
  if(istek.method !== "GET") return;
  var url = new URL(istek.url);
  if(url.origin !== location.origin) return;

  var sayfa = istek.mode === "navigate" || /\.html$/.test(url.pathname);
  if(sayfa){
    e.respondWith(
      fetch(istek).then(function(yanit){
        var kopya = yanit.clone();
        caches.open(CACHE).then(function(c){ c.put(istek, kopya); });
        return yanit;
      }).catch(function(){
        return caches.match(istek).then(function(m){ return m || caches.match("./index.html"); });
      })
    );
    return;
  }
  e.respondWith(
    caches.match(istek).then(function(m){
      if(m) return m;
      return fetch(istek).then(function(yanit){
        if(yanit && yanit.status === 200){
          var kopya = yanit.clone();
          caches.open(CACHE).then(function(c){ c.put(istek, kopya); });
        }
        return yanit;
      });
    })
  );
});
