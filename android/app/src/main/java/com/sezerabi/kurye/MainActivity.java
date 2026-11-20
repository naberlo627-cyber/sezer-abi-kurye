package com.sezerabi.kurye;

import android.Manifest;
import android.annotation.SuppressLint;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.provider.Settings;
import android.webkit.GeolocationPermissions;
import android.webkit.PermissionRequest;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;

import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;
import androidx.core.content.FileProvider;
import androidx.webkit.WebViewAssetLoader;

import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;

/**
 * Sezar Abi Kurye Android kabuğu.
 *
 * index.html, manifest ve simgeler APK içine gömülüdür; WebViewAssetLoader ile
 * https://appassets.androidplatform.net/assets/www/ altından sunulur. Böylece
 * sayfa güvenli bir kaynakta (https) çalışır ve konum izni isteyebilir.
 */
public class MainActivity extends AppCompatActivity {

    private static final String BASE =
            "https://appassets.androidplatform.net/assets/www/index.html";
    private static final int REQ_CAMERA = 5711;
    private static final int REQ_LOCATION = 5712;

    private WebView web;
    private ValueCallback<Uri[]> filePathCallback;
    private PermissionRequest pendingWebPermission;
    private GeolocationPermissions.Callback pendingGeoCallback;
    private String pendingGeoOrigin;

    private final ActivityResultLauncher<Intent> fileChooser =
            registerForActivityResult(new ActivityResultContracts.StartActivityForResult(), result -> {
                if (filePathCallback == null) return;
                Uri[] uris = null;
                if (result.getResultCode() == RESULT_OK && result.getData() != null) {
                    Intent data = result.getData();
                    if (data.getClipData() != null) {
                        int n = data.getClipData().getItemCount();
                        uris = new Uri[n];
                        for (int i = 0; i < n; i++) uris[i] = data.getClipData().getItemAt(i).getUri();
                    } else if (data.getData() != null) {
                        uris = new Uri[]{data.getData()};
                    }
                }
                filePathCallback.onReceiveValue(uris);
                filePathCallback = null;
            });

    @SuppressLint("SetJavaScriptEnabled")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        final WebViewAssetLoader loader = new WebViewAssetLoader.Builder()
                .addPathHandler("/assets/", new WebViewAssetLoader.AssetsPathHandler(this))
                .build();

        web = new WebView(this);
        web.setBackgroundColor(Color.parseColor("#F1F7F7"));
        setContentView(web);

        web.addJavascriptInterface(new AppBridge(), "SEZAR_APP");

        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setDatabaseEnabled(true);
        s.setAllowFileAccess(true);
        s.setAllowContentAccess(true);
        s.setMixedContentMode(WebSettings.MIXED_CONTENT_COMPATIBILITY_MODE);
        s.setGeolocationEnabled(true);
        // Varlıklar APK içinde gömülü; eski WebView önbellekten göstermesin.
        s.setCacheMode(WebSettings.LOAD_NO_CACHE);
        // Tek tema: açık. Cihaz koyu moddayken içerik koyulaştırmasın.
        if (android.os.Build.VERSION.SDK_INT >= 29) {
            s.setForceDark(WebSettings.FORCE_DARK_OFF);
        }
        if (android.os.Build.VERSION.SDK_INT >= 33) {
            s.setAlgorithmicDarkeningAllowed(false);
        }
        web.clearCache(true);

        web.setWebViewClient(new WebViewClient() {
            @Override
            public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
                return loader.shouldInterceptRequest(request.getUrl());
            }

            @Override
            public void onPageFinished(WebView view, String url) {
                // Sayfa, APK içinde çalıştığını bilsin.
                view.evaluateJavascript(
                        "window.SEZAR_APP_MODE=true;"
                        + "if(window.sezarAppMode)window.sezarAppMode();", null);
            }
        });

        web.setWebChromeClient(new WebChromeClient() {
            @Override
            public void onGeolocationPermissionsShowPrompt(String origin,
                                                           GeolocationPermissions.Callback callback) {
                // Navigasyon için konum şart: izin varsa doğrudan ver,
                // yoksa Android iznini isteyip sonucu beklet.
                if (hasLocationPermission()) {
                    callback.invoke(origin, true, true);
                } else {
                    pendingGeoCallback = callback;
                    pendingGeoOrigin = origin;
                    requestPermissions(new String[]{
                            Manifest.permission.ACCESS_FINE_LOCATION,
                            Manifest.permission.ACCESS_COARSE_LOCATION}, REQ_LOCATION);
                }
            }

            @Override
            public void onPermissionRequest(final PermissionRequest request) {
                if (hasCameraPermission()) {
                    request.grant(request.getResources());
                } else {
                    pendingWebPermission = request;
                    requestPermissions(new String[]{Manifest.permission.CAMERA}, REQ_CAMERA);
                }
            }

            @Override
            public boolean onShowFileChooser(WebView view, ValueCallback<Uri[]> callback,
                                             FileChooserParams params) {
                filePathCallback = callback;
                try {
                    fileChooser.launch(params.createIntent());
                    return true;
                } catch (Exception e) {
                    filePathCallback = null;
                    return false;
                }
            }
        });

        Uri data = getIntent() != null ? getIntent().getData() : null;
        web.loadUrl(data != null ? data.toString() : BASE);
    }

    /* --- sayfa köprüsü ---
       Dış bağlantıları (Google Maps, telefon, WhatsApp) uygulama dışında açar.
       install(): yeni APK'yı indirip sistem kurulum ekranını açar. */
    private class AppBridge {
        @android.webkit.JavascriptInterface
        public void open(String url) {
            if (url == null || url.isEmpty()) return;
            runOnUiThread(() -> {
                try {
                    startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse(url)));
                } catch (Exception e) {
                    Toast.makeText(MainActivity.this, "Açılacak uygulama bulunamadı",
                            Toast.LENGTH_SHORT).show();
                }
            });
        }

        @android.webkit.JavascriptInterface
        public void install(String url) {
            if (url == null || url.isEmpty()) return;
            runOnUiThread(() -> Toast.makeText(MainActivity.this,
                    "Güncelleme indiriliyor…", Toast.LENGTH_SHORT).show());
            new Thread(() -> apkIndirKur(url)).start();
        }

        @android.webkit.JavascriptInterface
        public void toast(String mesaj) {
            if (mesaj == null) return;
            runOnUiThread(() -> Toast.makeText(MainActivity.this, mesaj, Toast.LENGTH_SHORT).show());
        }
    }

    /* APK'yı önbelleğe indirir, FileProvider ile sistem kurulum ekranını açar.
       REQUEST_INSTALL_PACKAGES izni yoksa kullanıcı ayarlara yönlendirilir. */
    private void apkIndirKur(String url) {
        try {
            File hedef = new File(getCacheDir(), "guncelleme.apk");
            HttpURLConnection bag = (HttpURLConnection) new URL(url).openConnection();
            bag.setInstanceFollowRedirects(true);
            bag.setConnectTimeout(15000);
            bag.setReadTimeout(30000);
            try (InputStream giris = bag.getInputStream();
                 FileOutputStream cikis = new FileOutputStream(hedef)) {
                byte[] tampon = new byte[8192];
                int n;
                while ((n = giris.read(tampon)) > 0) cikis.write(tampon, 0, n);
            }
            if (Build.VERSION.SDK_INT >= 26 && !getPackageManager().canRequestPackageInstalls()) {
                runOnUiThread(() -> {
                    Toast.makeText(this, "Kurulum izni gerekiyor", Toast.LENGTH_LONG).show();
                    try {
                        startActivity(new Intent(Settings.ACTION_MANAGE_UNKNOWN_APP_SOURCES,
                                Uri.parse("package:" + getPackageName())));
                    } catch (Exception ignored) {
                    }
                });
                return;
            }
            Uri apkUri = FileProvider.getUriForFile(this, getPackageName() + ".fileprovider", hedef);
            Intent kur = new Intent(Intent.ACTION_VIEW);
            kur.setDataAndType(apkUri, "application/vnd.android.package-archive");
            kur.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_ACTIVITY_NEW_TASK);
            runOnUiThread(() -> startActivity(kur));
        } catch (Exception e) {
            runOnUiThread(() -> Toast.makeText(this, "Güncelleme indirilemedi",
                    Toast.LENGTH_LONG).show());
        }
    }

    @Override
    public void onRequestPermissionsResult(int kod, String[] izinler, int[] sonuclar) {
        super.onRequestPermissionsResult(kod, izinler, sonuclar);
        boolean verildi = sonuclar.length > 0 && sonuclar[0] == PackageManager.PERMISSION_GRANTED;

        if (kod == REQ_LOCATION && pendingGeoCallback != null) {
            pendingGeoCallback.invoke(pendingGeoOrigin, verildi, false);
            pendingGeoCallback = null;
            pendingGeoOrigin = null;
        } else if (kod == REQ_CAMERA && pendingWebPermission != null) {
            if (verildi) pendingWebPermission.grant(pendingWebPermission.getResources());
            else pendingWebPermission.deny();
            pendingWebPermission = null;
        }
    }

    private boolean hasLocationPermission() {
        return ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION)
                == PackageManager.PERMISSION_GRANTED
                || ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION)
                == PackageManager.PERMISSION_GRANTED;
    }

    private boolean hasCameraPermission() {
        return ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA)
                == PackageManager.PERMISSION_GRANTED;
    }

    @Override
    public void onBackPressed() {
        if (web != null && web.canGoBack()) {
            web.goBack();
        } else {
            super.onBackPressed();
        }
    }
}
