package com.example.hope;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.res.Resources;
import android.graphics.Rect;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.design.widget.BottomNavigationView;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.DefaultItemAnimator;
import android.support.v7.widget.GridLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.util.TypedValue;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.List;

import Adapters.GenreAdapter;
import Models.Genre;

public class GenrePage extends AppCompatActivity {

    private RecyclerView recyclerView;
    private GenreAdapter adapter;
    private List<Genre> musicGenres;
    BottomNavigationView bottomNavigationView;


    private String usename;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_genreview);

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
//        bottomNavigationView.setOnNavigationItemSelectedListener(new BottomNavigationView.OnNavigationItemSelectedListener() {
//            @Override
//            public boolean onNavigationItemSelected(@NonNull MenuItem item) {
//                switch (item.getItemId()) {
//                    case R.id.action_recents:
//                        Intent i = new Intent(getApplicationContext(), Hot100.class);
//                        startActivity(i);
//                        break;
//                    case R.id.action_favorites:
//                        //Toast.makeText(Hot100.this, "Favorites", Toast.LENGTH_SHORT).show();
//                        Intent genres = new Intent(getApplicationContext(), GenrePage.class);
//                        startActivity(genres);
//                        break;
//                    case R.id.action_nearby:
//                        Toast.makeText(GenrePage.this, "Nearby", Toast.LENGTH_SHORT).show();
//                        break;
//                }
//                return true;
//            }
//        });


        usename=getIntent().getStringExtra("UN");


        recyclerView = (RecyclerView) findViewById(R.id.recycler_view);

        musicGenres = new ArrayList<>();
        adapter = new GenreAdapter(this, musicGenres,usename);


        RecyclerView.LayoutManager mLayoutManager = new GridLayoutManager(this, 1);
        recyclerView.setLayoutManager(mLayoutManager);
        recyclerView.addItemDecoration(new GridSpacingItemDecoration(1, dpToPx(10), true));
        recyclerView.setItemAnimator(new DefaultItemAnimator());
        recyclerView.setAdapter(adapter);





        displayGenres();

    }


    public void setUsename(String usename) {
        this.usename = usename;
    }

    public String getUsename() {
        return usename;
    }

    private void displayGenres() {
        int[] covers = new int[]{
                R.drawable.country,
                R.drawable.electronicdance,
                R.drawable.goat,
                R.drawable.gospel,
                R.drawable.hiphop,
                R.drawable.holiday,
                R.drawable.international,
                R.drawable.latin,
                R.drawable.pop,
                R.drawable.rock
        };

        Genre a = new Genre("Country", covers[0]);
        musicGenres.add(a);

        a = new Genre("ElectronicDance", covers[1]);
        musicGenres.add(a);

        a = new Genre("GOAT",  covers[2]);
        musicGenres.add(a);

        a = new Genre("Gospel", covers[3]);
       musicGenres.add(a);

        a = new Genre("HipHop",  covers[4]);
        musicGenres.add(a);

        a = new Genre("Holiday", covers[5]);
        musicGenres.add(a);

        a = new Genre("International", covers[6]);
        musicGenres.add(a);

        a = new Genre("Latin", covers[7]);
        musicGenres.add(a);

        a = new Genre("Pop", covers[8]);
        musicGenres.add(a);

        a = new Genre("Rock", covers[9]);
        musicGenres.add(a);





        adapter.notifyDataSetChanged();
    }

    /**
     * RecyclerView item decoration - give equal margin around grid item
     */
    public class GridSpacingItemDecoration extends RecyclerView.ItemDecoration {

        private int spanCount;
        private int spacing;
        private boolean includeEdge;

        public GridSpacingItemDecoration(int spanCount, int spacing, boolean includeEdge) {
            this.spanCount = spanCount;
            this.spacing = spacing;
            this.includeEdge = includeEdge;
        }

        @Override
        public void getItemOffsets(Rect outRect, View view, RecyclerView parent, RecyclerView.State state) {
            int position = parent.getChildAdapterPosition(view); // item position
            int column = position % spanCount; // item column


            if (includeEdge) {
                outRect.left = spacing - column * spacing / spanCount; // spacing - column * ((1f / spanCount) * spacing)
                outRect.right = (column + 1) * spacing / spanCount; // (column + 1) * ((1f / spanCount) * spacing)

                if (position < spanCount) { // top edge
                    outRect.top = spacing;
                }
                outRect.bottom = spacing; // item bottom
            } else {
                outRect.left = column * spacing / spanCount; // column * ((1f / spanCount) * spacing)
                outRect.right = spacing - (column + 1) * spacing / spanCount; // spacing - (column + 1) * ((1f /    spanCount) * spacing)
                if (position >= spanCount) {
                    outRect.top = spacing; // item top
                }
            }
        }
    }

    private int dpToPx(int dp) {
        Resources r = getResources();
        return Math.round(TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, dp, r.getDisplayMetrics()));
    }


}
