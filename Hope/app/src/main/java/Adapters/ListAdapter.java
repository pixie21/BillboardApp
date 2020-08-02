package Adapters;

import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.example.hope.R;
import com.example.hope.Wikipage;
import com.example.hope.YoutubePage;
import com.squareup.picasso.Picasso;

import java.io.IOException;
import java.net.URL;
import java.util.List;

import Models.Hot100;

/**
 * Created by ankit on 27/10/17.
 */

public class ListAdapter extends RecyclerView.Adapter<ListAdapter.ViewHolder> {

    private Context context;
    private List<Hot100> list;

    public ListAdapter(Context context, List<Hot100> list) {
        this.context = context;
        this.list = list;
    }

    @Override
    public ViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        View v = LayoutInflater.from(context).inflate(R.layout.list_layout, parent, false);
        return new ViewHolder(v);
    }

    @Override
    public void onBindViewHolder(ViewHolder holder, int position) {

        final Hot100 hot100 = list.get(position);
        Picasso.with(context).load(hot100.getUrl()).into(holder.thumbnail);
        holder.textTitle.setText(hot100.getTitle());
        holder.textArtist.setText(hot100.getArtist());
        holder.textpeakPos.setText("Peak Position \n "+ String.valueOf(hot100.getPeakPos()));
        holder.textlastPos.setText("Last Week  \n " + String.valueOf(hot100.getLastPos()));
        holder.textisNew.setText("IsNew \n " + String.valueOf(hot100.isNew()));
        holder.textrank.setText("Rank \n " + String.valueOf(hot100.getRank()));
        holder.textweeks.setText("Weeks on Chart \n " + String.valueOf(hot100.getWeeks()));
        holder.texturl.setText("Url \n" + hot100.getUrl());
        holder.linearLayout.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent=new Intent(context, YoutubePage.class);
                intent.putExtra("song",hot100.getTitle());
                intent.putExtra("Artist",hot100.getArtist());
                intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                context.startActivity(intent);
//                Toast.makeText(context,
//                        "It has been clicked",Toast.LENGTH_SHORT ).show();

            }

        });
    }
       // Picasso.get().load(texturl).into(view);
    //URL url = URL.(Hot100.getUrl());

    @Override
    public int getItemCount() {
        return list.size();
    }

    public class ViewHolder extends RecyclerView.ViewHolder {
        public TextView textTitle, textpeakPos, textlastPos, textArtist, textisNew, textrank, textweeks, texturl;
        public ImageView thumbnail;
        public LinearLayout linearLayout;



        public ViewHolder(View itemView) {
            super(itemView);
            thumbnail = itemView.findViewById(R.id.thumbnail);
            texturl = itemView.findViewById(R.id.text_view_result);
            textTitle = itemView.findViewById(R.id.main_title);
            textArtist = itemView.findViewById(R.id.main_artist);
            textlastPos = itemView.findViewById(R.id.main_lastPos);
            textisNew = itemView.findViewById(R.id.main_isNew);
            textrank = itemView.findViewById(R.id.main_rank);
            textpeakPos = itemView.findViewById(R.id.main_peakPos);
            textweeks = itemView.findViewById(R.id.main_weeks);
            linearLayout= itemView.findViewById(R.id.listout);




//            Bitmap bmp = null;
//            try {
//                bmp = BitmapFactory.decodeStream(Hot100.getUrl().openConnection().getInputStream());
//            } catch (IOException e) {
//                e.printStackTrace();
//            }
//            thumbnail.setImageBitmap(bmp);

            //textRating = itemView.findViewById(R.id.main_rating);
            //textYear = itemView.findViewById(R.id.main_year);
        }
    }

}
