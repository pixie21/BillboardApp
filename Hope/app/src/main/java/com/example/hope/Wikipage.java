package com.example.hope;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class Wikipage extends AppCompatActivity {



    public String url= "https://en.wikipedia.org/wiki/";
    public String name;
    public String url1;
    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.webview);
        Intent intent = getIntent();
        name=intent.getExtras().getString("Artist");
        if (name.contains("Featuring")){
            name=name.substring(0,name.indexOf("Featuring"));
        }
        else if(name.contains("&")){
            name=name.substring(0,name.indexOf("&"));
        }
//        else if(name.contains(",")){
//            //name.split(",");
//            name = name.replace(",", "&");
//            //name=name.substring(0,name.indexOf("&"));
//        }

        Log.d("URL", name);

        String newname= name.replaceAll(" ", "_");

        url1=url+newname;

        WebView webView = (WebView) findViewById(R.id.load_url_web_view);
        webView.setWebViewClient(new WebViewClient());
        webView.loadUrl(url1);
    }
}