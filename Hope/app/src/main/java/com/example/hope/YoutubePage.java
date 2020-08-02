package com.example.hope;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class YoutubePage extends AppCompatActivity {



    public String url= "https://music.youtube.com/search?q=";
    public String name;
    public String song;
    public String url1;
    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.webview);
        Intent intent = getIntent();
        name=intent.getExtras().getString("Artist");
        song=intent.getExtras().getString("song");
//        if (name.contains(" ")){
//            name=name.substring(0,name.indexOf("Featuring"));
//        }
//        else if(name.contains("&")){
//            name=name.substring(0,name.indexOf("&"));
//        }
//        else if(name.contains(",")){
//            //name.split(",");
        name = name.replace(" ", "+");
        //name=name.substring(0,name.indexOf("&"));

        song = song.replace(" ","+");
//        }

        Log.d("URL", name);
        Log.d("URL2", song);

        String newname= name+"+"+song;

        url1=url+newname;
        Log.d("newurl", url1);

        WebView webView = (WebView) findViewById(R.id.load_url_web_view);
        webView.setWebViewClient(new WebViewClient());
        webView.loadUrl(url1);
    }
}
