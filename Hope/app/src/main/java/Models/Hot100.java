package Models;

public class Hot100 {

    public String title;
    public String artist;
    public int peakPos;
    public int lastPos;
    public boolean isNew;
    public int rank;
    public int weeks;
    public String url;



    public Hot100() {

    }


    //public Hot100(String title, String artist, int rating, int year) {
    public Hot100(String title, String artist, int peakPos, int lastPos, boolean isNew, int rank, int weeks, String url) {
        this.title = title;
        this.artist = artist;
        this.peakPos = peakPos;
        this.lastPos = lastPos;
        this.isNew = isNew;
        this.rank = rank;
        this.weeks = weeks;
        this.url = url;
        //this.rating = rating;
        //this.year = year;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getArtist() {
        return artist;
    }

    public void setArtist(String artist) {
        this.artist = artist;
    }


    public boolean isNew() {
        return isNew;
    }

    public void setNew(boolean aNew) {
        isNew = aNew;
    }

    public int getPeakPos() {
        return peakPos;
    }

    public void setPeakPos(int peakPos) {
        this.peakPos = peakPos;
    }

    public int getLastPos() {
        return lastPos;
    }

    public void setLastPos(int lastPos) {
        this.lastPos = lastPos;
    }

    public int getRank() {
        return rank;
    }

    public void setRank(int rank) {
        this.rank = rank;
    }

    public int getWeeks() {
        return weeks;
    }

    public void setWeeks(int weeks) {
        this.weeks = weeks;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }
}
