package Adapters;

import android.content.Context;
import android.content.Intent;
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
import com.squareup.picasso.Picasso;

import java.util.List;

import Models.Artists;
import Models.Hot100;

/**
 * Created by ankit on 27/10/17.
 */

public class ArtistListAdapter extends RecyclerView.Adapter<ArtistListAdapter.ViewHolder> {

    private Context context;
    private List<Artists> list;

    public ArtistListAdapter(Context context, List<Artists> list) {
        this.context = context;
        this.list = list;
    }

    @Override
    public ViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        View v = LayoutInflater.from(context).inflate(R.layout.top_artists, parent, false);
        return new ViewHolder(v);
    }

    @Override
    public void onBindViewHolder(ViewHolder holder, int position) {
        final Artists artists = list.get(position);
        Picasso.with(context).load(artists.getArtisturl()).into(holder.artist_Picture);
        holder.textName.setText(artists.getName());
        holder.textLastWeek.setText("Last Week"+String.valueOf(artists.getLastWeek()));
        holder.textPeakPosition.setText("Peak Position \n "+String.valueOf(artists.getPeakpostion()));
        holder.textWeeksOnChart.setText("Weeks on Chart \n "+String.valueOf(artists.getWeeksonchart()));
        holder.textisNew.setText("IsNew \n "+String.valueOf(artists.isNew()));
        holder.textRank.setText("Rank \n "+String.valueOf(artists.getRank()));
        
        holder.linearLayout1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent=new Intent(context, Wikipage.class);
                intent.putExtra("Artist",artists.getName());
                intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                context.startActivity(intent);
               // Toast.makeText(context,
                //        "It has been clicked",Toast.LENGTH_SHORT ).show();
            }
        });

    }

    @Override
    public int getItemCount() {
        return list.size();
    }

    public class ViewHolder extends RecyclerView.ViewHolder {
        public TextView textName, textLastWeek, textPeakPosition, textWeeksOnChart, textisNew, textRank;
        public LinearLayout linearLayout1;
        public ImageView artist_Picture;

        public ViewHolder(View itemView) {
            super(itemView);

            textName = itemView.findViewById(R.id.artist_name);
            artist_Picture = itemView.findViewById(R.id.thumbnail_artist);
            textLastWeek = itemView.findViewById(R.id.artist_lastweek);
            textPeakPosition = itemView.findViewById(R.id.artist_peakposition);
            textWeeksOnChart = itemView.findViewById(R.id.artist_weeksonchart);
            textisNew = itemView.findViewById(R.id.artist_isNew);
            textRank = itemView.findViewById(R.id.artist_rank);
            linearLayout1= itemView.findViewById(R.id.listout1);

        }
    }

}

