package com.example.hope;

import android.app.ProgressDialog;
import android.content.Intent;
import android.support.annotation.NonNull;
import android.support.design.widget.BottomNavigationView;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.DividerItemDecoration;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.MenuItem;
import android.widget.Toast;

import com.android.volley.DefaultRetryPolicy;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.RetryPolicy;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonArrayRequest;
import com.android.volley.toolbox.Volley;
import com.squareup.picasso.Picasso;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

import Adapters.ListAdapter;
import Models.Artists;

public class Rock extends AppCompatActivity {

    private String url = "http://192.168.1.106:5001/bbrock";

    private RecyclerView mList;

    private LinearLayoutManager linearLayoutManager;
    private DividerItemDecoration dividerItemDecoration;
    private List<Models.Hot100> hot100List;
    private RecyclerView.Adapter adapter;
    BottomNavigationView bottomNavigationView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.hot100);
        bottomNavigationView = (BottomNavigationView) findViewById(R.id.nav);
        bottomNavigationView.setSelectedItemId(R.id.action_nearby);
        bottomNavigationView.setOnNavigationItemSelectedListener(new BottomNavigationView.OnNavigationItemSelectedListener() {
            @Override
            public boolean onNavigationItemSelected(@NonNull MenuItem item) {
                switch (item.getItemId()) {
                    case R.id.action_recents:
                        Intent i = new Intent(getApplicationContext(), Hot100.class);
                        startActivity(i);
                        break;
                    case R.id.action_favorites:
                        //Toast.makeText(Hot100.this, "Favorites", Toast.LENGTH_SHORT).show();
                        Intent artist_list = new Intent(getApplicationContext(), TopArtists.class);
                        startActivity(artist_list);
                        break;
                    case R.id.action_nearby:
                        Intent genres = new Intent(getApplicationContext(), GenrePage.class);
                        startActivity(genres);
                        break;
                }
                return true;
            }
        });

        mList = findViewById(R.id.main_list);

        hot100List = new ArrayList<>();
        adapter = new ListAdapter(getApplicationContext(), hot100List);

        linearLayoutManager = new LinearLayoutManager(this);
        linearLayoutManager.setOrientation(LinearLayoutManager.VERTICAL);
        dividerItemDecoration = new DividerItemDecoration(mList.getContext(), linearLayoutManager.getOrientation());

        mList.setHasFixedSize(true);
        mList.setLayoutManager(linearLayoutManager);
        mList.addItemDecoration(dividerItemDecoration);
        mList.setAdapter(adapter);
        getData();
    }

    private void getData() {
        final ProgressDialog progressDialog = new ProgressDialog(this);
        progressDialog.setMessage("Loading...");
        progressDialog.show();

        JsonArrayRequest jsonArrayRequest = new JsonArrayRequest(url, new Response.Listener<JSONArray>() {
            @Override
            public void onResponse(JSONArray response) {
                for (int i = 0; i < response.length(); i++) {
                    try {
                        JSONObject jsonObject = response.getJSONObject(i);

                        Models.Hot100 hot100 = new Models.Hot100();
                        hot100.setTitle(jsonObject.getString("title"));
                        hot100.setArtist(jsonObject.getString("artist"));
                        hot100.setNew(jsonObject.getBoolean("isNew"));
                        hot100.setPeakPos(jsonObject.getInt("peakPos"));
                        hot100.setLastPos(jsonObject.getInt("lastPos"));
                        hot100.setRank(jsonObject.getInt("rank"));
                        hot100.setWeeks(jsonObject.getInt("weeks"));
                        hot100.setUrl(jsonObject.getString("url"));


                        hot100List.add(hot100);
                    } catch (JSONException e) {
                        e.printStackTrace();
                        progressDialog.dismiss();
                    }
                }
                adapter.notifyDataSetChanged();
                progressDialog.dismiss();
            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Log.e("Volley", error.toString());
                progressDialog.dismiss();
            }
        });

        jsonArrayRequest.setRetryPolicy(new RetryPolicy() {
            @Override
            public int getCurrentTimeout() {
                return 200000;
            }

            @Override
            public int getCurrentRetryCount() {
                return 50000;
            }

            @Override
            public void retry(VolleyError error) throws VolleyError {

            }
        });
        RequestQueue requestQueue = Volley.newRequestQueue(this);
        requestQueue.add(jsonArrayRequest);
        //jsonArrayRequest.setRetryPolicy(new DefaultRetryPolicy(5001,DefaultRetryPolicy.DEFAULT_MAX_RETRIES,DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));
    }
}