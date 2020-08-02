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

import Adapters.ArtistListAdapter;
import Adapters.ListAdapter;

public class TopArtists extends AppCompatActivity {

    private String url = "http://192.168.1.106:5001/ba100";

    private RecyclerView mList;

    private LinearLayoutManager linearLayoutManager;
    private DividerItemDecoration dividerItemDecoration;
    private List<Models.Artists> artistsList;
    private RecyclerView.Adapter adapter1;
    BottomNavigationView bottomNavigationView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.hot100);
        bottomNavigationView = (BottomNavigationView) findViewById(R.id.nav);
        bottomNavigationView.setSelectedItemId(R.id.action_favorites);
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

        artistsList = new ArrayList<>();
        adapter1 = new ArtistListAdapter(getApplicationContext(), artistsList);

        linearLayoutManager = new LinearLayoutManager(this);
        linearLayoutManager.setOrientation(LinearLayoutManager.VERTICAL);
        dividerItemDecoration = new DividerItemDecoration(mList.getContext(), linearLayoutManager.getOrientation());

        mList.setHasFixedSize(true);
        mList.setLayoutManager(linearLayoutManager);
        mList.addItemDecoration(dividerItemDecoration);
        mList.setAdapter(adapter1);

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

                        Models.Artists artists = new Models.Artists();
                        artists.setName(jsonObject.getString("artist"));
                        artists.setLastweek(jsonObject.getInt("lastPos"));
                        artists.setPeakpostion(jsonObject.getInt("peakPos"));
                        artists.setWeeksonchart(jsonObject.getInt("weeks"));
                        artists.setNew(jsonObject.getBoolean("isNew"));
                        artists.setRank(jsonObject.getInt("rank"));
                        artists.setArtisturl(jsonObject.getString("url"));
                        // hot100.setRating(jsonObject.getInt("rating"));
                        // hot100.setYear(jsonObject.getInt("releaseYear"));

                        artistsList.add(artists);
                    } catch (JSONException e) {
                        e.printStackTrace();
                        progressDialog.dismiss();
                    }
                }
                adapter1.notifyDataSetChanged();
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
    }
}

