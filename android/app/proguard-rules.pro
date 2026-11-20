# WebView köprüleri yansıma ile çağrılır; adları korunmalı.
-keepclassmembers class com.sezerabi.kurye.MainActivity$* {
    @android.webkit.JavascriptInterface <methods>;
}
