package Adapters;

import android.content.Context;
import android.content.Intent;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import com.bumptech.glide.Glide;
import com.example.hope.Country;
import com.example.hope.ElectronicDance;
import com.example.hope.GOAT;
import com.example.hope.Gospel;
import com.example.hope.HipHop;
import com.example.hope.Holiday;
import com.example.hope.Hot100;
import com.example.hope.International;
import com.example.hope.Latin;
import com.example.hope.Pop;
import com.example.hope.R;
import com.example.hope.Rock;

import java.util.List;

import Models.Genre;

public class GenreAdapter extends RecyclerView.Adapter<GenreAdapter.MyViewHolder> {

    private Context mContext;
    private List<Genre> musicGenres;
    private Genre bg;
    private String uname;


    public class MyViewHolder extends RecyclerView.ViewHolder {
        public TextView title, count;
        public ImageView thumbnail, overflow;

        public MyViewHolder(View view) {
            super(view);
            title = (TextView) view.findViewById(R.id.title);
            //count = (TextView) view.findViewById(R.id.count);
            thumbnail = (ImageView) view.findViewById(R.id.thumbnail);
            //overflow = (ImageView) view.findViewById(R.id.overflow);
        }
    }


    public GenreAdapter(Context mContext, List<Genre> musicGenres, String Username) {
        this.mContext = mContext;
        this.musicGenres = musicGenres;
        this.uname=Username;
    }

    @Override
    public MyViewHolder onCreateViewHolder(final ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext()).inflate(R.layout.genreview_row, parent, false);
        final TextView genreView = itemView.findViewById(R.id.title);
        final ImageView musicCover = itemView.findViewById(R.id.thumbnail);
        musicCover.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View itemView){

                String genre="Country";
                        genre=genreView.getText().toString();
                Class genreclass= null;

                //Attempt to use string resource to generate class

                try {
                    genreclass=Class.forName("com.example.hope."+genre);
                } catch (ClassNotFoundException e) {
                    e.printStackTrace();
                }

                Intent intent=new Intent(itemView.getContext(),genreclass);
                intent.putExtra("Genre",genre);
                itemView.getContext().startActivity(intent);


//                if (genre == "Country"){
//                    Intent intent=new Intent(itemView.getContext(), Country.class);
//                    itemView.getContext().startActivity(intent);
//                }
//                if (genre == "GOAT"){
//                    Intent intent=new Intent(itemView.getContext(), GOAT.class);
//                    itemView.getContext().startActivity(intent);
//                }
//                if (genre == "Gospel"){
//                    Intent intent=new Intent(itemView.getContext(), Gospel.class);
//                    itemView.getContext().startActivity(intent);
//                }
//                if (genre == "HipHop"){
//                    Intent intent=new Intent(itemView.getContext(), HipHop.class);
//                    itemView.getContext().startActivity(intent);
//                }
//                if (genre == "Holiday"){
//                    Intent intent=new Intent(itemView.getContext(), Holiday.class);
//                    itemView.getContext().startActivity(intent);
//                }
//                if (genre == "International"){
//                    Intent intent=new Intent(itemView.getContext(), International.class);
//                    itemView.getContext().startActivity(intent);
//                }
//                if (genre == "Latin"){
//                    Intent intent=new Intent(itemView.getContext(), Latin.class);
//                    itemView.getContext().startActivity(intent);
//                }
//                if (genre == "Pop"){
//                    Intent intent=new Intent(itemView.getContext(), Pop.class);
//                    itemView.getContext().startActivity(intent);
//                }
//                if (genre == "Rock"){
//                    Intent intent=new Intent(itemView.getContext(), Rock.class);
//                    itemView.getContext().startActivity(intent);
//                }
//                if (genre == "ElectronicDance"){
//                    Intent intent=new Intent(itemView.getContext(), ElectronicDance.class);
//                    itemView.getContext().startActivity(intent);
//                }



//                Intent intent=new Intent(itemView.getContext(), NavBarActivity.class);
//                intent.putExtra("Genre",genre);
//                intent.putExtra("UN",uname);
//                itemView.getContext().startActivity(intent);

            }
        });

        return new MyViewHolder(itemView);
    }



    @Override
    public void onBindViewHolder(final MyViewHolder holder, int position) {
        Genre genre = musicGenres.get(position);
        final String tit=genre.getName();
        holder.title.setText(genre.getName());

        Glide.with(mContext).load(genre.getThumbnail()).into(holder.thumbnail);

    }



    @Override
    public int getItemCount() {
        return musicGenres.size();
    }


}
